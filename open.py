import os
import subprocess
import psutil
import webbrowser
from urllib.parse import quote
import speak


apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": "WINWORD.EXE",
    "excel": "EXCEL.EXE",
    "chrome": "chrome.exe",
    "vs code": "Code.exe",
    "file explorer": "explorer.exe",
    "cmd": "cmd.exe",
}

known_sites = {
    "whatsapp": "https://web.whatsapp.com",
    "youtube": "https://www.youtube.com",
    "spotify": "https://open.spotify.com",
    "netflix": "https://www.netflix.com",
    "gmail": "https://mail.google.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://twitter.com",
    "chatgpt": "https://chat.openai.com",
}


def find_chrome():
    paths = [
        os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    ]

    for path in paths:
        if os.path.exists(path):
            return path

    return None


def open_app(app_name):
    app_name = app_name.lower().strip()

    if app_name == "chrome":
        chrome_path = find_chrome()

        if chrome_path:
            try:
                subprocess.Popen([chrome_path])
                speak.speak("Opening Chrome")
            except Exception as e:
                print("Chrome error:", e)
                speak.speak("Couldn't open Chrome")
        else:
            speak.speak("Chrome was not found")

        return

    app = apps.get(app_name)

    if not app:
        speak.speak(f"I don't know how to open {app_name}")
        return

    try:
        subprocess.Popen(app)
        speak.speak(f"Opening {app_name}")
    except Exception as e:
        print("Open error:", e)
        speak.speak(f"Couldn't open {app_name}")


def open_app_website(app_name):
    app_name = app_name.lower().strip()

    url = known_sites.get(app_name)

    try:
        if url:
            webbrowser.open(url)
            speak.speak(f"Opening {app_name}")
        else:
            search_url = "https://www.google.com/search?q=" + quote(app_name)
            webbrowser.open(search_url)
            speak.speak(f"Searching for {app_name}")

    except Exception as e:
        print("Website error:", e)
        speak.speak("Unable to open it")


def open(query):
    query = query.lower().strip()

    if query in apps:
        open_app(query)
    else:
        open_app_website(query)


def get_pids_by_name(process_name):
    process_name = process_name.lower()
    pids = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = proc.info["name"]

            if name and name.lower() == process_name:
                pids.append(proc.info["pid"])

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return pids


def close_app(app_name):
    app_name = app_name.lower().strip()

    process_names = {
        "chrome": "chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "paint": "mspaint.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "vs code": "Code.exe",
        "file explorer": "explorer.exe",
        "cmd": "cmd.exe",
    }

    process_name = process_names.get(app_name)

    if not process_name:
        speak.speak(f"I don't know how to close {app_name}")
        return

    pids = get_pids_by_name(process_name)

    if not pids:
        speak.speak(f"{app_name} is not running")
        return

    closed = 0

    for pid in pids:
        try:
            process = psutil.Process(pid)
            process.terminate()
            closed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if closed:
        speak.speak(f"Closed {app_name}")
    else:
        speak.speak(f"Couldn't close {app_name}")


def close_all(app_name):
    close_app(app_name)