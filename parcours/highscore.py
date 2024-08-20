import tkinter as tk
from tkinter import PhotoImage
import serial

# Serielle Verbindung zum Arduino herstellen
ser = serial.Serial("COM5", 9600)

# Hauptfenster erstellen
root = tk.Tk()
root.title("Droneverse Timer")

# Fenstergröße festlegen
root.geometry("1500x800")

# Bild laden
background_image = PhotoImage(file="bg_new.png")

# Label mit dem Bild erstellen und in das Fenster einfügen
label = tk.Label(root, image=background_image)
label.place(x=0, y=0, relwidth=1, relheight=1)

# Canvas erstellen und Hintergrundbild anzeigen
canvas = tk.Canvas(root, width=1400, height=700)
canvas.pack(fill=tk.BOTH, expand=True)  # Canvas auf die gesamte Fenstergröße ausdehnen

# Hintergrundbild auf das Canvas zeichnen
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Breite und Höhe des Rechtecks
rect_width = 400
rect_height = 100
corner_radius = 20  # Radius der abgerundeten Ecken

# Rechteck links im Fenster platzieren
rect_x_left = 100  # x-Koordinate der linken Seite des Rechtecks
rect_y_center = 400  # y-Koordinate des Zentrums des Rechtecks

# Die X-Koordinaten so anpassen, dass das Rechteck links ausgerichtet ist
rect_x0 = rect_x_left  # Linksseite des Rechtecks
rect_y0 = rect_y_center - rect_height // 2
rect_x1 = rect_x_left + rect_width
rect_y1 = rect_y_center + rect_height // 2


def create_rounded_rectangle(x0, y0, x1, y1, r, **kwargs):
    """Erzeugt ein abgerundetes Rechteck auf dem Canvas."""
    points = [
        x0 + r,
        y0,
        x0 + r,
        y0,
        x1 - r,
        y0,
        x1 - r,
        y0,
        x1,
        y0,
        x1,
        y0 + r,
        x1,
        y0 + r,
        x1,
        y1 - r,
        x1,
        y1 - r,
        x1,
        y1,
        x1 - r,
        y1,
        x1 - r,
        y1,
        x0 + r,
        y1,
        x0 + r,
        y1,
        x0,
        y1,
        x0,
        y1 - r,
        x0,
        y1 - r,
        x0,
        y0 + r,
        x0,
        y0 + r,
        x0,
        y0,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)


# Abgerundetes Rechteck zeichnen mit weißer Kontur und ohne Füllung
create_rounded_rectangle(
    rect_x0, rect_y0, rect_x1, rect_y1, corner_radius, outline="white", width=3, fill=""
)

# Text "Timer" links über dem Rechteck platzieren
text_x_left = rect_x0  # Direkt an der linken Kante des Rechtecks beginnen
text_y = rect_y0 - 10  # Abstand oberhalb des Rechtecks, abhängig von der Schriftgröße

# Text "Timer" in weißer Schrift ohne Hintergrund erstellen
canvas.create_text(
    text_x_left,
    text_y,
    text="Timer",
    anchor=tk.SW,
    font=("Helvetica", 30, "bold"),
    fill="white",
)

# Zeitlabel innerhalb des Rechtecks hinzufügen
time_label = canvas.create_text(
    (rect_x0 + rect_x1) // 2,
    (rect_y0 + rect_y1) // 2,
    text="00:00:00.000",
    font=("Helvetica", 40, "bold"),
    fill="#192632",
)

# Weiße Rechteck-Parameter
rect_x = 800  # x-Koordinate der oberen linken Ecke
rect_y = 350  # y-Koordinate der oberen linken Ecke
rect_width = 450  # Breite des Rechtecks
rect_height = 350  # Höhe des Rechtecks

# Weißes Rechteck auf dem Canvas erstellen
white_rectangle = canvas.create_rectangle(
    rect_x,
    rect_y,
    rect_x + rect_width,
    rect_y + rect_height,
    fill="white",  # Füllfarbe (weiß)
    outline="white",  # Randfarbe (weiß)
)


# Arduino Timer auslesen und aktualisieren
def read_from_arduino():
    if ser and ser.in_waiting > 0:
        try:
            line = ser.readline().decode("utf-8").rstrip()
            canvas.itemconfig(time_label, text=line)
        except:
            pass
    root.after(100, read_from_arduino)


