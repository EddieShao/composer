import unittest
import note
import chord


class TestIsCrunchy(unittest.TestCase):
    """Test cases for the is_crunchy method in the Chord class."""

    def test_neutral(self):
        """The Chord is neutral."""

        n = note.Note('G#4', True)
        c = chord.Chord(n)

        actual = c.is_crunchy()
        expected = False
        self.assertEqual(actual, expected)

    def test_one_note(self):
        """The Chord contains one note."""

        n = note.Note('Ab3', True)
        c = chord.Chord(n)
        c.build_chord('major suspended 2', 1)

        actual = c.is_crunchy()
        expected = False
        self.assertEqual(actual, expected)

    def test_2_notes_crunch(self):
        """The Chord contains 2 notes that are dissonant."""

        n = note.Note('G3', True)
        c = chord.Chord(n)
        c.build_chord('major suspended 2', 2)

        actual = c.is_crunchy()
        expected = True
        self.assertEqual(actual, expected)

    def test_2_notes_no_crunch(self):
        """The Chord contains 2 notes that are NOT dissonant."""

        n = note.Note('Fx4', True)
        c = chord.Chord(n)
        c.build_chord('augmented', 2)

        actual = c.is_crunchy()
        expected = False
        self.assertEqual(actual, expected)

    def test_many_notes_crunch(self):
        """The Chord contains more than 1 note and at least 2 are dissonant with each other."""

        n = note.Note('C3', True)
        c = chord.Chord(n)
        c.build_chord('major suspended 4')

        actual = c.is_crunchy()
        expected = True
        self.assertEqual(actual, expected)

    def test_many_notes_no_crunch(self):
        """The Chord contains more than 1 note and none are dissonant with each other."""

        n = note.Note('Gb3', True)
        c = chord.Chord(n)
        c.build_chord('minor', 7)

        actual = c.is_crunchy()
        expected = False
        self.assertEqual(actual, expected)

    def test_end_crunch_1(self):
        """The Chord contains a dissonance between the 11th tone and 1st or 2nd tone in the key."""

        n = note.Note('Ab3', True)
        c = chord.Chord(n)
        c.build_chord('major', 5)
        c.add_notes('major 7')

        actual = c.is_crunchy()
        expected = True
        self.assertEqual(actual, expected)

    def test_end_crunch_2(self):
        """The Chord contains a dissonance between the 10th tone and 1st or 2nd tone in the key."""

        n = note.Note('C280', True)
        c = chord.Chord(n)
        c.build_chord('major', 5)
        c.add_notes('minor 7')

        actual = c.is_crunchy()
        expected = True
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
