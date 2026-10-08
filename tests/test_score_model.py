"""Core score model regression tests (no Qt dependency)."""

from fractions import Fraction as F
import unittest

from openscore.score import (
    Chord, Clef, KeySignature, Measure, Note, Part, Pitch, Rest, Score,
    Staff, TimeSignature, Voice, create_blank_piano_score, exact_fraction,
)


class PrimitiveTests(unittest.TestCase):
    """Check exact time and written musical pitch metadata."""

    def test_quarter_and_triplet_are_exact(self):
        self.assertEqual(exact_fraction('1/4') + exact_fraction('1/12'), F(1, 3))
        self.assertEqual(TimeSignature(6, 8).duration, F(3, 4))

    def test_float_timing_is_rejected(self):
        with self.assertRaises(TypeError):
            exact_fraction(0.25)
        with self.assertRaises(TypeError):
            Note(Pitch('C', 4), 0.0, F(1, 4))

    def test_meter_validations(self):
        for signature in ((0, 4), (4, 3), (4, 0), (True, 4), (4, False)):
            with self.subTest(signature=signature), self.assertRaises(ValueError):
                TimeSignature(*signature)

    def test_pitch_spelling_and_midi(self):
        sharp = Pitch('c', 4, 1)
        flat = Pitch('D', 4, -1)
        self.assertEqual(sharp.midi_number, 61)
        self.assertEqual(sharp.midi_number, flat.midi_number)
        self.assertNotEqual(sharp, flat)
        self.assertEqual(str(sharp), 'C#4')

    def test_pitch_range_check(self):
        self.assertEqual(Pitch('C', -1).midi_number, 0)
        with self.assertRaises(ValueError):
            _ = Pitch('C', 12).midi_number
        with self.assertRaises(ValueError):
            Pitch('H', 4)

    def test_key_signatures(self):
        self.assertEqual(KeySignature(-3, 'minor').fifths, -3)
        with self.assertRaises(ValueError):
            KeySignature(8)
        with self.assertRaises(ValueError):
            KeySignature(0, 'dorian')


class EventTests(unittest.TestCase):
    """Check immutability, onset semantics and chord constraints."""

    def test_exact_note_and_rest_end(self):
        note = Note(Pitch('A', 4), '1/12', '1/6')
        self.assertEqual(note.end, F(1, 4))
        self.assertEqual(Rest(0, F(1, 2)).end, F(1, 2))

    def test_invalid_event_times(self):
        for start, duration in ((-1, F(1, 4)), (0, 0), (1, -1)):
            with self.subTest(start=start, duration=duration), self.assertRaises(ValueError):
                Rest(start, duration)

    def test_chord_contains_unique_pitches(self):
        pitches = (Pitch('C', 4), Pitch('E', 4), Pitch('G', 4))
        chord = Chord(pitches, 0, F(1, 4))
        self.assertEqual(chord.end, F(1, 4))
        with self.assertRaises(ValueError):
            Chord((), 0, 1)
        with self.assertRaises(ValueError):
            Chord((pitches[0], pitches[0]), 0, 1)

    def test_voice_sorted_insertion(self):
        voice = Voice()
        voice.add_event(Note(Pitch('D', 4), F(1, 4), F(1, 4)))
        voice.add_event(Note(Pitch('C', 4), 0, F(1, 4)))
        self.assertEqual([e.start for e in voice.events], [F(0), F(1, 4)])
        self.assertEqual(voice.occupied_duration, F(1, 2))

    def test_overlapping_voice_is_rejected_atomically(self):
        voice = Voice()
        voice.add_event(Rest(0, F(1, 2)))
        with self.assertRaises(ValueError):
            voice.add_event(Note(Pitch('C', 4), F(1, 4), F(1, 4)))
        self.assertEqual(len(voice.events), 1)

    def test_voice_gaps_identified(self):
        voice = Voice([Note(Pitch('C', 4), 0, F(1, 4)),
                       Note(Pitch('D', 4), F(1, 2), F(1, 2))])
        self.assertEqual(voice.gaps(F(1)), [(F(1, 4), F(1, 2))])
        self.assertFalse(voice.is_complete(F(1)))


