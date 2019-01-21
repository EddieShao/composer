import unittest
import note
import chord


class TestCorrectLocation(unittest.TestCase):
    """Test cases for the correct_location method in the Chord class."""

    def test_start_at_end(self):
        """Start searching from the last index in the Chord."""

        n = note.Note('Ab3', True)
        c = chord.Chord(n)
        c.build_chord('minor', 6)

        actual = c.correct_location(5, 'G')
        expected = 6
        self.assertEqual(actual, expected)

    def test_not_in_key(self):
        """add_tone is not in the Chord's key."""

        n = note.Note('G3', True)
        c = chord.Chord(n)
        c.build_chord('major')

        actual = c.correct_location(0, 'Bbb')
        expected = 1
        self.assertEqual(actual, expected)

    def test_already_exists(self):
        """Notes with argument tone already exist in a Chord."""

        n = note.Note('C3', True)
        c = chord.Chord(n)
        c.build_chord('major', 5)

        actual = c.correct_location(0, 'G')
        expected = 5
        self.assertEqual(actual, expected)

    def test_one_note(self):
        """self.notes contains 1 note."""

        n = note.Note('G3', True)
        c = chord.Chord(n)
        c.build_chord('minor', 1)

        actual = c.correct_location(0, 'C')
        expected = 1
        self.assertEqual(actual, expected)

    def test_2_notes_middle(self):
        """self.notes has 2 notes and a Note with tone add_tone should be added in between the 2 notes."""

        n = note.Note('B2', True)
        c = chord.Chord(n)
        c.build_chord('major', 2)

        actual = c.correct_location(0, 'C#')
        expected = 1
        self.assertEqual(actual, expected)

    def test_many_notes_middle(self):
        """self.notes has more than 2 notes and a Note with tone add_tone should be added after the first pair."""

        n = note.Note('C#3', True)
        c = chord.Chord(n)
        c.build_chord('diminished', 4)

        actual = c.correct_location(0, 'F#')
        expected = 2
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
