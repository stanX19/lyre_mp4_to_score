import cv2

def print_pixel_rgb(image_path, x, y):
    # Load the image
    image = cv2.imread(image_path)

    # Get the RGB values of the selected pixel
    pixel_rgb = image[y, x]

    # Print the RGB values
    print(f"RGB values at ({x}, {y}): {pixel_rgb}")

# Usage
image_path = r"C:\Users\DELL\PycharmProjects\pythonProject\lyre_mp3_to_notes\srcs\assets\first_note.png"
x = 23  # x-coordinate of the pixel
y = 53  # y-coordinate of the pixel
print_pixel_rgb(image_path, x, y)
