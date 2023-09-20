import os
import cv2
import numpy as np

import dateset
regions_to_clear = [
            dateset.PHYSICAL_STRENGTH,
            dateset.NAVIGATION_BAR,
            dateset.BOX_SUMBER,
            dateset.UID
        ]
# 定义清除区域的函数
def clear_region_in_image(image, x1, y1, x2, y2):  
    result = image.copy()
    result[y1:y2, x1:x2] = 0
    return result

# 指定图像文件所在的目录
img_path = r'C:\Users\Administrator\Desktop\Sprict\images'

# 获取目录中的所有文件
image_files = [f for f in os.listdir(img_path) if f.endswith('.png')]  # 只处理扩展名为.jpg的图像文件

# 遍历图像文件并处理
for image_file in image_files:
    # 构建完整的图像文件路径
    image_file_path = os.path.join(img_path, image_file)
    
    # 读取图像
    image = cv2.imread(image_file_path)
    
    # 遍历清除区域
    for region in regions_to_clear:
        x1, y1, x2, y2 = region
        image = clear_region_in_image(image, x1, y1, x2, y2)
        output_file_path = os.path.join(img_path, image_file)
        cv2.imwrite(output_file_path, image)
    
    # 构建保存的文件路径（在同一目录中）
    
    
    # 保存处理后的图像
    
    
    print(f"已处理并保存: {output_file_path}")

print("处理完成。")
