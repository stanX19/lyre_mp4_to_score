import cv2
import numpy as np
from srcs import utils
from remove_mask import remove_mask

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def concatenate_videos_horizontally(video1, video2):
    return np.concatenate((video1, video2), axis=1)

def compare_videos(video1_path, video2_path):
    # Create video capture objects
    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)

    width = 720
    # Get dimensions of the first video
    vid_width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create window
    cv2.namedWindow('Multiple Videos', cv2.WINDOW_NORMAL)

    displacement = 36
    start = 180
    vid1_fc = 0
    vid2_fc = 0
    for i in range(start):
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()
        vid1_fc += 1
        vid2_fc += 1
    for i in range(displacement):
        ret2, frame2 = video2.read()
        vid2_fc += 1
    while True:
        ret1, frame1 = video1.read()
        ret2, frame2 = video2.read()
        vid1_fc += 1
        vid2_fc += 1

        if not ret1 or not ret2:
            break

        frame1_resized = resize_frame(frame1, vid_width, vid_height)
        frame2_resized = resize_frame(frame2, vid_width, vid_height)

        processed_frame = remove_mask(frame1_resized, frame2_resized)

        video_horizontal = concatenate_videos_horizontally(frame1_resized, frame2_resized)
        video_horizontal = resize_frame(video_horizontal, width, int((width / 2) * vid_height / vid_width))
        processed_frame_resized = resize_frame(processed_frame, width, int(width * vid_height / vid_width))

        display_frame = np.concatenate((video_horizontal, processed_frame_resized), axis=0)

        cv2.imshow('Multiple Videos', display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video1.release()
    video2.release()
    cv2.destroyAllWindows()


def main():
    video2_path = r"../assets/test_videos/masks/yoimiya story quest mask.mp4"
    video1_path = r"../assets/test_videos/yoimiya story quest.mp4"

    compare_videos(video1_path, video2_path)

if __name__ == "__main__":
    main()
