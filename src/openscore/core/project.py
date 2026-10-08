"""Project shell for v0.0.1. This is not yet a musical score model."""

from dataclasses import dataclass


@dataclass(slots=True)
class ProjectSession:
    """Track the currently active, unsaved project placeholder.

    Inputs: `name` is the optional display name of the active project.
    Outputs: the `has_project` property exposes whether one exists.
    """

    name: str | None = None

    @property
    def has_project(self) -> bool:
        """Return True if a placeholder project has been created."""
        return self.name is not None

    def create_new(self, name: str = "Untitled") -> None:
        """Replace the current in-memory project with a new placeholder.

        Args:
            name: Display name of the new project; cannot be blank.

        Returns:
            None. Updates the current instance in place.
        """
        if not name.strip():
            raise ValueError("Project name cannot be blank")
        self.name = name.strip()

    def clear(self) -> None:
        """Return to the state where no project is open."""
        self.name = None
