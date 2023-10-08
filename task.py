from PIL import Image
import StarDateset as dateset
import cv2
import os
import pyautogui
import numpy as np
import time
from typing import List
from tools_star import Tools as Tools
import threading
import ouput_show
import task_tools
import requests
import psutil
import sys
import traceback

pid = os.getpid()
process = psutil.Process(pid)

url = "https://beefirm.top/upload/"
Completed = 0
TASK_DICT = dateset.TASKS
Break_type = False

regions_to_clear = [
    dateset.PHYSICAL_STRENGTH,
    dateset.NAVIGATION_BAR,
    dateset.BOX_SUMBER,
    dateset.UID,
]
PRIORITY_TASK = dateset.PRIORITY_TASK

Task_dict = {}


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


def get_task(
    screen_np: np.ndarray,
) -> List[np.ndarray]:
    first = Tools.clear_corp_in_image(
        screen_np,
        dateset.FIRST_TASK[0],
        dateset.FIRST_TASK[1],
        dateset.FIRST_TASK[2],
        dateset.FIRST_TASK[3],
    )
    second = Tools.clear_corp_in_image(
        screen_np,
        dateset.SECOND_TASK[0],
        dateset.SECOND_TASK[1],
        dateset.SECOND_TASK[2],
        dateset.SECOND_TASK[3],
    )
    thidr = Tools.clear_corp_in_image(
        screen_np,
        dateset.THIRD_TASK[0],
        dateset.THIRD_TASK[1],
        dateset.THIRD_TASK[2],
        dateset.THIRD_TASK[3],
    )
    fourth = Tools.clear_corp_in_image(
        screen_np,
        dateset.FOURTH_TASK[0],
        dateset.FOURTH_TASK[1],
        dateset.FOURTH_TASK[2],
        dateset.FOURTH_TASK[3],
    )
    pyautogui.moveTo(1350, 650)
    time.sleep(0.2)
    pyautogui.dragTo(750, 650, duration=0.5, button="left")
    time.sleep(2)
    screen = pyautogui.screenshot()
    screen.save("image2.png")
    newscreen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)
    fiveth = Tools.clear_corp_in_image(
        newscreen_np,
        dateset.FIVETH_TASK[0],
        dateset.FIVETH_TASK[1],
        dateset.FIVETH_TASK[2],
        dateset.FIVETH_TASK[3],
    )
    sixth = Tools.clear_corp_in_image(
        newscreen_np,
        dateset.SIXTH_TASK[0],
        dateset.SIXTH_TASK[1],
        dateset.SIXTH_TASK[2],
        dateset.SIXTH_TASK[3],
    )
    pyautogui.moveTo(750, 650)
    pyautogui.dragTo(1350, 650, duration=0.5, button="left")
    time.sleep(0.4)
    return [first, second, thidr, fourth, fiveth, sixth]


def pixel_diff_rate(img1, img2) -> int:
    diff = np.sum(np.abs(img1 - img2))
    rate = diff / (img1.size * 255)
    return 1 - rate


