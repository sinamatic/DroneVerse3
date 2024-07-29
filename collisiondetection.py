# Lisa Berbig
# Stand 29-07-2024
"""
Dieses Programm dient dazu zu verhindern, dass eine Drohne über einen bestimmten Bereich hinausfliegt.
Dafür wird das Bild einer 360° Kamera zu einem 180° Bild verarbeitet. Daraus wird ein binäres Differenzbild erstellt, in welchem weiße Pixel in den Randbereichen erkannt werden.
"""
import numpy as np
import cv2


def _init_(self):
    self.shape = None
    print()


def crop_sides(image, crop_fraction):
    height, width = image.shape[:2]

    # Berechne den Start- und Endpunkt für das Zuschneiden
    crop_width = int(width * crop_fraction)
    start_x = crop_width
    end_x = width - crop_width
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def run_collission_detection(collission_callback):
    collission = False
    # Definiere den Randbereich in px
    margin_size = 10
    cap = cv2.VideoCapture(0)
    old_frame = None

    while True:
        ret, frame = cap.read()
        cropped_frame = crop_sides(frame, 0.25)

        if ret:
            gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)

            if old_frame is not None:
                diff = cv2.absdiff(old_frame, gray)
                _, bin_diff = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
                cv2.imshow("diff_frame", bin_diff)

                # Extrahiere die Randbereiche
                top_margin = bin_diff[:margin_size, :]
                bottom_margin = bin_diff[-margin_size:, :]
                left_margin = bin_diff[:, :margin_size]
                right_margin = bin_diff[:, -margin_size:]

                # Überprüfe, ob in den Randbereichen weiße Pixel (255) vorhanden sind
                top_has_white = np.any(top_margin == 255)
                bottom_has_white = np.any(bottom_margin == 255)
                left_has_white = np.any(left_margin == 255)
                right_has_white = np.any(right_margin == 255)

                # Ausgabe der Ergebnisse
                if top_has_white:
                    print("Gefahrbereich vorne")
                    collission = "forward"

                if bottom_has_white:
                    print("Gefahrbereich hinten")
                    collission = "backward"

                if left_has_white:
                    print("Gefahrbereich links")
                    collission = "left"

                if right_has_white:
                    print("Gefahrbereich rechts")
                    collission = "right"

                if not (
                    top_has_white
                    or bottom_has_white
                    or left_has_white
                    or right_has_white
                ):
                    print("Sicherer Bereich")

                collission_callback(collission)

            old_frame = gray

            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        else:
            print("ERROR!")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # callback funktion, print hier wird überschrieben in main.py
    run_collission_detection(
        lambda collission: print(f"collissiondetection.py {collission}")
    )
