import cv2
import numpy as np
import imutils
import lineNotify


def load_yolov4_model():
    net = cv2.dnn.readNet("app/yolo/yolov4.weights", "app/yolo/yolov4.cfg")
    return net

def yolo_detect(frame, net, classes, colors):
    img = cv2.resize(frame, None, fx=0.5, fy=0.5)
    height, width, channels = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())
    
    boxes = []
    confidences = []
    class_ids = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                if class_id == 0:
                    lineNotify.lineNotify(img)



    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.3)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[class_ids[i] % 7]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y - 5), font, 1, color, 1)
    
    return img

def main(mode="video"):
    with open("app/yolo/family.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 255, 255), (255, 255, 255), (200, 200, 200), (200, 0, 200)]
    net = load_yolov4_model()
    
    VIDEO_IN = None
    if mode == "pic":
        VIDEO_IN = cv2.VideoCapture('app/img/2.jpg')
    elif mode == "video":
        VIDEO_IN = cv2.VideoCapture(0)
    elif mode == "ipcam":
        VIDEO_IN = cv2.VideoCapture("192.168.1.100:8080/video")
    else:
        print("mode error!")
        return


    while True:
        hasFrame, frame = VIDEO_IN.read()
        if not hasFrame:
            break
        
        img = yolo_detect(frame, net, classes, colors)
        cv2.imshow('Frame', imutils.resize(img, width=400))
        
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    
    VIDEO_IN.release()
    cv2.destroyAllWindows()

# 調用 main 函式，mode = "pic" 表示處理照片，mode="video"表示處理即時影像,mode="ipcam"表示影像來源為ip監視器
main(mode="video")
