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

    for j, image_path in enumerate(image_paths):
        image_pil = Image.open(image_path).convert('L')
        image = numpy.array(image_pil, 'uint8')

        # get label of image (use naming pattern crying_face-1.jpg, crying_face-2.jpg, etc)
        label = os.path.split(image_path)[1].split('-')[0]

        faces = frontal_face_cascade.detectMultiScale(image, minSize=(100,100))

        faces = group_faces(faces)

        for i, (x, y, w, h) in enumerate(faces):
            if len(faces) > 1:
                print("outputting image")
                image_pil.crop((x, y, x+w, y+h)).save('output/' + label + str(i) + str(j) + '.jpg')
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


def group_faces(faces):
    if len(faces) < 2:
        return faces

    min_x = float('inf')
    min_y = float('inf')
    max_x = -1
    max_y = -1
    for face in faces:
        if face[0] < min_x:
            min_x = face[0]
        if face[1] < min_y:
            min_y = face[1]
        if face[0]+face[2] > max_x:
            max_x = face[0]+face[2]
        if face[1]+face[3] > max_y:
            max_y = face[1] + face[3]

    return [[min_x, min_y, max_x-min_x, max_y-min_y]]


if __name__ == '__main__':

    (images, labels) = get_images_and_labels("./training")

    print("IMAGES", images)
    print("LABELS", labels)
    numpy_array = numpy.array(labels)
    label_code_array = []
    for label in labels:
        label_code_array.append(lookup_code(label))

    recognizer.train(images, numpy.array(label_code_array))
    classify_image("happy-10.jpg")




