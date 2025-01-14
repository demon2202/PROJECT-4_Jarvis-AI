import speech_recognition as sr
import os
import webbrowser
import datetime
import time
import requests
import pyttsx3

# Text-to-speech engine
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to take microphone input
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Could not understand audio, please try again.")
            return ""

# News function for India
def get_news():
    api_key = "09bf968387dd4dc2884a907524109bbc"  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    try:
        response = requests.get(url)
        news_data = response.json()
        if news_data["status"] == "ok":
            articles = news_data["articles"][:5]  # Fetch top 5 news articles
            say("Here are the top news headlines for India.")
            for i, article in enumerate(articles):
                title = article.get("title", "No title available")
                say(f"Headline {i + 1}: {title}")
        else:
            say("I couldn't fetch the news details. Please check the API key or connection.")
    except Exception as e:
        say("Sorry, I encountered an error while fetching the news.")

# Reminders functionality
reminders = []

def add_reminder(reminder):
    global reminders
    if reminder.strip():
        reminders.append(reminder)
        say(f"Reminder added: {reminder}")
    else:
        say("Please provide a valid reminder.")

def list_reminders():
    global reminders
    if reminders:
        say("Here are your reminders:")
        for i, reminder in enumerate(reminders):
            say(f"Reminder {i + 1}: {reminder}")
    else:
        say("You have no reminders.")

# Weather updates
def get_weather():
    api_key = "your_openweather_api_key"  # Replace with your OpenWeather API key
    city = "your_city"  # Replace with your preferred city
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        weather_data = response.json()
        if weather_data["cod"] == 200:
            temp = weather_data["main"]["temp"]
            description = weather_data["weather"][0]["description"]
            say(f"The current temperature in {city} is {temp} degrees Celsius with {description}.")
        else:
            say("I couldn't fetch the weather details. Please check the city name or API key.")
    except Exception as e:
        say("Sorry, I encountered an error while fetching the weather.")

# Music directory and player
music_dir = "C:/Users/Harsh/Downloads"  # Replace with your music folder path
music_files = [file for file in os.listdir(music_dir) if file.endswith(('.mp3', '.wav'))]
current_index = 0

def play_music(index):
    global current_index
    current_index = index
    if 0 <= current_index < len(music_files):
        music_path = os.path.join(music_dir, music_files[current_index])
        print(f"Playing: {music_files[current_index]}")
        say(f"Playing {music_files[current_index]}")
        os.startfile(music_path)
    else:
        say("No more songs available.")

# Timer and alarm
def set_timer(seconds):
    try:
        seconds = int(seconds)
        say(f"Timer set for {seconds} seconds.")
        time.sleep(seconds)
        say("Time's up!")
    except ValueError:
        say("Please provide a valid number for the timer.")

# Main function
if __name__ == "__main__":
    print("Welcome to Jarvis AI")
    say("Welcome to Jarvis AI BOSS")
    while True:
        query = takeCommand()

        if not query:
            continue

        # News command
        if "news" in query:
            get_news()

        # Weather command
        elif "weather" in query:
            get_weather()

        # Reminder commands
        elif "add reminder" in query:
            reminder_text = query.replace("add reminder", "").strip()
            add_reminder(reminder_text)

        elif "all reminder" in query or "show " in query:
            list_reminders()

        # Music commands
        elif "play music" in query:
            play_music(current_index)

        elif "next song" in query:
            if current_index + 1 < len(music_files):
                current_index += 1
                play_music(current_index)
            else:
                say("You are already at the last song.")

        elif "previous song" in query:
            if current_index - 1 >= 0:
                current_index -= 1
                play_music(current_index)
            else:
                say("You are already at the first song.")

        # Timer command
        elif "set timer" in query:
            seconds = query.replace("set timer", "").strip()
            set_timer(seconds)

        # Exit command
        elif "exit" in query or "quit" in query:
            say("Goodbye BOSS. Have a great day!")
            break

        else:
            say("I'm sorry, I didn't understand that. Can you please repeat?")
