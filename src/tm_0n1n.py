TM_0N1N = {
    # q0: find leftmost unmarked 0
    ("q0", "X"): ("q0", "X", "R"),
    ("q0", "0"): ("q1", "X", "R"),
    ("q0", "Y"): ("q3", "Y", "R"),
    ("q0", "1"): ("q_reject", "1", "S"),
    ("q0", "_"): ("q_accept", "_", "S"),

    # q1: find matching unmarked 1 (no 0 allowed!)
    ("q1", "X"): ("q1", "X", "R"),
    ("q1", "Y"): ("q1", "Y", "R"),
    ("q1", "1"): ("q2", "Y", "L"),
    ("q1", "0"): ("q1", "0", "R"),
    ("q1", "_"): ("q_reject", "_", "S"),

    # q2: return to left end
    ("q2", "X"): ("q2", "X", "L"),
    ("q2", "Y"): ("q2", "Y", "L"),
    ("q2", "0"): ("q2", "0", "L"),
    ("q2", "1"): ("q2", "1", "L"),
    ("q2", "_"): ("q0", "_", "R"),

    # q3: final verification — only Ys allowed
    ("q3", "Y"): ("q3", "Y", "R"),
    ("q3", "_"): ("q_accept", "_", "S"),
    ("q3", "1"): ("q_reject", "1", "S"),
    ("q3", "0"): ("q_reject", "0", "S"),
    ("q3", "X"): ("q_reject", "X", "S"),
}
