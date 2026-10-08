"""Written staves: ordered measure containers with staff-level notation."""

from dataclasses import dataclass, field

from .measure import Measure
from .primitives import Clef, KeySignature, TimeSignature


@dataclass(slots=True)
class Staff:
    """A notation staff with clef, initial key and an ordered list of bars."""

    clef: Clef = Clef.TREBLE
    key_signature: KeySignature = field(default_factory=KeySignature)
    measures: list[Measure] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate supplied staff metadata and measure ordering."""
        if not isinstance(self.clef, Clef):
            raise TypeError("Staff clef must be a Clef enum")
        if not isinstance(self.key_signature, KeySignature):
            raise TypeError("Staff key_signature must be a KeySignature")
        old = list(self.measures)
        self.measures = []
        for measure in old:
            self.add_measure(measure)

    def add_measure(self, measure: Measure) -> None:
        """Append a bar; enforce sequential numbering starting at 1."""
        if not isinstance(measure, Measure):
            raise TypeError("Staff accepts Measure instances only")
        expected_number = len(self.measures) + 1
        if measure.number != expected_number:
            raise ValueError(f"Expected measure {expected_number}, got {measure.number}")
        self.measures.append(measure)

    def new_measure(self, time_signature: TimeSignature | None = None) -> Measure:
        """Append a fresh empty bar, inheriting meter from its predecessor.

        Args: optional override to start a new meter.
        Returns: new Measure already attached to this staff.
        """
        meter = time_signature or (self.measures[-1].time_signature if self.measures else TimeSignature())
        measure = Measure(number=len(self.measures) + 1, time_signature=meter)
        self.add_measure(measure)
        return measure
