import cv2
import json
from utils import score_list_to_nightly, score_list_to_recorded_nightly, score_list_to_score


def brightness_diff_to_keys(diff_per_frame: list[list[int]], difference_threshold=5, decrease_needed=0):
    keys = "ZXCVBNMASDFGHJQWERTYU"
    keys_per_frame = []

    changes_status = [0 for _ in range(21)]
    # 0 = None
    # 1 = first positive
    # 2 = first negative
    # 3 = second negative
    # ...

    neutral_status = [0 for _ in range(21)]
    # 1 = first neutral
    # 2 = second neutral

    for all_diff in diff_per_frame:
        this_frame_key = ""

        for idx, diff in enumerate(all_diff):
            if diff > difference_threshold:
                if changes_status[idx] == 0:  # None
                    changes_status[idx] = 1
                elif changes_status[idx] > 1:  # Consecutive note press detected
                    keys_per_frame.append(keys[idx])
                    changes_status[idx] = 1
                elif changes_status[idx] == 1:  # ??? error, treat as 0
                    pass  # status[idx] = 1
            elif diff < 0:
                if changes_status[idx] >= 1:
                    changes_status[idx] += 3
            elif diff == 0.0:
                neutral_status[idx] += 1
                if neutral_status[idx] == 2:  # allow one frame no changes but still decreasing
                    changes_status[idx] = 0
                    neutral_status[idx] = 0

            if changes_status[idx] == decrease_needed + 1:
                changes_status[idx] = 0
                this_frame_key += keys[idx]

        keys_per_frame.append(this_frame_key)

    return keys_per_frame


def get_video_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def keys_to_score_list(keys_per_frame, video_path):
    fps = get_video_fps(video_path)
    spf = 1 / fps
    score_list = [0.0]

    for keys in keys_per_frame:
        if keys:
            score_list.append(keys)
            score_list.append(0.0)
        score_list[-1] += spf

    if isinstance(score_list[0], float):
        score_list.pop(0)
    if isinstance(score_list[-1], float):
        score_list.pop(-1)

    return score_list


def save_as_txt_score(score_list, path):
    score = score_list_to_score(score_list)

    score = score.split("\n", 1)[1]
    score = score.replace("-", " ").replace("\n", " ")
    while "  " in score:
        score = score.replace("  ", " ")

    with open(path, 'w+') as f:
        f.write(score)


def save_as_recorded_nightly(score_list, name):
    export_path = f'data\\{name}.genshinsheet.json'
    nightly = score_list_to_recorded_nightly(score_list, name)

    with open(export_path, 'w+') as f:
        f.write(nightly)

def save_as_composed_nightly(score_list, name):
    export_path = f'data\\{name}.genshinsheet.json'
    nightly = score_list_to_nightly(score_list, name)

    with open(export_path, 'w+') as f:
        f.write(nightly)


def brightness_diff_to_score_list(video_path, diff_per_frame, difference_threshold=5, decrease_needed=0):
    keys = brightness_diff_to_keys(diff_per_frame, difference_threshold, decrease_needed)
    score_list = keys_to_score_list(keys, video_path)
    return score_list


def main():
    name = "Lantern Rite"
    diff_data_path = 'data\\diff_per_frame.json'
    video_path = f'assets\\{name}.mp4'
    difference_threshold = 5
    decrease_needed = 0

    with open(diff_data_path, 'r') as json_file:
        diff_per_frame = json.load(json_file)

    score_list = brightness_diff_to_score_list(video_path, diff_per_frame, difference_threshold, decrease_needed)
    save_as_txt_score(score_list, "data\\output_score.txt")
    save_as_nightly(score_list, name)


if __name__ == '__main__':
    main()
