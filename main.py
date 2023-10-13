from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow
from PyQt6.QtGui import QAction
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # add menu bars
        file_menu = self.menuBar().addMenu("File")
        help_menu = self.menuBar().addMenu("Help")

        # add submenu for both
        file_menu_item = QAction("Add Student", self)
        file_menu.addAction(file_menu_item)

        help_menu_item = QAction("About", self)
        help_menu.addAction(help_menu_item)


# INSTANTIATE THE APP THEN CALL ABOVE QWIDGET INSTANCE.
app = QApplication(sys.argv)
age_calculator = MainWindow()

# TO SHOW THE APP AND EXIT, REMEMBER ITS A LOOP.
age_calculator.show()
sys.exit(app.exec())
