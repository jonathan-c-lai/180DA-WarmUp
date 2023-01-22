import random
import time

import speech_recognition as sr

# used code from https://realpython.com/python-speech-recognition/#putting-it-all-together-a-guess-the-word-game
# that professor/TA linked in lab
# modified to make the words pool more difficult to distinguish, for example cat, hat, bat
# modified to make it so that it is not a guessing game but now detects word recognition accuracy:
#       the game picks some number of words to display and I say the word to see if the computer recognizes it correctly.
#       the score is now a score for how good the computer was able to detect it


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["cat", "dog", "mouse", "hat", "bat"]
    NUM_WORDS = 3
    PROMPT_LIMIT = 5
    SCORE = 0

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # format the instructions string
    instructions = (
        "Say the word that is printed on the screen\n"
        "Word pool: {words}\n"
    ).format(words=', '.join(WORDS))

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    for i in range(NUM_WORDS):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        # get a random word from the list
        word = random.choice(WORDS)

        for j in range(PROMPT_LIMIT):
            print('Say this word: ', word)
            attempt = recognize_speech_from_mic(recognizer, microphone)
            if attempt["transcription"]:
                break
            if not attempt["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if attempt["error"]:
            print("ERROR: {}".format(attempt["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(attempt["transcription"]))

        # determine if attempt is correct
        attempt_is_correct = attempt["transcription"].lower() == word.lower()

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if attempt_is_correct:
            print("Correct!".format(word))
            SCORE += 1
            print(SCORE, "\n")
        else:
            print("That was wrong")
            print("Score unchanged: ", SCORE, "\n")