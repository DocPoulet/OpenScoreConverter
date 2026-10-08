"""Standalone demo: build a complete C4/D4/E4 score without a GUI."""

from fractions import Fraction

from openscore.score import Pitch, create_blank_piano_score


def main() -> None:
    """Build a right-hand 4/4 phrase and print its exact structure."""
    score = create_blank_piano_score("First melody")
    bar = score.parts[0].staves[0].measures[0]
    bar.add_note(Pitch("C", 4), Fraction(1, 4))
    bar.add_note(Pitch("D", 4), Fraction(1, 4))
    bar.add_note(Pitch("E", 4), Fraction(1, 2))
    print(f"Score: {score.title}")
    print(f"Part: {score.parts[0].name} | Meter: {bar.time_signature}")
    for event in bar.voices[0].events:
        print(f"  {event.pitch} | start={event.start} | duration={event.duration}")
    print(f"Measure complete: {bar.is_complete}")
    print(f"Validation issues: {len(score.validate())}")


if __name__ == '__main__':
    main()
