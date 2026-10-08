"""Monophonic written voices. Different voices may overlap each other."""

from dataclasses import dataclass, field
from fractions import Fraction

from .events import Chord, Note, Rest, ScoreEvent
from .primitives import exact_fraction


@dataclass(slots=True)
class Voice:
    """A chronological, non-overlapping sequence of events in one measure."""

    events: list[ScoreEvent] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Normalize initial event ordering and validate non-overlap."""
        incoming = list(self.events)
        self.events = []
        for event in incoming:
            self.add_event(event)

    @property
    def end(self) -> Fraction:
        """Return the last event's end, or zero for an empty voice."""
        return self.events[-1].end if self.events else Fraction(0)

    @property
    def occupied_duration(self) -> Fraction:
        """Return total explicit event time, excluding unfilled gaps."""
        return sum((event.duration for event in self.events), Fraction(0))

    def add_event(self, event: ScoreEvent) -> None:
        """Insert an event chronologically; reject any same-voice overlap.

        Args: event is a Note, Rest or Chord with local start/duration.
        Returns: None, raising ValueError without mutation on overlap.
        """
        if not isinstance(event, (Note, Rest, Chord)):
            raise TypeError("Voice events must be Note, Rest or Chord")
        if any(event.start < existing.end and existing.start < event.end for existing in self.events):
            raise ValueError("Events in the same voice cannot overlap")
        self.events.append(event)
        self.events.sort(key=lambda item: item.start)

    def gaps(self, measure_duration: Fraction) -> list[tuple[Fraction, Fraction]]:
        """Return uncovered [start, end) regions within the measure.

        Args: measure_duration is the effective measure capacity.
        Returns: list of exact (start, end) gap tuples.
        """
        limit = exact_fraction(measure_duration)
        if limit <= 0:
            raise ValueError("Measure duration must be positive")
        missing: list[tuple[Fraction, Fraction]] = []
        cursor = Fraction(0)
        for event in self.events:
            if event.start > cursor:
                missing.append((cursor, min(event.start, limit)))
            cursor = max(cursor, event.end)
        if cursor < limit:
            missing.append((cursor, limit))
        return [(start, end) for start, end in missing if end > start]

    def is_complete(self, measure_duration: Fraction) -> bool:
        """Return True when explicit events fill the full measure with no gaps."""
        limit = exact_fraction(measure_duration)
        return bool(self.events) and self.end <= limit and not self.gaps(limit)
