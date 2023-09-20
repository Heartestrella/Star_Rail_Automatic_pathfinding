import pyautogui
import pygetwindow as gw
import cv2
import time
import numpy as np  
import dateset
import time
import os
import json
# 定义游戏窗口的标题，根据您的游戏窗口标题进行调整
game_window_title_en = "Star Rail"
game_window_title_zh = "崩坏：星穹铁道"
Map_code = False #默认状态
regions_to_clear = [
            dateset.PHYSICAL_STRENGTH,
            dateset.NAVIGATION_BAR,
            dateset.BOX_SUMBER,
            dateset.UID
        ]

current_dir = os.path.dirname(__file__)

def is_game_window_focused():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        print("Active Window Title:", active_window.title)  # 调试信息：打印当前活动窗口标题
        if active_window.title == game_window_title_en or active_window.title == game_window_title_zh:
            return True
    return False

def is_map_page(screen_image):
    img_path  = os.path.join(current_dir, 'images')
    image_files = [f for f in os.listdir(img_path) if f.endswith('.png')]
    for i in image_files:
        print(i)
        # 构建模板图像的完整路径
        template_path = os.path.join(img_path, i)
        # 读取模板图像
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.78  # 设置匹配阈值，可以根据需要进行调整

        locations = cv2.findNonZero((result >= threshold).astype(int))
        print(locations)
        print(result)
        if locations is not None:
            return True
        else:
            return False


def click(Map_code,img_name):
    #非yolov获取坐标时
    # time.sleep(1)
    # pyautogui.moveTo(dateset.BODY_OF_SEA[0],dateset.BODY_OF_SEA[1]) 
    # pyautogui.click()
    
    # time.sleep(1)
    # pyautogui.moveTo(dateset.BODY_OF_SEA[2],dateset.BODY_OF_SEA[3])
    # pyautogui.click()

    # time.sleep(1)
    # pyautogui.moveTo(dateset.TP[0],dateset.TP[1])
    # pyautogui.click()
    if Map_code:
        img_name = f'{img_name}.png'

        detect_script_path = os.path.join(current_dir, 'yolov5_Star', 'detect.py')
        pt_mod_path = os.path.join(current_dir, 'yolov5_Star', 'Star.pt')
        json_path = os.path.join(current_dir, 'yolov5_Star', 'source.json')
        print(json_path)
        shell = f'python {detect_script_path} --weights {pt_mod_path} --source {img_name}'
        os.system(shell)
        with open(json_path, 'r') as json_file:
            data = json.load(json_file)
        anchor_point_data = None
        for item in data:
            if item["class_name"] == "Anchor_point":
                anchor_point_data = item
                break
        center = anchor_point_data['center']
        print(center)
        os.remove(img_name)
        pyautogui.moveTo(int(center[0]),int(center[1]))
        pyautogui.click()
        time.sleep(0.7)
        pyautogui.moveTo(dateset.TP[0],dateset.TP[1])
        pyautogui.click()

def clear_region_in_image(image, x1, y1, x2, y2):  
    result = image.copy()
    result[y1:y2, x1:x2] = 0
    return result

while True:
    if is_game_window_focused():
        print("已进入到游戏")
        screen = pyautogui.screenshot()  # 获取屏幕截图
        screen_np = np.array(screen)  # 将屏幕截图转换为NumPy数组
        
        # screen_np = clear_region_in_image(screen_np,dateset.PHYSICAL_STRENGTH[0],dateset.PHYSICAL_STRENGTH[1],dateset.PHYSICAL_STRENGTH[2],dateset.PHYSICAL_STRENGTH[3])
        # screen_np = clear_region_in_image(screen_np,dateset.NAVIGATION_BAR[0],dateset.NAVIGATION_BAR[1],dateset.NAVIGATION_BAR[2],dateset.NAVIGATION_BAR[3])
        # screen_np = clear_region_in_image(screen_np,dateset.BOX_SUMBER[0],dateset.BOX_SUMBER[1],dateset.BOX_SUMBER[2],dateset.BOX_SUMBER[3])
        # screen_np = clear_region_in_image(screen_np,dateset.UID[0],dateset.UID[1],dateset.UID[2],dateset.UID[3])
        # 定义要清除的区域坐标

        
        if Map_code == False:
            img_name = time.time()
            for region in regions_to_clear:
                x1, y1, x2, y2 = region
                screen_np = clear_region_in_image(screen_np, x1, y1, x2, y2)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)  # 转换为灰度图像

            if not is_map_page(screen_gray):
                print("不是地图页面")
                print("已输入 'm'")  # 调试信息：打印按下 'm' 键
                pyautogui.press('m')
                Map_code = True
                screen.save(f'{img_name}.png')
                #cv2.imwrite(f'{img_name}.png', np.array(pyautogui.screenshot()))   #使用opencv保存图片出现颜色异常的情况
                click(Map_code,img_name)
            else:
                print("已进入地图页面")
                screen.save(f'{img_name}.png')
              #  cv2.imwrite(f'{img_name}.png', np.array(pyautogui.screenshot())) 
                Map_code = True
                click(Map_code,img_name)
                

    time.sleep(1)