import sys
import os
import numpy
from PIL import Image
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2


codes = ['angry', 'happy']

frontal_face_path = "./cascades/haarcascade_frontalface_default.xml"
frontal_face_cascade = cv2.CascadeClassifier(frontal_face_path)
recognizer = cv2.createLBPHFaceRecognizer()

def get_images_and_labels(path):

    # put training images in 'path' directory
    image_paths = [os.path.join(path, f) for f in filter( lambda f: not f.startswith('.'), os.listdir(path))]

    # array of face images
    images = []

    # label assigned to image
    labels = []

    for image_path in image_paths:
        image_pil = Image.open(image_path).convert('L')
        image = numpy.array(image_pil, 'uint8')

        # get label of image (use naming pattern crying_face-1.jpg, crying_face-2.jpg, etc)
        label = os.path.split(image_path)[1].split('-')[0]

        faces = frontal_face_cascade.detectMultiScale(image)
        print(faces)

        for(x, y, w, h) in faces:
            print("doing a thing to a face")
            images.append(image[y: y+h, x: x+w])
            labels.append(label)

    print(images)
    print(labels)
    return images, labels


def classify_image(path):
    image_path = os.path.join(path)
    image_pil = Image.open(image_path).convert('L')
    image = numpy.array(image_pil, 'uint8')
    face = frontal_face_cascade.detectMultiScale(image)

    for (x, y, w, h) in face:
        predicted_label_code, confidence = recognizer.predict(image[y: y+h, x: x+w])
        actual_label = os.path.split(image_path)[1].split('-')[0]
        predicted_label = lookup_label(predicted_label_code)
        if predicted_label == actual_label:
            print("Correctly predicted with confidence", confidence)
        else:
            print("Incorrectly recognized as", predicted_label)


def lookup_label(code):
    return codes[code]


def lookup_code(label):
    return codes.index(label)

if __name__ == '__main__':

    (images, labels) = get_images_and_labels("./training")

    print("IMAGES", images)
    print("LABELS", labels)
    numpy_array = numpy.array(labels)
    label_code_array = []
    for label in labels:
        label_code_array.append(lookup_code(label))

    recognizer.train(images, numpy.array(label_code_array))
    classify_image("angry-11.jpg")




