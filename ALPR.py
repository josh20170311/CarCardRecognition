import cv2
import pytesseract
import re
import os
import time

KSIZE = 3
SIGMA_X = 20
THRESHOLD = 29
MAX = 256


def formatk(s):
    t = ''
    for x in s:
        if x not in "0123456789QWERTYUIOPASDFGHJKLZXCVBNM":
            continue
        t += x
    return t


def alpr(imagefile="TR/images/c13.jpg", image=None, th1=THRESHOLD, th2=MAX):
    list_results = []
    list_boxes = []
    org = image
    org_rec = org
    gray = cv2.cvtColor(org, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (KSIZE, KSIZE), SIGMA_X)
    canny = cv2.Canny(blur, th1, th2)
    (contours, _) = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0, len(contours)):
        rec = cv2.boundingRect(contours[i])  # get rectangle from each contour

        x, y, w, h = rec
        r = w / h
        if r > 2.375 * 1.1 or r < 2.375 * 0.9 or w < 50 or h < 50:
            continue

        cut = org[y:y + h, x:x + w]

        t = pytesseract.image_to_string(cut, config="-l eng --oem 1 --psm 7")  # OCR
        t = formatk(t)
        print(t)

        cv2.rectangle(org_rec, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)

        list_results.append(t)
        list_boxes.append(rec)
    cv2.rectangle(org_rec, (250, 370), (405, 430), (0, 255, 0), thickness=2)
    for i in range(0, len(list_results)):
        t = list_results[i]
        x, y, w, h = list_boxes[i]
        cv2.putText(org_rec, t, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        match = re.match(r'^[\w]{6,7}$', t)
        if match:
            return t, org_rec
    return "Not Found", org_rec


def canny_result(image=None):
    blur = cv2.GaussianBlur(image, (KSIZE, KSIZE), SIGMA_X)
    canny = cv2.Canny(blur, THRESHOLD, MAX)
    return canny


def boundROI(image):
    h = len(image)
    w = len(image[0])
    x1 = int(w * 0.33)
    x2 = int(w * 0.66)
    y1 = int(h * 0.6)
    y2 = int(h * 0.9)
    return (x1, y1), (x2, y2)


def charimport():
    CHARDIR = "./22x44/"
    addrs = os.listdir(CHARDIR)

    char_map_list = []
    charlist = []
    for addr in addrs:
        char = cv2.imread(CHARDIR + addr)
        gray = cv2.cvtColor(char, cv2.COLOR_RGB2GRAY)
        char_map_list.append(gray)
        charlist.append(addr.split(".")[0])
    return char_map_list, charlist


char_map_list, charlist = charimport()


def character(imchar):
    resized = cv2.resize(imchar, (22, 44))
    sum = 0
    length = len(char_map_list)
    rate_list = []
    for mapIndex in range(0, length):
        char_map = char_map_list[mapIndex]
        for i in range(0, 44):  # row
            for j in range(0, 22):  # column
                if char_map[i, j] > 0 and resized[i, j] > 0:
                    sum += 1
                elif char_map[i, j] == 0 and resized[i, j] == 0:
                    sum += 1
        r = sum / (22 * 44)  # similarity
        rate_list.append(r)
        if r > 0.9:
            return charlist[mapIndex]
        sum = 0
    return charlist[rate_list.index(max(rate_list))]  # return the most similar char


def characterRecognition(image):
    (x1, y1), (x2, y2) = boundROI(image)
    ROI = image[y1:y2, x1:x2]

    zoomin = cv2.resize(ROI, (len(ROI[0]) * 4, len(ROI) * 4))
    gray = cv2.cvtColor(zoomin, cv2.COLOR_RGB2GRAY)
    ret, binarized = cv2.threshold(gray, 128, 256, cv2.THRESH_BINARY)
    canny = cv2.Canny(binarized, 256, 256)
    (contours, _) = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        rec = cv2.boundingRect(contour)
        x, y, w, h = rec
        r2 = w / h
        if 2.375 * 0.9 < r2 < 2.375 * 1.1:
            plate = binarized[y:y + h, x:x + w]
            plate_color = zoomin[y:y + h, x:x + w]
            canny_plate = cv2.Canny(plate, 0, 256, )
            (contours_char, _) = cv2.findContours(canny_plate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            rec_list = set()
            for contour_char in contours_char:
                rec_char = cv2.boundingRect(contour_char)
                rec_list.add(rec_char)

            rec_list = list(rec_list)
            rec_list.sort()

            text = ''
            for rec in rec_list:
                xx, yy, ww, hh = rec
                rr = hh / ww
                if (1.7 < rr < 2.2 and hh > len(plate) * 0.5) or (6.1 < rr < 6.4):  # number '1' hh/ww ~= 6.23
                    text += character(plate[yy:yy + hh, xx:xx + ww])
            if 5 < len(text):
                return text
    return "Not Found"


def displayROI(image):
    p1, p2 = boundROI(image)
    result = cv2.rectangle(image, p1, p2, (0, 0, 255))
    result = cv2.putText(result, "ROI", p1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return result
