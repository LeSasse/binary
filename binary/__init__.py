import numpy as np


def _str_to_bools(n: str):
    return [bool(int(x)) for x in n]


def _bools_to_str(n: list):
    return "".join([str(int(x)) for x in _check_all_bool(n)])


def _check_all_bool(n: list):
    for x in n:
        assert isinstance(x, bool), (
            "Binary arrays must only consist of"
            " boolean type"
        )
    return n


def _check_binary_str(n: str):
    for x in n:
        assert x in ["0", "1"], "string not binary representation"
    return n


def _xor(a: bool, b: bool):
    """ xor logical operator """

    assert isinstance(a, bool), "input to _xor must be boolean"
    assert isinstance(b, bool), "input to _xor must be boolean"
    return (a or b) and not (a and b)


def _add_binary(A: list, B: list, carry_in=False):
    A_rev = A[::-1]
    B_rev = B[::-1]
    result = []
    for a, b in zip(A_rev, B_rev):
        _sum, carry_in = _full_adder(carry_in, a, b)
        result.append(_sum)

    if carry_in:
        result.append(carry_in)

    return result[::-1]


def _half_adder(a, b):
    _check_all_bool([a, b])
    return _xor(a, b), a and b


def _full_adder(carry_in, a, b):
    _check_all_bool([a, b])

    sum_out_halfadder_1, carry_out_halfadder_1 = _half_adder(a, b)
    sum_out_halfadder_2, carry_out_halfadder_2 = _half_adder(
        carry_in, sum_out_halfadder_1
    )
    return (
        sum_out_halfadder_2,
        carry_out_halfadder_2 or carry_out_halfadder_1
    )


def _invert(A: list):
    return [not a for a in A]


def _subtract_binary(A: list, B: list):
    B = _get_twos_complement(B)
    return _add_binary(A, B, carry_in=True)


def _get_twos_complement(A: list):
    A = _invert(A)
    add_one_ = [False for x in range(len(A) - 1)] + [True]
    return _add_binary(A, add_one_)


