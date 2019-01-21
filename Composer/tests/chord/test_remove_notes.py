import unittest
import note
import chord


class TestRemoveNotes(unittest.TestCase):
    def test_neutral(self):
        """The Chord is neutral."""

        n = note.Note('F#4', True)
        c = chord.Chord(n)
        c.remove_notes('major 7')

        self.assertEqual(c.notes, [])

    def test_1_note_remove(self):
        """The Chord has 1 note that is removed."""

        n = note.Note('Bb2', True)
        c = chord.Chord(n)
        c.build_chord('minor', 1)
        c.remove_notes('perfect 1')

        self.assertEqual(c.notes, [])

    def test_1_note_keep(self):
        """The Chord has 1 note that is NOT removed."""

        n = note.Note('A#4', True)
        c = chord.Chord(n)
        c.build_chord('major', 1)
        c.remove_notes('perfect 5')

        self.assertEqual(c.notes, [n])


if __name__ == '__main__':
    unittest.main()
