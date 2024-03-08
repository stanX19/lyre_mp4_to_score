import os.path
import cv2
import numpy as np
from srcs.deduce_key_pos import deduce_all_key_pos
from srcs import utils
from srcs import Path


def remove_dupes(positions: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    key_positions = []

    for pt in positions:
        # Calculate the width and height of each grid cell
        cell_width = pt[2]
        cell_height = pt[3]

        # Calculate the coordinates of the matched key position
        key_x = pt[0]
        key_y = pt[1]

        # Check if the key position is already detected
        for existing_position in key_positions:
            # Compare the cell position and distance from existing detections
            if (abs(key_x - existing_position[0]) <= cell_width and
                    abs(key_y - existing_position[1]) <= cell_height):
                break
        else:  # if not is_duplicate:
            key_positions.append(pt)

    return key_positions


def cv2_match_key(frame_gray: np.ndarray, template_gray: np.ndarray,
                  threshold: float, scales: list[float]) -> list[list[int]]:
    key_positions = []

    for scale in scales:
        template_resized = cv2.resize(template_gray, (int(template_gray.shape[1] * scale),
                                                      int(template_gray.shape[0] * scale)))
        result = cv2.matchTemplate(frame_gray, template_resized, cv2.TM_CCORR_NORMED)
        loc = np.where(result >= threshold)

        # Process the matching locations
        for pt in zip(*loc[::-1]):
            # Calculate the width and height of each grid cell
            cell_width = template_resized.shape[1]
            cell_height = template_resized.shape[0]

            # Calculate the coordinates of the matched key position
            key_x = pt[0]
            key_y = pt[1]

            # Check if the key position is already detected
            for existing_position in key_positions:
                # Compare the cell position and distance from existing detections
                if (abs(key_x - existing_position[0]) <= cell_width and
                        abs(key_y - existing_position[1]) <= cell_height):
                    break
            else:  # if not is_duplicate:
                key_positions.append([key_x, key_y, cell_width, cell_height, scale])

        if len(key_positions) >= 21:
            break

    return key_positions


def cv2_loop_through(video_path: str, note_template_path: str, threshold: float,
                     scales: list[float], start_form=1) -> list[tuple[int, int, int, int]]:
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    first_note_template = cv2.imread(note_template_path)  # , cv2.IMREAD_GRAYSCALE)
    template_scaled = cv2.cvtColor(first_note_template, cv2.COLOR_BGR2GRAY)
    note_positions = []

    # Binary search pattern
    start_gap = total_frames // 2
    scanned_frames = set()  # Keep track of scanned frames

    while start_gap >= 1:
        f_count = start_form

        while cap.isOpened() and f_count <= total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_count)
            if f_count not in scanned_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert the frame to grayscale
                frame_scaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                note_positions += cv2_match_key(frame_scaled, template_scaled, threshold, scales)
                note_positions = remove_dupes(note_positions)

                height, width, _ = frame.shape
                deduced_note_positions = deduce_all_key_pos(note_positions, width, height)

                if len(deduced_note_positions) != 21:
                    if note_positions:
                        for idx, position in enumerate(note_positions):
                            pt1 = (position[0], position[1])
                            pt2 = (position[0] + position[2], position[1] + position[3])
                            cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

                    # for position in [[405, 658], [405, 793], [405, 929]]:
                    #     pt1 = (position[0], position[1])
                    #     pt2 = (position[0] + 5, position[1] + 5)
                    #     cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)

                    # resize for display
                    resized_frame = utils.cv2_resize_to_fit(frame)

                    # fancy stats
                    top_left = (200, 200)  # (note_positions[14][0], max(0, note_positions[14][1] - 100))
                    message = "Frame: {:<10} [Locating Keys]\nFrames scanned:{:>7.2f}% {:>7}/{})".format(
                        f_count,
                        round(len(scanned_frames) / total_frames * 100, 2), f"({len(scanned_frames)}", total_frames
                    )
                    utils.cv2_print_texts(resized_frame, message, top_left,
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), (200, 200, 200), 1)
                    cv2.imshow('Locating Keys (resized)', resized_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    cap.release()
                    cv2.destroyAllWindows()
                    return deduced_note_positions

                scanned_frames.add(f_count)  # Mark frame as scanned
            f_count += start_gap

        # Reduce the gap for the next iteration
        start_gap //= 2

    raise RuntimeError("mp4 to lyre: Failed to locate keys")


# def cv2_loop_through0(video_path, note_template_path, threshold, scales, start_form=1):
#     cap = cv2.VideoCapture(video_path)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#
#     first_note_template = cv2.imread(note_template_path)  # , cv2.IMREAD_GRAYSCALE)
#     template_scaled = cv2.cvtColor(first_note_template, cv2.COLOR_BGR2GRAY)
#     note_positions = []
#
#     f_count = 0
#     while f_count + 1 < start_form and cap.isOpened():
#         cap.read()
#         f_count += 1
#     while cap.isOpened():
#         f_count += 1
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         # Convert the frame to grayscale
#         frame_scaled = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         note_positions += cv2_match_key(frame_scaled, template_scaled, threshold, scales)
#         note_positions = remove_dupes(note_positions)
#
#         height, width, _ = frame.shape
#         deduced_note_positions = deduce_all_key_pos(note_positions, width, height)
#
#         if len(deduced_note_positions) != 21:
#             if note_positions:
#                 for idx, position in enumerate(note_positions):
#                     pt1 = (position[0], position[1])
#                     pt2 = (position[0] + position[2], position[1] + position[3])
#                     cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 2)
#
#             # resize for display
#             resized_frame = utils.cv2_resize_to_fit(frame)
#
#             # fancy stats
#             top_left = (200, 200)  # (note_positions[14][0], max(0, note_positions[14][1] - 100))
#             message = "Frame: {:<10} [Locating Keys]\nFrames scanned:{:>7.2f}% {:>7}/{})".format(
#                 f_count,
#                 round(f_count / total_frames * 100, 2), f"({f_count}", total_frames
#             )
#             utils.cv2_print_texts(resized_frame, message, top_left,
#                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), (200, 200, 200), 1)
#             cv2.imshow('Locating Keys (resized)', resized_frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         else:
#             cap.release()
#             cv2.destroyAllWindows()
#             return deduced_note_positions
#
#     raise RuntimeError("Failed to locate keys")


def main():
    video_path = r"D:\Downloads\flower dance.mp4"
    note_template_path = os.path.join(Path.assets, 'templates/first_note.png')
    threshold = 0.955
    scales = np.linspace(0.5, 1.2, num=8)
    result = cv2_loop_through(video_path, note_template_path, threshold, scales, 1)

    for x, y, width, height, scale in result:
        print(x, y)


if __name__ == '__main__':
    main()
