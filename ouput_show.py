from tkinter import ttk
import keyboard
import tkinter as tk
import sys

def run_mainloop():
    global window, window_type
    window_type = True
    window = tk.Tk()
    window.attributes("-alpha", 0.5)
    window.configure(bg="black")
    window.overrideredirect(True)
    style = ttk.Style()
    style.configure("TEntry", font=("Arial", 12, "italic"))
    # 获取屏幕的宽度和高度
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 600  # 窗口宽度
    window_height = 300  # 窗口高度
    window_x = 0  # screen_width - window_width
    window_y = screen_height - window_height - 50
    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")
    text_box = tk.Text(window, bg="black", fg="white", font=("Courier", 12))
    text_box.pack(expand=True, fill="both")
    output_stream = CustomOutputStream(text_box)
    sys.stdout = output_stream
    window.attributes("-topmost", True)
    window.attributes("-disabled", True)

    # 注册热键回调函数

    window.mainloop()


def keyboard_():
    #   keyboard.on_release(hotkey_pressed)
    while True:
        keyboard.wait("ctrl+shift+a")
        hotkey_pressed()


class CustomOutputStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.insert("end", text)
        self.text_widget.see("end")


def hide_window():
    window.withdraw()


def show_window():
    window.deiconify()


def hotkey_pressed():
    global window_type
    if window_type:
        hide_window()
        window_type = False
    else:
        show_window()
        window_type = True
