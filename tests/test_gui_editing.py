"""Optional offscreen Qt integration tests for the new interactive editor."""

import os
import unittest
from fractions import Fraction as F

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication
    from openscore.editor import EventPath
    from openscore.score import Note, Pitch
    from openscore.ui.main_window import MainWindow
except ImportError:
    QApplication = None


@unittest.skipUnless(QApplication is not None, "PySide6 not installed")
class EditingWindowTests(unittest.TestCase):
    """Check that Qt controls mutate the same Score used by the renderer."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = MainWindow()
        self.window.create_new_project()
        self.workspace = self.window._project

    def tearDown(self):
        # Tests modify in-memory scores but must never open a modal discard dialog.
        self.window._dirty = False
        self.window.close()

    def test_click_insert_handler_updates_score_and_selection(self):
        self.workspace._insert_at_position(0, Pitch("C", 5), F(0))
        measure = self.window.session.score.parts[0].staves[0].measures[0]
        self.assertEqual(len(measure.voices[0].events), 1)
        self.assertEqual(measure.voices[0].events[0].pitch, Pitch("C", 5))
        self.assertTrue(self.window._dirty)
        self.assertEqual(self.workspace.selection, [EventPath(0, 0, 0, 0, 0)])
        self.assertTrue(any(i.data(0) == (0,0,0,0,0) for i in self.workspace.score_view.scene().items()))

    def test_property_editor_updates_selected_note(self):
        self.workspace._insert_at_position(0, Pitch("C", 5), F(0))
        self.workspace.pitch_step.setCurrentText("D")
        self.assertEqual(self.workspace.editor.event(self.workspace.selection[0]).pitch, Pitch("D", 5))
        self.workspace.property_duration.setCurrentIndex(1)
        self.assertEqual(self.workspace.editor.event(self.workspace.selection[0]).duration, F(1, 2))

    def test_delete_button_removes_note(self):
        self.workspace._insert_at_position(0, Pitch("C", 5), F(0))
        self.workspace.delete_selection()
        self.assertEqual(len(self.workspace.editor.measure(0).voices[0].events), 0)

    def test_keyboard_note_append_and_new_measure(self):
        self.workspace.set_mode("insert")
        self.workspace._key_command("C")
        self.workspace.add_measure()
        self.workspace._key_command("D")
        self.assertEqual(len(self.workspace.editor.measure(1).voices[0].events), 1)
        self.assertEqual(self.workspace.active_measure, 1)

    def test_selection_click_ctrl_toggle(self):
        first = self.workspace.editor.insert_note(0, Pitch("C", 5), F(1,4))
        second = self.workspace.editor.insert_note(0, Pitch("D", 5), F(1,4))
        self.workspace._refresh()
        self.workspace._event_clicked(first, False)
        self.workspace._event_clicked(second, True)
        self.assertEqual(len(self.workspace.selection), 2)
        self.workspace._event_clicked(first, True)
        self.assertEqual(self.workspace.selection, [second])


if __name__ == "__main__":
    unittest.main()
