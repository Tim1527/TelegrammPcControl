import numpy
import cv2
import pyautogui

#Возвращает координаты курсора на скриншоте распознавая розовый цвет
def coords(img_name):
    img = cv2.imread(f"{img_name}")

    resized = cv2.resize(img, (1920,1080), interpolation=cv2.INTER_AREA)
    cv2.imwrite(img_name,resized)

    img = resized

    low_pink = numpy.array((135,140,210), numpy.uint8)
    high_pink = numpy.array((140,170,255), numpy.uint8)
    try:

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_pink = cv2.inRange(img_hsv,low_pink, high_pink)
        moments = cv2.moments(mask_pink,1)

        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']
        # if dArea > 150:
        x = int(dM10/dArea) #координаты в разрешении 1280х720
        y = int(dM01 / dArea)
        return [x, y]

    except:
        cv2.imwrite("Images/ErrorImage.png", img)
        return [0,0]

#Добавляет(рисует) курсор на скриншоте
def add_cursor(img_name):
    x, y = pyautogui.position()
    cv2.imwrite(img_name, cv2.circle(cv2.imread(img_name), (x, y), 5, (0, 0, 255), 0))
    cv2.imwrite(img_name, cv2.circle(cv2.imread(img_name), (x, y), 6, (0, 0, 0), 0))

#делает и сохраняет фото с камеры
def PhotoCam(kamera_number):
    try:
        cap = cv2.VideoCapture(kamera_number)
        # for i in range(30):
        #     cap.read()
        ret, frame = cap.read()
        cv2.imwrite('Images/cam_old.png', frame)
        cap.release()
        return True
    except: return False

