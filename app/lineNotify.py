import requests
import cv2
from datetime import datetime

last_notify_time = datetime.min

def lineNotify(img,interval=5):
    global last_notify_time
    now = datetime.now()
    if (now - last_notify_time).total_seconds() >= interval:
        url = 'https://notify-api.line.me/api/notify'
        token = '83mhTEJUPROyicFuGtarhfR5rkHz4YI7iHVtytToh5m'  # 設定 LINE Notify 權杖
        headers = {
            'Authorization': 'Bearer ' + token
        }
        data = {
            'message': '智慧偵測已偵測到人像，請使用者留意！'
        }
        _, img_encoded = cv2.imencode('.jpg', img)  # 將圖片轉換為二進位編碼
        imageFile = {'imageFile': img_encoded.tobytes()}  # 設定圖片資訊
        requests.post(url, headers=headers, data=data, files=imageFile)
        last_notify_time = now