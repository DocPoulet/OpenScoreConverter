"""Current project session and its independent in-memory musical score."""

from dataclasses import dataclass

from ..score import Score, create_blank_piano_score, create_demo_piano_score


@dataclass(slots=True)
class ProjectSession:
    """Keep one active editable score in memory; persistence comes later.

    Attributes:
        name: Display name, or None when no score is open.
        score: Musical document, or None when no project is open.
    """

    name: str | None = None
    score: Score | None = None

    @property
    def has_project(self) -> bool:
        """Return True when the session owns a real musical score."""
        return self.score is not None

    def create_new(self, name: str = "Untitled") -> None:
        """Replace the project with a fresh piano right-hand score.

        Args: display name, which cannot be blank.
        Returns: None. Previous in-memory score is replaced.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Project name cannot be blank")
        title = name.strip()
        new_score = create_blank_piano_score(title)
        self.name = title
        self.score = new_score

    def load_demo(self) -> None:
        """Replace the active project with an editable demonstration score.

        Args: none.
        Returns: None. The score remains in memory, not saved to disk.
        """
        self.score = create_demo_piano_score()
        self.name = self.score.title

    def clear(self) -> None:
        """Return to welcome state by dropping the active score."""
        self.name = None
        self.score = None
