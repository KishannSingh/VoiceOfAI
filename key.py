import keyboard
import speak
import time


def key(command):
    keyboard.press_and_release(command)


def press_enter():
    keyboard.press_and_release("enter")


def type(query):
    text_to_type = query.replace("type ", "", 1).strip()

    if text_to_type:
        speak.speak(f"Typing {text_to_type}")
        time.sleep(0.5)
        keyboard.write(text_to_type)