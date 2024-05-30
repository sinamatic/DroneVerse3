import cv2
import mediapipe as mp


def beispielfunktion1():
    print("Dies ist die Beispielfunktion 1 aus Modul 1.")


def beispielfunktion2():
    print("Dies ist die Beispielfunktion 2 aus Modul 1.")

    ###
    ### ROIs
    ###


def draw_rois(frame_flipped, roi_top, roi_bottom, roi_middle_left, roi_middle_right):

    height, width, _ = frame_flipped.shape
    cv2.rectangle(
        frame_flipped,
        (roi_middle_left, roi_top),
        (roi_middle_right, roi_bottom),
        (0, 255, 0),
        2,
    )
    cv2.rectangle(frame_flipped, (0, 0), (width, roi_top), (255, 0, 0), 2)
    cv2.rectangle(frame_flipped, (0, roi_bottom), (width, height), (255, 0, 0), 2)


def start_roibased_gesture_detection(frame_flipped, gesture_direction, hands, mp_hands):

    # Define top and bottom Rois
    height, width, _ = frame_flipped.shape
    roi_top = int(height / 4)
    roi_bottom = int(3 * height / 4)
    roi_middle_left = int(width / 4)
    roi_middle_right = int(3 * width / 4)

    results = hands.process(frame_flipped)

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
                gesture_direction = 1

            # Finger unten
            elif finger_y > roi_bottom:
                gesture_direction = 2

            else:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                # Finger rechts
                if index_finger_tip.x < thumb_tip.x:
                    gesture_direction = 3

                # Finger links
                elif index_finger_tip.x > thumb_tip.x:
                    gesture_direction = 4

                # Kein Finger
                else:
                    gesture_direction = 5
    print_gesture_direction(gesture_direction)
    return gesture_direction


def print_gesture_direction(gesture_direction):
    if gesture_direction == 1:
        print("Finger oben")
    elif gesture_direction == 2:
        print("Finger unten")
    elif gesture_direction == 3:
        print("Finger rechts")
    elif gesture_direction == 4:
        print("Finger links")
    elif gesture_direction == 5:
        print("Kein Finger")
