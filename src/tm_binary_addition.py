TM_BINARY_ADDITION = {
    # q0: find leftmost unmarked 0
    ("q_0", "0"): ("q_0", "0", "R"),
    ("q_0", "1"): ("q_0", "1", "R"),
    ("q_0", "+"): ("q_dec", "+", "L"),
    ("q_0", "_"): ("q_halt", "_", "S"),

    ("q_dec", "1"): ("q_findEnd", "0", "R"),
    ("q_dec", "0"): ("q_dec", "1", "L"),
    ("q_dec", "_"): ("q_clean", "_", "R"),

    ("q_findEnd", "0"): ("q_findEnd", "0", "R"),
    ("q_findEnd", "1"): ("q_findEnd", "1", "R"),
    ("q_findEnd", "+"): ("q_findEnd", "+", "R"),
    ("q_findEnd", "_"): ("q_inc", "_", "L"),

    ("q_inc", "0"): ("q_return", "1", "L"),
    ("q_inc", "1"): ("q_inc", "0", "L"),
    ("q_inc", "+"): ("q_return", "1", "L"),

    ("q_return", "0"): ("q_return", "0", "L"),
    ("q_return", "1"): ("q_return", "1", "L"),
    ("q_return", "+"): ("q_return", "+", "L"),
    ("q_return", "_"): ("q_0", "_", "R"),

    ("q_clean", "0"): ("q_clean", "_", "R"),
    ("q_clean", "1"): ("q_clean", "_", "R"),
    ("q_clean", "+"): ("q_halt", "_", "R"),
}