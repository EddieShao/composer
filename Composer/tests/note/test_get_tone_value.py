import note
from hypothesis import given
from hypothesis.strategies import integers


def simple_note_setup() -> note.Note:
    """Initialize a simple Note."""
    return note.Note('G#3', True)


def test_regular_tone() -> None:
    """The tone is a regular harmonic."""
    n = simple_note_setup()
    assert n.get_tone_value() == 8


def test_special_tone() -> None:
    """The tone is a double sharp or double flat."""
    n = note.Note('Ax5', False)
    assert n.get_tone_value() == 11


@given(octave=integers())
def test_null_octave(octave: int) -> None:
    """Test if the octave of the Note has no effect on get_tone_value."""
    n = note.Note('C' + str(octave), False)
    assert n.get_tone_value() == 0


if __name__ == '__main__':
    import pytest
    pytest.main(['test_get_tone_value.py'])  # Name of Python test file here.
