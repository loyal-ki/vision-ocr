import cv2


def convert_image_to_bytes(image) -> bytes:
    retval, buffer = cv2.imencode(".jpg", image)
    img_bytes = buffer.tobytes()
    return img_bytes
