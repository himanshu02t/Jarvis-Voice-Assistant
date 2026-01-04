# tts_test.py
import pyttsx3
import time

engine = pyttsx3.init()  # on Windows this uses 'sapi5'; on Linux 'espeak' etc.

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
        print("TTS finished")
    except Exception as e:
        print("TTS error:", e)

if __name__ == "__main__":
    print("About to speak...")
    speak("This is a T T S test. Can you hear me?")
    time.sleep(0.5)
    print("Done.")
