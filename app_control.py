import tkinter as tk


class ControlApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1920x1080")
        self.root.configure(bg="black")
        self.choosen_control = None

        # Create buttons
        self.create_button("Gestenerkennung starten", self.set_gestenerkennung)
        self.create_button("Handysteuerung starten", self.set_handysteuerung)
        self.create_button("Tastatursteuerung starten", self.set_tastatursteuerung)

    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command, bg="white")
        button.pack(pady=20)

    def set_gestenerkennung(self):
        self.choosen_control = "Gestenerkennung"
        print(f"Gewählte Steuerung: {self.choosen_control}")

    def set_handysteuerung(self):
        self.choosen_control = "Handysteuerung"
        print(f"Gewählte Steuerung: {self.choosen_control}")

    def set_tastatursteuerung(self):
        self.choosen_control = "Tastatursteuerung"
        print(f"Gewählte Steuerung: {self.choosen_control}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ControlApp(root)
    root.mainloop()
