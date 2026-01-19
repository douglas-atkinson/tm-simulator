from tm_0n1n import TM_0N1N
from tm_replace_0s_with_Xs import TM_REPLACE_0s_WITH_XS
from tm_replace_0s_with_Xs_after_0 import TM_REPLACE_0s_WITH_XS_AFTER_0
from tm_even_0s_odd_1s import TM_EVEN_0s_ODD_1s
from tm_palindrome_checker import TM_PALINDROME_CHECKER
from tm_binary_addition import TM_BINARY_ADDITION

MACHINES = {
    "Replace0sWithXs": {
        "transitions": TM_REPLACE_0s_WITH_XS,
        "input_alphabet": {"0", "1"},
        "tape_alphabet": {"0", "1", "X", "_"},
        "start": "q0",
        "accept": "q_accept",
        "reject": "q_reject",
    },
    "Replace0sWithXsAfter0": {
        "transitions": TM_REPLACE_0s_WITH_XS_AFTER_0,
        "input_alphabet": {"0", "1"},
        "tape_alphabet": {"0", "1", "X", "_"},
        "start": "q_start",
        "accept": "q_halt",
        "reject": "q_reject",
    },
    "0n1n": {
        "transitions": TM_0N1N,
        "input_alphabet": {"0", "1"},
        "tape_alphabet": {"0", "1", "X", "Y", "_"},
        "start": "q0",
        "accept": "q_accept",
        "reject": "q_reject",
    },
    "Even0sOdd1s": {
        "transitions": TM_EVEN_0s_ODD_1s,
        "input_alphabet": {"0", "1"},
        "tape_alphabet": {"0", "1", "_"},
        "start": "q_ee",
        "accept": "q_accept",
        "reject": "q_reject",
    },
    "PalindromeChecker": {
        "transitions": TM_PALINDROME_CHECKER,
        "input_alphabet": {"0", "1"},
        "tape_alphabet": {"0", "1", "_"},
        "start": "q0",
        "accept": "q_accept",
        "reject": "q_reject",
    },
    "BinaryAddition": {
        "transitions": TM_BINARY_ADDITION,
        "input_alphabet": {"0", "1", "+"},
        "tape_alphabet": {"0", "1", "+", "_"},
        "start": "q_0",
        "accept": "q_halt",
        "reject": "q_reject",
    },

}