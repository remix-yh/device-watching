import cv2
import io
from PIL import Image
import numpy as np

ON_OFF_JUDGE_COUNT = 5  # 何回閾値を上回った、または下回ったらステータスを変えるか
VALUE_THRESH = 150      # 明度(Value)の閾値
DEVICE_ID = 1           # 使用するデバイスのID

cap = cv2.VideoCapture(DEVICE_ID)

# 複数領域を判定できるように、リストにする
bbox_list = []
bbox1 = { 'id' : 1, 'x' : 150, 'y' : 150, 'width': 100, 'height' : 100 }
bbox_list.append(bbox1)

# 領域ごとのステータスを保持する
bbox_status_dict = {}
for bbox in bbox_list:
    bbox_status_dict[bbox['id']] = {"count":0, "status": False }

while True:
    ret, frame = cap.read()
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    for bbox in bbox_list:
        bbox_status = bbox_status_dict[bbox['id']]
        value = np.average(hsv_image[bbox['y']:bbox['y']+bbox['height'],bbox['x']:bbox['x']+bbox['width'],2])

        if bbox_status["status"]:
            if VALUE_THRESH > value:
                bbox_status["count"] = bbox_status["count"] + 1
        else:
            if VALUE_THRESH <= value:
                bbox_status["count"] = bbox_status["count"] + 1

        if bbox_status["count"] >= ON_OFF_JUDGE_COUNT:
            bbox_status["status"] = not(bbox_status["status"])
            bbox_status["count"] = 0

        if bbox_status["status"]:
            cv2.putText(frame,'Stopping',(50,50),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 200), thickness=2)
        else:
            cv2.putText(frame,'Running',(50,50),cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 200, 0), thickness=2)

        cv2.rectangle(frame, (bbox['x'], bbox['y']), (bbox['x']+bbox['width'], bbox['x']+bbox['height']), (0, 0, 255), 2)
        
        cv2.putText(frame,'v={0}'.format(value),(bbox['x'],bbox['y']),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), thickness=1)
        
    cv2.imshow('camera capture', frame)
    
    k = cv2.waitKey(1000)
    if k == 27: # ESCキーで終了
        break

cap.release()
cv2.destroyAllWindows()