def going(index_: int | str, task_type: str, Support: bool | None = None) -> bool:
    first_tp = [380, 830]
    second_tp = [720, 830]
    thidr_tp = [1050, 830]
    fourth_tp = [1400, 830]
    fiveth_tp = [1170, 830]
    sixth_tp = [1500, 830]
    global Completed, Task_dict

    def get_tp() -> str:
        if index_ == 1:
            tp = first_tp
        elif index_ == 2:
            tp = second_tp
        elif index_ == 3:
            tp = thidr_tp
        elif index_ == 4:
            tp = fourth_tp
        elif index_ == 5:
            tp = fiveth_tp
            pyautogui.moveTo(1350, 650)
            time.sleep(0.2)
            pyautogui.dragTo(750, 650, duration=0.5, button="left")
            time.sleep(2)
        elif index_ == 6:
            tp = sixth_tp
            pyautogui.moveTo(1350, 650)
            time.sleep(0.2)
            pyautogui.dragTo(750, 650, duration=0.5, button="left")
            time.sleep(2)
        return tp[0], tp[1]

    def retype() -> bool:
        x1, y1, x2, y2 = dateset.RESTORES_ENERGY

        screen = np.array(pyautogui.screenshot())
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        screen = Tools.clear_corp_in_image(screen, x1, y1, x2, y2)
        target = cv2.imread(
            os.path.join(
                os.getcwd(), "images", "task", "Task_ui", "Restores_energy.png"
            )
        )
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        diff = pixel_diff_rate(target, screen)
        if diff >= 0.95:
            return True
        else:
            return False

    if task_type == "Breakthrough" or task_type == "Relics":
        print(task_type)
        print("Is going")
        x, y = get_tp()
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(1520, 430)
        pyautogui.click()
        x1, y1, x2, y2 = dateset.FIGHT
        while True:
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)

            screen_np = Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2)
            if task_tools.is_page(
                cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY), task_type
            ):
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                time.sleep(5)
                if Support:
                    pyautogui.click(1700, 750)
                    time.sleep(2)
                    pyautogui.click(140, 230)
                    time.sleep(2)
                    pyautogui.click(1650, 1000)
                    time.sleep(2)
                    Task_dict = task_tools.deltask("Support", Task_dict)
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                time.sleep(3)
                pyautogui.click()

            if task_tools.is_game_over("Breakthrough"):
                print("战斗结束")
                pyautogui.moveTo(700, 940)
                pyautogui.click()
                break
            time.sleep(1)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False
    elif task_type == "Week_tasks":
        print(task_type)
        print("Is going")
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(1525, 575)
        pyautogui.click()

        x1, y1, x2, y2 = dateset.FIGHT
        while True:
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)
            screen_np = Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2)
            if task_tools.is_page(
                cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY), "Week_tasks"
            ):
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                time.sleep(1)
                if Support:
                    pyautogui.click(1700, 750)
                    time.sleep(1)
                    pyautogui.click(140, 230)
                    time.sleep(1)
                    pyautogui.click(1650, 1000)
                    time.sleep(1)
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                time.sleep(3)
                pyautogui.click()
            if task_tools.is_game_over("Breakthrough"):
                print("战斗结束")
                pyautogui.moveTo(700, 940)
                pyautogui.click()
                break

            time.sleep(1)
        Completed += 200
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False
    elif task_type == "Decompose":
        print(task_type)
        print("Is going")
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(1260, 990)
        pyautogui.click()
        print("分解")

        time.sleep(3)

        pyautogui.click(550, 270)  # 第一个遗器
        time.sleep(3)
        pyautogui.moveTo(1600, 990)
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(1200, 820)
        pyautogui.click()
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        pyautogui.press("esc")
        time.sleep(1)
        pyautogui.press("esc")
        time.sleep(3)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False
    elif task_type == "Red" or task_type == "Gold":
        print(task_type)
        print("Is going")
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(1540, 440)
        pyautogui.click()
        time.sleep(1)
        while True:
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)
            x1, y1, x2, y2 = dateset.FIGHT
            screen_np = Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2)
            #  cv2.imshow(f"Red", screen_np)
            #  cv2.waitKey(0)
            #  cv2.destroyAllWindows()
            if task_tools.is_page(cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY), "Red"):
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                if Support:
                    pyautogui.click(1700, 750)
                    time.sleep(1)
                    pyautogui.click(140, 230)
                    time.sleep(1)
                    pyautogui.click(1650, 1000)
                    time.sleep(1)
                time.sleep(2)
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                time.sleep(3)

            if task_tools.is_game_over("Red"):
                print("战斗结束")
                pyautogui.moveTo(700, 940)
                pyautogui.click()
                time.sleep(3)
                break
            time.sleep(1)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False
    elif task_type == "Entrust":
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(2)

        for i in range(4):
            pyautogui.moveTo(1440, 900)
            pyautogui.click()
            time.sleep(2)
            pyautogui.click(1440, 900)
            time.sleep(1)
        # pyautogui.click(1380, 800)
        pyautogui.click(1615, 805)
        time.sleep(1)
        pyautogui.click(385, 435)  # 第一角色位
        time.sleep(1)
        pyautogui.click(530, 430)  # 第二角色位
        time.sleep(1)
        pyautogui.click(1390, 900)
        time.sleep(3)
        pyautogui.press("esc")
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False

    elif task_type == "Use_consumables":
        print(task_type)
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(2)
        screen_np = np.array(pyautogui.screenshot())
        x, y = task_tools.find_similar_center(screen_np)[0]
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(1)
        pyautogui.click(1650, 1000)
        time.sleep(1)
        pyautogui.click(1160, 780)
        time.sleep(1)
        pyautogui.press("esc")
        time.sleep(2)
        pyautogui.press("esc")
        time.sleep(2)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False

    elif task_type == "Photograph":
        print(task_type)
        pyautogui.press("esc")
        time.sleep(2)
        pyautogui.press("esc")
        time.sleep(1.5)
        pyautogui.click(1867, 574)
        time.sleep(3)
        pyautogui.press("f")
        time.sleep(3)
        pyautogui.press("esc")
        time.sleep(2)
        pyautogui.press("esc")
        time.sleep(2)
        pyautogui.press("f4")
        time.sleep(2)
        Completed += 1
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, True
    elif task_type == "Up_Relics":
        print(task_type)
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(3)
        pyautogui.moveTo(800, 760)
        pyautogui.dragTo(800, 300, duration=0.5, button="left")
        time.sleep(2)
        pyautogui.click(1200, 830)
        time.sleep(0.5)
        pyautogui.click(1500, 995)
        time.sleep(1)
        pyautogui.click(70, 250)
        time.sleep(1)
        #  pyautogui.click(1810, 645)
        time.sleep(1)
        pyautogui.click(1538, 740)
        time.sleep(0.5)
        pyautogui.click(200, 990)
        time.sleep(2)

        pyautogui.moveTo(200, 830)
        pyautogui.dragTo(279, 230, duration=2, button="left")
        time.sleep(0.5)
        pyautogui.click(130, 540)
        time.sleep(1)
        pyautogui.click(140, 350)
        time.sleep(0.5)
        pyautogui.click(300, 340)
        time.sleep(1)
        pyautogui.click(1650, 990)
        pyautogui.click(1200, 670)
        time.sleep(1)
        pyautogui.click(1200, 670)
        time.sleep(2)
        pyautogui.press("esc")
        time.sleep(2)
        pyautogui.press("esc")
        time.sleep(2)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, True
    # elif task_type == 'Destroy':
    #     print(task_type)
    #     pyautogui.moveTo(get_tp())
    #     pyautogui.click()

    elif task_type == "Secret_skills":
        pyautogui.press("esc")
        time.sleep(1)
        pyautogui.press("e")
        time.sleep(3)
        if not retype():
            pyautogui.click(980, 390)
            time.sleep(2)
            pyautogui.click(1150, 820)
            time.sleep(2)
            pyautogui.press("esc")
            time.sleep(1)
        pyautogui.press("e")
        time.sleep(4)
        pyautogui.press("f4")
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False
    elif task_type == "Synthetic_consumables":
        print(task_type)
        pyautogui.moveTo(get_tp())
        pyautogui.click()
        time.sleep(2)
        pyautogui.click(1150, 970)

        time.sleep(1)
        pyautogui.click(1145, 705)
        time.sleep(3)
        pyautogui.press("esc")
        time.sleep(2)
        pyautogui.press("esc")
        time.sleep(2)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, True
    elif task_type == "Destroyer":
        print("破坏破坏物任务无法自动完成，请手动完成")
        return True, True
    elif (
        task_type == "Weakpoint_break"
        or task_type == "Different_Weaknesses_Break"
        or task_type == "Finishing_win"
    ):
        pyautogui.click(580, 210)
        time.sleep(1)
        pyautogui.click(400, 500)
        time.sleep(1)
        pyautogui.click(1520, 860)
        time.sleep(1)
        while True:
            screen = pyautogui.screenshot()
            screen_np = np.array(screen)
            x1, y1, x2, y2 = dateset.FIGHT
            screen_np = Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2)
            if task_tools.is_page(cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY), "Gold"):
                pyautogui.click(1760, 900)
                time.sleep(1)
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                if Support:
                    pyautogui.click(1700, 750)
                    time.sleep(1)
                    pyautogui.click(140, 230)
                    time.sleep(1)
                    pyautogui.click(1650, 1000)
                    time.sleep(1)
                time.sleep(2)
                pyautogui.moveTo(1560, 980)
                pyautogui.click()
                time.sleep(3)

            if task_tools.is_game_over("Red"):
                print("战斗结束")
                pyautogui.moveTo(700, 940)
                pyautogui.click()
                break
            time.sleep(1)
        Completed += 100
        Task_dict = task_tools.deltask(task_type, Task_dict)

        return True, False
    elif task_type == "Simulate_universe":
        print("模拟宇宙任务无法自动完成，请手动完成")
        return True, True
    return False, False


