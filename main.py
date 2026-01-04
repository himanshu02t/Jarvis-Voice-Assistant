import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musicLibrary
import newsLibrary
import os
from gtts import gTTS
import pygame
#from openai import OpenAI




is_speaking = False

# --------- SETUP ----------

def speak(text):
    global is_speaking
    is_speaking = True
    tts = gTTS(text)
    tts.save("news.mp3")

    pygame.mixer.init()
    pygame.mixer.music.load("news.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()
    os.remove("news.mp3")


    is_speaking = False


'''def aiProcess(command):
    try:
        client = OpenAI(api_key="YOUR_API_KEY")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis. Reply briefly."},
                {"role": "user", "content": command}
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        return "Sorry, I am unable to connect to the AI service right now."

   '''


offline_answers = {
    "what is python": "Python is a popular programming language used for web development, AI, and automation.",
    "what is coding": "Coding means writing instructions that computers can understand.",
    "who are you": "I am Jarvis, your virtual assistant.",
    "what can you do": "I can open websites, play music, and read the latest news.",
    "who made you": "I was created by Himanshu as a programming project.",
    "hello": "Hello! How can I help you?",
    "hi": "Hi there! What can I do for you?"
}



# --------- COMMAND HANDLER ----------
def processCommand(c):
    print("Command received:", c)
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")

    
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        parts = c.split(" ")
        if len(parts) > 1:
            song = parts[1]
            link = musicLibrary.music.get(song)
            if link:
                webbrowser.open(link)
            else:
                speak("Song not found")
        else:
            speak("Please say the song name")    

    elif "today's news" in c or "today's headlines" in c or "news" in c:
        print("NEWS BLOCK ENTERED")

        speak("Here are today's news")
        

        articles = newsLibrary.get_news()

        if not articles:
            speak("Sorry, I could not fetch the news")
            return

        for i, article in enumerate(articles, start=1):
            speak(f"News {i}")
            speak(article["title"])
            speak(article["description"])
            time.sleep(1)

        speak("That is all for today's news")

    else:
        reply = offline_answers.get(c)
        if reply:
           speak(reply)
        else:
           speak("Sorry, AI feature is disabled right now.")
 

# --------- MAIN LOOP ----------
if __name__ == "__main__":
    speak("Hello Himanshu, Jarvis is ready")

    while True:
        if is_speaking:
            time.sleep(0.1)
            continue

        r = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                r.adjust_for_ambient_noise(source, duration=0.3)
                audio = r.listen(source, timeout=8, phrase_time_limit=3)

            word = r.recognize_google(audio, language="en-IN")
            print("Heard:", word)

            if "jarvis" in word.lower():
                speak("Yes")

                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=6, phrase_time_limit=5)

                command = r.recognize_google(audio, language="en-IN")
                processCommand(command)
                time.sleep(3)

        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("ERROR:", e)
