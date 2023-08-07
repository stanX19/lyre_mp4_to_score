import json
import math
import statistics

try:
    from .common import first_float
except ImportError:
    from common import first_float


def score_list_to_score(score_list):
    all_keys = "ZXCVBNMASDFGHJQWERTYUzxcvbnmasdfghjqwertyu"
    all_time = [i for i in score_list if type(i) == float]
    try:
        average_time = statistics.mode(all_time)  # mode
    except statistics.StatisticsError:  # if no mode or 2 mode
        average_time = None
    if not average_time or all_time.count(average_time) < len(all_time) / 4:
        average_time = sorted(all_time)[round(len(all_time) / 2)]  # use median

    # edit average dashes here: ↓
    lowest_lim = average_time / 16
    lowest_time = min([i for i in all_time if i >= lowest_lim])

    score = ""
    for msg in score_list:
        if type(msg) == float:
            msg = (round(msg / lowest_time)) * "-"
        elif len(msg) > 1:
            msg = [key for key in msg if key in all_keys]
            msg = f"({''.join(set(msg))})"
        score += msg

    # score has been created but have no line break
    # so it is created here
    # edit length of each line below:
    line_break = 70
    to_break = line_break
    score = score.replace("-", " ").strip().replace(" ", "-")
    score = list(score)
    for idx, key in enumerate(score):
        if idx > to_break and key == "-" and idx != len(score) - 1 and score[idx + 1] != '-':
            score[idx] = "\n"
            to_break += line_break
    #                         0.0059 is delay by time.sleep() function
    score = f"(beat{round(lowest_time - 0.0059, 3)})-\n{''.join(score)}"
    return score


def key_list_to_score_list(key_list: list):
    score_list = [0.0]
    temp_beat = 0.15
    for key in key_list:
        if "beat" in key.lower():
            temp_beat = first_float(key)
        elif key == "-":
            score_list[-1] += temp_beat + 0.0059
        elif key.isnumeric():
            score_list[-1] += (temp_beat * (float(key) / 10)) + 0.0059
        else:
            score_list.append(key)
            score_list.append(0.109)
    return score_list


def score_list_to_nightly(score_list: list, name="Undefined"):
    all_time = [i for i in score_list if type(i) == float]
    try:
        average_time = statistics.mode(all_time)  # mode
    except statistics.StatisticsError:  # if no mode or 2 mode
        average_time = None
    if not average_time or all_time.count(average_time) < len(all_time) / 4:
        average_time = sorted(all_time)[round(len(all_time) / 2)]  # use median

    #  edit average dashes here, must be divisible by 2:
    average_spacing = 8

    lowest_time = average_time / average_spacing

    bpm = round(60 / lowest_time)
    jsonFile = {"data": {"isComposed": True, "isComposedVersion": True, "appName": "Genshin"}, "name": name, "bpm": bpm,
                "pitch": "C", "breakpoints": [0], "instruments": ["Lyre", "Lyre", "Lyre"]}
    KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    NOTES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    KN = dict(zip(KEYS, NOTES))

    columns = []
    idx = 0
    while idx < len(score_list):
        if isinstance(score_list[idx], float):
            ratio = score_list[idx] / lowest_time
            columns += [0, []] * round(ratio)  # get_representative_key([],ratio)
            idx += 1
            continue
        # current note is str
        note = [[KN[key], "100"] for key in score_list[idx].upper() if key in KN]
        try:
            length = score_list[idx + 1]
            ratio = math.ceil(length / lowest_time)
        except IndexError:
            ratio = 1

        if ratio % 2:  # odd number, very awkward
            ratio -= 1  # already using ceil
        notes_list = [[0, note]] + [[0, []]] * (ratio - 1)  # get_representative_key(note, ratio)
        columns += notes_list
        idx += 2
    jsonFile["columns"] = columns
    jsonFile = json.dumps([jsonFile])
    return jsonFile


def score_list_to_recorded_nightly(score_list: list, name="Undefined"):
    json_file = {"name": name, "type": "recorded",
                 "instruments": [{"name": "Lyre", "volume": 90, "pitch": ""}], "pitch": "C", "bpm": 220,
                 "data": {"isComposed": False, "isComposedVersion": False, "appName": "Genshin"}}

    KEYS = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    NOTES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    KN = dict(zip(KEYS, NOTES))

    notes = []
    cum_time = 100
    for val in score_list:
        if isinstance(val, float):
            cum_time += val * 1000
        if isinstance(val, str):
            for key in val:
                notes.append([KN[key], cum_time, "1"])

    json_file["notes"] = notes
    result = json.dumps([json_file])
    return result
