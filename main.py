from sys import argv, exit

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, \
    QTableWidget, QTableWidgetItem, QPushButton, QToolBar, QStatusBar

from components.AboutMessageBox import AboutMessageBox
from components.DatabaseConnection import DatabaseConnection
from components.DeleteDialog import DeleteDialog
from components.EditDialog import EditDialog
from components.InsertDialog import InsertDialog
from components.SearchDialog import SearchDialog


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
        dialog = InsertDialog(self.load_students)
        dialog.exec()

    def create_search_student_dialog(self):
        dialog = SearchDialog(self.table, self.handle_cell_click)
        dialog.exec()

    def create_edit_cell_dialog(self):
        dialog = EditDialog(self.table, self.load_students)
        dialog.exec()

    def create_delete_cell_dialog(self):
        dialog = DeleteDialog(self.table, self.load_students)
        dialog.exec()

    def create_about_message_box(self):
        message_box = AboutMessageBox()
        message_box.exec()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_students()
    exit(app.exec())
