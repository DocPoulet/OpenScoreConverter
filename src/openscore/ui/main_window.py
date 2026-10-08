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
    """Main window for the v0.0.4 interactive note editor.

    Inputs: none; project state is initially empty.
    Outputs: signals/actions perform only the features this version supports.
    """

    def __init__(self) -> None:
        """Initialize window, action wiring, pages and persisted geometry."""
        super().__init__()
        self.session = ProjectSession()
        self._dirty = False
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
        self._project.feedback.connect(self.statusBar().showMessage)
        self._project.modified.connect(self._mark_dirty)

        self._build_actions()
        self._build_menus()
        self._build_toolbar()
        self.statusBar().showMessage("Ready — v0.0.4 interactive score editor")

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
        self.demo_action.setStatusTip("Edit notes, rests and chords in the example score")
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
        if not self._confirm_discard():
            return
        self.session.create_new()
        self._dirty = False
        self._project.set_score(self.session.score)
        self._pages.setCurrentWidget(self._project)
        self.setWindowTitle(f"{self.session.name} — {APP_NAME}")
        self.statusBar().showMessage("Blank staff ready · Select Add note and click a staff position", 8000)

    def open_demo_project(self) -> None:
        """Show a built-in score containing events that can now be edited."""
        if not self._confirm_discard():
            return
        self.session.load_demo()
        self._dirty = False
        self._project.set_score(self.session.score)
        self._pages.setCurrentWidget(self._project)
        self.setWindowTitle(f"{self.session.name} — {APP_NAME}")
        self.statusBar().showMessage("Example loaded · Click a note to edit it · Unsaved edits will be lost on exit", 8000)

    def show_about(self) -> None:
        """Display project version and license information."""
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"{APP_NAME} v{VERSION}\n\n"
            "Open-source music transcription and score editing.\n"
            "Current release: editable in-memory treble-clef scores.\n"
            "Save/load and Undo/Redo are planned for later versions.\n\n"
            "License: GNU GPL-3.0-only",
        )

    def _mark_dirty(self) -> None:
        """Mark the document as edited; saving is not implemented yet."""
        self._dirty = True
        if self.session.has_project:
            self.setWindowTitle(f"* {self.session.name} — {APP_NAME}")

    def _confirm_discard(self) -> bool:
        """Ask before discarding unsaved edits; returns True to continue."""
        if not self._dirty:
            return True
        answer = QMessageBox.question(
            self, "Discard unsaved changes?",
            "This version cannot save scores yet. Discard your current edits?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return answer == QMessageBox.StandardButton.Yes

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        """Save the window geometry when the user closes the application.

        Args:
            event: Qt close event.

        Returns:
            None.
        """
        if not self._confirm_discard():
            event.ignore()
            return
        QSettings(APP_ORGANIZATION, APP_NAME).setValue(
            "main_window/geometry", self.saveGeometry()
        )
        super().closeEvent(event)
