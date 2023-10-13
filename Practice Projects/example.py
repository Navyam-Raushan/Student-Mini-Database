from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton

import sys
from datetime import datetime


# MAKE CLASS FOR EACH WINDOW
class AgeCalculator(QWidget):
    # OVERWRITE INIT METHOD OF QWIDGET
    def __init__(self):
        # CALL SUPER METHOD TO INHERIT ALL PROPERTY
        super().__init__()
        self.setWindowTitle("Age Calculator")
        grid = QGridLayout()

        name = QLabel("Name:")
        self.name_edit = QLineEdit()

        dob = QLabel("Date of Birth DD/MM/YY:")
        self.dob_edit = QLineEdit()

        # ADD BUTTON AND OUTPUT AREA
        calculate_age_button = QPushButton("Calculate Age")

        # MAKING BUTTON FUNCTIONAL
        calculate_age_button.clicked.connect(self.calculate_age)

        # ADD AFTER BUTTON IS CLICKED.
        self.output_area = QLabel("")

        # ATTACH THESE LABELS (WIDGETS) TO THE GRID
        grid.addWidget(name, 0, 0)
        grid.addWidget(self.name_edit, 0, 1)
        grid.addWidget(dob, 1, 0)
        grid.addWidget(self.dob_edit, 1, 1)

        # FORMAT TO ADD (row_n, column_n rowspan, colspan)
        grid.addWidget(calculate_age_button, 2, 0, 1, 2)
        grid.addWidget(self.output_area, 3, 0, 1, 2)

        # SET THE LAYOUT TO GRID THAT YOU MADE
        self.setLayout(grid)

    def calculate_age(self):
        current_year = datetime.now().year
        user_dob = self.dob_edit.text()


        # This can also be done by concept of list.strip()
        year_of_birth = datetime.strptime(user_dob, "%d/%m/%Y").date().year
        age = current_year - year_of_birth

        # OUTPUT TO SHOW
        to_show = f"{self.name_edit.text()} is {age} years old."
        self.output_area.setText(to_show)


# INSTANTIATE THE APP THEN CALL ABOVE QWIDGET INSTANCE.
app = QApplication(sys.argv)
age_calculator = AgeCalculator()

# TO SHOW THE APP AND EXIT, REMEMBER ITS A LOOP.
age_calculator.show()
sys.exit(app.exec())

