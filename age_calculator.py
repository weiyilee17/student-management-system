from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton
from sys import argv, exit
from datetime import datetime


class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Age Calculator')
        grid = QGridLayout()

        # Create label and line edit widgets
        name_label = QLabel('Name: ')
        self.name_line_edit = QLineEdit()

        birth_date_label = QLabel('Date of Birth MM/DD/YYYY: ')
        self.birth_date_line_edit = QLineEdit()

        calculate_button = QPushButton('Calculate Age')
        calculate_button.clicked.connect(self.calculate_age)

        self.result_label = QLabel('')

        # Add widgets to grid
        # row 0, col 0
        grid.addWidget(name_label, 0, 0)
        grid.addWidget(self.name_line_edit, 0, 1)

        grid.addWidget(birth_date_label, 1, 0)
        grid.addWidget(self.birth_date_line_edit, 1, 1)

        # we want the button to span around 1 row, 2 columns
        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.result_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_age(self):
        current_date = datetime.now()
        birth_date = self.birth_date_line_edit.text()
        date_of_birth = datetime.strptime(birth_date, '%m/%d/%Y')

        age = int((current_date - date_of_birth).days / 365)

        self.result_label.setText(f'{self.name_line_edit.text()} is {age} years old.')


if __name__ == '__main__':
    app = QApplication(argv)
    age_calculator = AgeCalculator()
    age_calculator.show()
    exit(app.exec())
