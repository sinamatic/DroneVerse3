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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    _, frame = cap.read()  # Lese ein Frame von der Kamera

    # Hintergrundbild laden und Größe anpassen
    background = cv2.imread("images/DSC01497.jpg")
    background = cv2.resize(background, (1920, 1080))

    # define rois
    height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right = define_rois(
        frame
    )

    # Zeichne die Regionen ein
    draw_rois(
        frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
    )

    running = True

    while running:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)

        # Hintergrundbild einfügen
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

                # draw skeleton in white
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(
                        color=(255, 255, 255), thickness=2, circle_radius=2
                    ),
                    mp_drawing.DrawingSpec(
                        color=(255, 255, 255), thickness=2, circle_radius=2
                    ),
                )
                direction_callback(direction)

        # Zeichne die erkannte Richtung auf dem Frame
        draw_direction_text(frame, direction)

        # Zeichne den Titel "DRONEVERSE" oben zentriert
        draw_title(frame, "DRONEVERSE")

        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)

        # quit program
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


def draw_direction_text(frame, direction):
    font = cv2.FONT_HERSHEY_PLAIN
    text = f"Direction: {direction}"
    font_scale = 2.0
    font_thickness = 6
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


def draw_title(frame, title):
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 3.0
    font_thickness = 8
    text_size = cv2.getTextSize(title, font, font_scale, font_thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2  # Zentriere horizontal
    text_y = text_size[1] + 20  # Oben mit etwas Abstand
    cv2.putText(
        frame,
        title,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        font_thickness,
        cv2.LINE_AA,
    )


def draw_rois(
    frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
):
    cv2.line(
        frame, (0, roi_top), (width, roi_top), (255, 255, 255), 2
    )  # Horizontale Linie oben
    cv2.line(
        frame, (0, roi_bottom), (width, roi_bottom), (255, 255, 255), 2
    )  # Horizontale Linie unten


def define_rois(frame):
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)
    return height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right


if __name__ == "__main__":
    # callback funktion, print hier wird überschrieben in main.py
    run_gesture_detection(lambda direction: print(f"gesturedetection.py {direction}"))
