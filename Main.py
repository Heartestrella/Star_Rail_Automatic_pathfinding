import pyautogui
import pygetwindow as gw
import cv2
import time
import numpy as np
import StarDateset as dateset
import time
import os
import json
import imagehash
from PIL import Image
import tkinter as tk
import threading
import ouput_show
from tools_star import Tools

zoom_type = False
# 定义游戏窗口的标题，根据您的游戏窗口标题进行调整

Map_code = False  # 默认状态
regions_to_clear = [
    dateset.PHYSICAL_STRENGTH,
    dateset.NAVIGATION_BAR,
    dateset.BOX_SUMBER,
    dateset.UID,
]
MAP_DIST = dateset.MAP_DIST
current_dir = os.path.dirname(__file__)
Down_type = False  # 用于尝试向下地图查找
Iin = None
BOX_SUMBER = None
MAP_BOX = []
Map_init = False
hotkey_combination = ["ctrl", "shift", "a"]

print("\033[91m The Star Rail's box ai by istrashguy \033[0m ")
print(
    "\033[91m Project Url: https://github.com/istrashguy/Star_Rail_Automatic_pathfinding \033[0m"
)


def clear_corp_in_image(image, x1, y1, x2, y2):
    result = image[y1:y2, x1:x2]
    return result


def hamming_distance(hash1, hash2):
    return bin(int(hash1, 16) ^ int(hash2, 16)).count("1")


def compute_ahash_similarity(hash1, hash2):
    distance = hamming_distance(hash1, hash2)
    similarity = 1 - (distance / 64.0)

    return similarity


def compute_ahash(image):
    image = Image.fromarray(image)
    ahash = imagehash.average_hash(image)
    ahash_string = str(ahash)

    return ahash_string


def wherearein(screen_image, img_path: list):
    screen_image = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
    for i in img_path:
        template = cv2.imread(i, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)

        threshold = 0.7

        locations = cv2.findNonZero((result >= threshold).astype(int))

        if locations is not None:
            return [True, i]
    return [False, None]


def draw_and_go():
    print("已经进入了绘制模式！")


def TP_click(BOX_SUMBER: dict, wherein: tuple, boxtype: bool) -> None:
    A_ = tuple(dateset.A_DRAGTO_B[:2])
    B_ = tuple(dateset.A_DRAGTO_B[2:4])
    print(f"wherein:{wherein}")
    global Down_type, MAP_BOX, zoom_type
    if zoom_type == False:
        pyautogui.moveTo(dateset.ZOOM_)
        pyautogui.click()
        zoom_type = True

    

    def get_next_coordinate(Previous_map: str):
        Previous_map_coordinate = getattr(dateset, Previous_map.upper())
        print(f"下一个地图:{Previous_map},下一个地图坐标:{Previous_map_coordinate}")
        Tools.move_and_click(Previous_map_coordinate)
        print(f"已到达:{Previous_map}")
        box_sumber(Map_code)
        time.sleep(0.5)

    # print("In TP click    ", BOX_SUMBER)
    

    parent_map, submap = wherein
    print(f"wherein: {wherein}")
    MAP_LIST = MAP_DIST[parent_map]

    if len(BOX_SUMBER) != 0:
        if submap != "Main_control_warehouse" and submap != "Viewing_car":
            print(f"MAP_BOX:{MAP_BOX}")
            if not boxtype:
                newest_file = None
                newest_timestamp = 0
                time.sleep(1)

                detect_script_path = os.path.join(
                    current_dir, "yolov5_Star", "detect.py"
                )
                pt_mod_path = os.path.join(current_dir, "yolov5_Star", "Star.pt")
                json_path = os.path.join(current_dir, "yolov5_Star", "source.json")
                pyautogui.screenshot().save("TARGET.PNG")

                shell = f"python {detect_script_path} --weights {pt_mod_path} --source TARGET.PNG"
                os.system(shell)
                print(shell)
                with open(json_path, "r") as json_file:
                    data = json.load(json_file)

                anchor_point_data = next(
                    (item for item in data if item["class_name"] == "Anchor_point"),
                    None,
                )

                if anchor_point_data:
                    center = anchor_point_data["center"]
                    print(center)
                    os.remove("TARGET.PNG")
                    Tools.move_and_click(center)
                    time.sleep(0.7)
                    Tools.move_and_click(dateset.TP)
                    draw_and_go()
            else:
                Previous_map = list(BOX_SUMBER.keys())[0]
                index = MAP_LIST.index(submap.capitalize())

                # 如果不在最底层
                if index != len(MAP_LIST):
                    if index + 1 == 8 and Down_type == False:
                        pyautogui.moveTo(A_)
                        time.sleep(0.2)
                        pyautogui.dragTo(B_, duration=0.5, button="left")
                        Down_type = True
                    # Previous_map = MAP_LIST[index + 1]
                    get_next_coordinate(Previous_map)
                # 如果在最底层
                elif index == len(MAP_LIST):
                    # Previous_map = MAP_LIST[index - 1]
                    get_next_coordinate(Previous_map)
        else:
            if submap == "Main_control_warehouse":
                index = MAP_LIST.index(submap)
                if int(index) == 0:
                    Previous_map = MAP_LIST[index + 1]
                    get_next_coordinate(Previous_map)
            elif submap == "Viewing_car":
                print(f"当前为TP_click的{parent_map}的Viewing_car模式")
                par_list = MAP_DIST[parent_map]
                if parent_map == "SPACE_STATION":
                    Previous_map = MAP_LIST[2]
                    get_next_coordinate(Previous_map)

                    box_sumber(Map_code)
                # elif parent_map == "Yalilo_VI":
                else:
                    Previous_map = MAP_LIST[0]
                    get_next_coordinate(Previous_map)
    else:
        print("当前星球已探索完毕")


