"""Measures with explicit voices, meter, and bounded written time."""

from dataclasses import dataclass, field
from fractions import Fraction

from .events import Chord, Note, Rest, ScoreEvent
from .primitives import Pitch, TimeSignature, exact_fraction
from .voice import Voice


@dataclass(slots=True)
class Measure:
    """A numbered measure with one or more independent written voices.

    Args:
        number: Human-readable 1-based measure index.
        time_signature: Meter in force for this measure.
        actual_duration: Optional shorter duration for pickup/partial bars.
        voices: Independent monophonic voices (initially one empty voice).
    """

    number: int = 1
    time_signature: TimeSignature = field(default_factory=TimeSignature)
    actual_duration: Fraction | None = None
    voices: list[Voice] = field(default_factory=lambda: [Voice()])

    def __post_init__(self) -> None:
        """Validate meter, numbering, pickup capacity, and initial voices."""
        if isinstance(self.number, bool) or not isinstance(self.number, int) or self.number < 1:
            raise ValueError("Measure number must be a positive integer")
        if not isinstance(self.time_signature, TimeSignature):
            raise TypeError("Measure.time_signature must be a TimeSignature")
        if self.actual_duration is not None:
            self.actual_duration = exact_fraction(self.actual_duration)
            if not 0 < self.actual_duration <= self.time_signature.duration:
                raise ValueError("Actual measure duration must be >0 and <= meter capacity")
        if not self.voices or any(not isinstance(voice, Voice) for voice in self.voices):
            raise ValueError("A measure must have at least one Voice")
        for voice in self.voices:
            if voice.end > self.duration:
                raise ValueError("An existing voice exceeds the measure duration")

    @property
    def duration(self) -> Fraction:
        """Return effective capacity in whole-note units, including pickup bars."""
        return self.actual_duration if self.actual_duration is not None else self.time_signature.duration

    @property
    def is_complete(self) -> bool:
        """Return True if every present voice explicitly fills the measure."""
        return all(voice.is_complete(self.duration) for voice in self.voices)

    def add_voice(self) -> int:
        """Create an empty voice and return its zero-based index."""
        self.voices.append(Voice())
        return len(self.voices) - 1

    def add_event(self, event: ScoreEvent, voice_index: int = 0) -> None:
        """Add a bounded event to a selected voice.

        Args: event has an explicit onset; voice_index is zero-based.
        Returns: None. A failed insertion leaves the model unchanged.
        """
        if isinstance(voice_index, bool) or not isinstance(voice_index, int) or voice_index < 0:
            raise ValueError("Voice index must be a non-negative integer")
        if not isinstance(event, (Note, Rest, Chord)):
            raise TypeError("Expected Note, Rest or Chord")
        if event.end > self.duration:
            raise ValueError("Event would extend beyond the end of the measure")
        if voice_index >= len(self.voices):
            raise IndexError("Voice does not exist; call add_voice() first")
        self.voices[voice_index].add_event(event)

    def _onset(self, voice_index: int, start: Fraction | int | str | None) -> Fraction:
        """Use an explicit onset or append to the end of a voice."""
        if voice_index < 0 or voice_index >= len(self.voices):
            raise IndexError("Voice does not exist")
        return self.voices[voice_index].end if start is None else exact_fraction(start)

    def add_note(self, pitch: Pitch, duration: Fraction | int | str,
                 start: Fraction | int | str | None = None, voice_index: int = 0) -> Note:
        """Create and insert a note; omitted start appends after the last event."""
        note = Note(pitch, self._onset(voice_index, start), exact_fraction(duration))
        self.add_event(note, voice_index)
        return note

    def add_rest(self, duration: Fraction | int | str,
                 start: Fraction | int | str | None = None, voice_index: int = 0) -> Rest:
        """Create and insert an explicit rest into a voice."""
        rest = Rest(self._onset(voice_index, start), exact_fraction(duration))
        self.add_event(rest, voice_index)
        return rest

    def add_chord(self, pitches: tuple[Pitch, ...], duration: Fraction | int | str,
                  start: Fraction | int | str | None = None, voice_index: int = 0) -> Chord:
        """Create a simultaneous chord within a single voice."""
        chord = Chord(pitches, self._onset(voice_index, start), exact_fraction(duration))
        self.add_event(chord, voice_index)
        return chord

    def gaps(self, voice_index: int = 0) -> list[tuple[Fraction, Fraction]]:
        """Return gaps in a selected voice (useful for validation UI)."""
        return self.voices[voice_index].gaps(self.duration)
