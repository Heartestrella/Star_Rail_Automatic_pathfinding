import os
import cv2
import numpy as np
import StarDateset as dateset

regions_to_clear = [
    dateset.PHYSICAL_STRENGTH,
    dateset.NAVIGATION_BAR,
    dateset.BOX_SUMBER,
    dateset.UID,
]
BOX_SUMBER = dateset.BOX_SUMBER
x1 = BOX_SUMBER[0]
y1 = BOX_SUMBER[1]
x2 = BOX_SUMBER[2]
y2 = BOX_SUMBER[3]


def dhash(image, hash_size=8):
    # 缩放图像尺寸，使其变为hash_size x (hash_size + 1)大小
    resized = cv2.resize(image, (hash_size, hash_size + 1))
    # 计算每一列的平均值，生成哈希值
    diff = resized[1:, :] > resized[:-1, :]
    return sum([2**i for (i, v) in enumerate(diff.flatten()) if v])


def hamming_distance(hash1, hash2):
    # 计算汉明距离，即不同位的数量
    return bin(hash1 ^ hash2).count("1")


def similarity(image1, image2, hash_size=8):
    # 计算图像的dHash值
    hash1 = dhash(image1, hash_size)
    hash2 = dhash(image2, hash_size)

    # 计算汉明距离
    distance = hamming_distance(hash1, hash2)

    # 计算相似度（值越小表示越相似）
    max_distance = hash_size * (hash_size + 1) // 2
    similarity = 1 - (distance / max_distance)

    return similarity


def clear_region_in_image(image, x1, y1, x2, y2):
    result = image.copy()
    result[y1:y2, x1:x2] = 0
    return result


def map():
    # 定义清除区域的函数

    # 指定图像文件所在的目录
    img_path = r"C:\Users\Administrator\Desktop\Sprict\images\box"

    # 获取目录中的所有文件
    image_files = [
        f for f in os.listdir(img_path) if f.endswith(".png")
    ]  # 只处理扩展名为.jpg的图像文件

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

        print(f"已处理并保存: {output_file_path}")

    print("处理完成。")


def clear_region_in_image(image, x1, y1, x2, y2):
    result = image.copy()
    result = result[y1:y2, x1:x2]
    # result[y1:y2, x1:x2] = 0
    return result



x1, y1, x2, y2 = dateset.FIGHT
#x1, y1, x2, y2 = [16, 11, 144, 41]

task_images = r"C:\Users\Administrator\Desktop\Sprict\images\task\Task_ui\3BF5DBBAE3157C6C8BA8F9DA9896F52B.png"
#task_images = r"C:\Users\Administrator\Desktop\Sprict\images\task\B3C67BA2877AEB36A2E88E9E77BB4636.png"
image = cv2.imread(task_images)
from tools_star import Tools

result_image = clear_region_in_image(image, x1, y1, x2, y2)
#result_image = clear_region_in_image(image, x1, y1, x2, y2)
# output_file = rf"C:\Users\Administrator\Desktop\Sprict\images\box\{s}_{p}_.png"
output_file =  r"C:\Users\Administrator\Desktop\Sprict\images\task\Task_ui\Gold.png"
cv2.imwrite(output_file, result_image)
print("Finsle")
# from tools_star import Tools

# input_path = (
#     r"C:\Users\Administrator\Desktop\Sprict\images\task\9217E640113BA67EE90CEC19528BB7E6.png"
# )
# x1, y2, x2, y2 = [611, 410, 903, 883]
# result_image = clear_region_in_image(cv2.imread(input_path), x1, y1, x2, y2)
# cv2.imwrite(f'{input_path}_', result_image)
# print("yes")
