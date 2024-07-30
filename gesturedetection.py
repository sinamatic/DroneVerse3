import cv2
import mediapipe as mp
import math

# Initialisiere Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # Hand skeleton
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


# Hauptfunktion zum Abrufen des Webcambildes und zur Erkennung der Handposition
def run_gesture_detection(direction_callback):
    cap = cv2.VideoCapture(0)  # Öffne die Kamera
    _, frame = cap.read()  # Lese ein Frame von der Kamera
    cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)  # Erstelle ein Fenster
    cv2.setWindowProperty(
        "Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN
    )  # Setze es auf Vollbild

    # define rois
    height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right = define_rois(
        frame
    )

    background = cv2.imread("images/DSC01497_Gestures.jpg")

    running = True

    while running:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)
        frame = background.copy()

        direction = "stop"

        # Überprüfe, ob der Zeigefinger in der oberen, unteren oder mittleren Region liegt
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Spiegeln der x-Koordinaten der Landmarks, damit Skelett richtigrum ist
                for landmark in hand_landmarks.landmark:
                    landmark.x = 1.0 - landmark.x

                index_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]

                finger_y = int(index_finger_tip.y * height)

                # Finger oben
                if finger_y < roi_top:
                    direction = "up"

                # Finger unten
                elif finger_y > roi_bottom:
                    direction = "down"

                else:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    # Schwellwerte definieren
                    treshold_backward = 0.06
                    treshold_forward = 0.2

                    # Berechne die Distanz zwischen Daumen und Zeigefinger
                    distance = math.sqrt(
                        (index_finger_tip.x - thumb_tip.x) ** 2
                        + (index_finger_tip.y - thumb_tip.y) ** 2
                    )

                    if distance < treshold_backward:
                        direction = "backward"
                    elif distance > treshold_forward:
                        direction = "forward"
                    else:
                        if index_finger_tip.x < thumb_tip.x:
                            direction = "left"
                        elif index_finger_tip.x > thumb_tip.x:
                            direction = "right"
                        else:
                            direction = "stop"

                # draw skeleton
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                direction_callback(direction)

        # Zeichne die erkannte Richtung auf dem Frame
        draw_direction_text(frame, direction)

        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)

        # quit program
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


def draw_direction_text(frame, direction):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"{direction}"
    font_scale = 3
    font_thickness = 5
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2  # Zentriere horizontal
    text_y = (frame.shape[0] + text_size[1]) // 2  # Zentriere vertikal
    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        cv2.LINE_AA,
    )


def define_rois(frame):
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)
    return height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right


def draw_rois(
    frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
):
    pass


if __name__ == "__main__":
    # callback funktion, print hier wird überschrieben in main.py
    run_gesture_detection(lambda direction: print(f"gesturedetection.py {direction}"))
