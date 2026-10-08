"""Pure layout calculations shared by the Qt preview and future export engines.

All rhythmic positions are exact; this module neither imports Qt nor mutates a
score.  Engraving here is intentionally limited to the pre-alpha notation set.
"""

from dataclasses import dataclass
from fractions import Fraction

from ..score import Measure, Pitch
from ..score.primitives import exact_fraction


@dataclass(frozen=True, slots=True)
class DurationGlyph:
    """A primitive note/rest shape: base duration, augmentation dots, tuplet.

    Args:
        base: Written undotted power-of-two duration (whole-note units).
        dots: Number of augmentation dots.
        tuplet: 3 denotes one of three notes in the time of two.
    """

    base: Fraction
    dots: int = 0
    tuplet: int | None = None


_BASES = tuple(Fraction(1, 2**power) for power in range(0, 6))


def duration_glyph(duration: Fraction | int | str) -> DurationGlyph | None:
    """Return a supported standard duration shape, otherwise None.

    Args: positive rational duration in whole-note units.
    Returns: shape for undotted, dotted (up to two dots), or a basic triplet;
             None if a truthful conventional glyph is not supported yet.
    """
    value = exact_fraction(duration)
    if value <= 0:
        raise ValueError("Notation duration must be positive")
    for base in _BASES:
        for dots in range(3):
            multiplier = sum((Fraction(1, 2**i) for i in range(dots + 1)), Fraction(0))
            if value == base * multiplier:
                return DurationGlyph(base, dots)
    for base in _BASES[2:]:  # quarter/eighth/etc triplets
        if value == base * Fraction(2, 3):
            return DurationGlyph(base, 0, 3)
    return None


_STEPS = {"C": 0, "D": 1, "E": 2, "F": 3, "G": 4, "A": 5, "B": 6}


def staff_step(pitch: Pitch, clef: str = "treble") -> int:
    """Return diatonic half-space offsets from the bottom staff line.

    Args: spelled pitch and supported clef string ('treble' or 'bass').
    Returns: 0 for E4 in treble (G2 in bass); +8 for upper staff line.
    Raises: ValueError for unsupported clef.
    """
    bottom = {"treble": ("E", 4), "bass": ("G", 2)}.get(clef)
    if bottom is None:
        raise ValueError(f"Unsupported staff clef: {clef}")
    letter, octave = bottom
    return 7 * (pitch.octave - octave) + _STEPS[pitch.step] - _STEPS[letter]


def measure_slots(measure: Measure) -> tuple[Fraction, ...]:
    """Return unique sorted onsets from every voice in one measure.

    Args: an existing Measure from the score model.
    Returns: immutable sorted Fraction onsets; at least 0 for an empty bar.
    """
    return tuple(sorted({Fraction(0)} | {
        event.start for voice in measure.voices for event in voice.events
    }))
