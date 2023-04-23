from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from components.DatabaseConnection import DatabaseConnection


class EditDialog(QDialog):
    def __init__(self, table, reload_function):
        super().__init__()
        self.table = table
        self.reload = reload_function
        self.setWindowTitle('Edit Student')
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        # Get selected row data
        selected_row_index = self.table.currentRow()
        self.selected_student_ID = self.table.item(selected_row_index, 0).text()
        selected_student_name = self.table.item(selected_row_index, 1).text()
        selected_course_name = self.table.item(selected_row_index, 2).text()
        selected_mobile_number = self.table.item(selected_row_index, 3).text()

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
            'UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s',
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

        self.reload()
        self.close()