Cost_Box = None
Cost_Box_sumber = None


def box_sumber(Map_code):
    global Cost_Box, Cost_Box_sumber,Map_init
    SPACE_STATION_BAR = (
        r"C:\Users\Administrator\Desktop\Sprict\images\box\SPACE_STATION.png"
    )
    YALUOLI_BAR = r"C:\Users\Administrator\Desktop\Sprict\images\box\Yalilo_VI.png"
    sleep_code = False
    if Map_code:
        img_path = r"C:\Users\Administrator\Desktop\Sprict\images\box"
        image_files = [f for f in os.listdir(img_path) if f.endswith(".png")]
        time.sleep(1)
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)
        screen_bar = screen_np.copy()
        barx1, bary1, barx2, bary2 = [100, 68, 290, 92]
        barimg = clear_corp_in_image(screen_bar, barx1, bary1, barx2, bary2)
        bool1, Iin = wherearein(barimg, [SPACE_STATION_BAR, YALUOLI_BAR])
        if bool1 and Iin != None:
            Iin = Iin.split("\\")[-1].split(".")[0]

            if Iin == "Yalilo_VI":
                BOX_SUMBER = dateset.BOX_SUMBER_[Iin]
            elif Iin == "SPACE_STATION":
                BOX_SUMBER = dateset.BOX_SUMBER_[Iin]

        box_completed = False
        # outer_key:主地图 outer_value:子地图
        #        print(BOX_SUMBER)
        if Cost_Box == None and Cost_Box_sumber == None:
            Cost_Box = BOX_SUMBER
            Cost_Box_sumber = len(Cost_Box)
        box_sumber_int = 0
        print(f"CONST_BOX_SMR:{Cost_Box_sumber}")
        if not Map_init:
            A_ = tuple(dateset.A_DRAGTO_B[:2])
            B_ = tuple(dateset.A_DRAGTO_B[2:4])
            pyautogui.moveTo(B_)
            time.sleep(0.2)
            pyautogui.dragTo(A_, duration=0.5, button="left")
            time.sleep(0.2)
            Tools.move_and_click([1500, 340])
            Map_init = True

        for inner_key, inner_value in BOX_SUMBER.items():
            # print(inner_value)
            # print(box_sumber_int)
            x1, y1, x2, y2 = inner_value
            print(f"Inner_value: {inner_value}")
            # print(inner_value)
            # print(inner_key)
            for image_file in image_files:
                image_file_path = os.path.join(img_path, image_file)
                image = cv2.imread(image_file_path)
                screen_gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
                screen_gray_ = clear_corp_in_image(screen_gray, x1, y1, x2, y2)

                ahash1 = compute_ahash(screen_gray_)
                ahash2 = compute_ahash(screen_gray2)
                #   print("当前文件:" + image_file)
                # print(
                #     f"Ahash1:{ahash1},Ahash2:{ahash2},当前文件:{image_file},Ahash1 Shape:{screen_gray_.shape},Ahash2 Shape:{screen_gray2.shape}"
                # )
                # if screen_gray_.shape == screen_gray2.shape:
                #     cv2.imshow("Image 1", screen_gray_)
                #     cv2.imshow("Image 2", screen_gray2)
                #     cv2.waitKey(0)
                #     cv2.destroyAllWindows()
                if ahash1 == ahash2 and screen_gray_.shape == screen_gray2.shape:
                    print(f"{inner_key}宝箱已开完")
                    MAP_BOX.append(inner_key)
                    print("当前文件:" + image_file)
                    print(f"当前位于{Iin}的{inner_key}")
                    del BOX_SUMBER[inner_key]
                    TP_click(BOX_SUMBER, (Iin, inner_key), boxtype=True)
                    sleep_code = True
                    box_completed = True
                    break
                else:
                    #  print("Bebug Mode")
                    # 以下用于判断是否位于主控舱段或观景车厢
                    x1_, y1_, x2_, y2_ = [1448, 304, 1618, 359]
                    corp_screen_gray = clear_corp_in_image(
                        cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY), x1_, y1_, x2_, y2_
                    )
                    Ahash1 = compute_ahash(corp_screen_gray)
                    image = cv2.imread("./images/box/Main_control_warehouse.png")
                    Ahash2 = compute_ahash(
                        cv2.cvtColor(
                            image,
                            cv2.COLOR_BGR2GRAY,
                        )
                    )
                    if Ahash1 == Ahash2:
                        print(f"当前位于{Iin}的Main_control_warehouse")
                        TP_click(
                            BOX_SUMBER,
                            (Iin, "Main_control_warehouse"),
                            boxtype=True,
                        )
                        box_completed = True
                        break
                    else:
                        x1_, y1_, x2_, y2_ = [1452, 215, 1603, 252]
                        Ahash1 = compute_ahash(
                            clear_corp_in_image(
                                cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY),
                                x1_,
                                y1_,
                                x2_,
                                y2_,
                            )
                        )
                        image = cv2.imread("./images/box/Viewing_car.png")
                        Ahash2 = compute_ahash(
                            cv2.cvtColor(
                                image,
                                cv2.COLOR_BGR2GRAY,
                            )
                        )
                        if Ahash1 == Ahash2:
                            print(f"当前位于{Iin}的Viewing_car")
                            TP_click(
                                BOX_SUMBER,
                                (Iin, "Viewing_car"),
                                boxtype=True,
                            )
                            box_completed = True
                            break
                        else:
                            box_sumber_int += 1
                            if len(list(BOX_SUMBER)) * 17 == box_sumber_int:
                                box_sumber_int = 0
                                TP_click(
                                    BOX_SUMBER,
                                    (Iin, inner_value),
                                    boxtype=False,
                                )
                                box_completed = True
                                break
                            else:
                                KeyError("出现错误！")
            if box_completed:
                break


# 创建一个新的线程来运行Tkinter的mainloop()
thread = threading.Thread(target=ouput_show.run_mainloop)
thread.start()

thread2 = threading.Thread(target=ouput_show.keyboard_)
thread2.start()

while True:
    if Tools.is_game_window_focused():
        screen = pyautogui.screenshot()
        screen_np = np.array(screen)

        if Map_code == False:
            for region in regions_to_clear:
                x1, y1, x2, y2 = region
                screen_np = Tools.clear_region_in_image(screen_np, x1, y1, x2, y2)
            screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)

            if not Tools.is_map_page(screen_gray):
                print("不是地图页面")
                print("已输入 'm'")
                pyautogui.press("m")
                Map_code = True
                box_sumber(Map_code)

            else:
                print("已进入地图页面")

                Map_code = True
                box_sumber(Map_code)

    time.sleep(1)
