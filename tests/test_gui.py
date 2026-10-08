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
        self.assertIn("Untitled", self.window.windowTitle())
        self.assertEqual(self.window._pages.currentWidget(), self.window._project)

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
