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




# import cv2
# import numpy as np
#
# # 读取照片
# picture = cv2.imread("work.PNG")
# if picture is None:
#     raise FileNotFoundError("Image not found")
#
# # 颜色分割 (修正阈值范围)
# hsv = cv2.cvtColor(picture, cv2.COLOR_BGR2HSV)
# # 定义HSV范围 (H:97-150, S:2-138, V:209-255)
# lower_bound = np.array([0, 0, 241])
# upper_bound = np.array([179, 207, 255])
# mask = cv2.inRange(hsv, lower_bound, upper_bound)
#
# # 开运算 (直接在掩码上操作)
# kernel = np.ones((5, 5), np.uint8)
# mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#
# # 找轮廓 (使用二值掩码)
# contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
# # 在原始图像上绘制结果
# result = picture.copy()
# for con in contours:
#     area = cv2.contourArea(con)
#     if area < 100:
#         continue
#
#     # 绘制边界矩形
#     x, y, w, h = cv2.boundingRect(con)
#     cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#     # 绘制多边形近似
#     perimeter = cv2.arcLength(con, True)
#     epsilon = 0.03 * perimeter
#     approx = cv2.approxPolyDP(con, epsilon, True)
#     cv2.polylines(result, [approx], isClosed=True, color=(255, 0, 0), thickness=2)
#
# # 显示并保存结果 (放在循环外)
# cv2.imshow("Result", result)
# cv2.imwrite("result.PNG", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()