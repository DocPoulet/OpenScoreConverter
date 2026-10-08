"""Welcome and empty-project views for the v0.0.1 shell."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class WelcomeView(QWidget):
    """Show a welcome card with a request to create a project.

    Emits:
        new_requested(): when the user clicks the New score button.
    """

    new_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create the welcome page and connect the primary action."""
        super().__init__(parent)
        self.setObjectName("root")
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.addStretch(1)

        card = QFrame()
        card.setObjectName("heroCard")
        card.setMaximumWidth(750)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(54, 45, 54, 50)
        card_layout.setSpacing(15)

        icon = QLabel("♫")
        icon.setObjectName("brandSymbol")
        icon.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        card_layout.addWidget(icon)

        version = QLabel("OPEN-SOURCE SCORE EDITOR   /   V0.0.1")
        version.setObjectName("eyebrow")
        version.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        card_layout.addWidget(version)

        title = QLabel("OpenScore Converter")
        title.setObjectName("heroTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Your workspace for musical notation and transcription.")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(18)
        actions = QHBoxLayout()
        actions.addStretch(1)
        button = QPushButton("＋  New score")
        button.setObjectName("primaryButton")
        button.setMinimumWidth(180)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(lambda _checked=False: self.new_requested.emit())
        actions.addWidget(button)
        actions.addStretch(1)
        card_layout.addLayout(actions)
        card_layout.addSpacing(13)

        note = QLabel("Foundation release · Musical editing starts in upcoming versions")
        note.setObjectName("mutedLabel")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)
        card_layout.addWidget(note)

        root.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        root.addStretch(2)


class ProjectPlaceholderView(QWidget):
    """Display an honest placeholder for an active, unsaved project.

    Inputs:
        name: current project name, through `set_project_name`.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Build a blank musical workspace placeholder."""
        super().__init__(parent)
        self.setObjectName("root")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 27, 36, 32)
        layout.setSpacing(16)

        self.project_title = QLabel("Untitled")
        self.project_title.setObjectName("pageTitle")
        layout.addWidget(self.project_title)

        description = QLabel("New in-memory project · Not saved to disk")
        description.setObjectName("subtitle")
        layout.addWidget(description)

        canvas = QFrame()
        canvas.setObjectName("scorePlaceholder")
        canvas_layout = QVBoxLayout(canvas)
        canvas_layout.setContentsMargins(30, 30, 30, 30)
        canvas_layout.addStretch(1)

        placeholder_title = QLabel("Empty score workspace")
        placeholder_title.setObjectName("pageTitle")
        placeholder_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        canvas_layout.addWidget(placeholder_title)

        placeholder_text = QLabel(
            "The score model arrives in v0.0.2.\n"
            "Sheet music rendering and editing will follow."
        )
        placeholder_text.setObjectName("mutedLabel")
        placeholder_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_text.setWordWrap(True)
        canvas_layout.addWidget(placeholder_text)
        canvas_layout.addStretch(1)
        layout.addWidget(canvas, stretch=1)

    def set_project_name(self, name: str) -> None:
        """Update the visible project name.

        Args:
            name: Name to display.

        Returns:
            None.
        """
        self.project_title.setText(name)
