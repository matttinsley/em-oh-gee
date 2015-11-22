import sys
import os
import numpy
import time
from PIL import Image
import classification_utils
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2

frontal_face_path = "./cascades/haarcascade_frontalface_default.xml"
frontal_face_cascade = cv2.CascadeClassifier(frontal_face_path)
recognizer = cv2.createLBPHFaceRecognizer()

# takes a PIL image format
def classify_image(image):
    image_pil = image.convert('L')
    image = numpy.array(image_pil, 'uint8')
    faces = frontal_face_cascade.detectMultiScale(image)

    faces = classification_utils.group_faces(faces)

    (x, y, w, h) = faces[0]
    predicted_label_code, confidence = recognizer.predict(image[y: y+h, x: x+w])
    print predicted_label_code
    print ("Classified:", classification_utils.lookup_label(predicted_label_code), "with confidence", confidence)
    print ""


def test_images(path):
    for image in filter( lambda f: not f.startswith('.'), os.listdir(path)):
        print image
        pil_image = Image.open(path + "/" + image)
        classify_image(pil_image)

def load_training():
    recognizer.load("recognizer.dat")

if __name__ == '__main__':

    # Do classification here
    while True:
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = frontal_face_cascade.detectMultiScale(gray)

        faces = classification_utils.group_faces(faces)
        for (x, y, w, h) in faces:
            cv2.rectangle(gray , (x, y), (x+w, y+h), (0, 255, 0), 2)
            predicted_label_code, confidence = recognizer.predict(gray[y: y+h, x: x+w])
            print "******************************", classification_utils.lookup_label(predicted_label_code)

        cv2.imshow('ImageWindow', gray)
        cv2.waitKey(1)
        time.sleep(1)

