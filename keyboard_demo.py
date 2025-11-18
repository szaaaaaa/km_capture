from pynput import keyboard  # 键盘监听主库 main keyboard listening library
import time                  # 获取时间戳 get timestamp
import json                  # 把事件字典转成 JSON 字符串（可选）transform event dict to JSON string (optional)

pressed_keys = set()   # 记录当前已经按下、尚未松开的键 record currently pressed keys
LOG_FILE = f"key_events/key_events_{int(time.time()*1000)}.jsonl"  #日志文件路径 log file pathpython keyboard_demo.py
SAVE_EVENTS = False # 保存时设 True，不保存设 False     save to file if True, else not

def save_event(event):
    """把事件追加写入文件（一行一个 JSON 字符串）write event to file as JSON string, one per line"""
    if not SAVE_EVENTS:
        return
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def get_timestamp():

    """获取当前时间戳，精确到毫秒 get current timestamp in milliseconds"""
    return int(time.time() * 1000)

def format_key_event(action, key):
    """格式化键盘事件为字典 format keyboard event as dict"""
    try:
        key_str = key.char  # 普通字符键 normal key
    except AttributeError:
        key_str = str(key)  # 特殊键 special key

    event = {
        'action': action,
        'type': 'keyboard',
        'key': key_str,
        'timestamp': get_timestamp()
    }
    return event

def on_press(key):
    # 如果这个 key 已经在集合里，说明是长按产生的自动重复，忽略. 
    # If the key is already in the set, it's an auto-repeat from long press, ignore it.
    if key in pressed_keys:
        return

    if key == keyboard.Key.esc:
        # 按下 ESC 键时，停止监听 
        # stop listener on ESC key press
        return False
    
    # 第一次按下这个 key，记录下来 
    # First time pressing this key, record it
    pressed_keys.add(key)

    event = format_key_event("down", key)
    print(event)

    save_event(event)  #保存到文件 save to file


def on_release(key):
    """键释放事件处理函数 key release event handler"""
    # 松开时，把这个 key 从集合里移除 remove the key from the set on release  
    pressed_keys.discard(key)

    event = format_key_event("up", key)
    print(event)

    save_event(event)#保存到文件 save to file
def start_keyboard_listener():
    """启动键盘监听器 start keyboard listener"""
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release,
            # 如果想把键盘事件“吃掉”，不传递给其他应用，设置 suppress=True；
            # If you want to "suppress" keyboard events so other apps don't receive them, set suppress=True;
            # 如果想让其他应用也能收到事件，设置为suppress=False。设置为True是为了终端不打印出来。
            # If you want other apps to receive the events, set suppress=False. Setting it to True prevents printing in the terminal.
            suppress=True
            ) as listener:
        listener.join()

# 主程序入口 main program entry point
if __name__ == "__main__":
    print("Starting keyboard listener. Press ESC to stop.")
    start_keyboard_listener()
    print("Keyboard listener stopped.")