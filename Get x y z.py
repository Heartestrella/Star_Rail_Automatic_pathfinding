import pyautogui
import time
import pygetwindow as gw

game_window_title_en = "Star Rail"
game_window_title_zh = "崩坏：星穹铁道"
Map_code = False #默认状态

def is_game_window_focused():
    active_window = gw.getActiveWindow()
    if active_window is not None:
       
        if active_window.title == game_window_title_en or active_window.title == game_window_title_zh:
            return True
    return False

last_mouse_state = False
import threading
import ouput_show
thread = threading.Thread(target=ouput_show.run_mainloop)
thread.start()

thread2 = threading.Thread(target=ouput_show.keyboard_)
thread2.start()
while True:
    if is_game_window_focused():
        print('已经进入游戏')
        x, y = pyautogui.position()
        mouse_state = pyautogui.mouseDown(button='left')
        
    #    if mouse_state :#and not last_mouse_state:
        print(f"坐标：({x}, {y})")
        
        last_mouse_state = mouse_state
        
    time.sleep(1)  # 减小休眠时间以提高响应速度
