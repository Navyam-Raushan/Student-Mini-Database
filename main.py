from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, \
    QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QComboBox, QBoxLayout
from PyQt6.QtGui import QAction
import sys
import sqlite3


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumWidth(500)

        # add menu bars
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        # add submenu for both
        # Two big errors encountered self.insert() must not call the method otherwise main window will
        # not be shown, secondly QVBoxLayout() must instantiate the object.
        file_menu_item = QAction("Add Student", self)
        file_menu_item.triggered.connect(self.insert)
        # add_student_action = QAction("Add student", self)
        # add_student_action.triggered.connect(self.insert)
        file_menu.addAction(file_menu_item)

        help_menu_item = QAction("About", self)
        help_menu.addAction(help_menu_item)

        # Central Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))

        # Unusual vertical indexing removal.
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
                print(row_data)
                # Adding data in cell coordinated use qtablewidgetitem.
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(column_data)))

        print(list(data_query))
        connection.close()

    def insert(self):
        insert_dialog = InsertDialog()
        insert_dialog.exec()


# To create a dialog we use QDialog
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # layout.stretch(1)

        # Added name widget, don't forget brackets.
        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # course widget
        self.course_name = QComboBox()
        courses = ["Math", "Biology", "Physics", "Astronomy"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Phone widget
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("+91 4567883322")
        layout.addWidget(self.phone)

        # Submit button to send it to database
        button = QPushButton("Add Student")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)
    def add_student(self):

        s_name = self.name.text()
        # Important how we get current index value
        s_course = self.course_name.currentText()
        s_phone = self.phone.text()

        connection = sqlite3.connect(database="database.db")
        cursor = connection.cursor()
        # insert_query = "INSERT INTO students (name, course, mobile) VALUES (?,?,?)"
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (s_name, s_course, s_phone))

        connection.commit()
        cursor.close()
        connection.close()

# INSTANTIATE THE APP THEN CALL ABOVE QWIDGET INSTANCE.
app = QApplication(sys.argv)
main_window = MainWindow()

# TO SHOW THE APP AND EXIT, REMEMBER ITS A LOOP.
main_window.load_data()
main_window.show()
sys.exit(app.exec())
