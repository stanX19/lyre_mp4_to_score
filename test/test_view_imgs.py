import cv2
import numpy as np

# Load the image
image = cv2.imread('../srcs/assets/templates/first_note.png', cv2.IMREAD_UNCHANGED)

# Create a copy of the image for visualization
image_with_displacement = image.copy()
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Draw a circle at the selected point on the image copy
        cv2.circle(image_with_displacement, (x, y), 2, (0, 0, 255), -1)
        # Display the image with the selected displacement point
        cv2.imshow('Image with Displacement', image_with_displacement)
        # Print the coordinates of the selected point
        print(f"Displacement Point: ({x}, {y})")

# Create a window to display the image with displacement
cv2.namedWindow('Image with Displacement')
cv2.imshow('Image with Displacement', image_with_displacement)

# Set the callback function for mouse events
cv2.setMouseCallback('Image with Displacement', mouse_callback)


# Wait for a key press to exit
cv2.waitKey(0)
cv2.destroyAllWindows()

