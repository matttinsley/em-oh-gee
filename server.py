from flask import Flask, request, render_template
from PIL import Image
from flask.ext.cors import CORS
import emoji
import face_recognition
import base64

app = Flask(__name__)
CORS(app)

def get_emoji(image_bin):
    with open('img.jpg', 'wb') as img_file:  
        img_file.write(image_bin)
        image = Image.open('img.jpg')

        return emoji.emojize(face_recognition.classify_image(image))

    return emoji.emojize(':pile_of_poo:')


@app.route('/facemoji/encrypted', methods=['POST'])
def base64_emoji():
    request.get_data()
    encrypted_image = request.data
    
    if str(encrypted_image).find('data:image/jpeg') != -1:
        encrypted_image = str(encrypted_image).lstrip('\'data:image/jpeg;base64')

    #print(encrypted_image)

    decoded_image = base64.b64decode(encrypted_image)

    #print("--- BEGIN DECODED IMAGE ---\n\n" + str(decoded_image))

    return get_emoji(decoded_image)


@app.route('/facemoji', methods=['POST'])
def emoji_for_face():
    img_data = request.data

    return get_emoji(img_data)


@app.route('/webcam')
def webcam():
    return render_template('classifier_demo.html', name="Webcam")


@app.route('/')
def test():
    return emoji.emojize(':smiling_face_with_heart-shaped_eyes:')

if __name__ == '__main__':
    face_recognition.load_training()
    app.run(debug=True, port=8000)
