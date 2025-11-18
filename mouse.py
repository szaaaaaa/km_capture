from pynput import mouse,keyboard
import time
import json
import csv
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Literal

mouse_listener = None 
SAVE_EVENTS = True # 保存时设 True，不保存设 False
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

def on_move(x: float, y: float) -> None:
    """鼠标移动时由 Listener 调用。"""
    ts = get_timestamp()
    handle_event('move', x=x, y=y, ts=ts)

def on_click(x: float, y: float, button, pressed: bool) -> None:
    """鼠标按下/弹起时由 Listener 调用。"""
    ts = get_timestamp()
    handle_event('click', x=x, y=y, button=str(button), pressed=pressed, ts=ts)

def on_scroll(x: float, y: float, dx: float, dy: float) -> None:
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


def start_mouse_listener():
    global mouse_listener
    mouse_listener = mouse.Listener(
        on_move=on_move,
        on_click=on_click,
        on_scroll=on_scroll
    )
    mouse_listener.start()
    return mouse_listener



if __name__ == "__main__":
    start_mouse_listener()