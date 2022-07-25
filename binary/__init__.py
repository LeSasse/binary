
from .utils import (
    _str_to_bools, _bools_to_str, _check_all_bool, _check_binary_str,
    _add_binary, _subtract_binary, _get_twos_complement
)


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

    def __eq__(self, other):
        
        if (self.signed != other.signed) or (self.n_bits != other.n_bits):
            return False
        
        for i, j in zip(self._booleans, other._booleans):
            if not i == j:
                return False

        return True

    def __gt__(self, other):
        assert (
            self.signed == other.signed
        ) or (self.n_bits == other.n_bits), ( 
            "Can't compare as one is signed but not the other "
            "or number of bits isn't the same"
        )
        if self.signed:
            if other._booleans[0] and not self._booleans[0]:
                return True
            if self._booleans[0] and not other._booleans[0]:
                return False

            for i, j in zip(self._booleans, other._booleans):
                if i > j:
                    return True
            return False

        for i, j in zip(self._booleans, other._booleans):
            if i > j:
                return True

    def __lt__(self, other):
        assert (
            self.signed == other.signed
        ) or (self.n_bits == other.n_bits), (
            "Can't compare as one is signed but not the other "
            "or number of bits isn't the same"
        )
        return not (self > other) and not (self == other)


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

    def __sub__(self, other_sequence):
        
        assert self.signed == other_sequence.signed
        assert self.n_bits == other_sequence.n_bits
        if not self.signed:
            assert self > other_sequence, (
                "For subtraction of unsigned numbers the minuend must be "
                "greater than the subtrahend"
            )
        
        res = _subtract_binary(self._booleans, other_sequence._booleans)
        if self.signed and (len(res) > len(self._booleans)):
            res = res[-self.n_bits:]
            """
            if self._booleans[0] == other_sequence._booleans[0]:
                assert self._booleans[0] == res[0], (
                    f"was {self._decimal} + {other_sequence._decimal}"
                )
            """
        elif len(res) > len(self._booleans):
            res = res[-self.n_bits:]
       
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
        -   {other_sequence}
            ----------------
        =   {BS_res}

        ({self._decimal} - {other_sequence._decimal} = {BS_res._decimal})
""")
        return BS_res

