import os.path
import easygui
from srcs import format_input
from srcs import process_video as pv
from srcs.mp4_to_lyre_types import *
from srcs.delay_frame_interpreter import *
from srcs import Path


def input_with_default(prompt, default):
    user_input = input(f"{prompt} ({default}): ")
    if user_input == "":
        return default
    return user_input


def basename(path: str) -> str:
    path = path.replace("\\", "/")
    return os.path.basename(os.path.splitext(path)[0])


def generate_dpf_filepath(video_path: str):
    return os.path.join(Path.data, f'dpf/{basename(video_path)}.dpf.json')


def load_dpf_from_history(video_path: str):
    with open(generate_dpf_filepath(video_path), 'r') as f:
        data = json.load(f)

    return data["fps"], data["dpf"]


def video_to_dpf_data(video_path: str, start=1) -> tuple[float, DpfType]:
    diff_per_frame_data = pv.process_video(video_path, **pv.default_configs(), start_form_frame=start)

    with open(generate_dpf_filepath(video_path), 'w+') as f:
        data_dict = {"fps": diff_per_frame_data[0], "dpf": diff_per_frame_data[1]}
        json.dump(data_dict, f)

    return diff_per_frame_data


def save_dpf_data_as_nightly_score(name: str, saving_func: SavingFuncType,
                                   diff_per_frame_data: tuple[float, DpfType], directory: str) -> str:
    difference_threshold = 10
    decrease_needed = 0

    fps, dpf = diff_per_frame_data
    score_list = brightness_diff_to_score_list(fps, dpf, difference_threshold, decrease_needed)

    save_as_txt_score(score_list, os.path.join(Path.data, "output_score.txt"))
    return saving_func(score_list, name, directory)


def _convert_one(video_path: str, name: str, saving_func: SavingFuncType, use_history: bool, directory: str):
    print(f"Processing {name}")
    if use_history:
        dpf_data = load_dpf_from_history(video_path)
    else:
        dpf_data = video_to_dpf_data(video_path)
    save_path = save_dpf_data_as_nightly_score(name, saving_func, dpf_data, directory)
    print(f"Completed; Saved as {save_path}")


def prompt_for_details(path: str) -> list[str, str, SavingFuncType, bool]:
    if os.path.exists(generate_dpf_filepath(path)):
        enter = ""
        while enter not in ["y", "yes", "n", "no"]:
            enter = input("Previous processing record found, skip video processing? [Y/n]: ").lower().strip()
        use_history = enter in ["y", "yes"]
    else:
        use_history = 0

    name = input_with_default(f"Video path: {path}\nname?", default=basename(path)).strip()

    if input("Save as recorded? [Y/n]: ").lower() in ["n", "no"]:
        saving_func = save_as_composed_nightly
        print(f"    [NAME: {name} | FORMAT: Composed]")
    else:
        saving_func = save_as_recorded_nightly
        print(f"    [NAME: {name} | FORMAT: Recorded]")
    return [path, name, saving_func, use_history]


def save_video_as_nightly(dst_path: str):
    video_path = easygui.fileopenbox("select designated 720p mp4 file", "Select Video",
                                     "D:\\Downloads\\", filetypes=["*.mp4"], multiple=True)
    queue: list[list[str, str, SavingFuncType, bool]] = []

    if video_path is None:
        return
    for path in video_path:
        args = prompt_for_details(path)
        queue.append(args)

    for args in queue:
        try:
            _convert_one(*args, directory=dst_path)
        except Exception as exc:
            print(exc)

    if not queue:
        print("???")

    input("press enter to exit")


def main():
    save_video_as_nightly(Path.data)


if __name__ == '__main__':
    main()

r"""
import os
import sys
sys.path.append(r"C:\Users\DELL\PycharmProjects\pythonProject")
import mp4_to_lyre
mp4_to_lyre.main.save_video_as_nightly("Desktop")
"""

