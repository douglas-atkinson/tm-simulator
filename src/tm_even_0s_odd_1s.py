TM_EVEN_0s_ODD_1s = {
    # q0: find leftmost unmarked 0
    ("q_ee", "0"): ("q_oe", "0", "R"),
    ("q_ee", "1"): ("q_eo", "1", "R"),
    ("q_ee", "_"): ("q_reject", "B", "S"),

    ("q_eo", "0"): ("q_oo", "0", "R"),
    ("q_eo", "1"): ("q_ee", "1", "R"),
    ("q_eo", "_"): ("q_accept", "_", "S"),

    ("q_oe", "0"): ("q_ee", "0", "R"),
    ("q_oe", "1"): ("q_oo", "1", "R"),
    ("q_oe", "_"): ("q_reject", "_", "S"),

    ("q_oo", "0"): ("q_eo", "0", "R"),
    ("q_oo", "1"): ("q_oe", "1", "R"),
    ("q_oo", "_"): ("q_reject", "_", "S"),
}