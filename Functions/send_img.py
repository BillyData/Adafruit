def send_image(image):
    # Resize the raw image into (224-height,224-width) pixels
    image_resized = cv2.resize(image, (800, 600), interpolation=cv2.INTER_AREA)

    # Convert the resized image to base64 format
    retval, buffer = cv2.imencode('.jpg', image_resized, [cv2.IMWRITE_JPEG_QUALITY, 70])
    jpg_as_text = base64.b64encode(buffer)

    if len(jpg_as_text) < 102400 :
        client.publish("Webcam", jpg_as_text)