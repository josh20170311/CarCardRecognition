import cv2
import pytesseract
import re

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


def characterRecognition(t1=100, t2=200):
    img_snapshot = cv2.imread("images/snapshot.png")
    img_cut = img_snapshot[370:430, 250:400]
    cv2.imshow("cut", img_cut)
    cv2.imshow("snapshot", img_snapshot)
    cv2.imwrite("cut.jpg", img_cut)
    cv2.waitKey(0)


def makeROI(image):
    h = len(image)
    w = len(image[0])
    x1 = int(w * 0.33)
    x2 = int(w * 0.66)
    y1 = int(h * 0.6)
    y2 = int(h * 0.9)
    result = cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255))
    result = cv2.putText(result, "ROI", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return result
# characterRecognition()
