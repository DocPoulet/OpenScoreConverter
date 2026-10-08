"""Top-level score, validation messages, and blank-piano factory."""

from dataclasses import dataclass, field

from .measure import Measure
from .part import Part
from .primitives import Clef, KeySignature, TimeSignature
from .staff import Staff


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A machine-readable warning for unfinished/ambiguous notation.

    Inputs: code is stable, location is a navigable model path, message is prose.
    """

    code: str
    location: str
    message: str


@dataclass(slots=True)
class Score:
    """Format-independent musical document (never a Qt or MIDI object).

    Args: title, optional composer, and ordered instrumental parts.
    """

    title: str = "Untitled"
    composer: str = ""
    parts: list[Part] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate title and supplied parts."""
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Score title cannot be blank")
        self.title = self.title.strip()
        if not isinstance(self.composer, str):
            raise TypeError("Composer must be a string")
        if any(not isinstance(part, Part) for part in self.parts):
            raise TypeError("Score parts must contain Part objects")

    def add_part(self, part: Part) -> None:
        """Append an instrumental part to the score; returns None."""
        if not isinstance(part, Part):
            raise TypeError("Expected a Part")
        self.parts.append(part)

    def validate(self) -> list[ValidationIssue]:
        """Report missing staves/bars and unfilled voice gaps.

        Incomplete measures are allowed during editing; validation reports
        warnings rather than inventing rests or rejecting draft scores.
        Returns: list of descriptive ValidationIssue objects.
        """
        issues: list[ValidationIssue] = []
        if not self.parts:
            issues.append(ValidationIssue("NO_PARTS", "score", "Score has no parts"))
        for pi, part in enumerate(self.parts):
            ppath = f"parts[{pi}]"
            if not part.staves:
                issues.append(ValidationIssue("NO_STAVES", ppath, "Part has no staves"))
            for si, staff in enumerate(part.staves):
                spath = f"{ppath}.staves[{si}]"
                if not staff.measures:
                    issues.append(ValidationIssue("NO_MEASURES", spath, "Staff has no measures"))
                for mi, measure in enumerate(staff.measures):
                    mpath = f"{spath}.measures[{mi}]"
                    for vi, voice in enumerate(measure.voices):
                        for start, end in voice.gaps(measure.duration):
                            issues.append(ValidationIssue(
                                "UNFILLED_VOICE", f"{mpath}.voices[{vi}]",
                                f"Unfilled interval [{start}, {end}) in measure {measure.number}",
                            ))
        return issues


def create_blank_piano_score(title: str = "Untitled") -> Score:
    """Make a single-staff, single-bar C-major 4/4 piano score.

    Args: title of the new document.
    Returns: independent editable Score, with an empty initial measure.
    """
    score = Score(title=title)
    part = Part(name="Piano")
    staff = Staff(clef=Clef.TREBLE, key_signature=KeySignature())
    staff.add_measure(Measure(number=1, time_signature=TimeSignature(4, 4)))
    part.add_staff(staff)
    score.add_part(part)
    return score
