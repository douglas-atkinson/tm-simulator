from tape import Tape

class TuringMachine:
    def __init__(
        self,
        transitions,
        start_state,
        accept_state,
        reject_state,
        blank="_",
    ):
        """

        :param transitions: dict mapping (state, symbol) -> (next_state, write_symbol, direction)
        direction ∈ {'L', 'R', 'S'}
        :param start_state:
        :param accept_state:
        :param reject_state:
        :param blank:
        """
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank = blank

        self.reset("")

    def reset(self, input_string):
        self.state = self.start_state
        self.tape = Tape(input_string, self.blank)
        self.halted = False

    def step(self):
        if self.halted:
            return

        # If already in a halting state, halt (defensive)
        if self.state in (self.accept_state, self.reject_state):
            self.halted = True
            return

        current_symbol = self.tape.read()
        key = (self.state, current_symbol)

        if key not in self.transitions:
            self.state = self.reject_state
            self.halted = True
            return

        next_state, write_symbol, direction = self.transitions[key]

        self.tape.write(write_symbol)

        if direction == "L":
            self.tape.move_left()
        elif direction == "R":
            self.tape.move_right()
        elif direction == "S":
            pass
        else:
            raise ValueError(f"Invalid direction: {direction}")

        self.state = next_state

        # Halt immediately upon entering accept/reject
        if self.state in (self.accept_state, self.reject_state):
            self.halted = True

    def run_to_halt(self, max_steps=10_000):
        """
        Runs the machine until it halts or exceeds max_steps
        (prevents infinite loops during experimentation)
        :param max_steps:
        :return:
        """
        steps = 0
        while not self.halted and steps < max_steps:
            self.step()
            steps += 1

        if steps >= max_steps:
            raise RuntimeError("TM exceeded maximum step limit")

    def is_accepting(self):
        return self.state == self.accept_state

    def is_rejecting(self):
        return self.state == self.reject_state

    def get_configuration(self):
        """
        Returns a snapshot of the current configuration
        (for debugging or UI display)
        :return:
        """
        tape_slice, head_pos = self.tape.get_view()
        return {
            "state": self.state,
            "tape": tape_slice,
            "head_position": head_pos,
        }

if __name__ == "__main__":
    from tm_0n1n import TM_0N1N

    tm = TuringMachine(
        transitions=TM_0N1N,
        start_state="q0",
        accept_state="q_accept",
        reject_state="q_reject",
    )

    tm.reset("")
    tm.run_to_halt()
    print(tm.is_accepting())  # True (n = 0)

    tm.reset("01")
    tm.run_to_halt()
    print(tm.is_accepting())  # True

    tm.reset("0011")
    tm.run_to_halt()
    print(tm.is_accepting())  # True

    tm.reset("0101")
    tm.run_to_halt()
    print(tm.is_accepting())  # False

    tm.reset("011")
    tm.run_to_halt()
    print(tm.is_accepting())  # False

    tm.reset("001")
    tm.run_to_halt()
    print(tm.is_accepting())  # False