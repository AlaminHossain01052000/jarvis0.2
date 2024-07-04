import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import os
from dotenv import load_dotenv
import time
import datetime
import pyjokes
import wikipedia

recognizer = sr.Recognizer()
engine = pyttsx3.init()
load_dotenv()

newsApiKey = os.getenv("NEWSAPI_API_KEY")
weatherApiKey = os.getenv("WEATHER_API_KEY")
newsUrl = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={newsApiKey}"
response = requests.get(newsUrl)
data = response.json()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in command.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif "open render" in command.lower():
        webbrowser.open("https://renderz.app/")
    elif command.lower().startswith('play'):
        musicName = command.lower().split(" ")[1]
        webbrowser.open(musicLibrary.music[musicName])
    elif "news" in command.lower():
        if data['status'] == 'ok':
            for article in data['articles']:
                speak(article['title'])
        else:
            print("Failed to fetch news")
    elif "weather" in command.lower():
        city = command.split("in")[-1].strip()
        # print(command,city)
        weatherUrl = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherApiKey}&units=metric"
        weather_response = requests.get(weatherUrl)
        weather_data = weather_response.json()
        if weather_data["cod"] != "404":
            main = weather_data["main"]
            weather_desc = weather_data["weather"][0]["description"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather_report = f"Weather in {city}: {weather_desc}, Temperature: {temperature}°C, Humidity: {humidity}%"
            speak(weather_report)
        else:
            speak("City not found.")
    elif "time" in command.lower():
        current_time = time.strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command.lower():
        current_date = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")
    elif "joke" in command.lower():
        joke = pyjokes.get_joke()
        speak(joke)
    elif "set timer" in command.lower():
        try:
            timer_seconds = int(command.split()[-2])
            speak(f"Setting a timer for {timer_seconds} seconds")
            time.sleep(timer_seconds)
            speak("Time's up!")
        except:
            speak("I couldn't understand the timer duration")
    elif "wikipedia" in command.lower():
        search_query = command.replace("wikipedia", "").strip()
        # print(search_query)
        summary = wikipedia.summary(search_query, sentences=2)
        speak(summary)

if __name__ == "__main__":
    print("Initializing Jarvis...")
    speak("Initializing Jarvis...")

    def speech_listen():
        while True:
            try:
                audio = ""
                with sr.Microphone() as source:
                    print("Say 'Hey Jarvis'")
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=15)
                print("Processing...")
                u_said = recognizer.recognize_google(audio, language='en-US')
                if u_said.lower() == "hey jarvis":
                    speak("Yes")
                    with sr.Microphone() as source:
                        print("Jarvis is listening....")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
                        command = recognizer.recognize_google(audio, language='en-US')
                        processCommand(command)
            except:
                print("Awaiting command.")

    speech_listen()
