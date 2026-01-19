class Tape:
    def __init__(self, input_string="", blank="_"):
        self.blank = blank
        self.tape = list(input_string) if input_string else [blank]
        self.head = 0

    def read(self):
        return self.tape[self.head]

    def write(self, symbol):
        self.tape[self.head] = symbol

    def move_left(self):
        if self.head == 0:
            # Extend tape to the left
            self.tape.insert(0, self.blank)
        else:
            self.head -= 1

    def move_right(self):
        self.head += 1
        if self.head == len(self.tape):
            # Extend tape to the right
            self.tape.append(self.blank)

    def get_view(self, window=10):
        """
        Returns a snapshot of the tape around the head
        for debugging or UI display
        :param window:
        :return:
        """
        start = max(0, self.head - window)
        end = min(len(self.tape), self.head + window + 1)

        tape_slice = self.tape[start:end]
        head_pos = self.head - start

        return tape_slice, head_pos

if __name__ == "__main__":
    t = Tape("01")
    print(t.read())  # '0'
    t.move_right()
    print(t.read())  # '1'
    t.move_right()
    print(t.read())  # '_'
    t.write('X')
    print(t.get_view())
    t.move_left()
    print(t.read())  # '1'
    t.move_left()
    t.move_left()
    print(t.read())  # '_'
    print(t.get_view())