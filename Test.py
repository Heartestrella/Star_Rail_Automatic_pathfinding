import cv2
import numpy as np

def find_similar_center(image_path, template_path, threshold=0.8):
    # 读取原始图像和模板图像
    original_image = cv2.imread(image_path)
    template = cv2.imread(template_path)

    # 使用模板匹配方法
    result = cv2.matchTemplate(original_image, template, cv2.TM_CCOEFF_NORMED)

    # 获取相似度大于阈值的匹配位置
    locations = np.where(result >= threshold)

    # 获取匹配中心点坐标
    center_points = []
    for pt in zip(*locations[::-1]):
        center_x = pt[0] + template.shape[1] // 2
        center_y = pt[1] + template.shape[0] // 2
        center_points.append((center_x, center_y))

    return center_points

# 使用示例
image_path = 'original_image.jpg'
template_path = 'template_image.jpg'
similar_centers = find_similar_center(image_path, template_path)

# 输出相似的中心点坐标
for center in similar_centers:
    print(f'Similar Center Point: {center}')
