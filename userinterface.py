# userinterface.py

# userinterface.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap

chosen_detection = "none"


def create_button(layout, text, command):
    button = QPushButton(text)
    button.setStyleSheet("background-color: black; font-size: 20px; font-weight: bold;")
    button.clicked.connect(command)
    layout.addWidget(button)


def set_gestenerkennung():
    chosen_detection = "gesture"
    print(f"Gewählte Steuerung: {chosen_detection}")
    close_window()


def set_handysteuerung():
    chosen_detection = "osc"
    print(f"Gewählte Steuerung: {chosen_detection}")
    close_window()


def set_tastatursteuerung():
    chosen_detection = "keyboard"
    print(f"Gewählte Steuerung: {chosen_detection}")
    close_window()


def close_window():
    window.close()


def start_user_interface():
    global window
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 600, 1080)
    window.setWindowTitle("User Interface")

    # Load and set the background image
    label = QLabel(window)
    pixmap = QPixmap("images/background.jpg")
    label.setPixmap(pixmap)
    label.setScaledContents(True)
    label.resize(window.size())

    # Create a layout to hold the buttons
    layout = QVBoxLayout()

    # Create buttons
    create_button(layout, "Gestenerkennung starten", set_gestenerkennung)
    create_button(layout, "Handysteuerung starten", set_handysteuerung)
    create_button(layout, "Tastatursteuerung starten", set_tastatursteuerung)

    # Set the layout for the window and add the label
    container = QWidget(window)
    container.setLayout(layout)
    container.setGeometry(
        150, 300, 300, 500
    )  # Position the container within the window

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_user_interface()
