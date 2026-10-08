"""Welcome and empty-project views for the v0.0.2 shell."""

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
    demo_requested = Signal()

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

        version = QLabel("OPEN-SOURCE SCORE EDITOR   /   V0.0.3")
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
        demo = QPushButton("View example score")
        demo.setCursor(Qt.CursorShape.PointingHandCursor)
        demo.clicked.connect(lambda _checked=False: self.demo_requested.emit())
        actions.addWidget(demo)
        actions.addStretch(1)
        card_layout.addLayout(actions)
        card_layout.addSpacing(13)

        note = QLabel("See the first staff preview · Editing arrives in v0.0.4")
        note.setObjectName("mutedLabel")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setWordWrap(True)
        card_layout.addWidget(note)

        root.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        root.addStretch(2)


