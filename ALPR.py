import cv2
import pytesseract
import re

def alpr(imagefile="TR/images/c13.jpg" , image=None):

    list_results = []
    print("imagefile = ", imagefile)
    org = image
    blur = cv2.GaussianBlur(org, (3, 3), 10)
    canny = cv2.Canny(blur, 29, 100)
    (contours, _) = cv2.findContours(canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(canny, contours, -1, (255, 0, 0), thickness=1)
    # cv2.imshow("canny", canny)
    for i in range(0, len(contours)):
        # print(i)
        rec = cv2.boundingRect(contours[i])  # draw a rec
        # print(rec)
        x, y, w, h = rec
        r = w/h
        if r > 2.375*1.1 or r < 2.375*0.9 or h < 20 or w < 50:
            continue
        # print(r)
        cv2.rectangle(org.copy(), (rec[0], rec[1]), (rec[0] + rec[2], rec[1] + rec[3]), (0, 0, 255), 0)
        # cv2.imshow("org", org)
        cut = org[y:y+h, x:x+w]
        t = pytesseract.image_to_string(cut, config="-l eng --oem 1 --psm 7")  # OCR
        list_results.append(t)
        print(t)
        # cv2.imshow("org", cut)
        # k = cv2.waitKey(0)
        # if k == 13:
           # cv2.imshow("org", org)
           # cv2.waitKey(0)
           # break
    for x in list_results:
        match = re.match(r'^[\w]{2,4}[., ][\w]{2,4}$', x)
        if match:
            return x
    return "Not found"
