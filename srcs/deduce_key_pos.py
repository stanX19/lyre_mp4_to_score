import statistics
from .mp4_to_lyre_types import *

def sorted_positions(positions: list[LocType]) -> list[LocType]:
    if not positions:
        return positions

    # Sort positions by y-coordinate (row)
    sorted_by_row = sorted(positions, key=lambda pos: pos[1])

    # Determine the unique rows, top = 3, bot = 1
    rows = {}
    row_category = 3
    previous_y = sorted_by_row[0][1]
    for position in sorted_by_row:
        y = position[1]
        if y - previous_y > position[3]:
            row_category -= 1
        rows[y] = row_category
        previous_y = y

    # Sort positions within each row category by x-coordinate (column)
    sorted_by_row_and_col = sorted(sorted_by_row, key=lambda pos: (rows[pos[1]], pos[0]))

    return sorted_by_row_and_col


def group_values(values: float, uncertainty: float) -> dict:
    grouped_values = {}
    for value in values:
        for group_key in grouped_values.keys():
            if abs(value - group_key) <= uncertainty:
                grouped_values[group_key].append(value)
                break
        else:
            grouped_values[value] = [value]
    return grouped_values


def sets_of_data_with_difference(sorted_data: list, difference: int, pixel_uncertainty: int) -> list[list[int]]:
    grouped_values = {}

    for value in sorted_data:
        for group_key in grouped_values:
            diff = value - grouped_values[group_key][-1]
            number = round(diff / difference)
            if min(diff % difference, -diff % difference) <= pixel_uncertainty * number:
                grouped_values[group_key].append(value)
                break
        else:
            grouped_values[value] = [value]

    return list(grouped_values.values())


def deduce_all_key_pos(key_positions: list[LocType],
                       screen_width, screen_height, pixel_uncertainty=10) -> list[LocType]:
    if not key_positions:
        return []

    # Determine the grid dimensions
    try:
        x_values = [element[0] for element in key_positions]
        y_values = [element[1] for element in key_positions]
        width_values = [element[2] for element in key_positions]
        height_values = [element[3] for element in key_positions]
        scale_values = [element[4] for element in key_positions]
    except IndexError:
        return key_positions

    # data
    grouped_y = group_values(y_values, pixel_uncertainty)
    grouped_x = group_values(x_values, pixel_uncertainty)
    width = int(statistics.median(width_values))   # assume all same scale
    height = int(statistics.median(height_values))
    scale = statistics.median(scale_values)

    sorted_x = sorted([statistics.mean(x_data) for x_data in grouped_x.values()])
    sorted_y = sorted([statistics.mean(y_data) for y_data in grouped_y.values()])

    x_ratio = 1.56  # actual 14/9 = (width + x_spacing) / width
    y_ratio = 1.24  # actual 88/71  = (height + y_spacing) / height
    ratio_uncertainty = 0.05

    desired_x_diff = width * x_ratio
    desired_y_diff = height * y_ratio
    x_uncertainty = ratio_uncertainty * desired_x_diff + pixel_uncertainty
    y_uncertainty = ratio_uncertainty * desired_y_diff + pixel_uncertainty

    # calculations
    possible_sets_of_x = sets_of_data_with_difference(sorted_x, int(desired_x_diff), x_uncertainty)
    possible_sets_of_y = sets_of_data_with_difference(sorted_y, int(desired_y_diff), y_uncertainty)

    filtered_sets_of_x = [s for s in possible_sets_of_x if
                          abs((s[-1] - s[0]) - desired_x_diff * 6) <= x_uncertainty * 6]
    filtered_sets_of_y = [t for t in possible_sets_of_y if
                          abs((t[-1] - t[0]) - desired_y_diff * 2) <= y_uncertainty * 2]

    # dummy param
    min_x, max_x, min_y, max_y = None, None, None, None

    if len(filtered_sets_of_x) == 1 and len(filtered_sets_of_y) == 1:
        min_x, max_x = filtered_sets_of_x[0][0], filtered_sets_of_x[0][-1]
        min_y, max_y = filtered_sets_of_y[0][0], filtered_sets_of_y[0][-1]

    elif len(filtered_sets_of_x) == 1 and len(possible_sets_of_y) == 1 and len(possible_sets_of_y[0]) > 1:
        set_of_y = possible_sets_of_y[0]
        # print(set_of_y)
        # print(filtered_sets_of_y)
        y_diff = set_of_y[-1] - set_of_y[-2]
        for n in range(1, 10):
            if abs(y_diff / n - desired_y_diff) < y_uncertainty:
                y_diff //= n
                break
        if set_of_y[-1] + y_diff + height > screen_height: # exceed boundary of screen
            min_y, max_y = set_of_y[-1] - 2 * y_diff, set_of_y[-1]
            min_x, max_x = filtered_sets_of_x[0][0], filtered_sets_of_x[0][-1]

    if min_x is not None and max_x is not None and min_y is not None and max_y is not None:
        ret = []
        dy = (max_y - min_y) / 2
        dx = (max_x - min_x) / 6
        for j in range(3):
            y = int(max_y - dy * j)
            for i in range(7):
                x = int(min_x + dx * i)
                ret.append([x, y, width, height, scale])
        return ret
    else:
        return key_positions


if __name__ == '__main__':
    x = sorted_positions([[609, 637, 93, 91, 0.8999999999999999], [750, 637, 93, 91, 0.8999999999999999], [1315, 637, 93, 91, 0.8999999999999999], [1456, 637, 93, 91, 0.8999999999999999], [891, 638, 93, 91, 0.8999999999999999], [1032, 638, 93, 91, 0.8999999999999999], [1175, 640, 93, 91, 0.8999999999999999], [610, 750, 93, 91, 0.8999999999999999], [751, 750, 93, 91, 0.8999999999999999], [1456, 750, 93, 91, 0.8999999999999999], [890, 751, 93, 91, 0.8999999999999999], [1031, 751, 93, 91, 0.8999999999999999], [1174, 751, 93, 91, 0.8999999999999999], [1314, 751, 93, 91, 0.8999999999999999], [608, 864, 93, 91, 0.8999999999999999], [750, 864, 93, 91, 0.8999999999999999], [892, 864, 93, 91, 0.8999999999999999], [1033, 864, 93, 91, 0.8999999999999999], [1174, 864, 93, 91, 0.8999999999999999], [1316, 864, 93, 91, 0.8999999999999999], [1456, 864, 93, 91, 0.8999999999999999]])
    print(x)