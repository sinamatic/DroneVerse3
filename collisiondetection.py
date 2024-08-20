# Author: Lisa Berbig

import numpy as np
import cv2
import sendCollision

collision_status = {"forward": False, "backward": False, "left": False, "right": False}


def crop_sides(image, crop_fraction):
    height, width = image.shape[:2]
    crop_width = int(width * crop_fraction)
    start_x = crop_width
    end_x = width - crop_width
    cropped_image = image[:, start_x:end_x]
    return cropped_image


def crop_image(image, crop_height, crop_width):
    height, width = image.shape[:2]

    start_y = (height - crop_height) // 2
    end_y = start_y + crop_height
    start_x = (width - crop_width) // 2
    end_x = start_x + crop_width

    cropped_image = image[start_y:end_y, start_x:end_x]
    return cropped_image


def run_collision_detection():
    # Randbereich in px
    margin_size = 100

    cap = cv2.VideoCapture(0)
    old_frame = None

    while True:
        ret, frame = cap.read()
        cropped_frame = crop_sides(frame, 0.25)
        cropped = crop_image(cropped_frame, 700, 600)

        if ret:
            gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

            if old_frame is not None:
                diff = cv2.absdiff(old_frame, gray)
                _, bin_diff = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
                cv2.imshow("diff_frame", bin_diff)

                top_margin = bin_diff[:margin_size, :]
                bottom_margin = bin_diff[-margin_size:, :]
                left_margin = bin_diff[:, :margin_size]
                right_margin = bin_diff[:, -margin_size:]

                top_has_white = np.any(top_margin == 255)
                bottom_has_white = np.any(bottom_margin == 255)
                left_has_white = np.any(left_margin == 255)
                right_has_white = np.any(right_margin == 255)

                if top_has_white:
                    print("Gefahrbereich vorne")
                    sendCollision.run_send_collsion("forward")

                elif bottom_has_white:
                    print("Gefahrbereich hinten")
                    sendCollision.run_send_collsion("backward")

                elif left_has_white:
                    print("Gefahrbereich links")
                    sendCollision.run_send_collsion("left")

                elif right_has_white:
                    print("Gefahrbereich rechts")
                    sendCollision.run_send_collsion("right")

                elif not (
                    top_has_white
                    or bottom_has_white
                    or left_has_white
                    or right_has_white
                ):
                    print("Sicherer Bereich")

            old_frame = gray

            if cv2.waitKey(30) & 0xFF == ord("q"):
                break
        else:
            print("ERROR!")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "_main_":
    run_collision_detection()
