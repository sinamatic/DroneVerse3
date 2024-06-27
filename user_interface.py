import tkinter as tk
from PIL import Image, ImageTk


def create_button(window, text, command):
    button = tk.Button(window, text=text, command=command, bg="white")
    button.pack(pady=20)
    button.configure(font=("Arial", 20, "bold"))


def set_gestenerkennung():
    choosen_control = "Gestenerkennung"
    print(f"Gewählte Steuerung: {choosen_control}")
    return choosen_control


def set_handysteuerung():
    choosen_control = "Handysteuerung"
    print(f"Gewählte Steuerung: {choosen_control}")
    return choosen_control


def set_tastatursteuerung():
    choosen_control = "Tastatursteuerung"
    print(f"Gewählte Steuerung: {choosen_control}")
    return choosen_control


def start_user_interface():

    window = tk.Tk()
    window.geometry("600x1080")

    # Load and set the background image
    image = Image.open("images/background.jpg")
    background_image = ImageTk.PhotoImage(image)
    background_label = tk.Label(window, image=background_image)
    background_label.place(relwidth=1, relheight=1)

    # Create a frame to hold the buttons and set its background to be transparent
    button_frame = tk.Frame(window, bg="blue", bd=10)
    button_frame.place(relx=0.5, rely=0.33, anchor="center")

    # Create buttons
    create_button(button_frame, "Gestenerkennung starten", set_gestenerkennung)
    create_button(button_frame, "Handysteuerung starten", set_handysteuerung)
    create_button(button_frame, "Tastatursteuerung starten", set_tastatursteuerung)
    window.mainloop()
