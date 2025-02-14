import speech_recognition as sr
import os
import webbrowser
import datetime
import time
import requests
import pyttsx3
import json
import wikipedia
import wolframalpha
import calendar
import pyautogui
import sys
import cv2
import numpy as np
from PIL import Image
import psutil
import platform
import socket
import cryptocompare
import yfinance as yf
from bs4 import BeautifulSoup
from pytube import YouTube
from forex_python.converter import CurrencyRates
from newsapi import NewsApiClient
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from playsound import playsound
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import random
import pyjokes
import speedtest
import qrcode
import face_recognition
import pygame
import openai

class JarvisAI:
    def __init__(self):
        # [Previous initialization code remains the same]
        
        # Initialize new components
        pygame.mixer.init()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}
        self.load_known_faces()
        
        # API Keys (replace with your keys)
        self.openai_key = "YOUR_OPENAI_API_KEY"
        openai.api_key = self.openai_key

    def load_known_faces(self):
        """Load known faces from faces directory"""
        faces_dir = "known_faces"
        if os.path.exists(faces_dir):
            for filename in os.listdir(faces_dir):
                if filename.endswith((".jpg", ".jpeg", ".png")):
                    name = os.path.splitext(filename)[0]
                    image_path = os.path.join(faces_dir, filename)
                    face_image = face_recognition.load_image_file(image_path)
                    face_encoding = face_recognition.face_encodings(face_image)[0]
                    self.known_faces[name] = face_encoding

    def face_recognition_security(self):
        """Implement face recognition security"""
        self.say("Initiating face recognition security check...")
        
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        
        if not ret:
            self.say("Could not access camera")
            return False
            
        face_locations = face_recognition.face_locations(frame)
        if face_locations:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            
            for name, known_encoding in self.known_faces.items():
                match = face_recognition.compare_faces([known_encoding], face_encoding)[0]
                if match:
                    self.say(f"Welcome back, {name}!")
                    cap.release()
                    return True
                    
        self.say("Unauthorized user detected!")
        cap.release()
        return False

    def generate_qr_code(self, data, filename="qr_code.png"):
        """Generate QR code from data"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(filename)
        self.say(f"QR code generated and saved as {filename}")

    def get_system_info(self):
        """Get detailed system information"""
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery()
        
        info = f"""
        System Information:
        CPU Usage: {cpu_usage}%
        Memory Used: {memory.percent}%
        Disk Usage: {disk.percent}%
        Operating System: {platform.system()} {platform.release()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        """
        if battery:
            info += f"Battery: {battery.percent}% {'Charging' if battery.power_plugged else 'Not Charging'}"
            
        self.say(info)

    def get_crypto_price(self, crypto_currency="BTC", base_currency="USD"):
        """Get cryptocurrency price"""
        try:
            price = cryptocompare.get_price(crypto_currency, currency=base_currency)
            self.say(f"Current {crypto_currency} price in {base_currency}: {price[crypto_currency][base_currency]}")
        except Exception as e:
            self.say(f"Sorry, couldn't fetch cryptocurrency price: {str(e)}")

    def get_stock_info(self, symbol):
        """Get stock market information"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            current_price = info.get('regularMarketPrice', 'N/A')
            previous_close = info.get('regularMarketPreviousClose', 'N/A')
            market_cap = info.get('marketCap', 'N/A')
            
            self.say(f"""
            Stock Information for {symbol}:
            Current Price: ${current_price}
            Previous Close: ${previous_close}
            Market Cap: ${market_cap:,}
            """)
        except Exception as e:
            self.say(f"Sorry, couldn't fetch stock information: {str(e)}")

    def download_youtube_video(self, url, audio_only=False):
        """Download YouTube video or audio"""
        try:
            yt = YouTube(url)
            if audio_only:
                stream = yt.streams.filter(only_audio=True).first()
                output_file = stream.download(output_path="downloads", filename_prefix="audio_")
                self.say(f"Audio downloaded: {output_file}")
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                output_file = stream.download(output_path="downloads")
                self.say(f"Video downloaded: {output_file}")
        except Exception as e:
            self.say(f"Sorry, couldn't download the video: {str(e)}")

    def currency_converter(self, amount, from_currency, to_currency):
        """Convert currency using real-time exchange rates"""
        try:
            c = CurrencyRates()
            result = c.convert(from_currency, to_currency, amount)
            self.say(f"{amount} {from_currency} is equal to {result:.2f} {to_currency}")
        except Exception as e:
            self.say(f"Sorry, couldn't convert currency: {str(e)}")

    def chat_with_gpt(self, prompt):
        """Chat with GPT model"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            self.say(answer)
        except Exception as e:
            self.say(f"Sorry, couldn't get a response from GPT: {str(e)}")

    def play_music_with_controls(self, file_path):
        """Play music with basic controls"""
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            print("\nMusic Controls:")
            print("P - Pause/Resume")
            print("S - Stop")
            print("+ - Volume Up")
            print("- - Volume Down")
            print("Q - Quit")
            
            command = input("Enter command: ").lower()
            
            if command == 'p':
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            elif command == 's':
                pygame.mixer.music.stop()
                break
            elif command == '+':
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1.0, current_volume + 0.1))
            elif command == '-':
                current_volume = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, current_volume - 0.1))
            elif command == 'q':
                pygame.mixer.music.stop()
                break

    def run(self):
        # Implement face recognition security
        if not self.face_recognition_security():
            self.say("Access denied. Shutting down.")
            return

        self.say("Hello! I'm Jarvis, your AI assistant. How can I help you today?")
        
        while True:
            self.check_reminders()
            query = self.take_command()
            
            if not query:
                continue

            # New command handlers
            if "system info" in query:
                self.get_system_info()

            elif "crypto" in query:
                parts = query.split()
                crypto = "BTC"  # default
                for part in parts:
                    if part.upper() in ["BTC", "ETH", "DOGE", "XRP"]:
                        crypto = part.upper()
                self.get_crypto_price(crypto)

            elif "stock price" in query:
                symbol = query.split("stock price")[-1].strip().upper()
                self.get_stock_info(symbol)

            elif "download youtube" in query:
                self.say("Please paste the YouTube URL:")
                url = input("URL: ")
                audio_only = "audio only" in query.lower()
                self.download_youtube_video(url, audio_only)

            elif "convert currency" in query:
                self.say("Amount to convert:")
                amount = float(input("Amount: "))
                self.say("From which currency? (e.g., USD)")
                from_curr = input("From: ").upper()
                self.say("To which currency? (e.g., EUR)")
                to_curr = input("To: ").upper()
                self.currency_converter(amount, from_curr, to_curr)

            elif "create qr code" in query:
                self.say("What data should I encode in the QR code?")
                data = input("Data: ")
                self.generate_qr_code(data)

            elif "chat gpt" in query:
                prompt = query.replace("chat gpt", "").strip()
                if prompt:
                    self.chat_with_gpt(prompt)
                else:
                    self.say("What would you like to ask GPT?")
                    prompt = self.take_command()
                    if prompt:
                        self.chat_with_gpt(prompt)

            # [Previous command handlers remain the same]

            elif "exit" in query or "goodbye" in query:
                self.say("Goodbye! Have a great day!")
                break

if __name__ == "__main__":
    jarvis = JarvisAI()
    jarvis.run()
