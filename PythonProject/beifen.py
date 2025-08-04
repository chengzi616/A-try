import cv2 as cv
import numpy as np  # 必须导入numpy


# ---------------------- 1. 颜色检测函数（和之前一致，无需修改） ----------------------
def detect_hsv_color(img, minh, maxh, mins, maxs):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h_mask1 = cv.threshold(hsv[:, :, 0], maxh, 255, cv.THRESH_BINARY_INV)[1]
    h_mask2 = cv.threshold(hsv[:, :, 0], minh, 255, cv.THRESH_BINARY)[1]
    if minh < maxh:
        h_mask = h_mask1 & h_mask2
    else:
        h_mask = h_mask1 | h_mask2
    s_mask = cv.inRange(hsv[:, :, 1], mins, maxs)
    return h_mask & s_mask


# ---------------------- 2. 主流程（修改关键行：np.int0 → np.int64） ----------------------
if __name__ == "__main__":
    # 1. 加载图像（替换为你的路径）
    img = cv.imread("output.png")
    if img is None:
        print("图片没找到！检查路径。")
        exit()

    # 2. 颜色检测（调整参数改检测颜色）
    mask = detect_hsv_color(img, minh=95, maxh=110, mins=180, maxs=255)

    # 3. 找轮廓
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # 4. 遍历轮廓，画最小矩形和多边形
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area < 100:  # 过滤小噪声
            continue

        # ---------- ① 最小旋转矩形 ----------
        rect = cv.minAreaRect(cnt)  # 计算最小旋转矩形
        box = cv.boxPoints(rect)  # 转成4个顶点（浮点数）
        box = np.int64(box)  # ← 关键修改！把浮点数转成64位整数（替代np.int0）
        cv.drawContours(img, [box], 0, (0, 255, 0), 2)  # 画绿色旋转矩形

        # ---------- ② 多边形拟合 ----------
        perimeter = cv.arcLength(cnt, True)
        epsilon = 0.02 * perimeter
        approx = cv.approxPolyDP(cnt, epsilon, True)
        cv.drawContours(img, [approx], 0, (255, 0, 0), 2)  # 画蓝色多边形

    # 5. 显示结果
    cv.imshow("检测结果", img)
    cv.waitKey(0)
    cv.destroyAllWindows()



