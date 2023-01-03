import cv2 as cv
import pytesseract
from PIL import Image

TESSERACT_PATH = r'/usr/local/bin/tesseract'

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def text_recognition():
    capture = cv.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(Image.fromarray(image))
        cv.imshow('Text Recognition', image)
        if cv.waitKey(1) and 0xFF == ord('q'):
            break
        print("Extracted Text: ", text)

    capture.release()
