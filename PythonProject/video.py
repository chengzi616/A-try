import cv2
import numpy as np

#读取照片
cap = cv2.VideoCapture("video.mp4")
if cap is None:
    print(" Not found")
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])


while True:
    ret, frame = cap.read()
    if not ret:  # 视频结束或读取失败
        break

#颜色分割
    # 转换为HSV颜色空间（便于颜色分割）
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 颜色分割：提取红色(棒棒糖）区域（合并两个区间）
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)


    #开运算
    kernel = np.ones((5,5),np.uint8)
    img_out = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    #找轮廓
    contours, _ = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for con in contours:
        area = cv2.contourArea(con)
        if area > 3000 or area < 1000:
            continue


        x, y, w, h = cv2.boundingRect(con)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        perimeter = cv2.arcLength(con, True)
        epsilon = 0.03 * perimeter
        approx = cv2.approxPolyDP(con, epsilon, True)

        cv2.polylines(frame,[approx], isClosed=True, color=(255, 0, 0), thickness=2  )
        cv2.imshow("Red Ball Tracking", frame)

            # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
cap.release()
cv2.destroyAllWindows()


