import cv2
import numpy as np

def remove_mask(picture, mask, opacity=0.345):
    # Resize the mask to match the picture dimensions
    mask_resized = cv2.resize(mask, (picture.shape[1], picture.shape[0]))

    # Invert the mask
    mask_inverted = cv2.bitwise_not(mask_resized)

    # Convert the picture and mask to float
    picture_float = picture.astype(float)
    mask_float = mask_inverted.astype(float)

    # Apply alpha blending
    result = picture_float * (1 - opacity) + mask_float * opacity

    # Convert the result back to uint8
    result = result.astype(np.uint8)

    return result






