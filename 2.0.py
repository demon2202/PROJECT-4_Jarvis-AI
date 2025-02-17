import tkinter as tk
from tkinter import scrolledtext
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

if __name__ == "__main__":
    assistant = ModernAIAssistant()
    assistant.root.mainloop()
