import tkinter as tk
from tkinter import scrolledtext, messagebox
import speech_recognition as sr
import pyttsx3
import threading
import os
import platform
import socket
import pyautogui
import cv2
import numpy as np
import random
import pyjokes
import qrcode
import datetime
from bs4 import BeautifulSoup
import requests
import webbrowser
import wikipedia
import subprocess
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import speedtest
import googletrans
from googletrans import Translator

class ModernAIAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Assistant")
        self.root.geometry("800x600")

        self.setup_core_components()
        self.setup_gui()

    def setup_core_components(self):
        """Initialize core AI components"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.recognizer = sr.Recognizer()

        # Face Recognition
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def setup_gui(self):
        """Create GUI components"""
        self.textbox = scrolledtext.ScrolledText(self.root, wrap="word", height=20, width=70)
        self.textbox.pack(pady=20)

        self.speak_button = tk.Button(self.root, text="Speak", command=self.voice_input)
        self.speak_button.pack()

    def voice_input(self):
        """Capture voice command"""
        with sr.Microphone() as source:
            self.textbox.insert(tk.END, "\nListening...\n")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            self.textbox.insert(tk.END, f"\nUser: {command}\n")
            response = self.process_command(command)
            self.speak(response)
        except sr.UnknownValueError:
            response = "Sorry, I couldn't understand."
            self.speak(response)

    def process_command(self, command):
        """Process and execute commands"""
        if "system info" in command:
            return self.get_system_info()
        elif "joke" in command:
            return pyjokes.get_joke()
        elif "screenshot" in command:
            return self.take_screenshot()
        elif "battery" in command:
            return self.get_battery_status()
        elif "qr code" in command:
            return self.generate_qr_code(command)
        elif "calculate" in command:
            return self.calculate(command)
        elif "news" in command:
            return self.get_local_news()
        elif "face" in command:
            return self.detect_face()
        elif "open" in command:
            return self.open_application(command)
        elif "search" in command:
            return self.search_web(command)
        elif "wikipedia" in command:
            return self.search_wikipedia(command)
        elif "play" in command:
            return self.play_music()
        elif "time" in command:
            return self.get_current_time()
        elif "weather" in command:
            return self.get_weather(command)
        elif "reminder" in command:
            return self.set_reminder(command)
        elif "email" in command:
            return self.send_email(command)
        elif "translate" in command:
            return self.translate_text(command)
        elif "internet speed" in command:
            return self.check_internet_speed()
        elif "ip address" in command:
            return self.find_my_ip()
        elif "youtube" in command:
            return self.open_youtube(command)
        elif "maps" in command:
            return self.open_maps(command)
        elif "social media" in command:
            return self.open_social_media(command)
        elif "read file" in command:
            return self.read_file(command)
        elif "write file" in command:
            return self.write_file(command)
        elif "cpu" in command or "memory" in command:
            return self.get_cpu_memory_usage()
        elif "exit" in command:
            self.root.quit()
            return "Goodbye!"
        else:
            return "I'm not sure how to help with that."

    def speak(self, text):
        """Speak output"""
        self.engine.say(text)
        self.engine.runAndWait()

    def get_system_info(self):
        """Return basic system information"""
        info = f"""
        OS: {platform.system()} {platform.release()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        Hostname: {socket.gethostname()}
        """
        return info

    def take_screenshot(self):
        """Capture and save a screenshot"""
        filename = "screenshot.png"
        pyautogui.screenshot().save(filename)
        return "Screenshot saved."

    def get_battery_status(self):
        """Get battery status (Windows only)"""
        try:
            battery = psutil.sensors_battery()
            return f"Battery: {battery.percent}% {'Charging' if battery.power_plugged else 'Not Charging'}"
        except:
            return "Battery info not available."

    def generate_qr_code(self, command):
        """Generate QR Code"""
        text = command.replace("qr code", "").strip()
        filename = "qrcode.png"
        qr = qrcode.make(text)
        qr.save(filename)
        return "QR Code generated."

    def calculate(self, command):
        """Simple calculator"""
        try:
            command = command.replace("calculate", "").strip()
            result = eval(command)
            return f"Result: {result}"
        except:
            return "Invalid calculation."

    def get_local_news(self):
        """Scrape news headlines"""
        url = "https://www.bbc.com/news"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        headlines = [headline.get_text() for headline in soup.find_all("h3")[:5]]
        return "\n".join(headlines) if headlines else "No news found."

    def detect_face(self):
        """Detect faces using OpenCV"""
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow("Face Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        return "Face detection stopped."

    def open_application(self, command):
        """Open an application"""
        app = command.replace("open", "").strip()
        try:
            if platform.system() == "Windows":
                os.startfile(app)
            elif platform.system() == "Darwin":
                subprocess.call(["open", "-a", app])
            else:
                subprocess.call([app])
            return f"Opening {app}"
        except:
            return f"Could not open {app}"

    def search_web(self, command):
        """Search the web"""
        query = command.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} on Google"

    def search_wikipedia(self, command):
        """Search Wikipedia"""
        query = command.replace("wikipedia", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Please be more specific: {e}"
        except wikipedia.exceptions.PageError:
            return "No results found."

    def play_music(self):
        """Play a random music file from the Music directory"""
        music_dir = os.path.expanduser("~/Music")
        if os.path.exists(music_dir):
            songs = os.listdir(music_dir)
            if songs:
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
                return f"Playing {song}"
            else:
                return "No music files found."
        else:
            return "Music directory not found."

    def get_current_time(self):
        """Get the current time"""
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}"

    def get_weather(self, command):
        """Get weather information for a location"""
        location = command.replace("weather", "").strip()
        if not location:
            return "Please specify a location."
        try:
            api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            if data["cod"] != "404":
                main = data["main"]
                weather = data["weather"][0]
                return f"Weather in {location}: {weather['description']}, Temperature: {main['temp']}°C, Humidity: {main['humidity']}%"
            else:
                return "Location not found."
        except:
            return "Failed to fetch weather data."

    def set_reminder(self, command):
        """Set a reminder"""
        try:
            parts = command.replace("reminder", "").strip().split(" in ")
            reminder_text = parts[0]
            time_str = parts[1]
            time_seconds = int(time_str.replace("seconds", "").replace("minutes", "").replace("hours", "").strip())
            if "minutes" in time_str:
                time_seconds *= 60
            elif "hours" in time_str:
                time_seconds *= 3600
            threading.Timer(time_seconds, self.speak, args=[f"Reminder: {reminder_text}"]).start()
            return f"Reminder set for {time_str}."
        except:
            return "Invalid reminder format. Example: 'reminder drink water in 5 minutes'."

    def send_email(self, command):
        """Send an email"""
        try:
            parts = command.replace("email", "").strip().split(" to ")
            subject = parts[0]
            recipient = parts[1]
            sender_email = "YOUR_EMAIL@gmail.com"  # Replace with your email
            sender_password = "YOUR_EMAIL_PASSWORD"  # Replace with your email password

            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient
            msg["Subject"] = subject

            body = "This is a test email sent by your AI Assistant."
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()
            return f"Email sent to {recipient}."
        except:
            return "Failed to send email."

    def translate_text(self, command):
        """Translate text to a specified language"""
        try:
            parts = command.replace("translate", "").strip().split(" to ")
            text = parts[0]
            lang = parts[1]
            translator = Translator()
            translation = translator.translate(text, dest=lang)
            return f"Translated text: {translation.text}"
        except:
            return "Failed to translate text."

    def check_internet_speed(self):
        """Check internet speed"""
        try:
            st = speedtest.Speedtest()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            return f"Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps"
        except:
            return "Failed to check internet speed."

    def find_my_ip(self):
        """Get public IP address"""
        try:
            ip = requests.get("https://api.ipify.org").text
            return f"Your public IP address is {ip}"
        except:
            return "Failed to fetch IP address."

    def open_youtube(self, command):
        """Open YouTube or search for a video"""
        query = command.replace("youtube", "").strip()
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            return f"Searching YouTube for {query}"
        else:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube."

    def open_maps(self, command):
        """Open Google Maps or search for a location"""
        query = command.replace("maps", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/maps/search/{query}")
            return f"Searching Google Maps for {query}"
        else:
            webbrowser.open("https://www.google.com/maps")
            return "Opening Google Maps."

    def open_social_media(self, command):
        """Open social media platforms"""
        platform = command.replace("social media", "").strip()
        if platform == "facebook":
            webbrowser.open("https://www.facebook.com")
            return "Opening Facebook."
        elif platform == "twitter":
            webbrowser.open("https://www.twitter.com")
            return "Opening Twitter."
        elif platform == "instagram":
            webbrowser.open("https://www.instagram.com")
            return "Opening Instagram."
        elif platform == "linkedin":
            webbrowser.open("https://www.linkedin.com")
            return "Opening LinkedIn."
        else:
            return "Unsupported social media platform."

    def read_file(self, command):
        """Read the contents of a text file"""
        filename = command.replace("read file", "").strip()
        if os.path.exists(filename):
            with open(filename, "r") as file:
                content = file.read()
            return f"File content:\n{content}"
        else:
            return "File not found."

    def write_file(self, command):
        """Write text to a file"""
        parts = command.replace("write file", "").strip().split(" with ")
        filename = parts[0]
        content = parts[1]
        try:
            with open(filename, "w") as file:
                file.write(content)
            return f"Content written to {filename}."
        except:
            return "Failed to write to file."

    def get_cpu_memory_usage(self):
        """Get CPU and memory usage"""
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        return f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%"

if __name__ == "__main__":
    assistant = ModernAIAssistant()
    assistant.root.mainloop()
