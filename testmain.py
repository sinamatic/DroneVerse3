import cv2
import mediapipe as mp

import gesturedetection_mp_roi
import dronecontrol

# Aufruf von Funktionen aus Modul 1
gesturedetection_mp_roi.beispielfunktion1()
gesturedetection_mp_roi.beispielfunktion2()

# Aufruf von Funktionen aus Modul 2
dronecontrol.beispielfunktion3()
dronecontrol.beispielfunktion4()

# Initialisiere Mediapipe einmalig
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)


def main():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()  # Camera initial setup
    gesture_direction = -1
    # gesturedetection_mp_roi.draw_rois(frame)

    while True:
        # Video Setup
        ret, frame = cap.read()  # Camera Update
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break
        frame_flipped = cv2.flip(frame, 1)  # Horizontal spiegeln

        # Gesture Detection
        gesturedetection_mp_roi.start_roibased_gesture_detection(
            frame_flipped, gesture_direction, hands, mp_hands
        )

        # Drone Control

        # show updated video
        # cv2.imshow("Frame", frame)

        # Quit program
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

        cv2.imshow("Frame", frame_flipped)

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
