"""A sample score used to inspect v0.0.3 rendering without editing tools."""

from fractions import Fraction as F

from .primitives import Pitch
from .score import Score, create_blank_piano_score


def create_demo_piano_score() -> Score:
    """Return a complete four-bar treble-clef preview with notes/rests/chords.

    Args: none.
    Returns: independent Score in 4/4 C major, featuring ledger lines,
             filled/hollow heads, note flags, a sharp and dotted rhythm.
    """
    score = create_blank_piano_score("First steps")
    score.composer = "OpenScore Converter · demonstration"
    staff = score.parts[0].staves[0]
    first = staff.measures[0]
    first.add_note(Pitch("C", 5), F(1, 4))
    first.add_note(Pitch("D", 5), F(1, 4))
    first.add_note(Pitch("E", 5), F(1, 8))
    first.add_note(Pitch("F", 5), F(1, 8))
    first.add_note(Pitch("G", 5), F(1, 4))

    second = staff.new_measure()
    second.add_chord((Pitch("C", 5), Pitch("E", 5), Pitch("G", 5)), F(1, 2))
    second.add_rest(F(1, 4))
    second.add_note(Pitch("A", 4), F(1, 8))
    second.add_note(Pitch("B", 4), F(1, 8))

    third = staff.new_measure()
    third.add_note(Pitch("C", 4), F(1))

    fourth = staff.new_measure()
    fourth.add_note(Pitch("F", 5, 1), F(1, 4))
    fourth.add_note(Pitch("G", 5), F(1, 8))
    fourth.add_note(Pitch("A", 5), F(1, 8))
    fourth.add_note(Pitch("G", 5), F(3, 8))
    fourth.add_rest(F(1, 8))
    return score
