from __future__ import annotations
from typing import List, Dict
import data
import note

# A Dictionary of intervals to their key values and short names.
# # This Dictionary should reflect the 'Chord modifying methods' in the class.
INTERVALS = {'perfect 1': (0, 'P1'), 'minor 2': (1, 'm2'), 'major 2': (2, 'M2'),
             'minor 3': (3, 'm3'), 'major 3': (4, 'M3'), 'perfect 4': (5, 'P4'),
             'augmented 4': (6, 'A4'), 'perfect 5': (7, 'P5'),
             'minor 6': (8, 'm6'), 'major 6': (9, 'M6'), 'minor 7': (10, 'm7'),
             'major 7': (11, 'M7')}
# The indices of the items in the Tuples of INTERVALS values.
VALUE_INDEX = 0
ABBREVIATION_INDEX = 1


class Chord:
    """A musical chord"""

    # Override basic methods
    def __init__(self, root_note: note.Note) -> None:
        """Initialize a musical Chord.

        Precondition: root_note must have parameter is_root == True.

        == Attributes ==
        root_note: The root note of this chord.
        size: The number of notes in this chord.
        mode: The mode of this chord (__init__ -> 'N/A').
        notes: A list of notes in this chord (__init__ -> []).
        key: The key this chord is in.

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> str(c.root_note)
        'C3'
        >>> c.size
        0
        >>> c.mode
        'N/A'
        >>> c.notes
        []
        >>> c.key
        ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
        """

        # Attribute types
        root_note: note.Note
        size: str
        mode: str
        notes: List[note.Note]
        key: List[str]

        self.root_note = root_note
        self.size = 0
        self.notes = []
        self.mode = 'N/A'

        data_set = data.Data()
        self.key = data_set.key_to_notes[root_note.tone]

    def __str__(self) -> str:
        """Return a string representation of self.

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 4)
        >>> str(c)
        'C major: C3, E3, G3, C4'
        """

        name_list = ''
        for note in self.notes:
            name_list += str(note) + ', '

        # Slicing used to ignore trailing ', ' string.
        return '{0} {1}: {2}'.format(self.root_note.tone, self.mode,
                                     name_list[:-2])

    def __eq__(self, other: Chord) -> bool:
        """Return True iff the string representations of self and other match.

        >>> n = note.Note('C4', True)
        >>> c1 = Chord(n)
        >>> c2 = Chord(n)
        >>> c1.build_chord('minor')
        >>> c2 == c1
        False
        >>> c2.build_chord('minor')
        >>> c2 == c1
        True
        """

        return str(self) == str(other)

    # Functional Chord methods
    def is_neutral(self) -> bool:
        """Return true iff self is a 'neutral' Chord.

        A neutral chord is a chord with mode 'N/A' and no notes.

        >>> n = note.Note('G3', True)
        >>> c = Chord(n)
        >>> c.is_neutral()
        True
        >>> c.build_chord('major', 6)
        >>> c.is_neutral()
        False
        >>> c.reset_chord()
        >>> c.is_neutral()
        True
        """

        return str(self) == self.root_note.tone + ' N/A: '

    # This is for you, Mrs. Taylor.
    def is_crunchy(self) -> bool:
        """Return True iff self is a crunchy chord
        A neutral or 1 note Chord cannot be crunchy.

        A crunchy chord consists of at least 1 pair of back-to-back notes that
        are either 1 or 2 semi-tones apart.

        >>> n = note.Note('G3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 4)
        >>> c.is_crunchy()
        False
        >>> c.add_notes('minor 7')
        >>> c.is_crunchy()
        True
        """

        # A dictionary of tones in this key to their respective values.
        tone_to_value = self.get_tone_values()

        for i in range(1, len(self.notes)):
            prev_val = tone_to_value[self.notes[i - 1].tone]
            this_val = tone_to_value[self.notes[i].tone]

            if 0 < this_val - prev_val <= 2 or (this_val == 0 and
                                                prev_val in [10, 11]) or \
                    (this_val in [0, 1] and prev_val == 11):
                return True

        return False

    def is_rich(self) -> bool:
        """Return True iff self is a rich chord.

        A rich chord consists of at least 2 different root notes with at least
        2 different notes in between them.

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 4)
        >>> c.is_rich()
        True
        >>> c.remove_notes('major 3')
        >>> c.is_rich()
        False
        """

        # A counter to check number of times a root note appears in self.notes.
        root_repeats = 0
        # A counter to check the number of notes in between 2 root notes.
        fill_count = 0
        # A list of fill_count values in between every pair of root notes.
        fill_list = []

        # for every note in self.notes:
        for note in self.notes:
            # if this note is a root note:
            if note.tone == self.key[0]:
                # append fill_count to fill_list
                fill_list.append(fill_count)
                # reset fill_count
                fill_count = 0
                # increment root_repeats by 1
                root_repeats += 1
            # otherwise (if its not a root note):
            else:
                # increment fill_count by 1
                fill_count += 1

        is_full = False
        for num in fill_list:
            if num > 1:
                is_full = True
                break

        # Return True if conditions are met.
        return is_full and root_repeats > 1

    def save_chord(self, mode: str, saved_chords: List[Chord]) -> None:
        """Save self as a custom Chord with name mode to saved_chords.
        self should NOT be saved if its 'neutral' or exists in saved_chords.

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> saved = []
        >>> c.build_chord('major suspended 4')
        >>> c.save_chord('my first chord', saved)
        >>> len(saved)
        1
        >>> print(saved[0])
        C my first chord: C3, F3, G3
        >>> c.reset_chord()
        >>> c.save_chord('my second chord', saved)
        >>> len(saved)
        1
        """

        # rename self according to user input
        self.mode = mode

        # Check if this Chord already exists in self.saved_chords.
        in_saved = False
        for chord in saved_chords:
            if self == chord:
                in_saved = True
                break

        if not self.is_neutral() and not in_saved:
            saved_chords.append(self)

    def reset_chord(self) -> None:
        """Remove all notes from chord, reset its key, and reset self.mode
        to a neutral term.

        >>> n = note.Note('E5', True)
        >>> c = Chord(n)
        >>> c.build_chord('minor', 5)
        >>> str(c)
        'E minor: E5, G5, B5, E6, G6'
        >>> c.reset_chord()
        >>> str(c)
        'E N/A: '
        """

        self.mode = 'N/A'
        self.key = []
        self.notes.clear()

    # Helper methods.
    def rename_chord(self, note_type: str, adding: bool) -> None:
        """Rename the Chord to either add or remove note_type from its name.
        If adding is True, add note_type to the Chord's name. Otherwise,
        remove note_type from the Chord's name if it exists.

        >>> n = note.Note('F3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 5)
        >>> c.rename_chord('m7', True)
        >>> str(c)
        'F major add m7: F3, A3, C4, F4, A4'
        >>> c.rename_chord('M4', True)
        >>> str(c)
        'F major add m7 M4: F3, A3, C4, F4, A4'
        >>> c.rename_chord('m7', False)
        >>> str(c)
        'F major add M4: F3, A3, C4, F4, A4'
        """
        # # This method works by editing self.mode. # #

        if (not adding) and (note_type in self.mode):
            # The index of the first character of interval in self.mode.
            note_type_index = self.mode.find(note_type)
            # The index of the first character of 'add' in self.mode.
            add_index = self.mode.find('add')

            # If interval is the ONLY interval following 'add' in self.mode...
            if self.mode[add_index:note_type_index] == 'add ' and note_type_index + len(note_type) == len(self.mode):
                self.mode = self.mode[:add_index - 1]
            # If there are other existing intervals after 'add' in self.mode...
            else:
                self.mode = self.mode[:note_type_index] + self.mode[note_type_index + len(note_type) + 1:]

        # If other intervals already exist in self.mode...
        if adding and 'add' in self.mode:
            self.mode += ' ' + note_type
        # If NO other intervals exist in self.mode...
        elif adding:
            self.mode += ' add ' + note_type

    def get_insert_indices(self, add_tone: str) -> List[int]:
        """Return a list of correct indices in self.notes to insert an add_tone
        note into. A maximum of one add_tone note may exist for every iteration
        of self.key.

        Precondition: add_tone in self.key

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 7)
        >>> c.get_insert_indices('B')
        [3, 6, 7]
        """

        # A list of correct location indexes to return.
        index_list = []

        # if self is neutral, return index_list empty
        if self.is_neutral():
            return index_list

        # find the location of the first root note
        root_index = self.find_note_location(0, self.root_note.tone)

        # while the location of the root note exists (!= -1):
        while root_index != -1:
            # find the first correct insert index and append it to index_list
            index_list.append(self.correct_location(root_index, add_tone))
            # using this location as a start, find the next root note
            root_index = self.find_note_location(index_list[-1], self.root_note.tone)

        return index_list

    def find_note_location(self, start: int, tone: str) -> int:
        """Return the index of the first appearance of a note with tone tone
        in self.notes[start:]. If no location is found, return -1.

        >>> n = note.Note('F3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major')
        >>> c.find_note_location(1, 'A')
        1
        >>> c.find_note_location(2, 'A')
        -1
        """

        for i in range(start, len(self.notes)):
            if self.notes[i].tone == tone:
                return i

        return -1

    def correct_location(self, start: int, add_tone: str) -> int:
        """Return the first correct location to insert a note with tone add_tone
        in self.notes[start:]. If a note with tone add_tone already exists
        in self.notes, return -1.

        Precondition: not self.is_neutral() and  0 <= start < len(self.notes)

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 5)
        >>> c.correct_location(0, 'F')
        2
        >>> c.correct_location(3, 'F')
        5
        """

        # if add_tone not in self.key, convert it accordingly
        add_tone = self.convert_note(add_tone)
        # A dictionary of tones in self.key to their comparison values.
        tone_to_value = self.get_tone_values()

        for i in range(start + 1, len(self.notes)):
            # If this is the correct location to insert...
            if self.notes[i].tone != add_tone and (tone_to_value[self.notes[i].tone] > tone_to_value[add_tone] >
                                                   tone_to_value[self.notes[i - 1].tone] or tone_to_value[add_tone] >
                                                   tone_to_value[self.notes[i - 1].tone] >
                                                   tone_to_value[self.notes[i].tone]):
                return i

        # Otherwise, the correct place to insert is at the end of the chord.
        return len(self.notes)

    def convert_note(self, add_tone: str) -> str:
        """If tone is not in self.key, convert it to the respective enharmonic
        tone in self.key. Otherwise, return tone unchanged.

        >>> n = note.Note('G3', True)
        >>> c = Chord(n)
        >>> c.convert_note('Bbb')
        'A'
        """

        # A Tuple of Tuples containing enharmonic tones of each other.
        enharmonic_list = ('C', 'Dbb', 'B#'), ('C#', 'Db'), ('D', 'Ebb'), \
                          ('D#', 'Eb'), ('E', 'Fb'), ('E#', 'F'), \
                          ('F#', 'Gb'), ('G', 'Abb', 'Fx'), ('G#', 'Ab'), \
                          ('A', 'Bbb'), ('A#', 'Bb'), ('B', 'Cb')

        for tone_list in enharmonic_list:
            if add_tone in tone_list:

                for tone in tone_list:
                    if tone in self.key:
                        return tone

        # If Composer runs correctly, this line should never be executed.
        return add_tone

    def get_tone_values(self) -> Dict[str, int]:
        """Return a dictionary where keys are tones in self.key and values are
        integers representing each tone's value. A tone's value is depended on
        its place in self.key (notes that come later in key have a higher value.

        >>> n = note.Note('G4', True)
        >>> c = Chord(n)
        >>> c.get_tone_values()
        {'G': 0, 'Ab': 1, 'A': 2, 'Bb': 3, 'B': 4, 'C': 5, 'C#': 6, 'D': 7, 'Eb': 8, 'E': 9, 'F': 10, 'F#': 11}
        """

        tone_to_value = {}

        for i in range(len(self.key)):
            tone_to_value[self.key[i]] = i

        return tone_to_value

    # Chord writing methods (add as many as you can!)
    # Main writing method: does the actual 'writing' of the Chord.
    def build_chord(self, mode: str, size: int = 3) -> None:
        """Modify self.notes to include size notes of a mode chord in the key
        of self.root_note.tone.

        Precondition: size > 0

        >>> n = note.Note('G3', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 4)
        >>> str(c)
        'G major: G3, B3, D4, G4'
        """

        # Initialize a data_set to gain access to chord writing methods.
        data_set = data.Data()

        self.mode = mode
        self.size += size
        octave = self.root_note.octave
        # Append the first note to self.notes.
        self.notes.append(self.root_note)

        for i in range(1, size):
            # Get the tone of the next note.
            tone = eval('self.' + data_set.chord_to_method[self.mode].format(
                'i', 'self.key'))
            n = note.Note(tone + str(octave), False)

            # If next tone appears in the next octave, increment octave by 1.
            if n.different_octave(self.notes[i - 1]):
                n.octave += 1
                octave += 1

            self.notes.append(n)

    @staticmethod
    def write_major(i: int, key: List[str]) -> str:
        """Return tone of a note in a major chord depending on the value of i.

        The value of i represents which 'part' of the chord the note represents
        (third, root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_major(4, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', \
        'A', 'Bb', 'B'])
        'E'
        """

        if i % 3 == 0:
            return key[0]
        elif i % 3 == 1:
            return key[4]
        else:
            return key[7]

    @staticmethod
    def write_minor(i: int, key: List[str]) -> str:
        """Return tone of a note in a minor chord depending on the value of i.

        The value of i represents which 'part' of the chord the note is (third,
        root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_minor(4, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', \
        'A', 'Bb', 'B'])
        'Eb'
        """

        if i % 3 == 0:
            return key[0]
        elif i % 3 == 1:
            return key[3]
        else:
            return key[7]

    @staticmethod
    def write_aug(i: int, key: List[str]) -> str:
        """Return tone of a note in a augmented chord depending on value of i.

        The value of i represents which 'part' of the chord the note is
        (third, root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_aug(5, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', \
        'A', 'Bb', 'B'])
        'Ab'
        """

        if i % 3 == 0:
            return key[0]
        elif i % 3 == 1:
            return key[4]
        else:
            return key[8]

    @staticmethod
    def write_dim(i: int, key: List[str]) -> str:
        """Return tone of a note in a diminished chord depending on value of i.

        The value of i represents which 'part' of the chord the note is (third,
        root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_dim(5, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', \
        'A', 'Bb', 'B'])
        'F#'
        """

        if i % 3 == 0:
            return key[0]
        elif i % 3 == 1:
            return key[3]
        else:
            return key[6]

    @staticmethod
    def write_major_sus4(i: int, key: List[str]) -> str:
        """Return the tone of a note in a major suspend 4 chord depending on
        the value of i.

        The value of i represents which 'part' of the chord the note is (third,
        root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_major_sus4(4, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', \
        'Ab', 'A', 'Bb', 'B'])
        'F'
        """

        if i % 3 == 0:
            return key[0]
        elif i % 3 == 1:
            return key[5]
        else:
            return key[7]

    @staticmethod
    def write_major_sus2(i: int, key: List[str]) -> str:
        """Return the tone of a note in a major suspend 2 chord depending on
        the value of i.

        The value of i represents which 'part' of the chord the note is (third,
        root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_major_sus2(4, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', \
        'Ab', 'A', 'Bb', 'B'])
        'D'
        """

        if i % 3 == 0:
            return key[0]
        elif i % 3 == 1:
            return key[2]
        else:
            return key[7]

    @staticmethod
    def write_major_sus24(i: int, key: List[str]) -> str:
        """Return the tone of a note in a major suspend 2 chord depending on
        the value of i.

        The value of i represents which 'part' of the chord the note is (third,
        root, fifth, seventh, etc.).

        >>> n = note.Note('C4', True)
        >>> c = Chord(n)
        >>> c.write_major_sus24(6, ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', \
        'Ab', 'A', 'Bb', 'B'])
        'F'
        """

        if i % 4 == 0:
            return key[0]
        elif i % 4 == 1:
            return key[2]
        elif i % 4 == 2:
            return key[5]
        else:
            return key[7]

    # Chord modifying methods
    def add_notes(self, note_type: str) -> None:
        """Add a note_type note for every cycle of the chord to self.notes.

        >>> n = note.Note('G4', True)
        >>> c = Chord(n)
        >>> c.build_chord('major', 4)
        >>> c.add_notes('major 7')
        >>> c.size
        6
        >>> str(c)
        'G major add M7: G4, B4, D5, F#5, G5, F#6'
        """

        # Find the index value of note_type if it exists.
        if note_type in INTERVALS:
            add_tone = self.key[INTERVALS[note_type][VALUE_INDEX]]
        # Otherwise, prompt the user with an error message.
        else:
            print('That is not a valid selection: please try again.')
            return

        # get all correct indexes to insert an add_tone note into
        index_list = self.get_insert_indices(add_tone)
        # for every index in index_list:
        for index in index_list:
            # create a note with tone add_tone and octave of the note right before the note at index
            n = note.Note(add_tone + str(self.notes[index - 1].octave), False)
            # if this new note should be in the next octave, increment it by 1
            if n.different_octave(self.notes[index - 1]):
                n.octave += 1
            # insert it into self.notes
            self.notes.insert(index, n)

            # increment all items after index in index_list by 1 to calibrate to new length of self.notes.
            for i in range(index_list.index(index) + 1, len(index_list)):
                index_list[i] += 1

        # increment the size of self by how many notes are added
        self.size += len(index_list)
        # Rename the mode of this Chord accordingly.
        self.rename_chord(INTERVALS[note_type][ABBREVIATION_INDEX], True)

    def remove_notes(self, note_type: str) -> None:
        """Remove all note_type notes from self.notes and rename self.mode.

        >>> n = note.Note('C3', True)
        >>> c = Chord(n)
        >>> c.build_chord('minor', 5)
        >>> c.add_notes('major 7')
        >>> c.add_notes('minor 7')
        >>> str(c)
        'C minor add M7 m7: C3, Eb3, G3, Bb3, B3, C4, Eb4, Bb4, B4'
        >>> c.remove_notes('major 7')
        >>> str(c)
        'C minor add m7: C3, Eb3, G3, Bb3, C4, Eb4, Bb4'
        """

        # If the Chord is neutral, stop the method call.
        if self.is_neutral():
            return

        # get the value of note_type, then use self.key to get the tone corresponding to that value.
        tone_value = INTERVALS[note_type][VALUE_INDEX]
        tone = self.key[tone_value]

        # indexing through each note in self.notes, append every NOT note_type note to not_removed
        not_removed = []
        for i in range(len(self.notes)):
            if self.notes[i].tone != tone:
                not_removed.append(self.notes[i])

        # re-assign not_removed as self.notes to 'remove' all the targeted notes.
        self.notes = not_removed
        # re-assign correct value for self.size
        self.size = len(not_removed)
        # rename self.mode accordingly
        self.rename_chord(INTERVALS[note_type][ABBREVIATION_INDEX], False)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all()
