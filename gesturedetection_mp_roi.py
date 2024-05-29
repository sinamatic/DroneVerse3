import cv2
import mediapipe as mp


def beispielfunktion1():
    print("Dies ist die Beispielfunktion 1 aus Modul 1.")


def beispielfunktion2():
    print("Dies ist die Beispielfunktion 2 aus Modul 1.")


###
### ROIs
###


def start_gesture_detection(frame, frame_rgb):

    # Define Rois
    height, width, _ = frame.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)

    # Draw Rois
    cv2.rectangle(
        frame,
        (roi_middle_left, roi_top),
        (roi_middle_right, roi_bottom),
        (0, 255, 0),
        2,
    )
    cv2.rectangle(frame, (0, 0), (width, roi_top), (255, 0, 0), 2)
    cv2.rectangle(frame, (0, roi_bottom), (width, height), (255, 0, 0), 2)

    # Initialisiere Mediapipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

    results = hands.process(frame_rgb)

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
