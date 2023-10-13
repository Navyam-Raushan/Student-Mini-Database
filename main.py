from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumWidth(500)

        # add menu bars
        file_menu = self.menuBar().addMenu("File")
        help_menu = self.menuBar().addMenu("Help")

        # add submenu for both
        file_menu_item = QAction("Add Student", self)
        file_menu.addAction(file_menu_item)

        help_menu_item = QAction("About", self)
        help_menu.addAction(help_menu_item)

        # Central Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)

        # set table to central widget
        self.setCentralWidget(self.table)

    # Loading the database data
    def load_data(self):
        connection = sqlite3.connect(database="database.db")
        data_query = connection.execute("SELECT * FROM students")

        # Write data query into a table
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(data_query):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                # Adding data in cell coordinated use qtablewidgetitem.
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(column_data)))

        connection.close()


# INSTANTIATE THE APP THEN CALL ABOVE QWIDGET INSTANCE.
app = QApplication(sys.argv)
main_window = MainWindow()

# TO SHOW THE APP AND EXIT, REMEMBER ITS A LOOP.
main_window.show()
main_window.load_data()
sys.exit(app.exec())
