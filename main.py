from sqlite3 import connect
from sys import argv, exit

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QToolBar, QStatusBar, \
    QGridLayout, QLabel, QMessageBox


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
        about_action.triggered.connect(self.create_about_message_box)

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

        # Create status bar and add status bar elements
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Detect a cell click
        self.table.cellClicked.connect(self.handle_cell_click)

    def handle_cell_click(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.create_edit_cell_dialog)

        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.create_delete_cell_dialog)

        already_existing_buttons = self.findChildren(QPushButton)

        if not already_existing_buttons:
            self.status_bar.addWidget(edit_button)
            self.status_bar.addWidget(delete_button)

    def load_students(self):
        connection = DatabaseConnection().connect()
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

    def create_edit_cell_dialog(self):
        dialog = EditDialog()
        dialog.exec()

    def create_delete_cell_dialog(self):
        dialog = DeleteDialog()
        dialog.exec()

    def create_about_message_box(self):
        message_box = AboutMessageBox()
        message_box.exec()


class DatabaseConnection:
    def __init__(self, database_file='database.db'):
        self.database_file = database_file

    def connect(self):
        connection = connect(self.database_file)
        return connection


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

    def add_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)',
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

        # Re-fetch data from the database
        main_window.load_students()

        self.close()


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
        connection = DatabaseConnection().connect()

        search_results = main_window.table.findItems(self.student_name_line_edit.text(), Qt.MatchFlag.MatchContains)

        for single_result in search_results:
            # single_result.row() returns the index of the row,
            # 1 is the column index of name ('ID', 'Name', 'Course', 'Mobile')
            main_window.table.item(single_result.row(), 1).setSelected(True)

        connection.close()

        self.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Edit Student')
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Get selected row data
        selected_row_index = main_window.table.currentRow()
        self.selected_student_ID = main_window.table.item(selected_row_index, 0).text()
        selected_student_name = main_window.table.item(selected_row_index, 1).text()
        selected_course_name = main_window.table.item(selected_row_index, 2).text()
        selected_mobile_number = main_window.table.item(selected_row_index, 3).text()

        self.student_name_line_edit = QLineEdit(selected_student_name)
        self.student_name_line_edit.setPlaceholderText('Name')
        layout.addWidget(self.student_name_line_edit)

        self.course_name_combo_box = QComboBox()
        self.course_name_combo_box.addItems(['Biology', 'Math', 'Astronomy', 'Physics'])
        self.course_name_combo_box.setCurrentText(selected_course_name)
        layout.addWidget(self.course_name_combo_box)

        self.mobile_number_line_edit = QLineEdit(selected_mobile_number)
        self.mobile_number_line_edit.setPlaceholderText('Mobile')
        layout.addWidget(self.mobile_number_line_edit)

        submit_button = QPushButton('Submit')
        submit_button.clicked.connect(self.edit_student)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def edit_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            'UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?',
            (
                self.student_name_line_edit.text(),
                self.course_name_combo_box.currentText(),
                self.mobile_number_line_edit.text(),
                self.selected_student_ID
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_students()
        self.close()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Delete Student')

        layout = QGridLayout()

        selected_row_index = main_window.table.currentRow()
        self.selected_student_ID = main_window.table.item(selected_row_index, 0).text()
        selected_student_name = main_window.table.item(selected_row_index, 1).text()

        confirmation_label = QLabel(f'Are you sure you want to delete the record for {selected_student_name}?')

        yes_button = QPushButton('Yes')
        yes_button.clicked.connect(self.delete_student)

        no_button = QPushButton('No')
        no_button.clicked.connect(self.close)

        layout.addWidget(confirmation_label, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)

        self.setLayout(layout)

    def delete_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute(
            'DELETE FROM students WHERE id = ?',
            # Adding , after the value to make it a tuple. Or otherwise, it would be treated as self.selected_student_ID
            (
                self.selected_student_ID,
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_students()
        self.close()

        """
            .exec() creates an event loop. Nesting .exec()s causes warning in the console:
            Cannot use native application modal dialog from nested event loop
            
            The documentation mentions that avoid using .exec(), and use .open() instead, but doesn't provide examples
            
            using .open() for DeleteDialog prevents the dialog from showing, I think it is because the way of opening
            a window modal is different from application modal?
            using .open() for delete_confirmation_message_box prevents delete_confirmation_message_box from showing,
            with the reason can't show modal when the parent doesn't exist. Can't be solved by closing after 
            delete_confirmation_message_box.open()
            
            This is a problem, but to solve it, it requires a deep dive into PyQt6, because there is no quick answer
            for this. Since this project is just an introduction to PyQt6, I won't spend too much time on this, but
            still worth taking notes in case needed in the future.
        """

        delete_confirmation_message_box = QMessageBox()
        delete_confirmation_message_box.setWindowTitle('Success')
        delete_confirmation_message_box.setText('The record has been deleted successfully.')
        delete_confirmation_message_box.exec()


class AboutMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('About')

        about_message = f"""Warning message TSMSendMessageToUIServer seems to be related to new M1 chips for the new \
MacBooks.
        
TSM AdjustCapsLockLEDForKeyTransitionHandling - _ISSetPhysicalKeyboardCapsLockLED Inhibit seems to be related \
to other languages that can be switched by Caps lock. 
    
Stackoverflow's suggestions says that the user should either remove the language or cancel the Caps lock \
switch language binding, which neither is a good solution. I would currently leave it as it is since it \
doesn't seem to harm, but would get back into it in the future if I make further PyQt6 applications and \
this warning is causing actual problems.
        """

        self.setText(about_message)


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_students()
    exit(app.exec())
