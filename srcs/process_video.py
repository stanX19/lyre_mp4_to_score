import os.path
import cv2
import numpy as np
import json
import time
from . import find_key_position
from . import utils
from . import Path
from .mp4_to_lyre_types import *


def process_video(video_path: str, note_template_path: str, threshold: float, scales: list[float],
                  target_pixel_displacement: tuple[int, int], start_form_frame=1
                  ) -> tuple[float, DpfType]:
    """
    Converts lyre video into dpf data
    :param video_path: path of lyre video
    :param note_template_path: path to png file
    :param threshold: min threshold for note_template matching
    :param scales: scales for template size to be resized
    :param target_pixel_displacement: from top left corner
    :param start_form_frame:
    :return: fps and diff_per_frame
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    note_brightness_history = []  # Track the history of detected note positions
    diff_per_frame = []

    if start_form_frame >= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
        raise ValueError("process video: Start frame > total frame in video")
    note_positions = find_key_position.cv2_loop_through(video_path, note_template_path, threshold,
                                                        scales, start_form_frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_form_frame)
    f_count = start_form_frame

    start_time = time.time()
    while cap.isOpened():
        f_count += 1
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        frame = cv2.resize(frame, (1920, 1080))
        frame_scaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # collect brightness
        current_note_brightness = []

        for idx, position in enumerate(note_positions):
            pt1 = (position[0], position[1])

            # Calculate the displacement from the top-left corner of the bounding box
            x_dis = target_pixel_displacement[0]
            y_dis = target_pixel_displacement[1]
            displacement_point = (pt1[0] + int(x_dis * position[4]), pt1[1] + int(y_dis * position[4]))

            # Record the brightness at the displacement point
            brightness = int(frame_scaled[displacement_point[1], displacement_point[0]])
            current_note_brightness.append(brightness)

            cv2.putText(frame, str(idx), (pt1[0], pt1[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Draw a small circle at the displacement point (for visualization)
            cv2.circle(frame, displacement_point, 2, (0, 0, 255), -1)

        current_diff_per_frame = [0] * 21

        # note press == decrease in brightness
        current_note_brightness = [max(current_note_brightness) - i for i in current_note_brightness]

        # Draw bounding boxes around the detected keys (for visualization)
        for idx, position in enumerate(note_positions):
            box_color = (0, 255, 0)
            pt1 = (position[0], position[1])
            pt2 = (position[0] + position[2], position[1] + position[3])
            if note_brightness_history:
                diff = current_note_brightness[idx] - note_brightness_history[-1][idx]
                current_diff_per_frame[idx] = diff

                if note_brightness_history and diff > 15:
                    box_color = (255, 255, 0)
                elif note_brightness_history and diff < 0:
                    box_color = (0, 0, 255)
            cv2.rectangle(frame, pt1, pt2, box_color, 2)

        note_brightness_history.append(current_note_brightness)
        diff_per_frame.append(current_diff_per_frame)

        # resize incase video too big
        resized_frame = utils.cv2_resize_to_fit(frame)

        # fancy stats
        top_left = (200, 200)  # (note_positions[14][0], max(0, note_positions[14][1] - 100))

        current_time = time.time()
        time_elapsed = current_time - start_time

        average_time_per_frame = time_elapsed / f_count

        # Calculate the estimated time remaining
        frames_remaining = total_frames - f_count
        estimated_time_remaining = frames_remaining * average_time_per_frame

        if estimated_time_remaining >= 60:
            minutes_remaining = int(estimated_time_remaining // 60)
            seconds_remaining = int(estimated_time_remaining % 60)
            time_remaining_str = "{:02d}:{:02d}".format(minutes_remaining, seconds_remaining)
        else:
            time_remaining_str = "{:.2f}s".format(estimated_time_remaining)

        message = "Frame:{:>7}/{}\nProgress:{:>7.2f}%\nEstimated Time Remaining: {}".format(
            f_count, total_frames,
            round(f_count / total_frames * 100, 2),
            time_remaining_str
        )
        utils.cv2_print_texts(resized_frame, message, top_left,
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), (200, 200, 200), 1)
        cv2.imshow(f'Processing Frame (resized) [{video_path}]', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return fps, diff_per_frame


def default_configs():
    note_template_path = Path.first_note
    threshold = 0.8
    scales = [1.0, 1.2, 1.1, 0.9, 0.8, 0.7, 0.6, 0.5]
    target_pixel_displacement = (23, 55)  # displacement from the top-left corner of the bounding box

    return locals()


def backup_configs():
    note_template_path = Path.first_note
    threshold = 0.92
    scales = np.linspace(0.7, 1.2, num=6)
    target_pixel_displacement = (23, 53)  # displacement from the top-left corner of the bounding box

    return locals()


def main():
    video_path = os.path.join(Path.assets, "test_videos/floral_breeze.mp4")  # 'assets/test_videos/cage.mp4'

    diff_per_frame_data = process_video(video_path, **default_configs(), start_form_frame=1)
    with open('data\\diff_per_frame.json', 'w+') as json_file:
        json.dump(diff_per_frame_data, json_file)


if __name__ == '__main__':
    main()
