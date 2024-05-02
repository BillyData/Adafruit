from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
from Adafruit_IO import MQTTClient
import sys
import time
from PIL import Image
import base64
import io

AIO_FEED_ID = "1089043"
AIO_USERNAME = "billy_nguyen"
AIO_KEY = "aio_WGSh37LWyOe2DT0vMDRA7kwd73qb"

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

def send_image(image):
    # Resize the raw image into (224-height,224-width) pixels
    image_resized = cv2.resize(image, (800, 600), interpolation=cv2.INTER_AREA)

    # Convert the resized image to base64 format
    retval, buffer = cv2.imencode('.jpg', image_resized, [cv2.IMWRITE_JPEG_QUALITY, 70])
    jpg_as_text = base64.b64encode(buffer)

    if len(jpg_as_text) < 102400 :
        client.publish("Webcam", jpg_as_text)

def display_hometown(name):
    hometown  = {
        "Khang\n":"Quang Nam",
        "Khoa\n":"Hue",
        "Trang\n":"Ha Noi",
        "Hưng\n":"Quang Ngai",
        "Bao\n":"Sai Gon",
        "Khoi\n":"Tien Giang",
        "Background\n":"Nowhere"
    }
    client.publish("Hometown", hometown[name])

def connected(client):
    print("Connected to the AIO server!!!!")
    client.subscribe(AIO_FEED_ID)


def subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to TOPIC!!!")


def disconnected(client):
    print("Disconnected from the AIO server!!!")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Received: " + payload)


client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    send_image(image)

    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Show the image in a window
    cv2.imshow("Webcam Image", image)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    client.publish("Confidence Score", str(np.round(confidence_score * 100))[:-2])
    client.publish("Person", f" This person is {class_name[2:]}")
    display_hometown(class_name[2:])

    time.sleep(5)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()



