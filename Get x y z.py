import pyautogui
import time
import pygetwindow as gw

game_window_title_en = "Star Rail"
game_window_title_zh = "崩坏：星穹铁道"
Map_code = False #默认状态

def is_game_window_focused():
    active_window = gw.getActiveWindow()
    if active_window is not None:
        print("Active Window Title:", active_window.title)  # 调试信息：打印当前活动窗口标题
        if active_window.title == game_window_title_en or active_window.title == game_window_title_zh:
            return True
    return False

while True:
   # if is_game_window_focused():
        x, y = pyautogui.position()
        print(f"鼠标坐标：({x}, {y})", end='\r')
        time.sleep(1)
