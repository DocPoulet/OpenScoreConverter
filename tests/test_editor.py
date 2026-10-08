"""No-Qt tests for transactional note editing."""

import unittest
from fractions import Fraction as F

from openscore.editor import EventPath, ScoreEditor, pitch_from_staff_step, shift_diatonic
from openscore.engraving import staff_step
from openscore.score import Chord, Note, Pitch, Rest, create_blank_piano_score


class EditorTests(unittest.TestCase):
    """Ensure edits stay within measure capacity and don't corrupt the score."""

    def setUp(self):
        self.score = create_blank_piano_score("Edit tests")
        self.editor = ScoreEditor(self.score)
        self.bar = self.editor.measure(0)

    def test_insert_defaults_to_sequential_note_entry(self):
        first = self.editor.insert_note(0, Pitch("C", 5), F(1, 4))
        second = self.editor.insert_note(0, Pitch("D", 5), F(1, 2))
        self.assertEqual(first.as_tuple(), (0, 0, 0, 0, 0))
        self.assertEqual(second.as_tuple(), (0, 0, 0, 0, 1))
        self.assertEqual(self.editor.event(second).start, F(1, 4))

    def test_insert_at_gap_keeps_ordered_events(self):
        late = self.editor.insert_note(0, Pitch("D", 5), F(1, 4), F(1, 2))
        early = self.editor.insert_note(0, Pitch("C", 5), F(1, 4), F(0))
        self.assertEqual(early.event, 0)
        self.assertEqual([e.start for e in self.bar.voices[0].events], [F(0), F(1, 2)])
        self.assertEqual(self.editor.event(EventPath(0,0,0,0,1)).pitch, Pitch("D", 5))

    def test_insert_overlap_does_not_modify_original(self):
        self.editor.insert_note(0, Pitch("C", 5), F(1, 2))
        original = self.bar.voices[0].events.copy()
        with self.assertRaisesRegex(ValueError, "overlap"):
            self.editor.insert_note(0, Pitch("D", 5), F(1, 4), F(1, 4))
        self.assertEqual(self.bar.voices[0].events, original)

    def test_overflow_does_not_modify_original(self):
        original = self.bar.voices[0].events.copy()
        with self.assertRaisesRegex(ValueError, "beyond"):
            self.editor.insert_note(0, Pitch("C", 5), F(1, 2), F(3, 4))
        self.assertEqual(self.bar.voices[0].events, original)

    def test_change_pitch_keeps_timing(self):
        path = self.editor.insert_note(0, Pitch("C", 5), F(1, 8))
        new_path = self.editor.change_pitch(path, Pitch("F", 5, 1))
        note = self.editor.event(new_path)
        self.assertEqual(note.pitch, Pitch("F", 5, 1))
        self.assertEqual(note.start, F(0))
        self.assertEqual(note.duration, F(1, 8))

    def test_diatonic_up_down_and_octave_wrap(self):
        self.assertEqual(shift_diatonic(Pitch("B", 4), 1), Pitch("C", 5))
        self.assertEqual(shift_diatonic(Pitch("C", 5), -1), Pitch("B", 4))
        path = self.editor.insert_note(0, Pitch("B", 4), F(1, 4))
        path = self.editor.transpose_diatonic(path, 1)
        self.assertEqual(self.editor.event(path).pitch, Pitch("C", 5))

    def test_chord_pitch_edit_rejected_without_mutating(self):
        chord = self.bar.add_chord((Pitch("C", 5), Pitch("E", 5)), F(1, 4))
        path = EventPath(0,0,0,0,0)
        with self.assertRaisesRegex(ValueError, "single notes"):
            self.editor.change_pitch(path, Pitch("G", 5))
        self.assertIs(self.bar.voices[0].events[0], chord)

    def test_change_duration_rejects_collision_atomically(self):
        path = self.editor.insert_note(0, Pitch("C", 5), F(1, 4))
        self.editor.insert_note(0, Pitch("D", 5), F(1, 4))
        original = self.bar.voices[0].events.copy()
        with self.assertRaises(ValueError):
            self.editor.change_duration(path, F(1, 2))
        self.assertEqual(self.bar.voices[0].events, original)

    def test_change_duration_rejects_overflow_atomically(self):
        path = self.editor.insert_note(0, Pitch("C", 5), F(1, 4), F(3, 4))
        with self.assertRaisesRegex(ValueError, "beyond"):
            self.editor.change_duration(path, F(1, 2))
        self.assertEqual(self.editor.event(path).duration, F(1, 4))

    def test_valid_change_duration_note_rest_chord(self):
        path = self.editor.insert_note(0, Pitch("C", 5), F(1, 4))
        new_path = self.editor.change_duration(path, F(1, 2))
        self.assertEqual(self.editor.event(new_path).duration, F(1, 2))
        rest = self.bar.add_rest(F(1, 4), start=F(1, 2))
        path_rest = EventPath(0,0,0,0,1)
        self.assertIsInstance(self.editor.event(self.editor.change_duration(path_rest, F(1, 2))), Rest)
        self.editor.delete(new_path)
        self.editor.delete(EventPath(0,0,0,0,0))
        chord = self.bar.add_chord((Pitch("C", 5), Pitch("G", 5)), F(1, 4))
        cp = self.editor.change_duration(EventPath(0,0,0,0,0), F(1, 2))
        self.assertIsInstance(self.editor.event(cp), Chord)

    def test_delete_one_note(self):
        path = self.editor.insert_note(0, Pitch("C", 5), F(1, 4))
        self.editor.delete(path)
        self.assertEqual(self.bar.voices[0].events, [])

    def test_new_measure_inherits_meter(self):
        self.assertEqual(self.editor.add_measure(), 1)
        self.assertEqual(self.editor.measure(1).duration, F(1))
        path = self.editor.insert_note(1, Pitch("E", 5), F(1))
        self.assertEqual(path.measure, 1)

    def test_two_voices_can_overlap(self):
        self.bar.add_voice()
        self.editor.insert_note(0, Pitch("C", 5), F(1, 2), F(0), 0)
        self.editor.insert_note(0, Pitch("E", 5), F(1, 2), F(0), 1)
        self.assertEqual(len(self.bar.voices), 2)

    def test_path_validation(self):
        self.assertEqual(EventPath.from_tuple((0, 0, 2, 0, 4)).as_tuple(), (0, 0, 2, 0, 4))
        for bad in ((0, 0, 0), (0, 0, -1, 0, 0), (0, 0, 0, True, 0)):
            with self.assertRaises(ValueError):
                EventPath.from_tuple(bad)

    def test_staff_step_round_trip_treble_and_bass(self):
        for clef in ("treble", "bass"):
            for step in range(-12, 18):
                note = pitch_from_staff_step(step, clef)
                self.assertEqual(staff_step(note, clef), step)

    def test_invalid_clav_and_step_rejected(self):
        with self.assertRaises(ValueError):
            pitch_from_staff_step(0, "percussion")
        with self.assertRaises(TypeError):
            pitch_from_staff_step(0.5)

    def test_negative_time_rejected(self):
        with self.assertRaises(ValueError):
            self.editor.insert_note(0, Pitch("C",5), F(1,4), F(-1,4))


if __name__ == "__main__":
    unittest.main()
