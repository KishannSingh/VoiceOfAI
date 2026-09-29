import psutil
import speak


def close_application(app_name):

    app_name = app_name.lower().strip()

    # Add .exe if it is not already present
    exe_name = app_name if app_name.endswith(".exe") else app_name + ".exe"

    found = False

    try:

        for proc in psutil.process_iter(["name"]):

            try:

                process_name = proc.info["name"]

                if process_name and process_name.lower() == exe_name:

                    proc.kill()

                    speak.speak(
                        f"{app_name} closed successfully."
                    )

                    found = True
                    return

            except psutil.NoSuchProcess:
                pass

            except psutil.AccessDenied:

                speak.speak(
                    f"Permission denied to close {app_name}."
                )

                return

    except Exception as e:

        print("Close error:", e)


    if not found:

        speak.speak(
            f"{app_name} is not running."
        )