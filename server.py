from flask import Flask, request
from PIL import Image
import emoji
import face_recognition

app = Flask(__name__)

emos = {1 : ':grinning_face:',
        2 : ':smiling_face_with_smiling_eyes:',
        3 : ':white_smiling_face:',
        4 : ':face_savouring_delicious_food:',
        5 : ':grinning_face_with_smiling_eyes:',
        6 : ':neutral_face:',
        7 : ':face_with_stuck-out_tongue:',
        8 : ':face_with_stuck-out_tongue_and_winking_eye:',
        9 : ':face_with_stuck-out_tongue_and_tightly-closed_eyes:',
        10 : ':pensive_face:',
        11 : ':face_throwing_a_kiss:',
        12 : ':winking_face:',
        13 : ':flushed_face:',
        14 : ':loudly_crying_face:',
        15 : ':angry_face:'}

@app.route('/facemoji', methods=['POST'])
def emoji_for_face():
    img_data = request.data
    #print(img_data)

    img_file = open('img.jpg', 'wb')
    img_file.write(img_data)

    image = Image.open('img.jpg')

    return emoji.emojize(face_recognition.classify_image(image))

@app.route('/')
def test():
    return '<h1>The thing works!!!</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    face_recognition.load_training()
