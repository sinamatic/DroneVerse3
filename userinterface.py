# userinterface.py

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QRadioButton,
    QButtonGroup,
)


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.chosen_detection = None
        self.chosen_control = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Drone Control Interface")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        detection_layout = QVBoxLayout()
        detection_label = QLabel("Choose Detection Method:")
        detection_layout.addWidget(detection_label)

        self.detection_group = QButtonGroup(self)

        gesture_radio = QRadioButton("Gesture")
        osc_radio = QRadioButton("OSC")
        keyboard_radio = QRadioButton("Keyboard")

        self.detection_group.addButton(gesture_radio)
        self.detection_group.addButton(osc_radio)
        self.detection_group.addButton(keyboard_radio)

        detection_layout.addWidget(gesture_radio)
        detection_layout.addWidget(osc_radio)
        detection_layout.addWidget(keyboard_radio)

        layout.addLayout(detection_layout)

        control_layout = QVBoxLayout()
        control_label = QLabel("Choose Control Method:")
        control_layout.addWidget(control_label)

        self.control_group = QButtonGroup(self)

        print_radio = QRadioButton("Print")
        tello_radio = QRadioButton("Tello")

        self.control_group.addButton(print_radio)
        self.control_group.addButton(tello_radio)

        control_layout.addWidget(print_radio)
        control_layout.addWidget(tello_radio)

        layout.addLayout(control_layout)

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_clicked)

        layout.addWidget(start_button)

        self.setLayout(layout)

    def start_clicked(self):
        detection_button = self.detection_group.checkedButton()
        control_button = self.control_group.checkedButton()

        if detection_button and control_button:
            self.chosen_detection = detection_button.text().lower()
            self.chosen_control = control_button.text().lower()
            self.close()
        else:
            error_dialog = QLabel("Please select both detection and control methods.")
            error_dialog.show()


def get_user_choices():
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    app.exec_()
    return ui.chosen_detection, ui.chosen_control


if __name__ == "__main__":
    chosen_detection, chosen_control = get_user_choices()
    if chosen_detection and chosen_control:
        print(f"Chosen Detection: {chosen_detection}")
        print(f"Chosen Control: {chosen_control}")
    else:
        print("Selection was not made properly.")
