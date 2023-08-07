import cv2
import numpy as np
import json
import find_key_position
import utils


def process_video(video_path, note_template_path, threshold, scales, target_pixel, start_form=1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    spf = 1 / fps
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    note_brightness_history = []  # Track the history of detected note positions
    diff_per_frame = []

    note_positions = find_key_position.cv2_loop_through(video_path, note_template_path, threshold,
                                                        scales, start_form)
    f_count = 0
    while f_count < start_form and cap.isOpened():
        cap.read()
        f_count += 1

    while cap.isOpened():
        f_count += 1
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        frame_scaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # collect brightness
        current_note_brightness = []

        for idx, position in enumerate(note_positions):
            pt1 = (position[0], position[1])

            # Calculate the displacement from the top-left corner of the bounding box
            x_dis = target_pixel[0]
            y_dis = target_pixel[1]
            displacement_point = (pt1[0] + int(x_dis * position[4]), pt1[1] + int(y_dis * position[4]))

            # Record the brightness at the displacement point
            brightness = int(frame_scaled[displacement_point[1], displacement_point[0]])
            current_note_brightness.append(brightness)

            cv2.putText(frame, str(idx), (pt1[0], pt1[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Draw a small circle at the displacement point (for visualization)
            cv2.circle(frame, displacement_point, 2, (0, 0, 255), -1)

        current_diff_per_frame = []

        # note press == decrease in brightness
        current_note_brightness = [max(current_note_brightness) - i for i in current_note_brightness]

        # Draw bounding boxes around the detected keys (for visualization)
        for idx, position in enumerate(note_positions):
            pt1 = (position[0], position[1])
            pt2 = (position[0] + position[2], position[1] + position[3])
            if note_brightness_history and idx < len(note_brightness_history):
                diff = current_note_brightness[idx] - note_brightness_history[-1][idx]
                current_diff_per_frame.append(diff)
                if note_brightness_history and diff > 15:
                    cv2.rectangle(frame, pt1, pt2, (255, 255, 0), 2)
                elif note_brightness_history and diff < 0:
                    cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 2)
                else:
                    cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)
            else:
                cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

        note_brightness_history.append(current_note_brightness)
        diff_per_frame.append(current_diff_per_frame)

        # resize incase video too big
        resized_frame = utils.cv2_resize_to_fit(frame)

        # fancy stats
        top_left = (200, 200)  # (note_positions[14][0], max(0, note_positions[14][1] - 100))
        message = "Frame:{:>7}/{}\nProgress:{:>7.2f}%\nTime passed:{:>7.2f}s".format(
            f_count, total_frames,
            round(f_count / total_frames * 100, 2),
            round(f_count * spf, 2),
        )
        utils.cv2_print_texts(resized_frame, message, top_left,
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), (200, 200, 200), 1)
        cv2.imshow(f'Processing Frame (resized) [{video_path}]', resized_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return diff_per_frame


def default_configs():
    note_template_path = 'assets/templates/first_note.png'
    threshold = 0.955
    scales = np.linspace(0.5, 1.2, num=8)
    target_pixel = (23, 55)  # displacement from the top-left corner of the bounding box

    return locals()


def backup_configs():
    note_template_path = 'assets/templates/first_note.png'
    threshold = 0.92
    scales = np.linspace(0.7, 1.2, num=6)
    target_pixel = (23, 53)  # displacement from the top-left corner of the bounding box

    return locals()


def main():
    video_path = 'assets/test_videos/cage.mp4'

    diff_per_frame = process_video(video_path, **default_configs(), start_form=90)
    with open('data\\diff_per_frame.json', 'w+') as json_file:
        json.dump(diff_per_frame, json_file)


if __name__ == '__main__':
    main()
