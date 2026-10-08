"""A musical part, which may contain multiple simultaneous staves."""

from dataclasses import dataclass, field

from .staff import Staff


@dataclass(slots=True)
class Part:
    """A named instrumental part, e.g. Piano, supporting multiple staves."""

    name: str
    staves: list[Staff] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Reject blank part names and invalid initial staff objects."""
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Part name cannot be blank")
        self.name = self.name.strip()
        if any(not isinstance(staff, Staff) for staff in self.staves):
            raise TypeError("Part staves must contain Staff objects")

    def add_staff(self, staff: Staff) -> None:
        """Append a staff to the part; returns None."""
        if not isinstance(staff, Staff):
            raise TypeError("Expected a Staff")
        self.staves.append(staff)
