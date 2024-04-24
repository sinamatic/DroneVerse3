import cv2
import mediapipe as mp

# Initialisiere Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


# Hauptfunktion zum Abrufen des Webcambildes und zur Erkennung der Handposition
def main():
    cap = cv2.VideoCapture(0)  # Öffne die Kamera
    _, frame = cap.read()  # Lese ein Frame von der Kamera
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)

    while True:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)

        # Überprüfe, ob der Zeigefinger in der oberen, unteren oder mittleren Region liegt
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]
                finger_y = int(index_finger_tip.y * height)
                finger_x = int(index_finger_tip.x * width)

                if finger_y < roi_top:
                    print("Oben")
                elif finger_y > roi_bottom:
                    print("Unten")
                elif roi_middle_left < finger_x < roi_middle_right:
                    print("Mitte")
                else:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    if index_finger_tip.x < thumb_tip.x:
                        print("Rechts")
                    elif index_finger_tip.x > thumb_tip.x:
                        print("Links")
                    else:
                        print("Hand ist nicht ausgerichtet")

        cv2.rectangle(frame, (0, 0), (width, roi_top), (255, 0, 0), 2)
        cv2.rectangle(frame, (0, roi_bottom), (width, height), (255, 0, 0), 2)
        cv2.rectangle(
            frame,
            (roi_middle_left, roi_top),
            (roi_middle_right, roi_bottom),
            (0, 255, 0),
            2,
        )

        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        if cv2.waitKey(1) & 0xFF == ord(
            "q"
        ):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
