"""Interactive single-staff score editor for OpenScore Converter v0.0.4.

Editing deliberately remains in-memory; saving and Undo/Redo are later phases.
The preview renderer is the existing v0.0.3 Qt scene with added click targets.
"""

from fractions import Fraction

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtWidgets import (
    QComboBox, QFrame, QGraphicsScene, QGraphicsView, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QVBoxLayout, QWidget,
)

from ...editor import EventPath, ScoreEditor, pitch_from_staff_step
from ...score import Chord, Note, Pitch, Rest, Score
from ..notation.scene_renderer import ScoreSceneRenderer

DURATIONS: tuple[tuple[str, Fraction], ...] = (
    ("Whole", Fraction(1)),
    ("Half", Fraction(1, 2)),
    ("Quarter", Fraction(1, 4)),
    ("Eighth", Fraction(1, 8)),
    ("Sixteenth", Fraction(1, 16)),
    ("Dotted half", Fraction(3, 4)),
    ("Dotted quarter", Fraction(3, 8)),
    ("Dotted eighth", Fraction(3, 16)),
)


class ScoreView(QGraphicsView):
    """Render a score, hit-test event paths and map pointer clicks to note slots."""

    event_clicked = Signal(object, bool)
    blank_clicked = Signal()
    note_position_clicked = Signal(int, object, object)
    key_command = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        """Build the Qt vector viewport with pan, zoom and keyboard focus."""
        super().__init__(parent)
        self._score_scene = QGraphicsScene(self)
        self._renderer = ScoreSceneRenderer(self._score_scene)
        self.setScene(self._score_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setBackgroundBrush(QBrush(QColor("#1c2635")))
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setMinimumHeight(330)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._zoom = 1.0
        self._score: Score | None = None
        self.mode = "select"
        self.duration = Fraction(1, 4)
        self.alter = 0
        self._renderer.draw(None)

    @property
    def zoom_percent(self) -> int:
        """Return the current zoom setting as a percentage."""
        return round(self._zoom * 100)

    def set_score(self, score: Score | None) -> None:
        """Load a fresh Score and reset scene transformation once."""
        self._score = score
        self.refresh()
        self.resetTransform()
        self._zoom = 1.0
        self.centerOn(self.scene().sceneRect().center())

    def refresh(self, selection=()) -> None:
        """Repaint changes without losing current zoom or scroll offsets."""
        self._renderer.draw(self._score, (path.as_tuple() for path in selection))

    def change_zoom(self, factor: float) -> None:
        """Keep zoom within 50%-250%."""
        target = min(2.5, max(0.5, self._zoom * factor))
        self.scale(target / self._zoom, target / self._zoom)
        self._zoom = target

    def reset_zoom(self) -> None:
        """Restore 100% zoom."""
        self.resetTransform()
        self._zoom = 1.0

    def _measure_at(self, x: float, y: float):
        """Locate a displayed measure close to the clicked staff lines."""
        for measure_idx, (left, right, top, capacity) in self._renderer.measure_geometry.items():
            if left <= x <= right and top - 27 <= y <= top + 83:
                return measure_idx, left, right, top, capacity
        return None

    def mousePressEvent(self, event) -> None:  # noqa: N802
        """Select a drawn event or insert a snapped note on a staff click."""
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return
        self.setFocus()
        position = self.mapToScene(event.position().toPoint())
        if self.mode == "select":
            for item in self.scene().items(position):
                raw = item.data(0)
                if isinstance(raw, tuple) and len(raw) == 5:
                    self.event_clicked.emit(
                        EventPath.from_tuple(raw),
                        bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier),
                    )
                    event.accept()
                    return
            self.blank_clicked.emit()
        else:
            found = self._measure_at(position.x(), position.y())
            if found is not None:
                index, left, right, top, measure_duration = found
                available = max(10.0, right - left - 56 - 45)
                relative = max(0.0, min(1.0, (position.x() - left - 56) / available))
                divisions = int(measure_duration / self.duration)
                if divisions <= 0:
                    self.key_command.emit("duration-too-long")
                    event.accept()
                    return
                slot = min(divisions - 1, max(0, int(relative * divisions + 0.5)))
                start = slot * self.duration
                diatonic = round((top + 48 - position.y()) / 6)
                pitch = pitch_from_staff_step(diatonic, alter=self.alter)
                self.note_position_clicked.emit(index, pitch, start)
            else:
                self.key_command.emit("outside-staff")
        event.accept()

    def keyPressEvent(self, event) -> None:  # noqa: N802
        """Forward supported note-entry, navigation and editing keys."""
        key = event.key()
        commands = {
            Qt.Key.Key_Delete: "delete",
            Qt.Key.Key_Backspace: "delete",
            Qt.Key.Key_Up: "up",
            Qt.Key.Key_Down: "down",
            Qt.Key.Key_Left: "previous",
            Qt.Key.Key_Right: "next",
            Qt.Key.Key_Escape: "select-mode",
            Qt.Key.Key_1: "duration-1",
            Qt.Key.Key_2: "duration-2",
            Qt.Key.Key_3: "duration-3",
            Qt.Key.Key_4: "duration-4",
            Qt.Key.Key_5: "duration-5",
        }
        if key in commands:
            self.key_command.emit(commands[key])
            event.accept()
            return
        if Qt.Key.Key_A <= key <= Qt.Key.Key_G and not event.modifiers():
            self.key_command.emit(chr(int(key)))
            event.accept()
            return
        super().keyPressEvent(event)


