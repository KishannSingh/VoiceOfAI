import speech_recognition as sr
import speak


def take_command():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        r.pause_threshold = 0.8
        r.non_speaking_duration = 0.5

        # Microphone noise calibration
        r.adjust_for_ambient_noise(
            source,
            duration=0.5
        )

        try:

            audio = r.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

        except sr.WaitTimeoutError:

            print("No speech detected.")
            return "none"

    try:

        print("Recognizing...")

        query = r.recognize_google(
            audio,
            language="en-IN"
        )

        query = query.lower().strip()

        print(f"User said: {query}")

        return query

    except sr.UnknownValueError:

        print("Could not understand the speech.")
        return "none"

    except sr.RequestError as e:

        print(
            f"Google Speech Recognition error: {e}"
        )

        return "none"

    except Exception as e:

        print(
            f"Recognition error: {type(e).__name__}: {e}"
        )

        return "none"