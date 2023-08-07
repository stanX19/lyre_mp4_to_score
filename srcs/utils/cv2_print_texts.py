import cv2
import numpy as np


def cv2_print_texts(frame: np.ndarray, message: str, top_left: tuple, font_type, scale: float, font_color: tuple,
                    outlining_color: tuple, font_width: int) -> np.ndarray:
    lines = message.split('\n')

    x, y = top_left
    _, line_height = cv2.getTextSize("A", font_type, scale, font_width)[0]
    line_height += 10

    for line in lines:
        cv2.putText(frame, line, (x, y), font_type, scale, outlining_color, int(font_width + 5 * scale), cv2.LINE_AA)
        cv2.putText(frame, line, (x, y), font_type, scale, font_color, font_width, cv2.LINE_AA)
        y += int(line_height)

    return frame


