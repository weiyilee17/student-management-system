from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QMessageBox

from components.DatabaseConnection import DatabaseConnection


class DeleteDialog(QDialog):
    def __init__(self, table, reload_function, update_status_bar_function):
        super().__init__()
        self.table = table
        self.reload = reload_function
        self.update_status_bar_function = update_status_bar_function
        self.setWindowTitle('Delete Student')

        layout = QGridLayout()

        selected_row_index = self.table.currentRow()
        self.selected_student_ID = self.table.item(selected_row_index, 0).text()
        selected_student_name = self.table.item(selected_row_index, 1).text()

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
            'DELETE FROM students WHERE id = %s',
            # Adding , after the value to make it a tuple. Or otherwise, it would be treated as self.selected_student_ID
            (
                self.selected_student_ID,
            )
        )

        connection.commit()
        cursor.close()
        connection.close()

        self.reload()

        # After searching a user, deleting him, if the status bar remains, when we edit, we would try to access
        # None.text(), and would crash the program. To prevent this, we hide the status bar after deleting an entry.
        self.table.setCurrentCell(-1, -1)
        self.update_status_bar_function()

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
