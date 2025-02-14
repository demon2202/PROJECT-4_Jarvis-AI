import customtkinter as ctk
import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import threading
import time
import json
import wave
import pyaudio
import numpy as np
from PIL import Image, ImageTk
import os
from datetime import datetime
import math
import webbrowser
import requests
import wikipedia
import wolframalpha
import calendar
import pyautogui
import cv2
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

class ModernAIAssistant:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("AI Assistant")
        self.root.geometry("800x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize core components
        self.setup_core_components()
        
        # Create and configure the GUI
        self.setup_gui()
        
        # Load conversation history
        self.conversation_history = []
        self.load_history()

    def setup_core_components(self):
        """Initialize all core AI components"""
        # Speech components
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.recognizer = sr.Recognizer()
        
        # Audio components
        self.audio_data = []
        self.is_recording = False
        self.is_listening = False
        self.p = pyaudio.PyAudio()
        
        # Translation
        self.translator = Translator()
        
        # AI/ML components
        self.wolfram_client = wolframalpha.Client('YOUR_WOLFRAM_ALPHA_KEY')
        self.openai.api_key = "YOUR_OPENAI_API_KEY"
        
        # Face recognition
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.known_faces = {}
        self.load_known_faces()
        
        # Initialize settings
        self.load_settings()

    def load_settings(self):
        """Load application settings"""
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                'voice_rate': 150,
                'voice_volume': 1.0,
                'language': 'en',
                'city': 'Your City',
                'news_api_key': 'YOUR_NEWS_API_KEY',
                'weather_api_key': 'YOUR_WEATHER_API_KEY',
                'email': 'your_email@gmail.com',
                'email_password': 'your_app_password'
            }
            self.save_settings()

    [... Previous GUI setup methods remain the same ...]

    def process_command(self, command):
        """Process user commands and generate responses"""
        command = command.lower()
        response = ""

        try:
            # System commands
            if "system info" in command:
                response = self.get_system_info()
            
            # Weather commands
            elif "weather" in command:
                response = self.get_weather()
            
            # News commands
            elif "news" in command:
                category = 'general'
                for cat in ['business', 'technology', 'sports', 'science', 'health']:
                    if cat in command:
                        category = cat
                response = self.get_news(category)
            
            # Translation commands
            elif "translate" in command:
                response = self.handle_translation(command)
            
            # Financial commands
            elif "crypto" in command:
                crypto = "BTC"
                for coin in ["ETH", "DOGE", "XRP"]:
                    if coin.lower() in command:
                        crypto = coin
                response = self.get_crypto_price(crypto)
            
            elif "stock price" in command:
                symbol = command.split("stock price")[-1].strip().upper()
                response = self.get_stock_info(symbol)
            
            # Media commands
            elif "download youtube" in command:
                response = self.handle_youtube_download(command)
            
            # Utility commands
            elif "create qr" in command:
                response = self.handle_qr_generation(command)
            
            # AI chat commands
            elif "chat" in command:
                prompt = command.replace("chat", "").strip()
                response = self.chat_with_gpt(prompt)
            
            # Help command
            elif "help" in command:
                response = self.get_help_text()
            
            # Exit command
            elif "exit" in command or "goodbye" in command:
                response = "Goodbye! Have a great day!"
                self.root.after(2000, self.root.quit)
            
            else:
                response = "I'm not sure how to help with that. Try asking for 'help' to see what I can do."

        except Exception as e:
            response = f"Sorry, I encountered an error: {str(e)}"

        return response

    def get_system_info(self):
        """Get system information"""
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
        return info

    def get_weather(self):
        """Get weather information"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.settings['city']}&appid={self.settings['weather_api_key']}&units=metric"
            response = requests.get(url)
            weather_data = response.json()
            
            if weather_data["cod"] == 200:
                temp = weather_data["main"]["temp"]
                humidity = weather_data["main"]["humidity"]
                desc = weather_data["weather"][0]["description"]
                return f"Current weather in {self.settings['city']}: {temp}°C, {desc}, Humidity: {humidity}%"
            else:
                return "Sorry, couldn't fetch weather information."
        except Exception as e:
            return f"Error getting weather: {str(e)}"

    def get_news(self, category='general'):
        """Get news updates"""
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={self.settings['news_api_key']}"
            response = requests.get(url)
            news_data = response.json()
            
            if news_data["status"] == "ok":
                articles = news_data["articles"][:5]
                news_text = f"\nTop {category} news:\n\n"
                for i, article in enumerate(articles, 1):
                    news_text += f"{i}. {article['title']}\n"
                return news_text
            else:
                return "Sorry, couldn't fetch news updates."
        except Exception as e:
            return f"Error getting news: {str(e)}"

    def handle_translation(self, command):
        """Handle translation requests"""
        try:
            if "to" in command:
                parts = command.split("to")
                text = parts[0].replace("translate", "").strip()
                target_lang = parts[1].strip()
                
                # Get language code
                lang_code = None
                for code, lang in LANGUAGES.items():
                    if target_lang.lower() in lang.lower():
                        lang_code = code
                        break
                
                if lang_code:
                    translation = self.translator.translate(text, dest=lang_code)
                    return f"Translation: {translation.text}"
                else:
                    return "Sorry, I don't recognize that language."
            else:
                return "Please specify the target language (e.g., 'translate hello to spanish')"
        except Exception as e:
            return f"Error in translation: {str(e)}"

    def get_crypto_price(self, crypto="BTC"):
        """Get cryptocurrency price"""
        try:
            price = cryptocompare.get_price(crypto, currency='USD')
            return f"Current {crypto} price: ${price[crypto]['USD']:,.2f}"
        except Exception as e:
            return f"Error getting crypto price: {str(e)}"

    def get_stock_info(self, symbol):
        """Get stock market information"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            current_price = info.get('regularMarketPrice', 'N/A')
            previous_close = info.get('regularMarketPreviousClose', 'N/A')
            return f"Stock Info for {symbol}:\nCurrent Price: ${current_price}\nPrevious Close: ${previous_close}"
        except Exception as e:
            return f"Error getting stock info: {str(e)}"

    def handle_youtube_download(self, command):
        """Handle YouTube video download"""
        try:
            # For demo purposes, using a sample URL
            url = "https://www.youtube.com/watch?v=sample"
            audio_only = "audio only" in command.lower()
            
            yt = YouTube(url)
            if audio_only:
                stream = yt.streams.filter(only_audio=True).first()
                output_file = stream.download(output_path="downloads", filename_prefix="audio_")
                return f"Audio downloaded: {output_file}"
            else:
                stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                output_file = stream.download(output_path="downloads")
                return f"Video downloaded: {output_file}"
        except Exception as e:
            return f"Error downloading video: {str(e)}"

    def handle_qr_generation(self, command):
        """Handle QR code generation"""
        try:
            data = command.replace("create qr", "").strip()
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(data)
            qr.make(fit=True)
            
            filename = f"qr_code_{int(time.time())}.png"
            qr.make_image(fill_color="black", back_color="white").save(filename)
            return f"QR code generated: {filename}"
        except Exception as e:
            return f"Error generating QR code: {str(e)}"

    def chat_with_gpt(self, prompt):
        """Chat with GPT model"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error chatting with GPT: {str(e)}"

    def get_help_text(self):
        """Get help information"""
        return """
        I can help you with:
        1. System Information: "system info"
        2. Weather Updates: "weather"
        3. News Updates: "news [category]"
        4. Translations: "translate [text] to [language]"
        5. Cryptocurrency Prices: "crypto [symbol]"
        6. Stock Information: "stock price [symbol]"
        7. YouTube Downloads: "download youtube [url]"
        8. QR Code Generation: "create qr [data]"
        9. AI Chat: "chat [message]"
        
        You can also use voice commands by clicking the microphone button!
        """

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernAIAssistant()
    app.run()
