"""Qt vector preview with editor hit targets (not a professional engraver).

Draws simple notation using Qt vectors.  Geometry is kept in this component so
v0.0.4 uses the same renderer and model, with small hit-test additions.
"""

from fractions import Fraction

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainterPath, QPen
from PySide6.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem

from ...engraving import duration_glyph, measure_slots, staff_step
from ...score import Chord, Note, Rest, Score

INK = QColor("#222b3a")
LINE = QColor("#596478")
MUTED = QColor("#7d8897")
PAPER = QColor("#ffffff")
ACCENT = QColor("#367dd1")
WARNING = QColor("#a94c38")


class ScoreSceneRenderer:
    """Paint the first staff of a Score into a QGraphicsScene.

    Args: scene to populate.
    Returns: a scene with no dependency on PDF, MIDI or external fonts.
    """

    STAFF_SPACING = 12.0
    SYSTEM_STEP = 210.0
    PAGE_WIDTH = 1060.0

    def __init__(self, scene: QGraphicsScene) -> None:
        """Store a Qt scene; no musical data is copied or changed."""
        self.scene = scene
        self.measure_geometry: dict[int, tuple[float, float, float, Fraction]] = {}
        self.selected_paths: set[tuple[int, ...]] = set()

    def _line(self, x1: float, y1: float, x2: float, y2: float,
              color: QColor = INK, width: float = 1.4) -> None:
        """Add an antialiasable vector line to the scene."""
        self.scene.addLine(x1, y1, x2, y2, QPen(color, width))

    def _text(self, message: str, x: float, y: float, size: int = 11,
              color: QColor = INK, bold: bool = False, center: bool = False,
              family: str = "Segoe UI") -> QGraphicsSimpleTextItem:
        """Place text without modifying the score model."""
        item = self.scene.addSimpleText(message, QFont(family, size, QFont.Weight.Bold if bold else QFont.Weight.Normal))
        item.setBrush(QBrush(color))
        if center:
            x -= item.boundingRect().width() / 2
        item.setPos(x, y)
        return item

    def draw(self, score: Score | None, selected_paths=()) -> None:
        """Clear old primitives and render one right-hand (treble) staff.

        Args: existing Score or None for the empty view.
        Returns: None. Scene items carry a model path in item.data(0).
        """
        self.scene.clear()
        self.measure_geometry.clear()
        self.selected_paths = set(selected_paths)
        if score is None or not score.parts or not score.parts[0].staves:
            self._empty_page()
            return
        staff = score.parts[0].staves[0]
        measures = staff.measures
        systems = max(1, (len(measures) + 1) // 2)
        height = max(675, 165 + systems * self.SYSTEM_STEP)
        self.scene.setSceneRect(0, 0, self.PAGE_WIDTH + 32, height + 35)
        self.scene.addRect(12, 12, self.PAGE_WIDTH, height,
                           QPen(QColor("#d4dce6"), 1), QBrush(PAPER))
        self._text(score.title, 542, 53, 22, INK, True, True)
        if score.composer:
            composer_label = self._text(score.composer, 0, 96, 10, MUTED)
            composer_label.setPos(990 - composer_label.boundingRect().width(), 96)
        self._text(score.parts[0].name + " · Right hand", 92, 139, 10, MUTED)
        if staff.key_signature.fifths != 0:
            self._text("Preview limitation: key signatures are not engraved yet.", 92, height - 65, 10, WARNING)
        if staff.clef.value != "treble":
            self._text("This preview currently supports treble clef only.", 92, 200, 13, WARNING)
            return
        for sys_idx in range(systems):
            system_bars = measures[sys_idx * 2:sys_idx * 2 + 2]
            top = 214 + sys_idx * self.SYSTEM_STEP
            self._system(staff, system_bars, sys_idx * 2, top)
        if not measures:
            self._text("No measures", 230, 230, 12, WARNING)
        if len(score.parts) > 1 or any(len(part.staves) > 1 for part in score.parts):
            self._text("Preview limitation: only the first staff is shown", 92, height - 45, 10, WARNING)

    def _empty_page(self) -> None:
        """Display a neutral scene when no score is assigned."""
        self.scene.setSceneRect(0, 0, 1060, 600)
        self.scene.addRect(12, 12, 1020, 560, QPen(QColor("#d4dce6")), QBrush(PAPER))
        self._text("Create a new score to see a staff", 531, 245, 15, MUTED, center=True)

    def _system(self, staff, bars, initial_index: int, top: float) -> None:
        """Paint five lines, a clef, meter and up to two bar contents."""
        left, right = 92.0, 990.0
        for n in range(5):
            y = top + n * self.STAFF_SPACING
            self._line(left, y, right, y, LINE, 1.05)
        self._line(left, top, left, top + 48, LINE, 1.5)
        # Test the requested font rather than showing a missing-glyph square.
        # Segoe UI Symbol is included with supported Windows installations.
        music_font = QFont("Segoe UI Symbol", 47)
        if QFontMetrics(music_font).inFontUcs4(0x1D11E):
            self._text("𝄞", left + 10, top - 43, 47, INK, family="Segoe UI Symbol")
        else:
            self._text("G clef", left + 8, top + 12, 11, INK, True)
        if bars:
            meter = bars[0].time_signature
            self._text(str(meter.numerator), left + 85, top - 1, 16, INK, True, True)
            self._text(str(meter.denominator), left + 85, top + 23, 16, INK, True, True)
        start = left + 121
        if not bars:
            self._line(right, top, right, top + 48, LINE, 1.5)
            return
        width = (right - start) / len(bars)
        for local_idx, bar in enumerate(bars):
            bar_start = start + local_idx * width
            bar_end = start + (local_idx + 1) * width
            if local_idx > 0:
                self._line(bar_start, top, bar_start, top + 48, LINE, 1.5)
            self._measure(bar, initial_index + local_idx, bar_start, bar_end, top)
        self._line(right - 4, top, right - 4, top + 48, INK, 2)

    def _measure(self, bar, bar_idx: int, x0: float, x1: float, top: float) -> None:
        """Position real model events at shared onset slots for all voices."""
        self._text(str(bar.number), x0 + 10, top - 39, 9, MUTED)
        self.measure_geometry[bar_idx] = (x0, x1, top, bar.duration)
        slots = measure_slots(bar)
        pad_l, pad_r = 56, 45
        usable = max(10, x1 - x0 - pad_l - pad_r)
        # Rhythmic x positions are proportional to written duration, so clicks
        # in Add Note mode can be snapped to the same time coordinate.
        positions = {onset: x0 + pad_l + usable * float(onset / bar.duration)
                     for onset in slots}
        # Tracking written alterations is local to each measure and octave.
        state: dict[tuple[str, int], int] = {}
        events = sorted(
            ((e.start, v_idx, e_idx, e) for v_idx, voice in enumerate(bar.voices)
             for e_idx, e in enumerate(voice.events)),
            key=lambda entry: (entry[0], entry[1], entry[2])
        )
        for onset, voice_idx, event_idx, event in events:
            x = positions[onset]
            model_path = (0, 0, bar_idx, voice_idx, event_idx)
            if isinstance(event, Rest):
                self._rest(event, x, top, model_path)
            else:
                pitches = (event.pitch,) if isinstance(event, Note) else event.pitches
                self._notes(event, pitches, x, top, state, model_path)
        if not events:
            self._text("Empty measure", (x0 + x1)/2, top + 66, 9, MUTED, center=True)

    def _notes(self, event, pitches, x: float, top: float,
               accidentals: dict, model_path: tuple[int, ...]) -> None:
        """Draw notehead(s), ledger lines, stems, flags, dots and alterations."""
        glyph = duration_glyph(event.duration)
        if glyph is None:
            self._text(f"[{event.duration}]", x, top + 70, 9, WARNING, center=True)
            return
        steps = sorted(staff_step(p) for p in pitches)
        highest = max(steps)
        stem_up = sum(steps) / len(steps) < 4
        # Offset adjacent seconds to preserve two visible noteheads in a chord.
        shift = {step: 0 for step in steps}
        for a, b in zip(steps, steps[1:]):
            if b - a == 1:
                shift[b if stem_up else a] = 13 if stem_up else -13
        y_positions = []
        for pitch in pitches:
            step = staff_step(pitch)
            ny = top + 48 - step * (self.STAFF_SPACING / 2)
            nx = x + shift[step]
            self._ledger(nx, ny, step)
            accidental = (pitch.step, pitch.octave)
            current = accidentals.get(accidental, 0)  # first preview: C major
            if pitch.alter != current:
                symbol = {1: "♯", -1: "♭", 0: "♮"}.get(pitch.alter, f"{pitch.alter:+d}")
                self._text(symbol, nx - 28, ny - 17, 17, INK)
                accidentals[accidental] = pitch.alter
            head = self.scene.addEllipse(nx - 10, ny - 6.5, 20, 13,
                                         QPen(INK, 1.8), QBrush(PAPER if glyph.base >= Fraction(1, 2) else INK))
            self._tag(head, model_path, f"{pitch} · {event.duration} whole notes")
            y_positions.append(ny)
        # Larger invisible clicking surface, especially useful for small notes.
        self._hit_area(x - 18, min(y_positions) - 14, 39,
                       max(y_positions) - min(y_positions) + 28, model_path)
        if glyph.base != 1:
            # Stems start from the outermost pitch opposite the stem direction.
            anchor_y = max(y_positions) if stem_up else min(y_positions)
            sx = x + (10 if stem_up else -10)
            tip_y = (min(y_positions) - 41 if stem_up
                     else max(y_positions) + 41)
            self._line(sx, anchor_y, sx, tip_y, INK, 1.8)
            flags = {Fraction(1, 8): 1, Fraction(1, 16): 2, Fraction(1, 32): 3}.get(glyph.base, 0)
            for idx in range(flags):
                self._flag(sx, tip_y, stem_up, idx)
        if glyph.dots:
            dot_y = y_positions[-1]
            if any(abs(dot_y - (top + n * 12)) < .1 for n in range(5)):
                dot_y -= 6
            for idx in range(glyph.dots):
                self.scene.addEllipse(x + 16 + 9 * idx, dot_y - 2.1, 4.2, 4.2,
                                      QPen(Qt.PenStyle.NoPen), QBrush(INK))
        if glyph.tuplet:
            self._text("3", x, min(y_positions) - 56, 10, ACCENT, True, True)

    def _ledger(self, x: float, y: float, step: int) -> None:
        """Draw all necessary ledger lines for a note outside the staff."""
        if step <= -2:
            for s in range(-2, step - 1, -2):
                self._line(x - 15, y + (step - s) * 6, x + 15, y + (step - s) * 6, LINE, 1.1)
        if step >= 10:
            for s in range(10, step + 1, 2):
                self._line(x - 15, y + (step - s) * 6, x + 15, y + (step - s) * 6, LINE, 1.1)

    def _flag(self, x: float, tip_y: float, upward: bool, flag_index: int) -> None:
        """Draw an individual eighth/sixteenth/thirty-second flag."""
        p = QPainterPath()
        y = tip_y + (flag_index * (9 if upward else -9))
        p.moveTo(x, y)
        if upward:
            p.cubicTo(x + 8, y + 6, x + 19, y + 9, x + 13, y + 24)
        else:
            p.cubicTo(x - 8, y - 6, x - 19, y - 9, x - 13, y - 24)
        self.scene.addPath(p, QPen(INK, 2.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

    def _rest(self, event: Rest, x: float, top: float, model_path: tuple[int, ...]) -> None:
        """Render a conventional basic rest symbol, or an explicit fallback."""
        glyph = duration_glyph(event.duration)
        if glyph is None:
            self._text(f"rest [{event.duration}]", x, top + 70, 9, WARNING, center=True)
            return
        y = top + 24
        if glyph.base == Fraction(1):
            item = self.scene.addRect(x - 11, top + 12, 22, 6, QPen(INK, .5), QBrush(INK))
        elif glyph.base == Fraction(1, 2):
            item = self.scene.addRect(x - 11, top + 18, 22, 6, QPen(INK, .5), QBrush(INK))
        elif glyph.base == Fraction(1, 4):
            p = QPainterPath()
            p.moveTo(x + 5, top + 4)
            p.lineTo(x - 2, top + 13)
            p.lineTo(x + 6, top + 20)
            p.lineTo(x - 5, top + 32)
            p.cubicTo(x - 16, top + 43, x - 4, top + 46, x + 2, top + 35)
            item = self.scene.addPath(p, QPen(INK, 3.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        else:
            p = QPainterPath()
            p.moveTo(x + 3, top + 6)
            p.lineTo(x - 4, top + 38)
            flags = {Fraction(1, 8): 1, Fraction(1, 16): 2, Fraction(1, 32): 3}.get(glyph.base, 1)
            for k in range(flags):
                fy = top + 8 + 9*k
                p.moveTo(x + 3, fy)
                p.cubicTo(x + 24, fy - 5, x + 16, fy + 10, x + 1, fy + 16)
            item = self.scene.addPath(p, QPen(INK, 2.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        self._tag(item, model_path, f"Rest · {event.duration} whole notes")
        self._hit_area(x - 17, top + 2, 34, 49, model_path)
        for k in range(glyph.dots):
            self.scene.addEllipse(x + 14 + 9*k, y - 2, 4.2, 4.2, QPen(Qt.PenStyle.NoPen), QBrush(INK))
        if glyph.tuplet:
            self._text("3", x, top - 39, 10, ACCENT, True, True)

    def _hit_area(self, x: float, y: float, width: float, height: float,
                  model_path: tuple[int, ...]) -> None:
        """Add a transparent tagged click target behind its notation symbol."""
        brush = (QBrush(QColor(56, 125, 209, 42)) if model_path in self.selected_paths
                 else QBrush(QColor(0, 0, 0, 0)))
        item = self.scene.addRect(x, y, width, height, QPen(Qt.PenStyle.NoPen), brush)
        item.setData(0, model_path)
        item.setZValue(2)

    def _tag(self, item, model_path: tuple[int, ...], tooltip: str) -> None:
        """Tag selectable visual items and highlight current selection."""
        item.setData(0, model_path)
        item.setToolTip(tooltip)
        item.setZValue(3)
        if model_path in self.selected_paths and hasattr(item, "setPen"):
            item.setPen(QPen(QColor("#367dd1"), 3.2))
