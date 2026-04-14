from PySide6.QtCore import QThread
from pynput import keyboard

sock = None


def send(cmd):
    sock.send((cmd + ',').encode(encoding='utf-8'))


class KeyThread(QThread):
    def __init__(self, socket):
        global sock
        super().__init__()
        self.key_up_flag = False
        self.key_down_flag = False
        self.key_right_flag = False
        self.key_left_flag = False
        sock = socket

    def on_press(self, key):
        try:
            if key == keyboard.Key.up and not self.key_up_flag:
                send("1")
                self.key_up_flag = True
            elif key == keyboard.Key.down and not self.key_down_flag:
                send("2")
                self.key_down_flag = True
            elif key == keyboard.Key.right and not self.key_right_flag:
                send("115")
                self.key_right_flag = True
            elif key == keyboard.Key.left and not self.key_left_flag:
                send("65")
                self.key_left_flag = True
        except AttributeError:
            print(f'알파벳 \'{key}\' 눌림')

    def on_release(self, key):
        try:
            if key == keyboard.Key.up and self.key_up_flag:
                send("0")
                self.key_up_flag = False
            elif key == keyboard.Key.down and self.key_down_flag:
                send("0")
                self.key_down_flag = False
            elif key == keyboard.Key.right and self.key_right_flag:
                send("90")
                self.key_right_flag = False
            elif key == keyboard.Key.left and self.key_left_flag:
                send("90")
                self.key_left_flag = False
        except AttributeError:
            print(f'알파벳 \'{key}\' 눌림')

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()