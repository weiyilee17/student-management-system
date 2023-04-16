from sqlite3 import connect
from sys import argv, exit

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QToolBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu('&File')
        help_menu_item = self.menuBar().addMenu('&Help')
        edit_menu_item = self.menuBar().addMenu('&Edit')

        # self connects the action to MainWindow
        add_student_action = QAction(QIcon('icons/add.png'), 'Add Student', self)
        add_student_action.triggered.connect(self.create_add_student_dialog)
        file_menu_item.addAction(add_student_action)

        about_action = QAction('About', self)
        help_menu_item.addAction(about_action)

        # help_menu_item doesn't show on Mac, so added this line
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_student_action = QAction(QIcon('icons/search.png'), 'Search', self)
        search_student_action.triggered.connect(self.create_search_student_dialog)
        edit_menu_item.addAction(search_student_action)

        # QWidget uses QGridLayout, QMainWindow uses QTableWidget and sets it to the central widget
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID', 'Name', 'Course', 'Mobile'))

        # Hides the 1, 2, 3, 4 ... on the left hand side of the table
        # In this case, we have IDs column, so the vertical header is not necessary
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)

        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

    def load_students(self):
        connection = connect('database.db')
        all_students = connection.execute('SELECT * FROM students')

        # When ever the program starts, it always starts at the beginning,
        # not from where it ended(which would be attaching)
        self.table.setRowCount(0)

        for row_index, row_data in enumerate(all_students):
            self.table.insertRow(row_index)

            for col_index, col_data in enumerate(row_data):
                self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

        connection.close()

    def create_add_student_dialog(self):
        dialog = InsertDialog()
        dialog.exec()

    def create_search_student_dialog(self):
        dialog = SearchDialog()
        dialog.exec()


# QDialog is like a Form Modal
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Student')
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.student_name_line_edit = QLineEdit()
        self.student_name_line_edit.setPlaceholderText('Name')
        layout.addWidget(self.student_name_line_edit)

        self.course_name_combo_box = QComboBox()
        self.course_name_combo_box.addItems(['Biology', 'Math', 'Astronomy', 'Physics'])
        layout.addWidget(self.course_name_combo_box)

        self.mobile_number_line_edit = QLineEdit()
        self.mobile_number_line_edit.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile_number_line_edit)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.add_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    # TODO: close the dialog after the new student record is successfully created
    def add_student(self):
        connection = connect('database.db')
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO students (name, course, mobile) VALUES (?, ?, ? )',
            # The course name can be replaced by self.course_name.itemText(self.course_name.current_index())
            (
                self.student_name_line_edit.text(),
                self.course_name_combo_box.currentText(),
                self.mobile_number_line_edit.text()
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        # R e-fetch data from the database
        main_window.load_students()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Search Student')
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.student_name_line_edit = QLineEdit()
        self.student_name_line_edit.setPlaceholderText('Name')
        layout.addWidget(self.student_name_line_edit)

        search_button = QPushButton('Search')
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_student(self):
        connection = connect('database.db')

        search_results = main_window.table.findItems(self.student_name_line_edit.text(), Qt.MatchFlag.MatchContains)

        for single_result in search_results:
            # single_result.row() returns the index of the row,
            # 1 is the column index of name ('ID', 'Name', 'Course', 'Mobile')
            main_window.table.item(single_result.row(), 1).setSelected(True)

        connection.close()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_students()
    exit(app.exec())
