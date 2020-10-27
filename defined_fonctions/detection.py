import numpy as np
import cv2


def face_detect(img):

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    pic = cv2.imread(img)
    img = img.split('.jpg')[0]
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.5,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    path = img.split('/')
    path = path[:-2]
    path = '/'.join(path)
    print(path)
    path = path+'/detected/croped_face.jpg'
    print("[INFO] Found {0} Faces!".format(len(faces)))
    for (x, y, w, h) in faces:
        cv2.rectangle(pic, (x, y), (x + w, y + h), (255, 0, 0), 2)
        crop_img = pic[y:y+h, x:x+w]
    # cv2.imshow('Face_Detector', crop_img)
    cv2.imwrite(path, crop_img)
    return path


def eyes_detect(place, img):
    img = face_detect(img)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml")

    pic = cv2.imread(img)

    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.5,
                                          minNeighbors=5,
                                          minSize=(8, 8),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = pic[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 3)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_gray, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 3)
    # cv2.imwrite('eyes.jpg', pic)
    # cv2.imwrite('eyesG.jpg', pic)


def dectect_nose(img):
    img = face_detect(img)
    nose_cascade = cv2.CascadeClassifier(
        cv2.samples.findFile('haarcascade_mcs_nose.xml'))

    pic = cv2.imread(img)
    img = img.split('.jpg')[0]
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

    nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 5)
    path = img.split('/')
    path = path[:-2]
    path = '/'.join(path)
    print(path)
    path = path+'/detected/nose.jpg'
    for (x, y, w, h) in nose_rects:
        print('[INFO] Nose detected !')
        ny1 = int(y-y/8)
        ny2 = int(y-y/12)
        cv2.rectangle(pic, (x, ny1),
                      (x+w, ny2+h), (0, 255, 0), 3)

        # cv2.imshow('nose_Detector', pic)

    cv2.imwrite(path, pic)
    cv2.destroyAllWindows()
    print(dir(pic))
    return path

    # cv2.imwrite(img+'_corped_nose.jpg', pic[ny1+1:ny2+h, x+1:x+w])


def detect_mouth(img):
    img = face_detect(img)
    smile_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_smile.xml")

    pic = cv2.imread(img)

    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

    smile = smile_cascade.detectMultiScale(gray, 1.7, 11)
    path = img.split('/')
    path = path[:-2]
    path = '/'.join(path)
    path = path+'/detected/mouth.jpg'
    print(path)
    try:
        y = max(s[1] for s in smile)
        for s in smile:
            if s[1] == y:
                (x, y, w, h) = s
                break
    except:
        (x, y, w, h) = smile

    y = int(y - 0.15*h)
    #crop_pic = pic[y:y+h, x:x+w]
    cv2.rectangle(pic, (x, y), (x+w, y+h), (0, 255, 0), 3)

    # cv2.imshow('mouth_Detector', crop_pic)
    cv2.imwrite(path, pic)
    return path


def eyes_detect2(img):
    img = face_detect(img)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml")

    pic = cv2.imread(img)
    img = img.split('.jpg')[0]
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.5,
                                          minNeighbors=5,
                                          minSize=(8, 8),
                                          flags=cv2.CASCADE_SCALE_IMAGE)
    roi_gray = gray
    roi_color = pic
    gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(roi_gray)
    path = img.split('/')
    path = path[:-2]
    path = '/'.join(path)
    path = path+'/detected/eyes.jpg'
    for (ex, ey, ew, eh) in eyes:
        print('[INFO] Eye detected !')
        cv2.rectangle(roi_color, (ex, ey),
                      (ex+eh, ey+ew), (0, 255, 0), 3)
        a = pic[ey+1:ey+eh, ex+1:ex+ew]
        #cv2.imwrite(img+'_eye{}_corped.jpg'.format(ex), a)
        # crop = pic[y:y+h, x:x+w]

    cv2.imwrite(path, roi_color)
    return path


# face_detect('a.jpg')
# eyes_detect2('a_croped_face.jpg')
# dectect_nose('a_croped_face.jpg')
