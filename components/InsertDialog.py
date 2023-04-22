from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QPushButton

from components.DatabaseConnection import DatabaseConnection


# QDialog is like a Form Modal
class InsertDialog(QDialog):
    def __init__(self, reload_function):
        super().__init__()
        self.setWindowTitle('Add Student')
        self.setFixedSize(300, 300)

        self.reload = reload_function

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
        self.reload()

        self.close()