class BinarySequence:
    """ Binary sequence with a boolean and a string representation


    """

    def __init__(
        self,
        sequence,
        n_bits: int = 8,
        signed: bool = False,
        verbosity: int = 0
    ):
        """ Initialise a binary sequence.

        Parameters
        -----------
        sequence : int or str or list
            if int, needs to be an integer that can be represented with
            n_bits. if list, should consist of boolean types.
            if str, str should only contain "0" or "1".

            TODO: take that from the user and
            determine n_bits yourself
        n_bits : int
            number of bits to represent sequence
        signed : bool
            whether to represent negative numbers as well
        verbosity : int
            level of print out

        Returns
        --------
        self: BinarySequence

        """
        self.signed = signed
        self.n_bits = n_bits
        self.verbosity = verbosity

        if isinstance(sequence, int):
            self.neg = sequence < 0 if self.signed else False
            self._decimal = sequence
            sequence = _check_all_bool(self._convert_to_binary(sequence))
            self._booleans = sequence
            self._str = _bools_to_str(sequence)
        elif isinstance(sequence, str):
            self.neg = bool(int(sequence[0])) if self.signed else False
            assert len(sequence) == n_bits, (
                "len(sequence should be equal to n_bits"
            )
            sequence = _check_binary_str(sequence)
            self._booleans = _str_to_bools(sequence)
            self._str = sequence
            self._decimal = self._convert_to_decimal(self._booleans)
        elif isinstance(sequence, list):
            self.neg = sequence[0] if self.signed else False
            # assert len(sequence) == n_bits, (
            #    "len(sequence should be equal to n_bits"
            # )
            sequence = _check_all_bool(sequence)
            self._booleans = sequence
            self._str = _bools_to_str(sequence)
            self._decimal = self._convert_to_decimal(self._booleans)

        self.min_dec, self.max_dec = self._can_represent()

        assert (
            self.min_dec <= self._decimal
        ) and (self._decimal <= self.max_dec), (
            f"I can't represent {self._decimal} with {self.n_bits} bits."
            f"I can only represent numbers between {self.min_dec} and "
            f"{self.max_dec}."
        )

    def _can_represent(self):
        """ Returns range of numbers the binary operator can represent
        in decimal

        """

        unsigned_max = self._convert_to_decimal(
            [True for x in range(self.n_bits)]
        )
        signed_max = self._convert_to_decimal(
            [False] + [True for x in range(self.n_bits - 1)]
        )
        signed_min = self._convert_to_decimal(
            [True] + [False for x in range(self.n_bits - 1)]
        )

        if self.signed:
            return signed_min, signed_max
        else:
            return 0, unsigned_max

    def _convert_to_binary(self, n: int, n_bits=None):
        """ convert decimal integers into binary representation

        Parameters
        ----------
        n : int
            decimal number to convert

        Returns
        --------
        binary : list of boolean values

        """

        if n_bits is None:
            n_bits = self.n_bits

        neg = False
        if self.signed:
            neg = n < 0
            sign = -1 if neg else 1
            n = n * sign

        positionals = [2 ** x for x in range(n_bits)][::-1]
        bin_n = []
        for i in positionals:
            bin_n.append(not n < i)
            n = n % i

        if neg:
            bin_n = _get_twos_complement(bin_n)

        return _check_all_bool(bin_n)

    def _convert_to_decimal(self, n: list):
        """ convert binary representation into decimal integer

        Parameters
        -----------
        n : list of booleans

        Returns
        --------
        dec : int

        """
        n = _check_all_bool(n)
        if self.signed:
            sign = -1 if n[0] else 1
        else:
            sign = 1

        if self.signed and n[0]:
            x = _get_twos_complement(n)
            return sum([(2**x) * int(y) for x, y in enumerate(x[::-1])]) * sign
        else:
            return sum([(2**x) * int(y) for x, y in enumerate(n[::-1])]) * sign

    def __str__(self):
        return self._str

    def __iter__(self):
        return iter(self._booleans)

    def __repr__(self):
        return (
            f"BinarySequence(sequence={self._str}, n_bits={self.n_bits}, "
            f"signed={self.signed}, verbosity={self.verbosity})"
        )

    def __add__(self, other_sequence):

        assert self.signed == other_sequence.signed
        assert self.n_bits == other_sequence.n_bits
        res = _add_binary(self._booleans, other_sequence._booleans)
        if self.signed and (len(res) > len(self._booleans)):
            res = res[-self.n_bits:]
            """
            if self._booleans[0] == other_sequence._booleans[0]:
                assert self._booleans[0] == res[0], (
                    f"was {self._decimal} + {other_sequence._decimal}"
                )
            """
        assert not (len(res) > len(self._booleans)), (
            f"This sum cannot be represented using {self.n_bits} bits!"
            f"(Sum was {self._decimal} + {other_sequence._decimal})"
        )

        BS_res = BinarySequence(
            res,
            signed=self.signed,
            n_bits=len(res)
        )

        x = "signed" if self.signed else "unsigned"
        if self.verbosity > 1:

            print(f"""

For binary sequences ({x}) of {self.n_bits} bits:

            {self}
        +   {other_sequence}
            ----------------
        =   {BS_res}

        ({self._decimal} + {other_sequence._decimal} = {BS_res._decimal})
""")
        return BS_res

    def __int__(self):
        return self._decimal

#############################################################################
# tests


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
        bin_x = BinarySequence(x, n_bits=8, signed=False, verbosity=2)
        bin_y = BinarySequence(y, n_bits=8, signed=False, verbosity=2)

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
        bin_x = BinarySequence(x, signed=True, verbosity=2)
        bin_y = BinarySequence(y, signed=True, verbosity=2)

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
        bin_x = BinarySequence(x, n_bits=16, signed=False, verbosity=2)
        bin_y = BinarySequence(y, n_bits=16, signed=False, verbosity=2)
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
        bin_x = BinarySequence(x, n_bits=16, signed=True, verbosity=2)
        bin_y = BinarySequence(y, n_bits=16, signed=True, verbosity=2)

        assert (bin_x + bin_y)._decimal == x + y, (
            "Problem with addition"
        )

        assert int(bin_x) == x, "Problem with int conversion"


if __name__ == "__main__":
    test_str_sequences()
    test_bool_sequences()
    test_unsigned_addition()
    test_signed()
    test_add_signed()
    test_unsigned_16bit()
    test_signed_16bit()