# Text "Top 10 Spieler" links über dem Rechteck platzieren
text_x_left = rect_x0 + 698  # Direkt an der linken Kante des Rechtecks beginnen
text_y = rect_y0 - 10  # Abstand oberhalb des Rechtecks, abhängig von der Schriftgröße

# Text "Top 10 Spieler" in weißer Schrift ohne Hintergrund erstellen
canvas.create_text(
    text_x_left,
    text_y,
    text="Top 10 Player",
    anchor=tk.SW,
    font=("Helvetica", 30, "bold"),
    fill="white",
)

# Top 10 Spielerliste
top10_list = []


def update_top10():
    for widget in root.place_slaves():
        if isinstance(widget, tk.Label) and "Top 10 Player" not in widget.cget("text"):
            widget.destroy()
    top10_sorted = sorted(top10_list, key=lambda x: x[1])
    for i, (name, time) in enumerate(top10_sorted[:10]):
        y_pos = rect_y0 - 20 + (i + 1) * 33
        tk.Label(
            root,
            text=f"{i+1}. {name} {time}",
            font=("Helvetica", 20, "bold"),
            fg="#192632",
            bg="white",
        ).place(x=810, y=y_pos)


# Eingabefeld und Button für Spielernamen
name_var = tk.StringVar()
name_entry = tk.Entry(
    root, textvariable=name_var, font=("Helvetica", 20), fg="#192632", bd=0, bg="white"
)
name_entry.place(x=rect_x0 + 3, y=rect_y1 + 75, width=rect_width - 20, height=40)


def save_time():
    name = name_var.get()
    time_text = canvas.itemcget(time_label, "text")
    if name and time_text != "00:00:00.000":
        top10_list.append((name, time_text))
        update_top10()


# Position des Eingabefelds und des abgerundeten Rechtecks
entry_x = rect_x0
entry_y = rect_y1 + 150
entry_width = 400
entry_height = 40

# Text "Name" als Überschrift über dem Eingabefeld
label_name_x = entry_x + 5
label_name_y = entry_y - 100  # Oberhalb des abgerundeten Rechtecks

canvas.create_text(
    label_name_x,
    label_name_y,
    text="Name",
    anchor=tk.W,
    font=("Helvetica", 18, "bold"),
    fill="white",
)

# Button zum Speichern der Zeit
save_button = tk.Button(
    root,
    text=">",
    command=save_time,
    bg="white",
    fg="#192632",
    font=("Helvetica", 20, "bold"),
    relief="flat",
)
save_button.place(x=rect_x1 + 20, y=rect_y_center - 20, width=40, height=40)


# Funktion zum Starten des Timers
def start_timer():
    ser.write(b"s")  # Signal an Arduino senden, um die Messung zu starten
    canvas.itemconfig(time_label, text="00:00:00.000")  # Timer zurücksetzen


# Funktion zum Stoppen des Timers
def stop_timer():
    ser.write(b"p")  # Signal an Arduino senden, um die Messung sofort abzubrechen


# Funktion zum Zurücksetzen der Zeit
def reset_timer():
    canvas.itemconfig(time_label, text="00:00:00.000")


# Buttons erstellen
start_button = tk.Button(
    root,
    text="Start",
    command=start_timer,
    bg="#65a32f",
    fg="#192632",
    font=("Helvetica", 20, "bold"),
    relief="flat",
)
start_button.place(x=rect_x1 - 400, y=rect_y_center + 200, width=80, height=40)

stop_button = tk.Button(
    root,
    text="Stop",
    command=stop_timer,
    bg="#bf4113",
    fg="#192632",
    font=("Helvetica", 20, "bold"),
    relief="flat",
)
stop_button.place(x=rect_x1 - 300, y=rect_y_center + 200, width=80, height=40)

reset_button = tk.Button(
    root,
    text="Reset",
    command=reset_timer,
    bg="#12a0e8",
    fg="#192632",
    font=("Helvetica", 20, "bold"),
    relief="flat",
)
reset_button.place(x=rect_x1 - 200, y=rect_y_center + 200, width=80, height=40)

# Automatische Updates starten
read_from_arduino()

# Hauptschleife starten
root.mainloop()
