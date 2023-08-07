import easygui
import format_input
import process_video as vmp
from delay_frame_interpreter import *


def task1(video_path, start=1):
    diff_per_frame = vmp.process_video(video_path, **vmp.default_configs(), start_form=start)
    with open('data\\diff_per_frame.json', 'w+') as json_file:
        json.dump(diff_per_frame, json_file)
    return diff_per_frame


def task2(video_path, name, saving_func, diff_per_frame=None):
    diff_data_path = 'data\\diff_per_frame.json'
    difference_threshold = 5
    decrease_needed = 0

    if diff_per_frame is None:
        with open(diff_data_path, 'r') as json_file:
            diff_per_frame = json.load(json_file)

    score_list = brightness_diff_to_score_list(video_path, diff_per_frame, difference_threshold, decrease_needed)

    save_as_txt_score(score_list, "data\\output_score.txt")
    saving_func(score_list, name)


def _convert_one(video_path, name, saving_func):
    print(f"Processing {name}")
    data = task1(video_path, 1)
    task2(video_path, name, saving_func, data)
    print("Completed;")


def main():
    video_path = easygui.fileopenbox("select designated 720p mp4 file", "Select Video",
                                     "D:\\Downloads\\", filetypes=["*.mp4"], multiple=True)
    queue = []
    
    for path in video_path:
        name = input(f"Video path: {path}\nname?: ")
        
        if input("Save as composed [Y/n]: ").lower() not in ["n", "no"]:
            saving_func = save_as_composed_nightly 
        else:
            saving_func = save_as_recorded_nightly
        queue.append([path, name, saving_func])

    redo_command = "\\re"

    if len(queue) == 1:
        args = queue[0]
        if redo_command in args[1]:
            task2(args[0], args[1].replace(redo_command, "").strip(), saving_func=args[2])
            print("completed")
        else:
            try:
                _convert_one(*args)
                format_input.main()
            except Exception as exc:
                print(exc)
    elif len(queue) > 1:
        for args in queue:
            try:
                _convert_one(*args)
            except Exception as exc:
                print(exc)
    else:
        print("???")

    input("press enter to exit")


if __name__ == '__main__':
    main()
