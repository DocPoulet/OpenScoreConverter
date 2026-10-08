"""Editing commands for v0.0.4 (undo/redo arrives in v0.0.5).

The editor never leaves a voice in an invalid state after a failed operation.
The GUI only stores model paths, not references to scene primitives.
"""

from dataclasses import dataclass
from fractions import Fraction

from ..score import Chord, Note, Pitch, Rest, Score
from ..score.voice import Voice
from ..score.primitives import exact_fraction

LETTERS = "CDEFGAB"


@dataclass(frozen=True, order=True, slots=True)
class EventPath:
    """Zero-based location of an event in a score. Re-resolve after mutations."""

    part: int
    staff: int
    measure: int
    voice: int
    event: int

    @classmethod
    def from_tuple(cls, value: tuple[int, ...]) -> "EventPath":
        """Convert a five-element renderer item identifier to an EventPath."""
        if len(value) != 5 or any(type(item) is not int or item < 0 for item in value):
            raise ValueError("Expected five non-negative integer path components")
        return cls(*value)

    def as_tuple(self) -> tuple[int, int, int, int, int]:
        """Return the existing scene-renderer-compatible identifier."""
        return self.part, self.staff, self.measure, self.voice, self.event


def pitch_from_staff_step(step: int, clef: str = "treble", alter: int = 0) -> Pitch:
    """Inverse of engraving.staff_step for one diatonic staff position.

    Inputs: offset in diatonic steps from bottom staff line, clef, alteration.
    Returns: a spelled Pitch retaining the requested accidental.
    """
    if type(step) is not int:
        raise TypeError("Staff step must be integer")
    origin = {"treble": ("E", 4), "bass": ("G", 2)}.get(clef)
    if origin is None:
        raise ValueError("Only treble and bass staff positions are supported")
    letter, octave = origin
    index = octave * 7 + LETTERS.index(letter) + step
    result_octave, result_step = divmod(index, 7)
    return Pitch(LETTERS[result_step], result_octave, alter)


def shift_diatonic(pitch: Pitch, steps: int) -> Pitch:
    """Transpose a note by written staff positions, preserving alteration."""
    if type(steps) is not int:
        raise TypeError("Steps must be an integer")
    index = pitch.octave * 7 + LETTERS.index(pitch.step) + steps
    octave, letter_index = divmod(index, 7)
    return Pitch(LETTERS[letter_index], octave, pitch.alter)


class ScoreEditor:
    """Perform validated mutations on the first or any explicitly selected staff.

    This object is reusable outside Qt and intentionally has no history stack yet.
    """

    def __init__(self, score: Score):
        """Keep the live Score used by the preview and the project session."""
        if not isinstance(score, Score):
            raise TypeError("ScoreEditor expects a Score")
        self.score = score

    def measure(self, index: int, part: int = 0, staff: int = 0):
        """Return the requested measure, raising IndexError on a bad path."""
        return self.score.parts[part].staves[staff].measures[index]

    def event(self, path: EventPath):
        """Retrieve the current Note, Rest or Chord at an event path."""
        return self.measure(path.measure, path.part, path.staff).voices[path.voice].events[path.event]

    def _commit(self, measure, voice_index: int, replacement: list) -> int:
        """Validate replacement voice completely before mutating live data."""
        proposed = Voice(replacement)
        if proposed.end > measure.duration:
            raise ValueError("The event would extend beyond the end of the measure")
        measure.voices[voice_index].events = proposed.events
        return 0

    def insert_note(self, measure_index: int, pitch: Pitch, duration: Fraction,
                    start: Fraction | None = None, voice_index: int = 0,
                    part: int = 0, staff: int = 0) -> EventPath:
        """Add a note, defaulting to the end of its voice; never create overlaps."""
        measure = self.measure(measure_index, part, staff)
        voice = measure.voices[voice_index]
        onset = voice.end if start is None else exact_fraction(start)
        new_note = Note(pitch, onset, exact_fraction(duration))
        measure.add_event(new_note, voice_index)
        return EventPath(part, staff, measure_index, voice_index,
                         next(i for i, item in enumerate(voice.events) if item is new_note))

    def delete(self, path: EventPath) -> None:
        """Remove a single event in-place after resolving the path."""
        self.measure(path.measure, path.part, path.staff).voices[path.voice].events.pop(path.event)

    def replace(self, path: EventPath, event: Note | Rest | Chord) -> EventPath:
        """Replace an event atomically; return its possibly changed sorted index."""
        measure = self.measure(path.measure, path.part, path.staff)
        current = measure.voices[path.voice].events
        proposed = current[:path.event] + current[path.event+1:] + [event]
        self._commit(measure, path.voice, proposed)
        updated = measure.voices[path.voice].events
        return EventPath(path.part, path.staff, path.measure, path.voice,
                         next(i for i, item in enumerate(updated) if item is event))

    def change_pitch(self, path: EventPath, pitch: Pitch) -> EventPath:
        """Change the spelling/height of one Note (not an entire Chord)."""
        event = self.event(path)
        if not isinstance(event, Note):
            raise ValueError("Pitch editing applies to single notes only")
        return self.replace(path, Note(pitch, event.start, event.duration))

    def transpose_diatonic(self, path: EventPath, steps: int) -> EventPath:
        """Move a selected Note by staff steps without changing its rhythm."""
        event = self.event(path)
        if not isinstance(event, Note):
            raise ValueError("Use the note properties to edit individual notes")
        return self.change_pitch(path, shift_diatonic(event.pitch, steps))

    def change_duration(self, path: EventPath, duration: Fraction) -> EventPath:
        """Change one event's length, rejecting overlaps or bar overflow."""
        event = self.event(path)
        duration = exact_fraction(duration)
        if isinstance(event, Note):
            replacement = Note(event.pitch, event.start, duration)
        elif isinstance(event, Chord):
            replacement = Chord(event.pitches, event.start, duration)
        else:
            replacement = Rest(event.start, duration)
        return self.replace(path, replacement)

    def add_measure(self, part: int = 0, staff: int = 0) -> int:
        """Append a 4/4 (or inherited meter) bar and return its index."""
        measures = self.score.parts[part].staves[staff].measures
        self.score.parts[part].staves[staff].new_measure()
        return len(measures) - 1