class MeasureTests(unittest.TestCase):
    """Verify meter bounds, sequential insertion and polyphonic voices."""

    def test_sequential_piano_measure(self):
        bar = Measure()
        bar.add_note(Pitch('C', 4), F(1, 4))
        bar.add_note(Pitch('D', 4), F(1, 4))
        bar.add_note(Pitch('E', 4), F(1, 2))
        self.assertEqual([e.start for e in bar.voices[0].events],
                         [F(0), F(1, 4), F(1, 2)])
        self.assertTrue(bar.is_complete)
        self.assertEqual(bar.duration, F(1))

    def test_one_quarter_missing(self):
        bar = Measure()
        bar.add_note(Pitch('C', 4), F(1, 4))
        bar.add_rest(F(1, 2))
        self.assertFalse(bar.is_complete)
        self.assertEqual(bar.gaps(), [(F(3, 4), F(1))])

    def test_measure_overfill_rejected_without_mutation(self):
        bar = Measure()
        bar.add_note(Pitch('C', 4), F(3, 4))
        with self.assertRaises(ValueError):
            bar.add_note(Pitch('D', 4), F(1, 2))
        self.assertEqual(len(bar.voices[0].events), 1)

    def test_6_8_triplets(self):
        bar = Measure(time_signature=TimeSignature(6, 8))
        for _ in range(9):
            bar.add_note(Pitch('C', 4), F(1, 12))
        self.assertTrue(bar.is_complete)
        self.assertEqual(bar.voices[0].end, F(3, 4))

    def test_polyphony_can_overlap_across_voices(self):
        bar = Measure()
        bar.add_chord((Pitch('C', 4), Pitch('E', 4)), 1)
        index = bar.add_voice()
        bar.add_note(Pitch('G', 5), F(1, 2), voice_index=index)
        bar.add_rest(F(1, 2), voice_index=index)
        self.assertTrue(bar.is_complete)
        self.assertEqual(len(bar.voices), 2)

    def test_missing_rest_in_second_voice_marks_bar_incomplete(self):
        bar = Measure()
        bar.add_rest(1)
        secondary = bar.add_voice()
        bar.add_note(Pitch('C', 5), F(1, 4), voice_index=secondary)
        self.assertFalse(bar.is_complete)

    def test_pickup_measure(self):
        pickup = Measure(time_signature=TimeSignature(4, 4), actual_duration=F(1, 4))
        pickup.add_note(Pitch('G', 4), F(1, 4))
        self.assertTrue(pickup.is_complete)
        with self.assertRaises(ValueError):
            Measure(actual_duration=F(5, 4))

    def test_voice_index_must_exist(self):
        bar = Measure()
        with self.assertRaises(IndexError):
            bar.add_note(Pitch('C', 4), F(1, 4), voice_index=1)
        with self.assertRaises(ValueError):
            bar.add_event(Rest(0, 1), voice_index=-1)


class DocumentTests(unittest.TestCase):
    """Exercise score hierarchy, new piano project and validation issues."""

    def test_blank_score_has_real_piano_hierarchy(self):
        score = create_blank_piano_score('Test piece')
        self.assertEqual(score.title, 'Test piece')
        self.assertEqual(score.parts[0].name, 'Piano')
        self.assertEqual(score.parts[0].staves[0].clef, Clef.TREBLE)
        self.assertEqual(score.parts[0].staves[0].measures[0].number, 1)
        self.assertEqual(score.parts[0].staves[0].measures[0].duration, 1)

    def test_each_blank_score_is_independent(self):
        a = create_blank_piano_score()
        b = create_blank_piano_score()
        a.parts[0].staves[0].measures[0].add_rest(1)
        self.assertFalse(b.parts[0].staves[0].measures[0].voices[0].events)

    def test_staff_sequential_measure_ids(self):
        staff = Staff()
        staff.new_measure(TimeSignature(3, 4))
        next_bar = staff.new_measure()
        self.assertEqual(next_bar.number, 2)
        self.assertEqual(next_bar.time_signature, TimeSignature(3, 4))
        with self.assertRaises(ValueError):
            staff.add_measure(Measure(number=4))

    def test_score_validation_reports_gaps(self):
        score = create_blank_piano_score()
        issues = score.validate()
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].code, 'UNFILLED_VOICE')
        score.parts[0].staves[0].measures[0].add_rest(1)
        self.assertEqual(score.validate(), [])

    def test_empty_structure_validation(self):
        self.assertEqual(Score().validate()[0].code, 'NO_PARTS')
        score = Score(parts=[Part('Violin')])
        self.assertEqual(score.validate()[0].code, 'NO_STAVES')

    def test_invalid_part_or_staff(self):
        with self.assertRaises(ValueError):
            Part('   ')
        with self.assertRaises(TypeError):
            Staff(clef='treble')


if __name__ == '__main__':
    unittest.main()
