
def _str_to_bools(n: str):
    return [bool(int(x)) for x in _check_binary_str(n)]


def _bools_to_str(n: list):
    return "".join([str(int(x)) for x in _check_all_bool(n)])


def _check_all_bool(n: list):
    for x in n:
        assert isinstance(x, bool), (
            "Binary arrays must only consist of"
            " boolean type!"
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
    """ adds two binary numbers represented by a list of boolean values

    """

    A_rev = _check_all_bool(A[::-1])
    B_rev = _check_all_bool(B[::-1])
    result = []
    for a, b in zip(A_rev, B_rev):
        _sum, carry_in = _full_adder(carry_in, a, b)
        result.append(_sum)

    if carry_in:
        result.append(carry_in)

    return result[::-1]


def _half_adder(a, b):
    """ sums bits a and b without a carry in, returns sum and carry out

    """

    _check_all_bool([a, b])
    return _xor(a, b), a and b


def _full_adder(carry_in, a, b):
    """ sums a and b and a carry in, returns sum and a carry out

    """
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
    """ subtraction is the same as addition if you get twos complement for
    the subtrahend. This is equivalent to inverting, then adding one.

    """
    B = _get_twos_complement(B)
    return _add_binary(A, B, carry_in=False)


def _get_twos_complement(A: list):
    """ invert bits and add one to get two's complement """
    A = _invert(A)
    add_one_ = [False for x in range(len(A) - 1)] + [True]
    return _add_binary(A, add_one_)
