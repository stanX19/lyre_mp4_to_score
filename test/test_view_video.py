import cv2
import numpy as np


def process_video(video_path, first_note_template_path, threshold, scales, target_pixel):
    cap = cv2.VideoCapture(video_path)

    f_count = 1
    while cap.isOpened():
        print(f"frame {f_count}")
        f_count += 1
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Processed Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    video_path = r"../srcs/assets/test_videos/floral_breezee.mp4"
    first_note_template_path = 'assets/first_note.png'
    threshold = 0.9
    scales = np.linspace(0.8, 1.2, num=5)
    target_pixel = (22, 50)  # displacement from the top-left corner of the bounding box

    process_video(video_path, first_note_template_path, threshold, scales, target_pixel)

if __name__ == '__main__':
    main()