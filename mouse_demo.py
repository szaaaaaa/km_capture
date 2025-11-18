from pynput import mouse,keyboard
import time
import json
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Literal

mouse_listener = None 
SAVE_EVENTS = False  # 保存时设 True，不保存设 False
LOG_FILE = f"mouse_events/mouse_events_{int(time.time()*1000)}.jsonl"  #日志文件路径 log file path

def save_event(event):
    """把事件追加写入文件（一行一个 JSON 字符串）write event to file as JSON string, one per line"""
    if not SAVE_EVENTS:
        return
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def get_timestamp() -> float:
    """返回当前高精度时间戳，用于标记事件发生时间。"""
    return time.time()

def handle_event(event_type: str, **kwargs) -> None:
    """
    统一处理所有鼠标事件：
    - event_type: 'move' / 'click' / 'scroll'
    - kwargs: 不同事件携带的字段，比如 x, y, button, pressed, dx, dy, ts 等
    """
    event = {
        'type': 'mouse',
        'event_type': event_type,
        'timestamp': get_timestamp(),
        **kwargs
    }
    print(event)
    save_event(event)  #保存到文件 save to file

def on_move(x: int, y: int) -> None:
    """鼠标移动时由 Listener 调用。"""
    ts = get_timestamp()
    handle_event('move', x=x, y=y, ts=ts)

def on_click(x: int, y: int, button, pressed: bool) -> None:
    """鼠标按下/弹起时由 Listener 调用。"""
    ts = get_timestamp()
    handle_event('click', x=x, y=y, button=str(button), pressed=pressed, ts=ts)

def on_scroll(x: int, y: int, dx: int, dy: int) -> None:
    """滚轮滚动时由 Listener 调用。"""
    ts = get_timestamp()
    handle_event('scroll', x=x, y=y, dx=dx, dy=dy, ts=ts)   

def on_key_press(key):
    """按下 ESC 时停止鼠标监听并退出程序."""
    global mouse_listener
    try:
        if key == keyboard.Key.esc:
            print("ESC pressed, stopping listeners...")
            if mouse_listener is not None:
                mouse_listener.stop()  # 停止鼠标监听
            return False  # 返回 False 会停止键盘监听
    except Exception as e:
        print(f"Error in on_key_press: {e}")


def run_mouse_listener() -> None:
    """
    创建 mouse.Listener 和 keyboard.Listener：
    - 鼠标监听负责捕获鼠标事件
    - 键盘监听负责检测 ESC，用于优雅退出
    """
    global mouse_listener

    # 1. 创建并启动鼠标监听（后台线程）
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()

    # 2. 主线程阻塞在键盘监听上，直到按下 ESC
    with keyboard.Listener(on_press=on_key_press) as key_listener:
        key_listener.join()

    print("Mouse and keyboard listeners stopped. Bye.")


if __name__ == "__main__":
    run_mouse_listener()