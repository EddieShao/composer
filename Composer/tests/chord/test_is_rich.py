import unittest
import note
import chord


class TestIsRich(unittest.TestCase):
    """Test cases for the method is_rich in the Chord class."""

    def test_neutral(self):
        """The Chord is neutral."""

        n = note.Note('C#4', True)
        c = chord.Chord(n)

        actual = c.is_rich()
        expected = False
        self.assertEqual(actual, expected)

    def test_one_note(self):
        """The Chord has one note."""

        n = note.Note('Fx4', True)
        c = chord.Chord(n)
        c.build_chord('major', 1)

        actual = c.is_rich()
        expected = False
        self.assertEqual(actual, expected)

    def test_octave_no_fill(self):
        """The Chord contains a whole octave, but less than 2 notes in between."""

        n = note.Note('Gb1', True)
        c = chord.Chord(n)
        c.build_chord('major', 12)
        c.remove_notes('major 3')

        actual = c.is_rich()
        expected = False
        self.assertEqual(actual, expected)

    def test_fill_no_octave(self):
        """The Chord contains more than 1 non-root note, but only 1 root octave."""

        n = note.Note('Bb3', True)
        c = chord.Chord(n)
        c.build_chord('augmented', 3)

        actual = c.is_rich()
        expected = False
        self.assertEqual(actual, expected)

    def test_rich(self):
        """The Chord contains multiple octaves with 2 or more notes in between."""

        n = note.Note('A#4', True)
        c = chord.Chord(n)
        c.build_chord('major suspended 24', 6)

        actual = c.is_rich()
        expected = True
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
