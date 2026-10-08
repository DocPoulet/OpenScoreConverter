"""Qt-independent musical primitives, expressed in exact written-note units."""

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction


class Clef(str, Enum):
    """Supported clef identifiers for a staff (not graphical glyphs)."""

    TREBLE = "treble"
    BASS = "bass"
    ALTO = "alto"
    TENOR = "tenor"
    PERCUSSION = "percussion"


def exact_fraction(value: Fraction | int | str) -> Fraction:
    """Convert a rational input to Fraction, rejecting inexact floats and bools.

    Args:
        value: Fraction, integer or fractional string, e.g. '1/12'.
    Returns:
        Exactly represented Fraction, or raises ValueError/TypeError.
    """
    if isinstance(value, bool) or not isinstance(value, (Fraction, int, str)):
        raise TypeError("Musical times must be Fraction, int or rational string; not float")
    return Fraction(value)


@dataclass(frozen=True, slots=True)
class Pitch:
    """A spelled pitch, preserving enharmonics (e.g. C#4 != Db4).

    Args:
        step: One of A, B, C, D, E, F, G (case-insensitive).
        octave: Scientific-pitch-notation octave (C4 is middle C).
        alter: Semitone alteration; -1 flat, 1 sharp, 0 natural.
    """

    step: str
    octave: int
    alter: int = 0

    def __post_init__(self) -> None:
        """Normalize letter and reject invalid musical pitch metadata."""
        if not isinstance(self.step, str) or self.step.upper() not in "ABCDEFG" or len(self.step) != 1:
            raise ValueError("Pitch step must be A, B, C, D, E, F or G")
        if isinstance(self.octave, bool) or not isinstance(self.octave, int):
            raise TypeError("Pitch octave must be an integer")
        if isinstance(self.alter, bool) or not isinstance(self.alter, int):
            raise TypeError("Pitch alteration must be an integer")
        object.__setattr__(self, "step", self.step.upper())

    @property
    def midi_number(self) -> int:
        """Return MIDI key 0–127; raise if pitch cannot be encoded in MIDI."""
        semitones = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
        value = (self.octave + 1) * 12 + semitones[self.step] + self.alter
        if not 0 <= value <= 127:
            raise ValueError("Pitch is outside MIDI note range 0..127")
        return value

    def __str__(self) -> str:
        """Return a human-friendly spelling of the pitch."""
        accidental = "#" * self.alter if self.alter > 0 else "b" * -self.alter
        return f"{self.step}{accidental}{self.octave}"


@dataclass(frozen=True, slots=True)
class TimeSignature:
    """Meter and its exact capacity measured in whole notes."""

    numerator: int = 4
    denominator: int = 4

    def __post_init__(self) -> None:
        """Require a positive integer numerator and power-of-two denominator."""
        if (isinstance(self.numerator, bool) or not isinstance(self.numerator, int)
                or self.numerator <= 0):
            raise ValueError("Time signature numerator must be a positive integer")
        if (isinstance(self.denominator, bool) or not isinstance(self.denominator, int)
                or self.denominator <= 0 or self.denominator & (self.denominator - 1)):
            raise ValueError("Time signature denominator must be a positive power of two")

    @property
    def duration(self) -> Fraction:
        """Return measure length, e.g. 6/8 = 3/4 of a whole note."""
        return Fraction(self.numerator, self.denominator)

    def __str__(self) -> str:
        """Format the meter, e.g. '3/4'."""
        return f"{self.numerator}/{self.denominator}"


@dataclass(frozen=True, slots=True)
class KeySignature:
    """Traditional key signature by circle-of-fifths and mode.

    Inputs: fifths from -7 (seven flats) to +7 (seven sharps), mode.
    """

    fifths: int = 0
    mode: str = "major"

    def __post_init__(self) -> None:
        """Validate conventional key signature values."""
        if isinstance(self.fifths, bool) or not isinstance(self.fifths, int) or not -7 <= self.fifths <= 7:
            raise ValueError("Key signature fifths must be an integer between -7 and 7")
        if self.mode not in ("major", "minor"):
            raise ValueError("Key signature mode must be 'major' or 'minor'")
