import cv2
import numpy as np

def custom_bgr_conversion(image, scale):
    # Split the image into B, G, and R channels
    b, g, r = cv2.split(image)

    # Apply custom transformations to the channels based on the scale
    b_transformed = b * scale[0] / 255.0
    g_transformed = g * scale[1] / 255.0
    r_transformed = r * scale[2] / 255.0

    # Merge the transformed channels back into a BGR image
    custom_bgr_image = cv2.merge([b_transformed, g_transformed, r_transformed])

    return custom_bgr_image

# Load the image
image_path = r"C:\Users\DELL\PycharmProjects\pythonProject\lyre_mp3_to_notes\srcs\assets\first_note.png"
image = cv2.imread(image_path)

# Define the scale based on the observed pixel BGR values [231, 240, 245]
scale = [231/255.0, 240/255.0, 245/255.0]

# Convert the image to the custom BGR color space
custom_bgr_image = custom_bgr_conversion(image, scale)

# Display the custom BGR image
cv2.imshow("Custom BGR Image", custom_bgr_image)
cv2.waitKey(0)
cv2.imshow("Custom BGR Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
