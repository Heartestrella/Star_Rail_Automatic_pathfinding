class Tools:
    import numpy as np

    def is_game_window_focused() -> bool:
        import pygetwindow as gw

        game_window_title_en = "Star Rail"
        game_window_title_zh = "崩坏：星穹铁道"
        active_window = gw.getActiveWindow()
        if active_window is not None:
            print("Active Window Title:", active_window.title)  # 调试信息：打印当前活动窗口标题
            if (
                active_window.title == game_window_title_en
                or active_window.title == game_window_title_zh
            ):
                return True
        return False

    def clear_corp_in_image(image: np, x1: int, y1: int, x2: int, y2: int) -> np:
        result = image[y1:y2, x1:x2]
        return result

    def hamming_distance(hash1, hash2):
        return bin(int(hash1, 16) ^ int(hash2, 16)).count("1")

    def compute_ahash_similarity(hash1, hash2):
        distance = Tools.hamming_distance(hash1, hash2)
        similarity = 1 - (distance / 64.0)

        return similarity

    def compute_ahash(image: np) -> str:
        from PIL import Image
        import imagehash

        image = Image.fromarray(image)
        ahash = imagehash.average_hash(image)
        ahash_string = str(ahash)

        return ahash_string

    def clear_region_in_image(image: np, x1: int, y1: int, x2: int, y2: int) -> np:
        result = image.copy()
        result[y1:y2, x1:x2] = 0
        return result

    def is_map_page(screen_image: np) -> bool:
        import os, cv2

        img_path = os.path.join(os.path.dirname(__file__), "images")
        image_files = [f for f in os.listdir(img_path) if f.endswith(".png")]
        for i in image_files:
            # 构建模板图像的完整路径
            template_path = os.path.join(img_path, i)
            # 读取模板图像
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            result = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)

            threshold = 0.78  # 设置匹配阈值，可以根据需要进行调整

            locations = cv2.findNonZero((result >= threshold).astype(int))
            #  print(result[0][0])
            if locations is not None:
                return True
            else:
                return False

    def move_and_click(coordinate) -> None:
        import pyautogui

        pyautogui.moveTo(coordinate[0], coordinate[1])
        pyautogui.click()

    
