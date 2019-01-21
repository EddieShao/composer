from __future__ import annotations
from typing import Optional

import data


class Note:
    """A musical note."""

    # Override basic methods
    def __init__(self, name: str, convert: bool) -> None:

        """Initialize a Note with tone and octave according to name.
        convert determines if self should be considered for converting
        into its enharmonic. octave will be set to 0 if no valid octave given.

        Precondition: convert == True iff initializing a root note.

        == Attributes ==
        tone: The tone of this note.
        octave: The octave this note is in.

        >>> note = Note('C#6', True)
        >>> note.tone
        'C#'
        >>> note.octave
        6
        """

        # Attribute types
        tone: str
        octave: int

        data_set = data.Data()
        split_index = self.find_num_index(name)

        # If octave is valid, set it. Otherwise, set it to 0.
        try:
            self.octave = int(name[split_index:])
        except ValueError:
            self.octave = -1

        tone = name[:split_index]

        # If the tone is NOT in the circle of 5ths,
        # convert it to its respective enharmonic in the circle of 5ths.
        if convert and tone in data_set.note_to_enharmonic:
            self.tone = data_set.note_to_enharmonic[tone]
        else:
            self.tone = tone

    def __str__(self) -> str:
        """Return a string representation of this Note.

        >>> note = Note('G3', True)
        >>> str(note)
        'G3'
        """

        return self.tone + str(self.octave)

    def __eq__(self, other: Note) -> bool:
        """Return True iff other has the same tone and octave as self.

        >>> n1 = Note('C4', True)
        >>> n2 = Note('C3', True)
        >>> n1 == n2
        False
        >>> n2 = Note('C4', True)
        >>> n1 == n2
        True
        """

        return self.tone == other.tone and self.octave == other.octave

    # Functional methods
    def reset_note(self) -> None:
        """Reset self to a neutral state.

        A neutral note should have a tone of N/A and an octave of -1.

        >>> n = Note('G3', True)
        >>> n.reset_note()
        >>> str(n)
        'N/A-1'
        """

        self.tone = 'N/A'
        self.octave = -1

    @staticmethod
    # Used in initialization of a Note.
    def find_num_index(name: str) -> int:
        """Return the index of the first numerical value in name. If none are
        found, return -1.

        >>> note = Note('Bb4', True)
        >>> note.find_num_index('Bb4')
        2
        """

        for i in range(len(name)):
            # If this character is a num or is a negative sign before a num...
            if name[i].isnumeric() or (name[i - 1] == '-' and
                                       name[i].isnumeric()):
                return i

        return -1

    def different_octave(self, other: Note) -> bool:
        """Assuming that self comes after other in a chord, return True iff
        self appears in the next octave after other.

        This method should ignore preset octaves and ONLY compare tones.

        >>> n1 = Note('G4', True)
        >>> n2 = Note('A4', True)
        >>> n1.different_octave(n2)
        True
        >>> n2.octave = 2
        >>> n1.different_octave(n2)
        True
        >>> n2 = Note('D5', True)
        >>> n1.different_octave(n2)
        False
        >>> n1 = Note('A3', True)
        >>> n1.different_octave(n2)
        False
        """

        # Collect the tonal values of self and other.
        self_value = self.get_tone_value()
        other_value = other.get_tone_value()

        return self_value <= other_value

    def get_tone_value(self) -> Optional[int]:
        """Return the numerical value of self's tone using tones_to_value.
        Return -1 if tone DNE in tones_to_value.

        >>> n = Note('B5', True)
        >>> n.get_tone_value()
        11
        >>> n.tone = 'Abb'
        >>> n.get_tone_value()
        7
        >>> n.tone = 'hello'
        >>> n.get_tone_value()
        -1
        """

        # A list of tones to their respective comparison value.
        # # Enharmonic notes have identical values.
        tones_to_value = {('C', 'Dbb', 'B#'): 0, ('Bx', 'C#', 'Db'): 1,
                          ('Cx', 'D', 'Ebb'): 2, ('D#', 'Eb', 'Fbb'): 3,
                          ('Dx', 'E', 'Fb'): 4,
                          ('E#', 'F', 'Gbb'): 5, ('Ex', 'F#', 'Gb'): 6,
                          ('Fx', 'G', 'Abb'): 7, ('G#', 'Ab'): 8,
                          ('Gx', 'A', 'Bbb'): 9, ('A#', 'Bb', 'Cbb'): 10,
                          ('Ax', 'B', 'Cb'): 11}

        for tone_list in tones_to_value:
            if self.tone in tone_list:
                return tones_to_value[tone_list]

        # self's tone is not a musical tone.
        return -1


if __name__ == '__main__':
    import doctest
    doctest.testmod()
