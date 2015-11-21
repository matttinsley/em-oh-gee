codes = ['angry', 'happy']

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


