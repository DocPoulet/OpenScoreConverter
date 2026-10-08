"""Rendering geometry and sample-model tests; all run without Qt."""

from fractions import Fraction as F
import unittest

from openscore.engraving import DurationGlyph, duration_glyph, measure_slots, staff_step
from openscore.score import Measure, Note, Pitch, Rest, create_demo_piano_score


class LayoutTests(unittest.TestCase):
    """Test exact geometry inputs, glyph lookup and nonmutation."""

    def test_staff_positions_treble(self):
        self.assertEqual(staff_step(Pitch("E", 4)), 0)
        self.assertEqual(staff_step(Pitch("F", 5)), 8)
        self.assertEqual(staff_step(Pitch("C", 4)), -2)
        self.assertEqual(staff_step(Pitch("A", 5)), 10)

    def test_staff_positions_bass_and_unsupported(self):
        self.assertEqual(staff_step(Pitch("G", 2), "bass"), 0)
        self.assertEqual(staff_step(Pitch("A", 3), "bass"), 8)
        with self.assertRaises(ValueError):
            staff_step(Pitch("C", 4), "percussion")

    def test_standard_durations(self):
        for base in (F(1), F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 32)):
            self.assertEqual(duration_glyph(base), DurationGlyph(base))

    def test_dotted_durations(self):
        self.assertEqual(duration_glyph(F(3, 8)), DurationGlyph(F(1, 4), 1))
        self.assertEqual(duration_glyph(F(7, 16)), DurationGlyph(F(1, 4), 2))

    def test_triplets_and_unsupported_duration(self):
        self.assertEqual(duration_glyph(F(1, 12)), DurationGlyph(F(1, 8), 0, 3))
        self.assertEqual(duration_glyph(F(1, 6)), DurationGlyph(F(1, 4), 0, 3))
        self.assertIsNone(duration_glyph(F(5, 16)))
        with self.assertRaises(ValueError):
            duration_glyph(0)
        with self.assertRaises(TypeError):
            duration_glyph(0.125)

    def test_measure_slots_merge_voices(self):
        bar = Measure()
        bar.add_note(Pitch("C", 4), F(1, 4))
        bar.add_note(Pitch("D", 4), F(1, 4))
        second = bar.add_voice()
        bar.add_event(Rest(F(1, 4), F(1, 2)), second)
        self.assertEqual(measure_slots(bar), (F(0), F(1, 4)))

    def test_blank_measure_has_first_slot(self):
        self.assertEqual(measure_slots(Measure()), (F(0),))

    def test_demo_is_complete_and_independent(self):
        demo = create_demo_piano_score()
        self.assertEqual(len(demo.parts[0].staves[0].measures), 4)
        self.assertEqual(demo.validate(), [])
        another = create_demo_piano_score()
        demo.parts[0].staves[0].measures.append(Measure(number=5))
        self.assertEqual(len(another.parts[0].staves[0].measures), 4)


if __name__ == "__main__":
    unittest.main()
