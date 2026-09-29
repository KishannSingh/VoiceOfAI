import tkinter as tk
import threading
import datetime
import pyautogui

import command
import speak
import open as open_module
import key
import web


assistant_running = False


def add_history(text):
    history_list.insert(tk.END, text)
    history_list.see(tk.END)


def start_listening():
    global assistant_running

    if assistant_running:
        return

    assistant_running = True
    listen_button.config(state="disabled")
    status_label.config(text="Listening...")

    thread = threading.Thread(target=listen_loop, daemon=True)
    thread.start()

def listen_loop():
    global assistant_running

    while assistant_running:
        query = command.take_command()

        if query == "none":
            continue

        add_history("You: " + query)

        process_command(query)

        import time
        time.sleep(0.5)

    status_label.config(text="Stopped")
    listen_button.config(state="normal")


def process_command(query):
    global assistant_running

    query = query.lower().strip()
    response = ""

    # Hello
    if query in ["hello", "hi", "hey"]:
        response = "Hello! I am VoAi."

    # Time
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {current_time}"
        speak.speak(response)

    # Wikipedia / What is
    elif (
        query.startswith("what is ")
        or query.startswith("meaning of ")
        or query.startswith("who is ")
    ):
        response = "Searching Wikipedia..."
        add_history("VoAi: " + response)
        response_label.config(text=response)

        web.search_for_meaning(query)
        return

    # Google search
    elif query.startswith("search for "):
        search_text = query.replace("search for ", "", 1).strip()

        if search_text:
            response = f"Searching for {search_text}"
            open_module.open_app_website(search_text)
        else:
            response = "Please tell me what to search for."

    # Screenshot
    elif "screenshot" in query or "take screenshot" in query:
        try:
            filename = "screenshot.png"
            pyautogui.screenshot(filename)
            response = "Screenshot taken successfully."
            speak.speak(response)
        except Exception as e:
            print("Screenshot error:", e)
            response = "Could not take screenshot."

    # Close all - IMPORTANT: before close
    elif query.startswith("close all "):
        app_name = query.replace("close all ", "", 1).strip()

        open_module.close_all(app_name)
        response = f"Closing all {app_name}"

    # Close app
    elif query.startswith("close "):
        app_name = query.replace("close ", "", 1).strip()

        open_module.close_app(app_name)
        response = f"Closing {app_name}"

    # Open app / website
    elif query.startswith("open "):
        item = query.replace("open ", "", 1).strip()

        open_module.open(item)
        response = f"Opening {item}"

    # Type
    elif query.startswith("type "):
        key.type(query)
        response = "Typing."

    # Enter
    elif query in ["enter", "press enter"]:
        key.press_enter()
        response = "Pressed Enter."

    # Press key
    elif query.startswith("press key "):
        key_name = query.replace("press key ", "", 1).strip()

        try:
            key.key(key_name)
            response = f"Pressed {key_name}"
        except Exception as e:
            print("Key error:", e)
            response = "Could not press that key."

    # Exit
    elif query in ["exit", "quit", "stop", "goodbye"]:
        response = "Goodbye!"
        speak.speak(response)
        assistant_running = False

    # Unknown
    else:
        response = "Sorry, I don't understand that command."

    add_history("VoAi: " + response)
    response_label.config(text=response)

    if query not in ["hello", "hi", "hey"] and not (
        query.startswith("what is ")
        or query.startswith("meaning of ")
        or query.startswith("who is ")
        or query.startswith("close ")
        or query.startswith("close all ")
        or query.startswith("open ")
        or query.startswith("search for ")
        or query.startswith("type ")
        or query.startswith("press key ")
    ):
        speak.speak(response)


# ---------------- GUI ----------------

window = tk.Tk()
window.title("VoAi - Virtual Assistant")
window.geometry("700x600")
window.configure(bg="#111827")


title_label = tk.Label(
    window,
    text="VOAI",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#111827"
)
title_label.pack(pady=(25, 5))


subtitle_label = tk.Label(
    window,
    text="Voice Based Desktop Assistant",
    font=("Arial", 12),
    fg="#9CA3AF",
    bg="#111827"
)
subtitle_label.pack()


status_label = tk.Label(
    window,
    text="Ready",
    font=("Arial", 13),
    fg="#60A5FA",
    bg="#111827"
)
status_label.pack(pady=15)


listen_button = tk.Button(
    window,
    text="🎤 Start Listening",
    font=("Arial", 14, "bold"),
    bg="#2563EB",
    fg="white",
    padx=25,
    pady=12,
    command=start_listening
)
listen_button.pack(pady=10)


response_label = tk.Label(
    window,
    text="Say a command...",
    font=("Arial", 13),
    fg="white",
    bg="#111827",
    wraplength=600
)
response_label.pack(pady=20)


history_title = tk.Label(
    window,
    text="Command History",
    font=("Arial", 13, "bold"),
    fg="white",
    bg="#111827"
)
history_title.pack(pady=(10, 5))


history_list = tk.Listbox(
    window,
    width=70,
    height=15,
    bg="#1F2937",
    fg="white",
    font=("Arial", 11),
    borderwidth=0
)
history_list.pack(padx=20, pady=10)


window.mainloop()