from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QComboBox
from sys import argv, exit


class AverageSpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Average Speed Calculator')
        grid = QGridLayout()

        distance_label = QLabel('Distance: ')
        self.distance_line_edit = QLineEdit()

        self.unit = QComboBox()
        self.unit.addItems(['Metric (km)', 'Imperial (miles)'])

        time_label = QLabel('Time (hours): ')
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton('Calculate')
        calculate_button.clicked.connect(self.calculate_average_speed)

        self.result_label = QLabel('')

        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.unit, 0, 2)

        grid.addWidget(time_label, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)

        grid.addWidget(calculate_button, 2, 0, 1, 2)
        grid.addWidget(self.result_label, 3, 0, 1, 2)

        self.setLayout(grid)

    def calculate_average_speed(self):
        average_speed = float(self.distance_line_edit.text()) / float(self.time_line_edit.text())

        if self.unit.currentText() == 'Metric (km)':
            speed = round(average_speed, 2)
            unit = 'km/h'
        else:
            speed = round(average_speed / 1.6, 2)
            unit = 'mph'

        self.result_label.setText(f'Average Speed: {speed} {unit}')


if __name__ == '__main__':
    app = QApplication(argv)
    average_speed_calculator_form = AverageSpeedCalculator()
    average_speed_calculator_form.show()
    exit(app.exec())
