import requests
import cv2
import time
import re

base = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0'
recog_url = f'{base}/recognizeText?mode=Printed'
key = '6d95329a7ca14f099798f0ddf30d5c1e'
headers_result = {'Ocp-Apim-Subscription-Key': key}  # 查看結果的請求標頭
headers_stream = {'Ocp-Apim-Subscription-Key': key,  # 辨識的請求標頭
                  'Content-Type': 'application/octet-stream'}


def get_license(img):
    img_encode = cv2.imencode('.jpg', img)[1]  # 將 img 編碼為 JPEG 格式，[1]返回資料, [0]返回是否成功
    img_bytes = img_encode.tobytes()  # 再將資料轉為 bytes, 此即為要傳送的資料
    Request_recognition = requests.post(recog_url,  # 發出 POST
                                        headers=headers_stream,
                                        data=img_bytes)
    if Request_recognition.status_code != 202:  # 202 代表接受請求
        print(Request_recognition.json())
        return '請求失敗'
    # --↓↓辨識請求成功↓↓--#
    result_url = Request_recognition.headers['Operation-Location']  # 取得查看結果的請求路徑
    Requset2 = requests.get(result_url, headers=headers_result)  # 發出 GET 請求
    while Requset2.status_code == 200 and Requset2.json()['status'] != 'Succeeded':
        Requset2 = requests.get(result_url, headers=headers_result)  # 繼續發出 GET
        time.sleep(0.5)
        print('status: ', Requset2.json()['status'])  # 顯示辨識狀態
    # --↓↓辨識完成↓↓--#
    carcard = ''  # 紀錄車牌
    lines = Requset2.json()['recognitionResult']['lines']
    for i in range(len(lines)):
        text = lines[i]['text']  # 取得辨識文字
        match1 = re.match(r'^[\w]{2,4}[-. ][\w]{2,4}$', text)  # 匹配是否為車牌格式
        if match1 != None:  # 匹配成功
            carcard = match1.group()
            return carcard
    if carcard == '':  # 無匹配結果
        return '找不到車牌'
