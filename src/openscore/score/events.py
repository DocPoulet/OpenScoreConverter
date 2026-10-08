"""Immutable notated events in a measure's local rational time."""

from dataclasses import dataclass
from fractions import Fraction

from .primitives import Pitch, exact_fraction


def _validate_time(start: Fraction, duration: Fraction) -> None:
    """Reject negative onsets and zero/negative written durations."""
    if start < 0:
        raise ValueError("An event cannot start before the measure")
    if duration <= 0:
        raise ValueError("An event duration must be positive")


@dataclass(frozen=True, slots=True)
class Note:
    """One pitched event with a local start and written duration.

    Times are fractions of a *whole note*: quarter=1/4, eighth=1/8.
    """

    pitch: Pitch
    start: Fraction
    duration: Fraction

    def __post_init__(self) -> None:
        """Coerce exact rational times and validate a single note."""
        if not isinstance(self.pitch, Pitch):
            raise TypeError("Note.pitch must be a Pitch")
        object.__setattr__(self, "start", exact_fraction(self.start))
        object.__setattr__(self, "duration", exact_fraction(self.duration))
        _validate_time(self.start, self.duration)

    @property
    def end(self) -> Fraction:
        """Return the exclusive end position in the measure."""
        return self.start + self.duration


@dataclass(frozen=True, slots=True)
class Rest:
    """One explicit rest; gaps in a voice are not automatically rests."""

    start: Fraction
    duration: Fraction

    def __post_init__(self) -> None:
        """Coerce and validate exact timing for a rest."""
        object.__setattr__(self, "start", exact_fraction(self.start))
        object.__setattr__(self, "duration", exact_fraction(self.duration))
        _validate_time(self.start, self.duration)

    @property
    def end(self) -> Fraction:
        """Return the exclusive end of this rest."""
        return self.start + self.duration


@dataclass(frozen=True, slots=True)
class Chord:
    """Simultaneous pitched notes with a common onset and duration.

    A later version may support note-specific ties and articulations.
    """

    pitches: tuple[Pitch, ...]
    start: Fraction
    duration: Fraction

    def __post_init__(self) -> None:
        """Require one or more unique pitches, and valid rational timing."""
        pitches = tuple(self.pitches)
        if not pitches or any(not isinstance(p, Pitch) for p in pitches):
            raise ValueError("Chord must contain one or more Pitch instances")
        if len(set(pitches)) != len(pitches):
            raise ValueError("Chord cannot contain duplicate written pitches")
        object.__setattr__(self, "pitches", pitches)
        object.__setattr__(self, "start", exact_fraction(self.start))
        object.__setattr__(self, "duration", exact_fraction(self.duration))
        _validate_time(self.start, self.duration)

    @property
    def end(self) -> Fraction:
        """Return the exclusive end of all notes in the chord."""
        return self.start + self.duration


ScoreEvent = Note | Rest | Chord