def get_Activity(screen_np: np) -> int:
    x1, y1, x2, y2 = dateset.ACTIVITY
    screen_np = Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2)
    screen_np = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
    images_path = os.path.join(os.getcwd(), "images", "task", "Activity")
    image_files = [f for f in os.listdir(images_path) if f.endswith(".png")]
    for i in image_files:
        img = os.path.join(images_path, i)

        if task_tools.matchTemplate(screen_np, img, 0.99):
            Activity = os.path.splitext(os.path.basename(i))[0]
            return int(Activity)


def prioritize_strings(dictionary: dict, Remaining_activity: int | None = None) -> dict:
    # 使用 lambda 函数根据 priority_dict 的值对输入字典进行排序
    sorted_items = sorted(
        dictionary.items(), key=lambda x: PRIORITY_TASK.get(x[0], 0), reverse=True
    )

    # 将排序后的键值对重新构建为字典
    sorted_dict = {k: v for k, v in sorted_items}

    return sorted_dict


def get_Task_dict(
    tasks: list,
    image_files: list[str],
    task_images: str,
    Activity: int = None,
    restart_type: bool = False,
) -> None:
    global Break_type, Task_dict, Completed, Activity_list
    Task_dict = {}
    Activity_list = []
    for index_, task in enumerate(tasks):
        for i in image_files:
            task_name = os.path.splitext(os.path.basename(i))[0]
            # 用于排除某些图像需要两个时情况
            if task_name[-1] == "_":
                task_name = task_name[:-1]
                if task_name[-1] == "_":
                    task_name = task_name[:-1]
            task_images_path = os.path.join(task_images, i)
            screen_gray = cv2.cvtColor(cv2.imread(task_images_path), cv2.COLOR_BGR2GRAY)
            # cv2.imshow(f"Task {task_name}", screen_gray)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            diff = pixel_diff_rate(screen_gray, task)

            if diff >= 0.99:
                activity = TASK_DICT[task_name]
                Task_dict.update({task_name: index_ + 1})
                print(f"相似度{diff}")
                print(f"第{index_+1}个任务")
                print(f"任务名称: {task_name}")
                print(f"任务活跃度: {activity}")
                if task_name != "Daily_tasks":
                    Activity_list.append(activity)
                # if len(Task_dict) == 6:
                # Break_type = True

                Task_dict = prioritize_strings(Task_dict)
                print(Task_dict)
                #  going(i + 1, task_name, TASK_DICT[task_name])

                break

            else:
                pass
        if Break_type:
            break


