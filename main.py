import cv2
import mediapipe as mp
from djitellopy import Tello

# Initialisiere Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


# Funktion zur Initialisierung der Drohne
def initialize_drone():
    drone = Tello()
    print("Drone initialized.")
    drone.connect()
    print("Drone connected.")
    drone.streamoff()
    drone.streamon()
    return drone


# Hauptfunktion zum Abrufen des Webcambildes und zur Erkennung der Handposition
def main():
    # reset drone position
    drone_x_direction = 0
    drone_y_direction = 0
    z_direction = 0
    drone_start_land = 0

    # testing boolean
    test_with_drone = False

    if test_with_drone:
        drone = initialize_drone()
        print("Drone initialized.")

    cap = cv2.VideoCapture(0)  # Öffne die Kamera
    _, frame = cap.read()  # Lese ein Frame von der Kamera

    # define rois
    height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right = define_rois(
        frame
    )

    while True:
        ret, frame = cap.read()  # Lese ein Frame von der Kamera
        if not ret:
            print("Fehler beim Abrufen des Bildes von der Kamera")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)  # Horizontal spiegeln
        results = hands.process(frame_rgb)

        # Zeichne die Regionen ein
        draw_rois(
            frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
        )

        # Überprüfe, ob der Zeigefinger in der oberen, unteren oder mittleren Region liegt
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[
                    mp_hands.HandLandmark.INDEX_FINGER_TIP
                ]
                finger_y = int(index_finger_tip.y * height)
                # finger_x = int(index_finger_tip.x * width)

                # Finger oben
                if finger_y < roi_top:
                    # drone_y_direction = drone_y_direction + 1
                    drone_y_direction = 1
                    print("Up \t Y-Direction: {}".format(drone_y_direction))

                # Finger unten
                elif finger_y > roi_bottom:
                    drone_y_direction = -1
                    print("Down \t Y-Direction: {}".format(drone_y_direction))

                else:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    # Finger rechts
                    if index_finger_tip.x < thumb_tip.x:
                        drone_x_direction = 1
                        print("Right \t X-Direction: {}".format(drone_x_direction))

                    # Finger links
                    elif index_finger_tip.x > thumb_tip.x:
                        drone_x_direction = -1
                        print("Left \t X-Direction: {}".format(drone_x_direction))

                    # Kein Finger
                    else:
                        print("Hand ist nicht ausgerichtet")

                # Drohnensteuerung
                if test_with_drone:
                    drone_control(
                        drone, drone_x_direction, drone_y_direction, drone_start_land
                    )

        cv2.imshow("Frame", frame)  # Zeige das Frame mit OpenCV an
        key = cv2.waitKey(1)  # Warte auf eine Tastatureingabe (1 ms Timeout)

        # quit program
        if key & 0xFF == ord("q"):  # Beende die Schleife, wenn 'q' gedrückt wird
            break

        # drone start
        elif key & 0xFF == ord("s"):  # Wenn 's' gedrückt wird, gib "s gedrückt" aus
            drone_start_land = 1
            print("s: Drone start \t")

        # drone land
        elif key & 0xFF == ord("l"):  # Wenn 's' gedrückt wird, gib "s gedrückt" aus
            drone_start_land = -1
            print("l: Drone land \t")

    cap.release()  # Gib die Ressourcen frei
    cv2.destroyAllWindows()


def drone_control(drone, drone_x_direction, drone_y_direction, drone_start_land):
    if drone_y_direction > 0:
        drone.move_up(1)
        print("Up")
    elif drone_y_direction < 0:
        drone.move_down(1)
        print("Down")
    elif drone_x_direction > 0:
        drone.move_right(1)
        print("Right")
    elif drone_x_direction < 0:
        drone.move_left(1)
        print("Left")
    elif drone_start_land < 0:
        drone.land()
        print("Landing … ")
    elif drone_start_land > 1:
        drone.takeoff()
        print("Takeoff …")


def draw_rois(
    frame, height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right
):
    cv2.rectangle(
        frame,
        (roi_middle_left, roi_top),
        (roi_middle_right, roi_bottom),
        (0, 255, 0),
        2,
    )
    cv2.rectangle(frame, (0, 0), (width, roi_top), (255, 0, 0), 2)
    cv2.rectangle(frame, (0, roi_bottom), (width, height), (255, 0, 0), 2)


def define_rois(frame):
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)
    return height, width, roi_top, roi_bottom, roi_middle_left, roi_middle_right


if __name__ == "__main__":
    main()
