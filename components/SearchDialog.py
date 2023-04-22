from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton

from components.DatabaseConnection import DatabaseConnection


class SearchDialog(QDialog):
    def __init__(self, table, focus_function):
        super().__init__()
        self.focus_on_selected_cell = focus_function
        self.table = table
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

        search_results = self.table.findItems(self.student_name_line_edit.text(), Qt.MatchFlag.MatchContains)

        for index, single_result in enumerate(search_results):
            # single_result.row() returns the index of the row,
            # 1 is the column index of name ('ID', 'Name', 'Course', 'Mobile')
            self.table.item(single_result.row(), 1).setSelected(True)

            """ Edit and delete selects the entry by self.table.currentRow(), which is set by self.table.cellClicked().
            In other words, when you click on the cell, it sets the current cell.
            
            Setting the name selected for the search result doesn't affect the currentRow(), so I use setCurrentCell()
            to make the first search result the current cell, so the user can edit or delete right after search.
            """
            if index == 0:
                self.table.setCurrentCell(single_result.row(), single_result.column())

        connection.close()

        self.focus_on_selected_cell()
        self.close()
