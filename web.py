import wikipedia
import speak


def search_for_meaning(word_query):

    word = (
        word_query
        .replace("meaning of", "")
        .replace("search for", "")
        .replace("what is", "")
        .strip()
    )

    if not word:

        speak.speak(
            "Please specify what you want to know."
        )
        return

    try:

        summary = wikipedia.summary(
            word,
            sentences=3
        )

        print("Wikipedia:", summary)

        speak.speak(
            f"According to Wikipedia, {summary}"
        )

    except wikipedia.exceptions.DisambiguationError:

        speak.speak(
            f"There are multiple results for {word}. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak.speak(
            f"Sorry, I couldn't find information about {word}."
        )

    except Exception as e:

        print(
            "Wikipedia error:",
            e
        )

        speak.speak(
            "Sorry, I couldn't search for that right now."
        )