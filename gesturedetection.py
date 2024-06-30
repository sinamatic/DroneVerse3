import cv2
import mediapipe as mp

# Initialisiere Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # Hand skeleton
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


def run_gesture_detection(direction_callback):
    cap = cv2.VideoCapture(0)  # Öffne die Kamera

    while True:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break

        height, width, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)

        # Überprüfe, ob der Zeigefinger in der oberen, unteren, rechten oder linken Region liegt
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Spiegeln der x-Koordinaten der Landmarks
                for landmark in hand_landmarks.landmark:
                    landmark.x = 1.0 - landmark.x

                # Variablen für die Fingerspitzen
                index_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]
                middle_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.MIDDLE_FINGER_TIP
                ]
                ring_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.RING_FINGER_TIP
                ]
                pinky_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.PINKY_TIP
                ]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Richtungsvariable initialisieren
                direction = None

                # Erkennung der Richtung anhand der Zeigefingerposition
                if (
                    index_finger_tip.x < thumb_tip.x - 0.1
                ):  # Prüfung für rechts (Offset für Toleranz)
                    direction = "right"
                elif (
                    index_finger_tip.x > thumb_tip.x + 0.1
                ):  # Prüfung für links (Offset für Toleranz)
                    direction = "left"

                if (
                    index_finger_tip.y < thumb_tip.y - 0.1
                ):  # Prüfung für oben (Offset für Toleranz)
                    direction = "up"
                elif (
                    index_finger_tip.y > thumb_tip.y + 0.1
                ):  # Prüfung für unten (Offset für Toleranz)
                    direction = "down"

                # Output der Richtung
                if direction:
                    print(f"Direction: {direction}")

                # Erkennung basierend auf Fingerposition (ROIs)
                """
                finger_x = int(index_finger_tip.x * width)
                finger_y = int(index_finger_tip.y * height)

                if finger_y < height * 0.25:
                    direction = "up"
                elif finger_y > height * 0.75:
                    direction = "down"
                elif finger_x < thumb_tip.x * width:
                    direction = "right"
                elif finger_x > thumb_tip.x * width:
                    direction = "left"
                else:
                    direction = "none"
                """
                # draw skeleton
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                direction_callback(direction)

        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)

        # quit program
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

        # drone start
        if key & 0xFF == ord("s"):  # Wenn 's' gedrückt wird, gib "s gedrückt" aus
            print("drone takeoff …")

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


# Beispiel-Callback-Funktion
def direction_callback(direction):
    print("Richtung:", direction)


# Starte die Gestenerkennung
run_gesture_detection(direction_callback)

# if __name__ == "__main__":
# callback funktion, print hier wird überschrieben in main.py
#  run_gesture_detection(lambda direction: print(f"gesturedetection.py {direction}"))
