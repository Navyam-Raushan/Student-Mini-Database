from PyQt6.QtWidgets import QGridLayout, QLineEdit, QLabel, \
    QPushButton, QComboBox, QWidget, QApplication
import sys


class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Speed Calculator")
        # self.setMinimumWidth(400)

        grid = QGridLayout()
        distance = QLabel("Distance:")
        self.distance_edit_line = QLineEdit()

        time = QLabel("Time (hours):")
        self.time_edit_line = QLineEdit()

        self.mode = QComboBox()
        self.mode.addItem('Metric (km)')
        self.mode.addItem('Imperial (miles)')

        calculate_button = QPushButton('Calculate')
        calculate_button.clicked.connect(self.calculate)

        self.output_label = QLabel("")

        # adding to the grid
        grid.addWidget(distance, 0, 0)
        grid.addWidget(self.distance_edit_line, 0, 1)
        grid.addWidget(self.mode, 0, 2)

        grid.addWidget(time, 1, 0)
        grid.addWidget(self.time_edit_line, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.output_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate(self):
        d = float(self.distance_edit_line.text())
        t = float(self.time_edit_line.text())
        speed = d / t

        # checking for unit
        if self.mode.currentText() == "Metric (km)":
            speed = round(speed, 2)
            unit = "km/h"

        if self.mode.currentText() == "Imperial (miles)":
            speed = round(speed * 0.621371, 2)
            unit = "miles/h"

        to_show = f"Average Speed: {speed} {unit}"
        self.output_label.setText(to_show)


app = QApplication(sys.argv)
speed_calc = SpeedCalculator()

speed_calc.show()
sys.exit(app.exec())