class ScoreWorkspace(QWidget):
    """One-staff note editor with pointer tools and a note properties inspector."""

    feedback = Signal(str)
    modified = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create the editor workspace, controls and event wiring."""
        super().__init__(parent)
        self.setObjectName("root")
        self.editor: ScoreEditor | None = None
        self.selection: list[EventPath] = []
        self.active_measure = 0
        self._syncing = False
        outer = QVBoxLayout(self)
        outer.setContentsMargins(22, 16, 22, 20)
        outer.setSpacing(10)

        headline = QHBoxLayout()
        name_group = QVBoxLayout()
        self.project_title = QLabel("Untitled")
        self.project_title.setObjectName("pageTitle")
        name_group.addWidget(self.project_title)
        self.summary_label = QLabel("New in-memory score")
        self.summary_label.setObjectName("subtitle")
        name_group.addWidget(self.summary_label)
        headline.addLayout(name_group, stretch=1)
        for caption, factor in (("−", .8), ("+", 1.25)):
            button = QPushButton(caption)
            button.setToolTip("Zoom out" if factor < 1 else "Zoom in")
            button.setFixedWidth(43)
            button.clicked.connect(lambda _checked=False, f=factor: self._update_zoom(f))
            headline.addWidget(button)
        self.zoom_label = QPushButton("100%")
        self.zoom_label.setFixedWidth(70)
        self.zoom_label.setToolTip("Reset zoom")
        self.zoom_label.clicked.connect(self._reset_zoom)
        headline.addWidget(self.zoom_label)
        outer.addLayout(headline)

        tools = QHBoxLayout()
        self.select_button = QPushButton("Select")
        self.add_button = QPushButton("Add note")
        for b in (self.select_button, self.add_button):
            b.setCheckable(True)
            tools.addWidget(b)
        self.select_button.clicked.connect(lambda: self.set_mode("select"))
        self.add_button.clicked.connect(lambda: self.set_mode("insert"))
        tools.addWidget(QLabel("Value:"))
        self.entry_duration = QComboBox()
        self._fill_durations(self.entry_duration)
        self.entry_duration.setCurrentIndex(2)
        self.entry_duration.currentIndexChanged.connect(self._entry_settings_changed)
        tools.addWidget(self.entry_duration)
        tools.addWidget(QLabel("Accidental:"))
        self.entry_alter = QComboBox()
        for label, alter in (("Natural", 0), ("Sharp ♯", 1), ("Flat ♭", -1)):
            self.entry_alter.addItem(label, alter)
        self.entry_alter.currentIndexChanged.connect(self._entry_settings_changed)
        tools.addWidget(self.entry_alter)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selection)
        tools.addWidget(self.delete_button)
        self.measure_button = QPushButton("+ Measure")
        self.measure_button.clicked.connect(self.add_measure)
        tools.addWidget(self.measure_button)
        tools.addStretch()
        outer.addLayout(tools)

        content = QHBoxLayout()
        frame = QFrame()
        frame.setObjectName("scorePreviewFrame")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(8, 8, 8, 8)
        self.score_view = ScoreView()
        frame_layout.addWidget(self.score_view)
        content.addWidget(frame, stretch=1)
        inspector = QFrame()
        inspector.setObjectName("editorInspector")
        inspector.setFixedWidth(238)
        props = QVBoxLayout(inspector)
        props.setContentsMargins(14, 14, 14, 14)
        props.addWidget(QLabel("NOTE PROPERTIES"))
        self.selected_label = QLabel("Click a note to edit it")
        self.selected_label.setWordWrap(True)
        self.selected_label.setObjectName("mutedLabel")
        props.addWidget(self.selected_label)
        props.addWidget(QLabel("Pitch letter"))
        self.pitch_step = QComboBox()
        self.pitch_step.addItems(list("CDEFGAB"))
        props.addWidget(self.pitch_step)
        props.addWidget(QLabel("Octave"))
        self.pitch_octave = QSpinBox()
        self.pitch_octave.setRange(-1, 9)
        props.addWidget(self.pitch_octave)
        props.addWidget(QLabel("Alteration"))
        self.pitch_alter = QComboBox()
        for label, alter in (("Natural", 0), ("Sharp ♯", 1), ("Flat ♭", -1)):
            self.pitch_alter.addItem(label, alter)
        props.addWidget(self.pitch_alter)
        props.addWidget(QLabel("Duration"))
        self.property_duration = QComboBox()
        self._fill_durations(self.property_duration)
        props.addWidget(self.property_duration)
        self.pitch_step.currentIndexChanged.connect(self._apply_pitch_properties)
        self.pitch_octave.valueChanged.connect(self._apply_pitch_properties)
        self.pitch_alter.currentIndexChanged.connect(self._apply_pitch_properties)
        self.property_duration.currentIndexChanged.connect(self._apply_duration_property)
        props.addStretch()
        self.measure_label = QLabel("Active measure: 1")
        self.measure_label.setObjectName("mutedLabel")
        props.addWidget(self.measure_label)
        content.addWidget(inspector)
        outer.addLayout(content, stretch=1)

        notice = QLabel(
            "Select: click a note · Ctrl+click: multi-select · ↑/↓: pitch · Delete: remove  ·  "
            "Add note: click on a staff or type A–G · 1–5: note value · Changes are not saved"
        )
        notice.setWordWrap(True)
        notice.setObjectName("mutedLabel")
        outer.addWidget(notice)

        self.score_view.event_clicked.connect(self._event_clicked)
        self.score_view.blank_clicked.connect(self.clear_selection)
        self.score_view.note_position_clicked.connect(self._insert_at_position)
        self.score_view.key_command.connect(self._key_command)
        self.set_mode("select")
        self._show_properties()

    @staticmethod
    def _fill_durations(combo: QComboBox) -> None:
        """Populate both note-length controls with exact Fraction values."""
        for label, duration in DURATIONS:
            combo.addItem(label, duration)

    def set_score(self, score: Score | None) -> None:
        """Replace the current in-memory document; clear stale selections."""
        self.editor = ScoreEditor(score) if score is not None else None
        self.selection.clear()
        self.active_measure = 0
        self.score_view.set_score(score)
        self.zoom_label.setText("100%")
        self.set_mode("select")
        self._update_summary()
        self._show_properties()

    def _update_summary(self) -> None:
        """Summarize the currently open score and number of measures."""
        if self.editor is None:
            self.project_title.setText("No active score")
            self.summary_label.setText("Create a score to begin")
        else:
            score = self.editor.score
            self.project_title.setText(score.title)
            staves = sum(len(part.staves) for part in score.parts)
            measures = sum(len(staff.measures) for part in score.parts for staff in part.staves)
            self.summary_label.setText(
                f"{len(score.parts)} part · {staves} staff · {measures} measure"
                + ("s" if measures != 1 else "") + " · In memory"
            )
        self.measure_label.setText(f"Active measure: {self.active_measure + 1}")

    def set_mode(self, mode: str) -> None:
        """Switch between selecting existing events and creating new notes."""
        if mode not in ("select", "insert"):
            raise ValueError("Unknown editing mode")
        self.score_view.mode = mode
        self.select_button.setChecked(mode == "select")
        self.add_button.setChecked(mode == "insert")
        self.score_view.viewport().setCursor(
            Qt.CursorShape.CrossCursor if mode == "insert" else Qt.CursorShape.ArrowCursor
        )
        self.score_view.setFocus()

    def _entry_settings_changed(self, *_args) -> None:
        """Apply chosen duration and accidental to future note insertions."""
        self.score_view.duration = self.entry_duration.currentData()
        self.score_view.alter = self.entry_alter.currentData()

    def _event_clicked(self, path: EventPath, multi: bool) -> None:
        """Select one event or toggle membership with Ctrl+click."""
        self.active_measure = path.measure
        if multi:
            if path in self.selection:
                self.selection.remove(path)
            else:
                self.selection.append(path)
        else:
            self.selection = [path]
        self._refresh()

    def clear_selection(self) -> None:
        """Clear the selection when clicking empty paper in Select mode."""
        self.selection.clear()
        self._refresh()

    def _refresh(self) -> None:
        """Rebuild preview and inspector while keeping zoom and scroll."""
        self.score_view.refresh(self.selection)
        self._show_properties()
        self._update_summary()

    def _show_properties(self) -> None:
        """Display an event's properties, without treating UI sync as edits."""
        valid = self.editor is not None and len(self.selection) == 1
        event = self.editor.event(self.selection[0]) if valid else None
        note = event if isinstance(event, Note) else None
        controls = (self.pitch_step, self.pitch_octave, self.pitch_alter, self.property_duration)
        for widget in controls:
            widget.setEnabled(valid if widget is self.property_duration else note is not None)
        self.delete_button.setEnabled(self.editor is not None and bool(self.selection))
        self.measure_button.setEnabled(self.editor is not None)
        if not valid:
            self.selected_label.setText(
                f"{len(self.selection)} events selected" if self.selection
                else "Click a note to edit it"
            )
            return
        self.selected_label.setText(
            f"Measure {self.selection[0].measure + 1} · "
            + (f"Note {event.pitch}" if note else "Chord" if isinstance(event, Chord) else "Rest")
            + f"\nStart {event.start} · Duration {event.duration}"
        )
        self._syncing = True
        try:
            if note:
                self.pitch_step.setCurrentText(note.pitch.step)
                self.pitch_octave.setValue(note.pitch.octave)
                idx = self.pitch_alter.findData(note.pitch.alter)
                self.pitch_alter.setCurrentIndex(idx if idx >= 0 else 0)
            idx = self.property_duration.findData(event.duration)
            self.property_duration.setCurrentIndex(idx)
        finally:
            self._syncing = False

    def _edit_committed(self, message: str) -> None:
        """Redraw a changed score and tell the main window it is unsaved."""
        self._refresh()
        self.modified.emit()
        self.feedback.emit(message + " · Unsaved changes")

    def _rejected(self, exc: Exception) -> None:
        """Show validation failures without losing existing notes or selection."""
        self.feedback.emit(f"Cannot edit note: {exc}")
        self._show_properties()

    def _insert_at_position(self, measure: int, pitch: Pitch, start: Fraction) -> None:
        """Insert a snapped note at the clicked position and pitch."""
        if not self.editor:
            return
        try:
            path = self.editor.insert_note(measure, pitch, self.score_view.duration, start)
        except (ValueError, IndexError) as exc:
            self._rejected(exc)
            return
        self.selection = [path]
        self.active_measure = measure
        self._edit_committed(f"Inserted {pitch} at {start} in measure {measure + 1}")
        self.score_view.setFocus()

    def _insert_keyboard(self, letter: str) -> None:
        """Append a typed A–G note to the active measure in Add Note mode."""
        if not self.editor or self.score_view.mode != "insert":
            return
        octave = 4 if letter in "AB" else 5
        pitch = Pitch(letter, octave, self.score_view.alter)
        try:
            path = self.editor.insert_note(self.active_measure, pitch, self.score_view.duration)
        except (ValueError, IndexError) as exc:
            self._rejected(exc)
            return
        self.selection = [path]
        self._edit_committed(f"Inserted {pitch} from keyboard")
        self.score_view.setFocus()

    def _apply_pitch_properties(self, *_args) -> None:
        """Update the selected single Note based on the inspector controls."""
        if self._syncing or not self.editor or len(self.selection) != 1:
            return
        path = self.selection[0]
        if not isinstance(self.editor.event(path), Note):
            return
        pitch = Pitch(self.pitch_step.currentText(), self.pitch_octave.value(),
                      self.pitch_alter.currentData())
        try:
            self.selection = [self.editor.change_pitch(path, pitch)]
        except (ValueError, IndexError) as exc:
            self._rejected(exc)
            return
        self._edit_committed(f"Changed note to {pitch}")

    def _apply_duration_property(self, *_args) -> None:
        """Resize a selected event only if it still fits without overlap."""
        if self._syncing or not self.editor or len(self.selection) != 1:
            return
        duration = self.property_duration.currentData()
        if duration is None:
            return
        try:
            self.selection = [self.editor.change_duration(self.selection[0], duration)]
        except (ValueError, IndexError) as exc:
            self._rejected(exc)
            return
        self._edit_committed(f"Changed duration to {duration}")

    def delete_selection(self) -> None:
        """Delete selected events, processing highest indices first per voice."""
        if not self.editor or not self.selection:
            return
        number = len(self.selection)
        for path in sorted(set(self.selection), reverse=True):
            self.editor.delete(path)
        self.selection.clear()
        self._edit_committed(f"Deleted {number} event(s)")
        self.score_view.setFocus()

    def add_measure(self) -> None:
        """Append a blank measure that can then receive clicked notes."""
        if self.editor is None:
            return
        self.active_measure = self.editor.add_measure()
        self.selection.clear()
        self._edit_committed(f"Created measure {self.active_measure + 1}")
        self.score_view.setFocus()

    def _key_command(self, command: str) -> None:
        """Dispatch note-entry shortcuts and select-mode navigation."""
        if command in "ABCDEFG" and len(command) == 1:
            self._insert_keyboard(command)
            return
        if command.startswith("duration-") and command[-1].isdigit():
            index = int(command[-1]) - 1
            if 0 <= index <= 4:
                self.entry_duration.setCurrentIndex(index)
                self.feedback.emit(f"Note entry duration: {self.entry_duration.currentText()}")
            return
        if command == "select-mode":
            self.set_mode("select")
            return
        if command == "delete":
            self.delete_selection()
            return
        if command in ("outside-staff", "duration-too-long"):
            self.feedback.emit("Click inside a measure" if command == "outside-staff"
                               else "The selected duration is longer than this measure")
            return
        if not self.editor or not self.selection:
            return
        if command in ("up", "down") and len(self.selection) == 1:
            try:
                self.selection = [self.editor.transpose_diatonic(
                    self.selection[0], 1 if command == "up" else -1
                )]
            except (ValueError, IndexError) as exc:
                self._rejected(exc)
                return
            self._edit_committed("Changed pitch by one staff step")
        elif command in ("previous", "next") and len(self.selection) == 1:
            path = self.selection[0]
            target = path.event + (-1 if command == "previous" else 1)
            voice = self.editor.measure(path.measure).voices[path.voice]
            if 0 <= target < len(voice.events):
                self.selection = [EventPath(path.part, path.staff, path.measure, path.voice, target)]
                self._refresh()

    def _update_zoom(self, factor: float) -> None:
        """Zoom and reflect its percentage in the toolbar."""
        self.score_view.change_zoom(factor)
        self.zoom_label.setText(f"{self.score_view.zoom_percent}%")

    def _reset_zoom(self) -> None:
        """Reset view transform and the corresponding label."""
        self.score_view.reset_zoom()
        self.zoom_label.setText("100%")
