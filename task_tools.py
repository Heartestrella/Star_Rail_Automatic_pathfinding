import pyautogui, numpy as np, StarDateset as dateset, cv2, os
from tools_star import Tools


def matchTemplate(img1: np, imgpath: str, threshold: float) -> bool:
    template = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img1, template, cv2.TM_CCOEFF_NORMED)

    locations = cv2.findNonZero((result >= threshold).astype(int))
    # print(f"Img path: {result[0][0]}")
    if locations is not None:
        return True
    else:
        return False


def is_page(screen_image, targetimg) -> bool:
    img_path = os.path.join(
        os.path.dirname(__file__), "images", "task", "Task_ui", f"{targetimg}.png"
    )
    locations = matchTemplate(screen_image, img_path, 0.6)

    return locations


def is_game_over(taskname) -> bool:
    if taskname == "Breakthrough":
        x1, y1, x2, y2 = dateset.BREAKTHROUGH_OVER
    elif taskname == "Red":
        x1, y1, x2, y2 = dateset.BREAKTHROUGH_OVER
    screen_np = np.array(pyautogui.screenshot())
    screen_np = cv2.cvtColor(
        Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2), cv2.COLOR_BGR2GRAY
    )

    targetpath = os.path.join(
        os.path.dirname(__file__), "images", "task", "Game_over", f"{taskname}.png"
    )
    locations = matchTemplate(screen_np, targetpath, 0.7)
    return locations


def can_get_activity() -> bool:
    x1, y1, x2, y2 = dateset.GET_ACTIVITY
    screen_np = np.array(pyautogui.screenshot())
    screen_np = cv2.cvtColor(
        Tools.clear_corp_in_image(screen_np, x1, y1, x2, y2), cv2.COLOR_BGR2GRAY
    )
    targetpath = os.path.join(
        os.path.dirname(__file__), "images", "task", "Game_over", f"Get_activity.png"
    )

    locations = matchTemplate(screen_np, targetpath, 0.69)
    return locations


def find_similar_center(image: np, threshold=0.8):
    # 使用模板匹配方法
    template_path = os.path.join(
        os.path.dirname(__file__), "images", "task", "Consumables"
    )
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_files = [f for f in os.listdir(template_path) if f.endswith(".png")]
    print(image_files)
    for img in image_files:
        img_path = template_path = os.path.join(
            os.path.dirname(__file__), "images", "task", "Consumables", img
        )
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(image, img, cv2.TM_CCOEFF_NORMED)

        locations = np.where(result >= threshold)

        center_points = []
        for pt in zip(*locations[::-1]):
            center_x = pt[0] + img.shape[1] // 2
            center_y = pt[1] + img.shape[0] // 2
            center_points.append((center_x, center_y))
        if center_points:
            return center_points


def deltask(completed_task: str, task_dict: dict) -> dict:
    if completed_task in task_dict:
        completed_task_index = task_dict[completed_task]

        del task_dict[completed_task]

        task_dict = {
            task: index + 1 if index < completed_task_index else index
            for task, index in task_dict.items()
        }
        return task_dict
