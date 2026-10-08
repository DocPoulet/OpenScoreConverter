"""In-memory score preview workspace (intentionally read-only in v0.0.3)."""

from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtWidgets import (
    QFrame, QGraphicsScene, QGraphicsView, QHBoxLayout, QLabel,
    QPushButton, QVBoxLayout, QWidget,
)

from ...score import Score
from ..notation.scene_renderer import ScoreSceneRenderer


class ScoreView(QGraphicsView):
    """Scrollable Qt vector score preview with future event IDs on noteheads."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Set up a white graphics-paper scene and comfortable zoom."""
        super().__init__(parent)
        self._score_scene = QGraphicsScene(self)
        self._renderer = ScoreSceneRenderer(self._score_scene)
        self.setScene(self._score_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.setBackgroundBrush(QBrush(QColor("#1c2635")))
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setMinimumHeight(330)
        self._zoom = 1.0
        self._renderer.draw(None)

    @property
    def zoom_percent(self) -> int:
        """Return current absolute zoom percentage."""
        return round(self._zoom * 100)

    def set_score(self, score: Score | None) -> None:
        """Rebuild the scene from model data without modifying that data."""
        self._renderer.draw(score)
        self.resetTransform()
        self._zoom = 1.0
        self.centerOn(self.scene().sceneRect().center())

    def change_zoom(self, factor: float) -> None:
        """Zoom uniformly between 50% and 250%, avoiding runaway scales."""
        zoom = min(2.5, max(.5, self._zoom * factor))
        self.scale(zoom / self._zoom, zoom / self._zoom)
        self._zoom = zoom

    def reset_zoom(self) -> None:
        """Return to one scene pixel per logical device pixel."""
        self.resetTransform()
        self._zoom = 1.0


class ScoreWorkspace(QWidget):
    """Read-only score preview and the metadata/zoom tools surrounding it."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create an accessible layout with a scrollable white page."""
        super().__init__(parent)
        self.setObjectName("root")
        outer = QVBoxLayout(self)
        outer.setContentsMargins(28, 20, 28, 23)
        outer.setSpacing(12)

        headline = QHBoxLayout()
        name_group = QVBoxLayout()
        self.project_title = QLabel("Untitled")
        self.project_title.setObjectName("pageTitle")
        name_group.addWidget(self.project_title)
        self.summary_label = QLabel("New in-memory score")
        self.summary_label.setObjectName("subtitle")
        name_group.addWidget(self.summary_label)
        headline.addLayout(name_group, stretch=1)
        for caption, factor in (("−", .8), ("+", 1.25)):
            button = QPushButton(caption)
            button.setToolTip("Zoom out" if factor < 1 else "Zoom in")
            button.setFixedWidth(43)
            button.clicked.connect(lambda _checked=False, f=factor: self._update_zoom(f))
            headline.addWidget(button)
        self.zoom_label = QPushButton("100%")
        self.zoom_label.setToolTip("Reset zoom to 100%")
        self.zoom_label.setFixedWidth(70)
        self.zoom_label.clicked.connect(self._reset_zoom)
        headline.addWidget(self.zoom_label)
        outer.addLayout(headline)

        frame = QFrame()
        frame.setObjectName("scorePreviewFrame")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(8, 8, 8, 8)
        self.score_view = ScoreView()
        frame_layout.addWidget(self.score_view)
        outer.addWidget(frame, stretch=1)
        notice = QLabel("Preview only · Notes are not editable yet · Changes are not saved")
        notice.setObjectName("mutedLabel")
        outer.addWidget(notice)

    def set_score(self, score: Score | None) -> None:
        """Update title, structural summary and preview from one Score."""
        if score is None:
            self.project_title.setText("No active score")
            self.summary_label.setText("Create a score to begin")
        else:
            self.project_title.setText(score.title)
            staves = sum(len(part.staves) for part in score.parts)
            measures = sum(len(staff.measures) for part in score.parts for staff in part.staves)
            self.summary_label.setText(
                f"{len(score.parts)} part · {staves} staff · {measures} measure"
                + ("s" if measures != 1 else "") + " · In memory"
            )
        self.score_view.set_score(score)
        self.zoom_label.setText("100%")

    def _update_zoom(self, factor: float) -> None:
        """Apply user-requested zoom and refresh the control label."""
        self.score_view.change_zoom(factor)
        self.zoom_label.setText(f"{self.score_view.zoom_percent}%")

    def _reset_zoom(self) -> None:
        """Reset zoom when its clickable label is pressed."""
        self.score_view.reset_zoom()
        self.zoom_label.setText("100%")
