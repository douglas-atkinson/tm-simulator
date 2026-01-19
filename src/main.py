import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLineEdit,
    QComboBox,
    QPlainTextEdit,
    QAction,
    QFileDialog,
    QMessageBox, QSlider,
)
from PyQt5.QtCore import Qt, QTimer

from tm_model import TuringMachine
from machines import MACHINES


class TuringMachineWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Turing Machine Simulator")
        self.setGeometry(200, 200, 800, 300)

        self._build_ui()
        self.load_machine()
        self._build_menu()

        self.run_timer = QTimer()
        self.run_timer.setInterval(400)
        self.run_timer.timeout.connect(self.run_step)

        self.speed_slider.valueChanged.connect(self.update_speed)

        self.tm = None
        self.step_count = 0

    def _build_ui(self):
        central = QWidget()
        main_layout = QVBoxLayout()

        # ===== Title =====
        title = QLabel("Turing Machine Simulator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        # ===== Start Display =====
        self.state_label = QLabel("State: q0")
        self.state_label.setAlignment(Qt.AlignCenter)
        self.state_label.setStyleSheet("font-size: 16px;")
        main_layout.addWidget(self.state_label)

        # ===== Tape Display =====
        tape_frame = QFrame()
        tape_layout = QHBoxLayout()
        tape_layout.setSpacing(5)

        # Create placeholder tape cells
        self.tape_cells = []
        for i in range(15):
            cell = QLabel("_")
            cell.setFixedSize(40, 40)
            cell.setAlignment(Qt.AlignCenter)
            cell.setStyleSheet(
                "border: 1px solid black; font-family: monospace; font-size: 16px;"
            )
            self.tape_cells.append(cell)
            tape_layout.addWidget(cell)

        tape_frame.setLayout(tape_layout)
        main_layout.addWidget(tape_frame, alignment=Qt.AlignCenter)

        # ===== Head Indicator =====
        self.head_layout = QHBoxLayout()
        self.head_layout.setSpacing(5)

        self.head_spacers = []

        # Create spacers aligned with tape cells
        for _ in range(len(self.tape_cells)):
            spacer = QWidget()
            spacer.setFixedSize(40, 20)
            self.head_spacers.append(spacer)
            self.head_layout.addWidget(spacer)

        self.head_label = QLabel("▲")
        self.head_label.setAlignment(Qt.AlignCenter)
        self.head_label.setStyleSheet("font-size: 18px; color: green;")
        self.head_layout.insertWidget(0, self.head_label)

        main_layout.addLayout(self.head_layout)

        # ===== Configuration Trace =====
        self.trace_box = QPlainTextEdit()
        self.trace_box.setReadOnly(True)
        self.trace_box.setMaximumHeight(150)
        self.trace_box.setMinimumHeight(150)
        self.trace_box.setStyleSheet(
            "font-family: monospace; font-size: 12px;"
        )

        main_layout.addWidget(QLabel("Configuration Trace:"))
        main_layout.addWidget(self.trace_box)

        # ===== Control Buttons =====
        button_layout = QHBoxLayout()

        self.step_button = QPushButton("Step")
        self.step_button.clicked.connect(self.step_tm)
        self.step_button.setEnabled(False)
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_tm)
        self.run_button.setEnabled(False)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_tm)

        button_layout.addWidget(self.step_button)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.reset_button)

        main_layout.addLayout(button_layout)

        # ===== Speed Control =====
        speed_layout = QHBoxLayout()

        speed_label = QLabel("Speed:")
        speed_label.setFixedWidth(50)

        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(400)
        self.speed_slider.setInvertedAppearance(True)
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(150)
        print(self.speed_slider.value())

        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)

        main_layout.addLayout(speed_layout)

        # ===== Input Area =====
        input_layout = QHBoxLayout()

        input_label = QLabel("Input:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter input string (e.g., 0011)")
        self.input_field.setFixedWidth(200)

        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input_field)
        input_layout.addStretch()

        main_layout.addLayout(input_layout)

        # ===== Machine Selector =====
        machine_layout = QVBoxLayout()

        machine_label = QLabel("Machine:")
        self.machine_selector = QComboBox()
        self.machine_selector.addItems(MACHINES.keys())
        self.machine_selector.setFixedWidth(200)
        self.machine_selector.currentIndexChanged.connect(self.load_machine)

        self.alphabet_label = QLabel("Σ: —")
        self.alphabet_label.setStyleSheet("font-style: italic;")

        machine_layout.addWidget(machine_label)
        machine_layout.addWidget(self.machine_selector)
        machine_layout.addWidget(self.alphabet_label)
        machine_layout.addStretch()

        main_layout.addLayout(machine_layout)


        central.setLayout(main_layout)
        self.setCentralWidget(central)

    def _build_menu(self):
        menu_bar = self.menuBar()

        # ===== File Menu =====
        file_menu = menu_bar.addMenu("&File")
        self.open_file_action = QAction("&Open Input File...", self)
        self.export_trace_action = QAction("&Export Configuration Trace...", self)
        self.export_csv_action = QAction("&Export Trace as CSV...", self)
        self.exit_action = QAction("E&xit", self)

        file_menu.addAction(self.open_file_action)
        export_menu = file_menu.addMenu("&Export")
        export_menu.addAction(self.export_trace_action)
        export_menu.addAction(self.export_csv_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # ===== About Menu =====
        about_menu = menu_bar.addMenu("&About")
        self.about_action = QAction("&About This Simulator", self)
        about_menu.addAction(self.about_action)

        # Connect actions
        self.exit_action.triggered.connect(self.close)
        self.open_file_action.triggered.connect(self.open_input_file)
        self.export_trace_action.triggered.connect(self.export_trace)
        self.export_csv_action.triggered.connect(self.export_trace_csv)
        self.about_action.triggered.connect(self.show_about)

    def close(self):
        pass

    def open_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Input File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
            self.input_field.setText(content)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to read file:\n{e}"
            )

    def export_trace(self):
        if self.trace_box.toPlainText().strip() == "":
            QMessageBox.information(
                self,
                "No Trace",
                "There is no configuration trace to export."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Configure Trace",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w") as f:
                f.write(str(self.trace_box.toPlainText()))

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export trace:\n{e}"
            )

    def export_trace_csv(self):
        text = self.trace_box.toPlainText().strip()
        if not text:
            QMessageBox.information(
                self,
                "No Trace",
                "There is no configuration trace to export."
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Trace as CSV",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_path:
            return

        try:
            with open(file_path, "w", newline="") as f:
                f.write("step,state,tape,head\n")

                for line in text.splitlines():
                    # Example:
                    # Step 003: (q1, X 0 1 1, head=2)

                    step_part, rest = line.split(": ", 1)
                    step = step_part.replace("Step ", "")

                    inside = rest.strip("()")
                    state, tape_part, head_part = inside.split(", ", 2)

                    tape = tape_part
                    head = head_part.replace("head=", "")

                    f.write(f"{step},{state},\"{tape}\",{head}\n")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export CSV:\n{e}"
            )

    def show_about(self):
        QMessageBox.information(
            self,
            "About This Simulator",
            "Turing Machine Simulator\n\n"
            "Designed for teaching and exploring\n"
            "Standard Turing Machines.\n\n"
            "Built with Python and PyQt."
        )

    def reset_tm(self):
        if self.run_timer.isActive():
            self.run_timer.stop()

        self.trace_box.clear()
        self.step_count = 0

        self.state_label.setStyleSheet("font-size: 16px;")

        machine = self.current_machine

        # Create a new Turing Machine instance
        self.tm = TuringMachine(
            transitions=machine["transitions"],
            start_state=machine["start"],
            accept_state=machine["accept"],
            reject_state=machine["reject"],
        )

        input_string = self.input_field.text()

        self.tm.reset(input_string)
        self.update_display()
        self.append_trace()
        self.step_button.setEnabled(True)
        self.run_button.setEnabled(True)

    def update_display(self):
        if not self.tm:
            return

        config = self.tm.get_configuration()
        state = config["state"]
        tape = config["tape"]
        head_pos = config["head_position"]
        self.update_head_position(head_pos)

        # Update the state label
        self.state_label.setText(f"State: {state}")
        # Visual feedback if halted
        if self.tm.is_accepting():
            self.state_label.setStyleSheet(
                "font-size: 16px; color: green; font-weight: bold;"
            )
        elif self.tm.is_rejecting():
            self.state_label.setStyleSheet(
                "font-size: 16px; color: red; font-weight: bold;"
            )


        # Clear all cells
        for cell in self.tape_cells:
            cell.setText("_")
            cell.setStyleSheet(
                "border: 1px solid black; font-family: monospace; font-size: 16px;"
            )

        # Display tape symbols
        for i, symbol in enumerate(tape):
            if i < len(self.tape_cells):
                self.tape_cells[i].setText(symbol)

        # Highlight head position
        if 0 <= head_pos < len(self.tape_cells):
            self.tape_cells[head_pos].setStyleSheet(
                "border: 2px solid red; font-family: monospace; font-size: 16px;"
            )

        if self.tm.halted:
            self.step_button.setEnabled(False)
            self.run_button.setEnabled(False)

    def step_tm(self):
        if not self.tm:
            return

        if self.tm.halted:
            self.update_display()
            self.append_trace()
            return

        self.run_button.setEnabled(False)
        self.tm.step()
        self.update_display()
        self.append_trace()

    def run_tm(self):
        if not self.tm:
            return

        if self.tm.halted:
            self.update_display()
            return

        # Disable controls during animation
        self.step_button.setEnabled(False)
        self.run_button.setEnabled(False)

        self.run_timer.start()

    def update_head_position(self, head_pos):
        # Remove the head label
        self.head_layout.removeWidget(self.head_label)

        # Reinsert at the correct position
        self.head_layout.insertWidget(head_pos, self.head_label)

    def run_step(self):
        if not self.tm or self.tm.halted:
            self.run_timer.stop()
            self.update_display()
            self.append_trace()
            return

        self.tm.step()
        self.update_display()
        self.append_trace()

        if self.tm.halted:
            self.run_timer.stop()

    def append_trace(self):
        try:
            if not self.tm:
                return

            config = self.tm.get_configuration()
            state = config["state"]
            tape = " ".join(config["tape"])
            head = config["head_position"]

            line = f"Step {self.step_count:03d}: ({state}, {tape}, head={head})"
            self.trace_box.appendPlainText(line)

            self.step_count += 1
        except Exception as e:
            print(f"Error: {e}")

    def update_speed(self, value):
        if self.run_timer:
            self.run_timer.setInterval(value)

    def load_machine(self):
        machine_name = self.machine_selector.currentText()
        machine = MACHINES[machine_name]

        self.current_machine = machine
        self.current_input_alphabet = machine["input_alphabet"]

        alphabet = ", ".join(sorted(self.current_input_alphabet))
        self.alphabet_label.setText(f"Σ: {alphabet}")

        # Invalidate any existing TM instance
        self.tm = None

        # Disable Step/Run until Reset
        self.step_button.setEnabled(False)
        self.run_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TuringMachineWindow()
    window.show()
    sys.exit(app.exec_())