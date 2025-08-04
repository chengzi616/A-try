import cv2
import numpy as np

#读取照片
picture = cv2.imread("work.PNG")
if picture is None:
    raise FileNotFoundError("Image not found")

#颜色分割
hsv = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
mask_h = cv2.inRange(h,0, 179)
mask_s = cv2.inRange(s,0, 207)
mask_v = cv2.inRange(v,241, 255)
mask_s_and_v = cv2.bitwise_and(mask_s, mask_v)
mask = cv2.bitwise_and(mask_h, mask_s_and_v)


#开运算
kernel = np.ones((5,5),np.uint8)
img_out = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

#找轮廓
result = picture.copy()
contours, _ = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for con in contours:
    area = cv2.contourArea(con)
    if area < 100:
        continue

    x, y, w, h = cv2.boundingRect(con)
    cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)

    perimeter = cv2.arcLength(con, True)
    epsilon = 0.03 * perimeter
    approx = cv2.approxPolyDP(con, epsilon, True)

    cv2.polylines(result,[approx], isClosed=True, color=(255, 0, 0), thickness=2  )
cv2.imshow("picture", result)
cv2.imwrite("picture.PNG", result)
cv2.waitKey(0)
cv2.destroyAllWindows()