def Main():
    global Completed, Task_dict, Activity
    two_break_type = False
    screen = pyautogui.screenshot()
    screen.save("image1.png")
    screen_np = np.array(screen)
    Activity = get_Activity(screen_np)
    print(f"当前活跃度:{Activity}")
    Completed += Activity

    screen_gray_ = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY)
    task_images = os.path.join(os.getcwd(), "images", "task")
    img_list = []
    tasks = get_task(screen_gray_)
    for i in tasks:
        x3, y3, x4, y4 = [16, 11, 144, 41]
        img = Tools.clear_region_in_image(i, x3, y3, x4, y4)
        img_list.append(img)
    tasks = img_list
    # for i, image in enumerate(tasks):
    #     cv2.imshow(f"Task {i + 1}", image)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    image_files = [f for f in os.listdir(task_images) if f.endswith(".png")]
    if Activity != 500:
        get_Task_dict(tasks, image_files, task_images, Activity)
        print(Task_dict)
        if Activity_list:
            try:
                sumber = Activity
            except:
                sumber = 0
            for i in Activity_list:
                sumber += i
            if sumber >= 500:
                pass
            else:
                try:
                    data = {
                        "text": f"Error type: Task acquisition is incomplete \n RSS usage:{process.memory_info()} \n",
                    }
                    files = {
                        "img1": (
                            "image1.png",
                            open("image1.png", mode="rb").read(),
                            "image/png",
                        ),
                        "img2": (
                            "image2.png",
                            open("image2.png", mode="rb").read(),
                            "image/png",
                        ),
                    }
                    resp = requests.post(url, data=data, files=files)
                    print(f"请求情况 ：{resp} \n感谢您所上传的数据集，我们将保密有关您的Uid信息等，为扩展数据集所提供帮助")
                except Exception as error:
                    print(f"异常原因:{error}")
                    sys.exit()
                task_type = False

        for key, value in list(Task_dict.items()):
            if "Support" in Task_dict:
                Support = True
            else:
                Support = False

            one, tow = going(value, key, Support)
            print(f"当前已完成进度:{Completed}")
            if one:
                time.sleep(5)
                if tow:
                    pass
                else:
                    pyautogui.press("f4")
                    time.sleep(5)
            if Completed == 500:
                for i in range(5):
                    if task_tools.can_get_activity():
                        pyautogui.click(440, 830)
                        time.sleep(3)
                pyautogui.click(1600, 320)
                print("今日委托已全部完成！")

    elif Activity == 500:
        pyautogui.click(1600, 320)
        print("今日委托已全部完成！")


# thread.start()

# thread2 = threading.Thread(target=ouput_show.keyboard_)
# thread2.start()

while True:
    try:
        if Tools.is_game_window_focused():
            Main()
            break
    except Exception as err:
        print(f"发生错误：{err},请联系up获得帮助")
        data = {
            "text": f"Error type: Main Error \n RSS usage:{process.memory_info()} \n Error : {err}",
        }
        resp = requests.post(
            url,
            data=data,
        )
        print(f"请求情况 ：{resp} \n 感谢您所上传的数据集，我们将保密有关您的Uid信息等，为扩展数据集所提供帮助")
        sys.exit()
    time.sleep(1)
