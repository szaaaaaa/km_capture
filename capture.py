from keyboard import start_keyboard_listener
from mouse import start_mouse_listener
from pynput import keyboard
import time


# ====== 在这里控制要不要启用各个模态 ======
ENABLE_KEYBOARD = True   # 只要把它改成 False，就不启用键盘监听
ENABLE_MOUSE    = False   # 改成 False，就不启用鼠标监听
# 例如：
# 只要键盘：ENABLE_KEYBOARD = True, ENABLE_MOUSE = False
# 只要鼠标：ENABLE_KEYBOARD = False, ENABLE_MOUSE = True
# 都不要：  ENABLE_KEYBOARD = False, ENABLE_MOUSE = False
# ======================================

def main():
    listeners = []

    if ENABLE_KEYBOARD:
        k_listener = start_keyboard_listener()
        listeners.append(k_listener)
        print("Keyboard listener started.")

    if ENABLE_MOUSE:
        m_listener = start_mouse_listener()
        listeners.append(m_listener)
        print("Mouse listener started.")

    if not listeners:
        print("No listeners enabled, exit.")
        return

    # 统一用 ESC 停止所有已启动的监听器
    def on_press(key):
        if key == keyboard.Key.esc:
            print("ESC pressed, stopping all listeners...")
            for l in listeners:
                l.stop()
            return False  # 停止这个“停止监听器”

    # 这个监听器只负责等 ESC，不做别的
    with keyboard.Listener(on_press=on_press) as stopper:
        stopper.join()

    # 等所有监听线程都结束
    for l in listeners:
        l.join()

    print("All listeners stopped.")


if __name__ == '__main__':
    main()
