import cv2
import mediapipe as mp

import gesturedetection_mp_roi
import dronecontrol


# Initialisiere Mediapipe einmalig
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)


def main():
    webcam = cv2.VideoCapture(0)

    while True:
        # Video Setup
        success, image = webcam.read()  # Camera Update
        if not success:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break
        image_flipped = cv2.flip(image, 1)  # Horizontal spiegeln

        # Gesture Detection
        gesture_directions = [
            "up",
            "down",
            "left",
            "right",
            "forward",
            "backward",
            "none",
        ]
        detected_gesture = gesturedetection_mp_roi.start_roibased_gesture_detection(
            image_flipped, gesture_directions, hands, mp_hands
        )

        # Drone Control
        if detected_gesture == "up":
            dronecontrol.drone_up()
        elif detected_gesture == "down":
            dronecontrol.drone_down()
        elif detected_gesture == "left":
            dronecontrol.drone_left()
        elif detected_gesture == "right":
            dronecontrol.drone_right()
        elif detected_gesture == "forward":
            dronecontrol.drone_forward()
        elif detected_gesture == "backward":
            dronecontrol.drone_backward()

        # show updated video
        # cv2.imshow("image", image)

        # Quit program
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

        cv2.imshow("image", image_flipped)

    webcam.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
