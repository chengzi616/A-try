# import cv2
# img_bgr = cv2.imread("output.png")
# img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
# img_h, img_s, img_v = cv2.split(img_hsv)
# mask_h = cv2.inRange(img_h, 165, 179)
# mask_s = cv2.inRange(img_s, 50, 200)
# mask_v = cv2.inRange(img_v, 100, 255)
# mask_h_and_s = cv2.bitwise_and(mask_h, mask_s)
# mask = cv2.bitwise_and(mask_h_and_s, mask_v)
# img_out = cv2.bitwise_and(img_bgr, img_bgr, mask = mask)
# cv2.imshow("img", img_out)
# cv2.imwrite("img_out.png", img_out)
# cv2.waitKey(0)

import cv2
import numpy as np

path = r'C:\Users\user\PycharmProjects\PythonProject\11.jpeg'


def empty(a):
    # 获取滑动条的值（不需要返回）
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)


# 创建窗口和滑动条
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 19, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 110, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 240, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 153, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

# 只读取一次图片
img = cv2.imread(path)
if img is None:
    print("错误：无法加载图像，请检查路径")
    exit()

while True:
    # 实时获取滑动条的值
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    # 转换色彩空间并创建掩码
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    # 显示图像
    cv2.imshow("Original", img)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", imgResult)

    # 按ESC或q退出
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cv2.destroyAllWindows()