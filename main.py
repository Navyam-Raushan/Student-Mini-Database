from PyQt6.QtWidgets import QApplication, QMessageBox, QVBoxLayout, \
    QLabel, QWidget, QStatusBar, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar, QGridLayout
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sys
import sqlite3


class Database:

    def connect(self, database_file="database.db"):
        connection = sqlite3.connect(database_file)
        return connection


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        # add menu bars
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        # add submenu for both
        # Two big errors encountered self.insert() must not call the method otherwise main window will
        # not be shown, secondly QVBoxLayout() must instantiate the object.
        file_menu_item = QAction(QIcon("icons/add.png"), "Add Student", self)
        file_menu_item.triggered.connect(self.insert)
        # add_student_action = QAction("Add student", self)
        # add_student_action.triggered.connect(self.insert)
        file_menu.addAction(file_menu_item)

        help_menu_item = QAction("About", self)
        help_menu.addAction(help_menu_item)
        help_menu_item.triggered.connect(self.about)

        # Adding edit menu and search dialog
        edit_menu = self.menuBar().addMenu("&Edit")
        search_bar_action = QAction(QIcon("icons/search.png"), "Search..", self)

        # When search bar is clicked (trigerred)
        search_bar_action.triggered.connect(self.search)
        edit_menu.addAction(search_bar_action)

        # Central Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))

        # Unusual vertical indexing removal.
        self.table.verticalHeader().setVisible(False)
        # set table to central widget
        self.setCentralWidget(self.table)

        # Adding Toolbar to Main Window.
        toolbar = QToolBar()
        toolbar.setMovable(True)
        toolbar.addAction(file_menu_item)
        toolbar.addAction(search_bar_action)
        self.addToolBar(toolbar)

        # Adding Status Bar to Main window
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect a cell click
        # then show edit and delete button
        self.table.cellClicked.connect(self.cell_click)

    # Loading the database data
    def load_data(self):
        connection = Database.connect(self)
        data_query = connection.execute("SELECT * FROM students")

        # Write data query into a table
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(data_query):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                # print(row_data)
                # Adding data in cell coordinated use qtablewidgetitem.
                self.table.setItem(row_number, column_number,
                                   QTableWidgetItem(str(column_data)))

        # print(list(data_query))
        connection.close()

    def insert(self):
        insert_dialog = InsertDialog()
        insert_dialog.exec()

    def search(self):
        search_dialog = SearchDialog()

        search_dialog.exec()

    def cell_click(self):
        edit_button = QPushButton("Edit")
        # when edit button is clicked we allow user to edit entries.
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        # Before adding we have to remove previous present button
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):

        edit_dialog = EditDialog()
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        content = """
        We have made this app using sqlite, Feel free to Use this
        And to give any suggestion fork on Github.
        """
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()
        # Getting Current index then getting current data of student.
        selected_row = main_window.table.currentRow()

        # All Data when user select a cell.
        self.selected_student_id = main_window.table.item(selected_row, 0).text()
        selected_name = main_window.table.item(selected_row, 1).text()
        selected_course = main_window.table.item(selected_row, 2).text()
        selected_mobile = main_window.table.item(selected_row, 3).text()

        # Added name widget, don't forget brackets.
        self.name = QLineEdit(selected_name)
        # self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        # course widget

        self.course_name = QComboBox()
        courses = ["Math", "Biology", "Physics", "Astronomy"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(selected_course)
        layout.addWidget(self.course_name)

        # Phone widget
        self.phone = QLineEdit(selected_mobile)
        # self.phone.setPlaceholderText("+91 4567883322")
        layout.addWidget(self.phone)

        # Submit button to send it to database
        button = QPushButton("Update Record")
        button.clicked.connect(self.update_record)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_record(self):
        # Get the data input by user send it to database
        # Current data would be get from QLineEdit only not clicked data of table.
        updated_name = self.name.text()
        updated_course = self.course_name.itemText(self.course_name.currentIndex())
        updated_phone = self.phone.text()

        connection = Database.connect(self)
        cursor = connection.cursor()

        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (updated_name, updated_course, updated_phone, self.selected_student_id))
        connection.commit()
        cursor.close()
        connection.close()

        # Updating table again..
        main_window.load_data()
        self.close()

        confirmation = QMessageBox()
        confirmation.setWindowTitle("Message")
        confirmation.setText("Record was edited Successfully.")
        confirmation.exec()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")

        layout = QGridLayout()
        label = QLabel("Are you sure you want to delete?")

        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 1)
        layout.addWidget(no, 1, 2)

        self.setLayout(layout)
        yes.clicked.connect(self.delete_record)
        no.clicked.connect(self.close_delete_widget)

    def close_delete_widget(self):
        self.close()

    def delete_record(self):
        # Write sql queries for delete operation
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = Database.connect(self)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()
        self.close()

        confirmation = QMessageBox()
        confirmation.setWindowTitle("Message")
        confirmation.setText("Record was deleted successfully.")
        confirmation.exec()


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

    # To add any new student.
    def add_student(self):
        s_name = self.name.text()
        # Important how we get current index value
        s_course = self.course_name.currentText()
        s_phone = self.phone.text()

        connection = Database.connect(self)
        cursor = connection.cursor()
        # insert_query = "INSERT INTO students (name, course, mobile) VALUES (?,?,?)"
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (s_name, s_course, s_phone))

        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()
        confirmation = QMessageBox()
        confirmation.setWindowTitle("Message")
        confirmation.setText("Record was Added successfully.")
        confirmation.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.search_name = QLineEdit()
        self.search_name.setPlaceholderText("Name")
        layout.addWidget(self.search_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_(self):
        name = self.search_name.text()
        connection = Database.connect(self)
        cursor = connection.cursor()

        search_results = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))

        # Now match the occurences with search_results and table data
        rows = list(search_results)
        # print(rows)

        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            # print(item)
            # item.row  will return the row number set selected will highlight it.
            main_window.table.item(item.row(), 1).setSelected(True)

            cursor.close()
            connection.close()


# INSTANTIATE THE APP THEN CALL ABOVE QWIDGET INSTANCE.
app = QApplication(sys.argv)
main_window = MainWindow()

# TO SHOW THE APP AND EXIT, REMEMBER ITS A LOOP.
main_window.load_data()
main_window.show()
sys.exit(app.exec())
