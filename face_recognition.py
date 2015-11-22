import sys
import numpy
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

    face = classification_utils.group_faces(faces)

    (x, y, w, h) = face
    predicted_label_code, confidence = recognizer.predict(image[y: y+h, x: x+w])
    return classification_utils.lookup_label(predicted_label_code)

def load_training():
    recognizer.load("recognizer.dat")

if __name__ == '__main__':
    pass
    # Do classification here
    # classify_image(pil_image_object)
