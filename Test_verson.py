import cv2

def image_similarity(image_path1, image_path2):
    # 读取两张图像
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    # 检查图像是否成功读取
    if img1 is None or img2 is None:
        return False

    # 使用均方差（Mean Squared Error）来比对图像
    mse = ((img1 - img2) ** 2).mean()

    # 计算相似度，MSE越小相似度越高
    similarity = 1 / (1 + mse)

    return similarity

# 两张图像的文件路径
image1_path = r"C:\Users\Administrator\Desktop\Sprict\images\task\Breakthrough.png"
image2_path = r"C:\Users\Administrator\Desktop\Sprict\images\task\Breakthrough_.png"

# 比对两张图像
similarity_score = image_similarity(image1_path, image2_path)

if similarity_score is not None:
    print(f'相似度：{similarity_score:.4f}')
else:
    print('图像读取失败或尺寸不匹配')
