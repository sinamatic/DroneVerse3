# Author: Sina Steinmüller

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
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt5.QtCore import Qt, QEvent


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()

        self.chosen_detection = None
        self.chosen_control = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Drone Control Interface")
        self.setGeometry(100, 100, 1792, 1120)  # Querformat Vollbild

        # Set background image
        self.set_background_image("images/DSC01497.jpg")

        # Main layout with vertical arrangement
        main_layout = QVBoxLayout()

        # Set a larger font
        font = QFont()
        font.setPointSize(20)

        # DRONEVERSE Header
        header_label = QLabel("DRONEVERSE")
        header_label.setStyleSheet("color: white;")
        header_label.setFont(QFont("Arial", 80, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label, alignment=Qt.AlignTop)

        # Upper part for texts and radio buttons
        upper_layout = QVBoxLayout()
        upper_layout.setSpacing(30)  # Space between sections

        # DETECTION METHODS
        detection_section = QVBoxLayout()
        detection_label = QLabel("How do you want to detect?")
        detection_label.setStyleSheet("color: white;")
        detection_label.setFont(font)
        detection_section.addWidget(detection_label)

        detection_methods_layout = QHBoxLayout()

        self.detection_group = QButtonGroup(self)

        # Gesture detection section
        gesture_section = QVBoxLayout()
        gesture_header = QLabel("Gesture detection")
        gesture_header.setStyleSheet("color: white;")
        gesture_header.setFont(QFont("Arial", 40, QFont.Bold))
        gesture_header.setAlignment(Qt.AlignLeft)
        gesture_section.addWidget(gesture_header)
        gesture_radio = QRadioButton("Gesture")
        gesture_radio.setStyleSheet("color: white;")
        gesture_radio.setFont(font)
        gesture_section.addWidget(gesture_radio)

        # Phone detection section
        phone_section = QVBoxLayout()
        phone_header = QLabel("OSC detection")
        phone_header.setStyleSheet("color: white;")
        phone_header.setFont(QFont("Arial", 40, QFont.Bold))
        phone_header.setAlignment(Qt.AlignLeft)
        phone_section.addWidget(phone_header)
        osc_radio = QRadioButton("OSC")
        osc_radio.setStyleSheet("color: white;")
        osc_radio.setFont(font)
        phone_section.addWidget(osc_radio)

        # Keyboard detection section
        keyboard_section = QVBoxLayout()
        keyboard_header = QLabel("Keyboard detection")
        keyboard_header.setStyleSheet("color: white;")
        keyboard_header.setFont(QFont("Arial", 40, QFont.Bold))
        keyboard_header.setAlignment(Qt.AlignLeft)
        keyboard_section.addWidget(keyboard_header)
        keyboard_radio = QRadioButton("Keyboard")
        keyboard_radio.setStyleSheet("color: white;")
        keyboard_radio.setFont(font)
        keyboard_section.addWidget(keyboard_radio)

        self.detection_group.addButton(gesture_radio)
        self.detection_group.addButton(osc_radio)
        self.detection_group.addButton(keyboard_radio)

        detection_methods_layout.addLayout(gesture_section)
        detection_methods_layout.addLayout(phone_section)
        detection_methods_layout.addLayout(keyboard_section)

        detection_section.addLayout(detection_methods_layout)
        upper_layout.addLayout(detection_section)

        # CONTROL METHODS
        control_section = QVBoxLayout()
        control_label = QLabel("What do you want to control?")
        control_label.setStyleSheet("color: white;")
        control_label.setFont(font)
        control_section.addWidget(control_label)

        control_methods_layout = QHBoxLayout()

        self.control_group = QButtonGroup(self)

        # Print controlled section
        print_section = QVBoxLayout()
        print_header = QLabel("Control Textoutputs")
        print_header.setStyleSheet("color: white;")
        print_header.setFont(QFont("Arial", 40, QFont.Bold))
        print_header.setAlignment(Qt.AlignLeft)
        print_section.addWidget(print_header)
        print_radio = QRadioButton("Print")
        print_radio.setStyleSheet("color: white;")
        print_radio.setFont(font)
        print_section.addWidget(print_radio)

        # Tello controlled section
        tello_section = QVBoxLayout()
        tello_header = QLabel("Control Tello Drone")
        tello_header.setStyleSheet("color: white;")
        tello_header.setFont(QFont("Arial", 40, QFont.Bold))
        tello_header.setAlignment(Qt.AlignLeft)
        tello_section.addWidget(tello_header)
        tello_radio = QRadioButton("Tello")
        tello_radio.setStyleSheet("color: white;")
        tello_radio.setFont(font)
        tello_section.addWidget(tello_radio)

        # Quadcopter controlled section
        quadcopter_section = QVBoxLayout()
        quadcopter_header = QLabel("Control Quadcopter Drone")
        quadcopter_header.setStyleSheet("color: white;")
        quadcopter_header.setFont(QFont("Arial", 40, QFont.Bold))
        quadcopter_header.setAlignment(Qt.AlignLeft)
        quadcopter_section.addWidget(quadcopter_header)
        quadcopter_radio = QRadioButton("Quadcopter")
        quadcopter_radio.setStyleSheet("color: white;")
        quadcopter_radio.setFont(font)
        quadcopter_section.addWidget(quadcopter_radio)

        self.control_group.addButton(print_radio)
        self.control_group.addButton(tello_radio)
        self.control_group.addButton(quadcopter_radio)

        control_methods_layout.addLayout(print_section)
        control_methods_layout.addLayout(tello_section)
        control_methods_layout.addLayout(quadcopter_section)

        control_section.addLayout(control_methods_layout)

        upper_layout.addLayout(control_section)

        # Spacer to push buttons to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        upper_layout.addItem(spacer)

        main_layout.addLayout(upper_layout)

        # START BUTTONS
        buttons_layout = QHBoxLayout()
        start_button = QPushButton("Start")
        start_button.setFont(font)
        start_button.setFixedHeight(100)  # Set a fixed height for the button
        start_button.clicked.connect(self.start_clicked)
        quit_button = QPushButton("Quit program")
        quit_button.setFont(font)
        quit_button.setFixedHeight(100)  # Set a fixed height for the button
        quit_button.clicked.connect(self.quit_clicked)
        buttons_layout.addWidget(start_button)
        buttons_layout.addWidget(quit_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def set_background_image(self, image_path):
        oImage = QPixmap(image_path)
        sImage = oImage.scaled(self.size(), Qt.IgnoreAspectRatio)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

    def start_clicked(self):
        detection_button = self.detection_group.checkedButton()
        control_button = self.control_group.checkedButton()

        if detection_button and control_button:
            self.chosen_detection = detection_button.text().lower()
            self.chosen_control = control_button.text().lower()
            self.close()
        else:
            error_dialog = QLabel("Please select both detection and control methods.")
            error_dialog.setStyleSheet("color: white;")
            error_dialog.setFont(QFont("Arial", 20))
            error_dialog.show()

    def quit_clicked(self):
        self.chosen_detection = None
        self.chosen_control = None
        self.quit_signal.emit()
        self.close()


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
