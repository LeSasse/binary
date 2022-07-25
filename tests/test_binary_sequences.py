
import numpy as np

from binary import BinarySequence

str_binaries_unsigned = {
    "10100010": (162, [True, False, True, False, False, False, True, False]),
    "01011101": (93, [False, True, False, True, True, True, False, True]),
    "11111111": (255, [True for x in range(8)]),
    "00000000": (0, [False for x in range(8)]),
    "01110101": (117, [False, True, True, True, False, True, False, True]),
    "01001000": (72, [False, True, False, False, True, False, False, False]),
}


str_binaries_signed = {
    "10000000": (-128, [True] + [False for x in range(7)]),
    "10000001": (-127, [True] + [False for x in range(6)] + [True]),
    "10000010": (-126, [
        True, False, False, False, False, False, True, False
    ]),
    "00000000": (0, [False for x in range(8)]),
    "01111110": (126, [False] + [True for x in range(6)] + [False]),
    "01111101": (125, [False] + [True for x in range(5)] + [False, True]),
}


def test_str_sequences():

    for str_seq, (int_repr, bools) in str_binaries_unsigned.items():

        a = BinarySequence(sequence=str_seq)
        assert a._decimal == int_repr, (
            f"Decimal representation incorrect for {str_seq}"
        )
        for i, j in zip(a._booleans, bools):
            assert i == j, (
                f"boolean representation incorrect for {str_seq}"
            )


def test_bool_sequences():

    for str_seq, (int_repr, bools) in str_binaries_unsigned.items():

        a = BinarySequence(sequence=bools)
        assert a._decimal == int_repr, (
            f"Decimal representation incorrect for {str_seq}"
        )
        assert str_seq == a._str, (
            f"String representation incorrect for {str_seq}"
        )


def test_dec_sequences():

    for str_seq, (int_repr, bools) in str_binaries_unsigned.items():
        a = BinarySequence(sequence=int_repr)
        assert a._decimal == int_repr, (
            f"Decimal representation incorrect for {str_seq}"
        )
        assert str_seq == a._str, (
            f"String representation incorrect for {str_seq}"
        )
        for i, j in zip(a._booleans, bools):
            assert i == j, (
                f"boolean representation incorrect for {str_seq}"
            )


def test_unsigned_addition():

    a = np.random.randint(low=0, high=100, size=100)
    b = np.random.randint(low=0, high=100, size=100)
    for x, y in zip(a, b):
        x = int(x)
        y = int(y)
        bin_x = BinarySequence(x, n_bits=8, signed=False)
        bin_y = BinarySequence(y, n_bits=8, signed=False)

        assert (bin_x + bin_y)._decimal == x + y, (
            "Problem with addition"
        )
        assert int(bin_x) == x, "Problem with int conversion"


def test_signed():

    for str_seq, (int_repr, bools) in str_binaries_signed.items():
        a = BinarySequence(sequence=int_repr, signed=True)
        assert a._decimal == int_repr, (
            f"Decimal representation incorrect for {str_seq}"
        )
        assert str_seq == a._str, (
            f"String representation incorrect for {str_seq}"
        )
        for i, j in zip(a._booleans, bools):
            assert i == j, (
                f"boolean representation incorrect for {str_seq}"
            )


def test_add_signed():

    a = np.random.randint(low=-30, high=30, size=100)
    b = np.random.randint(low=-30, high=30, size=100)
    for x, y in zip(a, b):
        x = int(x)
        y = int(y)
        bin_x = BinarySequence(x, signed=True)
        bin_y = BinarySequence(y, signed=True)

        assert (bin_x + bin_y)._decimal == x + y, (
            f"Problem with addition {x} + {y} = {x+y}\n"
            f"{bin_x._decimal}\n"
            f"{bin_y._decimal}\n"
            f"  {bin_x}\n"
            f"+ {bin_y}\n"
            f"= {bin_x + bin_y}\n"
            f"{(bin_x + bin_y)._decimal}"
        )

        assert int(bin_x) == x, "Problem with int conversion"


def test_unsigned_16bit():

    a = np.random.randint(low=0, high=4000, size=100)
    b = np.random.randint(low=0, high=4000, size=100)
    for x, y in zip(a, b):
        x = int(x)
        y = int(y)
        bin_x = BinarySequence(x, n_bits=16, signed=False)
        bin_y = BinarySequence(y, n_bits=16, signed=False)
        assert (bin_x + bin_y)._decimal == x + y, (
            "Problem with addition"
        )

        assert int(bin_x) == x, "Problem with int conversion"


def test_signed_16bit():

    a = np.random.randint(low=-2769, high=2768, size=100)
    b = np.random.randint(low=-2769, high=2768, size=100)
    for x, y in zip(a, b):
        x = int(x)
        y = int(y)
        bin_x = BinarySequence(x, n_bits=16, signed=True)
        bin_y = BinarySequence(y, n_bits=16, signed=True)

        assert (bin_x + bin_y)._decimal == x + y, (
            "Problem with addition"
        )

        assert int(bin_x) == x, "Problem with int conversion"


def test_unsigned_subtraction():

    a = np.random.randint(low=100, high=200, size=100)
    b = np.random.randint(low=0, high=50, size=100)
    for x, y in zip(a, b):
        x = int(x)
        y = int(y)
        bin_x = BinarySequence(x, n_bits=8, signed=False, verbosity=2)
        bin_y = BinarySequence(y, n_bits=8, signed=False, verbosity=2)

        assert (bin_x - bin_y)._decimal == x - y, (
            "Problem with subtraction"
        )
        assert int(bin_x) == x, "Problem with int conversion"


if __name__ == "__main__":
    test_unsigned_subtraction()
