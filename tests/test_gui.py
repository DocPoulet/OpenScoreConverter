"""Qt widget smoke tests; require PySide6 to be installed."""

import os
import unittest

# Allow GUI integration checks on headless CI machines.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication
    from openscore.ui.main_window import MainWindow
except ImportError:
    QApplication = None
    MainWindow = None


@unittest.skipUnless(QApplication is not None, "PySide6 not installed")
class MainWindowTests(unittest.TestCase):
    """Exercise the real Qt window without displaying it on screen."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()

    def test_window_opens_without_project(self):
        self.assertFalse(self.window.session.has_project)
        self.assertIn("OpenScore Converter", self.window.windowTitle())

    def test_new_action_changes_workspace(self):
        self.window.new_action.trigger()
        self.assertTrue(self.window.session.has_project)
        self.assertIsNotNone(self.window.session.score)
        self.assertIn("1 part", self.window._project.summary_label.text())
        self.assertIn("Untitled", self.window.windowTitle())
        self.assertEqual(self.window._pages.currentWidget(), self.window._project)

    def test_example_score_displays_graphical_events(self):
        self.window.demo_action.trigger()
        self.assertEqual(len(self.window.session.score.parts[0].staves[0].measures), 4)
        scene = self.window._project.score_view.scene()
        self.assertGreater(len(scene.items()), 30)
        self.assertTrue(any(item.data(0) == (0, 0, 0, 0, 0) for item in scene.items()))
        self.assertIn("4 measures", self.window._project.summary_label.text())

    def test_preview_zoom_and_reset(self):
        self.window.demo_action.trigger()
        self.window._project.score_view.change_zoom(1.25)
        self.assertEqual(self.window._project.score_view.zoom_percent, 125)
        self.window._project.score_view.reset_zoom()
        self.assertEqual(self.window._project.score_view.zoom_percent, 100)

    def test_new_score_renders_empty_staff(self):
        self.window.new_action.trigger()
        scene = self.window._project.score_view.scene()
        self.assertTrue(any("Empty measure" in item.text() for item in scene.items()
                            if hasattr(item, "text")))

    def test_unavailable_actions_are_disabled(self):
        self.assertFalse(self.window.open_action.isEnabled())
        self.assertFalse(self.window.save_action.isEnabled())
        self.assertFalse(self.window.undo_action.isEnabled())
        self.assertFalse(self.window.redo_action.isEnabled())

    def test_status_bar_toggle(self):
        self.window.show()
        self.app.processEvents()
        self.window.status_bar_action.setChecked(False)
        self.assertFalse(self.window.statusBar().isVisible())
        self.window.status_bar_action.setChecked(True)
        self.assertTrue(self.window.statusBar().isVisible())


if __name__ == "__main__":
    unittest.main()
