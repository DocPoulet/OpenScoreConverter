"""Desktop application frame, menus and project-page switching."""

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QToolBar

from ..config import APP_NAME, APP_ORGANIZATION, VERSION
from ..core.project import ProjectSession
from .widgets.score_workspace import ScoreWorkspace
from .widgets.welcome_view import WelcomeView


class MainWindow(QMainWindow):
    """Main window for the v0.0.3 notation preview.

    Inputs: none; project state is initially empty.
    Outputs: signals/actions perform only the features this version supports.
    """

    def __init__(self) -> None:
        """Initialize window, action wiring, pages and persisted geometry."""
        super().__init__()
        self.session = ProjectSession()
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(str(Path(__file__).resolve().parents[1] / "assets" / "logo.svg")))
        self.resize(1150, 740)
        self.setMinimumSize(760, 530)

        self._pages = QStackedWidget(self)
        self._welcome = WelcomeView(self)
        self._project = ScoreWorkspace(self)
        self._pages.addWidget(self._welcome)
        self._pages.addWidget(self._project)
        self._pages.setCurrentWidget(self._welcome)
        self.setCentralWidget(self._pages)
        self._welcome.new_requested.connect(self.create_new_project)
        self._welcome.demo_requested.connect(self.open_demo_project)

        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self.statusBar().showMessage("Ready — v0.0.3 score preview")

        settings = QSettings(APP_ORGANIZATION, APP_NAME)
        saved_geometry = settings.value("main_window/geometry")
        if saved_geometry is not None:
            self.restoreGeometry(saved_geometry)

    def _build_actions(self) -> None:
        """Create actions and connect only implemented commands."""
        self.new_action = QAction("&New score", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.setStatusTip("Create a new in-memory piano score")
        self.new_action.triggered.connect(self.create_new_project)

        self.demo_action = QAction("Open &example score", self)
        self.demo_action.setStatusTip("Preview notes, rests and chords in an example score")
        self.demo_action.triggered.connect(self.open_demo_project)

        self.open_action = QAction("&Open…", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.setEnabled(False)
        self.open_action.setStatusTip("Coming in a later release")

        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.setEnabled(False)
        self.save_action.setStatusTip("Project persistence arrives in a later release")

        self.save_as_action = QAction("Save &as…", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.save_as_action.setEnabled(False)

        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.exit_action.triggered.connect(self.close)

        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.setEnabled(False)

        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.setEnabled(False)

        self.status_bar_action = QAction("&Status bar", self)
        self.status_bar_action.setCheckable(True)
        self.status_bar_action.setChecked(True)
        self.status_bar_action.toggled.connect(self.statusBar().setVisible)

        self.about_action = QAction("&About OpenScore Converter", self)
        self.about_action.triggered.connect(self.show_about)

    def _build_menus(self) -> None:
        """Create the File, Edit, View and Help menus."""
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.demo_action)
        file_menu.addSeparator()
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self.status_bar_action)

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _build_toolbar(self) -> None:
        """Add an early toolbar with only available functions enabled."""
        toolbar = QToolBar("Main", self)
        toolbar.setObjectName("main_toolbar")
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.addToolBar(toolbar)
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.demo_action)
        toolbar.addSeparator()
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)

    def create_new_project(self) -> None:
        """Create a real in-memory piano score and show its summary."""
        self.session.create_new()
        self._project.set_score(self.session.score)
        self._pages.setCurrentWidget(self._project)
        self.setWindowTitle(f"{self.session.name} — {APP_NAME}")
        self.statusBar().showMessage("Blank treble staff ready · Choose 'Open example score' to see notation", 8000)

    def open_demo_project(self) -> None:
        """Show a built-in score demonstrating the read-only notation renderer."""
        self.session.load_demo()
        self._project.set_score(self.session.score)
        self._pages.setCurrentWidget(self._project)
        self.setWindowTitle(f"{self.session.name} — {APP_NAME}")
        self.statusBar().showMessage("Example score loaded · hover notes for pitch and duration", 8000)

    def show_about(self) -> None:
        """Display project version and license information."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} v{VERSION}\n\n"
            "Open-source music transcription and score editing.\n"
            "Current release: read-only staff and note rendering.\n\n"
            "License: GNU GPL-3.0-only",
        )

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        """Save the window geometry when the user closes the application.

        Args:
            event: Qt close event.

        Returns:
            None.
        """
        QSettings(APP_ORGANIZATION, APP_NAME).setValue(
            "main_window/geometry", self.saveGeometry()
        )
        super().closeEvent(event)
