import cv2
import numpy as np

def main():
    # 1. 配置：选择视频源（0为摄像头，或替换为视频路径如"video.mp4"）
    cap = cv2.VideoCapture("video.mp4")  # 摄像头
    # cap = cv2.VideoCapture("red_ball_video.mp4")  # 本地视频

    # 2. 定义红色在HSV空间的范围（根据实际环境调整）
    # 红色在HSV中分为两个区间（0-10和170-179）
    lower_red1 = np.array([0, 120, 70])    # 低范围
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])  # 高范围
    upper_red2 = np.array([179, 255, 255])

    while True:
        # 3. 读取视频帧
        ret, frame = cap.read()
        if not ret:  # 视频结束或读取失败
            break

        # 4. 转换为HSV颜色空间（便于颜色分割）
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 5. 颜色分割：提取红色区域（合并两个区间）
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = cv2.bitwise_or(mask1, mask2)  # 合并两个红色掩码

        # 6. 形态学操作：去除噪声（开运算）
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # 7. 查找轮廓（只保留外轮廓，减少计算量）
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 8. 遍历轮廓，筛选有效目标并框选
        for cnt in contours:
            # 过滤小面积轮廓（去除噪声）
            area = cv2.contourArea(cnt)
            if area < 100:  # 面积阈值，根据目标大小调整
                continue

            # ① 最小外接矩形（轴对齐）
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 绿色矩形

            # ② 多边形拟合（逼近轮廓，更贴合形状）
            # 计算轮廓周长，epsilon为拟合精度（周长的2%）
            perimeter = cv2.arcLength(cnt, closed=True)
            epsilon = 0.02 * perimeter
            approx = cv2.approxPolyDP(cnt, epsilon, closed=True)
            # 绘制多边形（蓝色）
            cv2.polylines(frame, [approx], isClosed=True, color=(255, 0, 0), thickness=2)

        # 9. 实时显示处理结果
        cv2.imshow("Red Ball Tracking", frame)

        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()