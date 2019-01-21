import unittest
import note


class TestDifferentOctave(unittest.TestCase):
    """Test cases for the different_octave method in the Note class."""

    def test_init_note(self):
        """A simple initialization of a Note."""

        n = note.Note('B4', True)
        self.assertEqual(str(n), 'B4')

    def test_same_tone_same_name(self):
        """n2 has the same tone as n1."""

        n1 = note.Note('F4', True)
        n2 = note.Note('F4', True)
        actual = n1.different_octave(n2)
        expected = True
        self.assertEqual(actual, expected)

    def test_same_tone_different_name(self):
        """n2 has the same tone, but as an enharmonic of n1."""

        n1 = note.Note('E#6', True)
        n2 = note.Note('F4', True)
        actual = n1.different_octave(n2)
        expected = True
        self.assertEqual(actual, expected)

    def test_C(self):
        """n1 has tone C and n2 has tone != C."""

        n1 = note.Note('C3', True)
        n2 = note.Note('A3', True)
        actual = n1.different_octave(n2)
        expected = True
        self.assertEqual(actual, expected)

    def test_before_C_to_after_C(self):
        """n1 has tone before C, n2 has tone after C."""

        n1 = note.Note('A4', True)
        n2 = note.Note('G12', True)
        actual = n1.different_octave(n2)
        expected = False
        self.assertEqual(actual, expected)

    def test_after_C_to_before_C(self):
        """n1 has tone after C, n2 has tone before C."""

        n1 = note.Note('F4', True)
        n2 = note.Note('Bb3', True)
        actual = n1.different_octave(n2)
        expected = True
        self.assertEqual(actual, expected)

    def test_both_after_n1_before_n2(self):
        """Both notes come after C, n1 comes before n2."""

        n1 = note.Note('F#5', True)
        n2 = note.Note('G3', True)
        actual = n1.different_octave(n2)
        expected = True
        self.assertEqual(actual, expected)

    def test_both_after_n1_after_n2(self):
        """Both notes come after C, n1 comes after n2."""

        n1 = note.Note('G8', True)
        n2 = note.Note('Fb5', True)
        actual = n1.different_octave(n2)
        expected = False
        self.assertEqual(actual, expected)

    def test_both_before_n1_before_n2(self):
        """Both notes come before C, n1 comes before n2."""

        n1 = note.Note('A#6', True)
        n2 = note.Note('B4', True)
        actual = n1.different_octave(n2)
        expected = True
        self.assertEqual(actual, expected)

    def test_both_before_n1_after_n2(self):
        """Both notes come before C, n1 comes after n2."""

        n1 = note.Note('Cb210', True)
        n2 = note.Note('A4', True)
        actual = n1.different_octave(n2)
        expected = False
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
