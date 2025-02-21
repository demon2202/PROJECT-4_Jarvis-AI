import tkinter as tk
from tkinter import scrolledtext, PhotoImage, ttk, filedialog
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
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ModernAIAssistant:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced AI Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2E3440")
        
        # Set application icon
        try:
            self.root.iconbitmap("ai_icon.ico")
        except:
            pass  # Icon file not found, continue without it
            
        # Setup theme and styles
        self.setup_theme()
        self.setup_core_components()
        self.setup_gui()
        
        # Command history
        self.command_history = []
        self.history_index = 0
        
        # Animations and visual effects
        self.typing_effect_speed = 10  # ms between characters
        self.is_listening = False
        
        # Easter eggs and personality
        self.compliment_list = [
            "You look great today!",
            "Your questions are always so interesting.",
            "I'm glad we're working together.",
            "You have excellent taste in AI assistants!",
            "Your creativity inspires me."
        ]

    def setup_theme(self):
        """Setup theme colors and styles"""
        # Nord theme colors
        self.colors = {
            "bg": "#2E3440",
            "fg": "#ECEFF4",
            "accent1": "#88C0D0",
            "accent2": "#5E81AC",
            "success": "#A3BE8C",
            "warning": "#EBCB8B",
            "error": "#BF616A",
            "dark": "#3B4252",
            "light": "#D8DEE9"
        }
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure button style
        self.style.configure(
            "TButton",
            background=self.colors["accent1"],
            foreground=self.colors["bg"],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            focusthickness=3,
            focuscolor=self.colors["accent2"]
        )
        self.style.map(
            "TButton",
            background=[("active", self.colors["accent2"])],
            relief=[("pressed", "groove"), ("active", "ridge")]
        )
        
        # Configure progressbar style
        self.style.configure(
            "TProgressbar",
            troughcolor=self.colors["dark"],
            background=self.colors["accent1"],
            thickness=8
        )

    def setup_core_components(self):
        """Initialize core AI components"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Get available voices and set a female voice if available
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "female" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
                
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

        # Face Recognition
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Command categories for the sidebar
        self.command_categories = {
            "System": ["system info", "battery", "screenshot", "time"],
            "Web": ["search", "news", "wikipedia", "weather"],
            "Media": ["play music", "detect face", "qr code"],
            "Tools": ["calculate", "open", "joke"],
            "Settings": ["voice settings", "ui theme", "clear chat"]
        }

    def setup_gui(self):
        """Create modern GUI components"""
        # Main container with two frames
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar for features and categories
        self.sidebar = tk.Frame(self.main_container, bg=self.colors["dark"], width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        # App logo and title in sidebar
        self.logo_frame = tk.Frame(self.sidebar, bg=self.colors["dark"])
        self.logo_frame.pack(fill=tk.X, pady=20)
        
        self.title_label = tk.Label(
            self.logo_frame, 
            text="NOVA AI", 
            font=("Segoe UI", 18, "bold"),
            fg=self.colors["accent1"],
            bg=self.colors["dark"]
        )
        self.title_label.pack()
        
        self.subtitle_label = tk.Label(
            self.logo_frame,
            text="Your Personal Assistant",
            font=("Segoe UI", 9),
            fg=self.colors["light"],
            bg=self.colors["dark"]
        )
        self.subtitle_label.pack(pady=(0, 10))
        
        # Add category buttons to sidebar
        self.category_buttons = {}
        for category, commands in self.command_categories.items():
            frame = tk.Frame(self.sidebar, bg=self.colors["dark"])
            frame.pack(fill=tk.X, pady=5)
            
            btn = tk.Button(
                frame,
                text=category,
                font=("Segoe UI", 11),
                bg=self.colors["dark"],
                fg=self.colors["fg"],
                activebackground=self.colors["accent2"],
                activeforeground=self.colors["fg"],
                bd=0,
                padx=10,
                pady=5,
                anchor="w",
                width=20,
                command=lambda c=category, cmds=commands: self.show_category_commands(c, cmds)
            )
            btn.pack(fill=tk.X)
            self.category_buttons[category] = btn
        
        # System stats in sidebar
        self.stats_frame = tk.Frame(self.sidebar, bg=self.colors["dark"])
        self.stats_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        self.cpu_label = tk.Label(
            self.stats_frame,
            text="CPU: 0%",
            font=("Segoe UI", 8),
            fg=self.colors["light"],
            bg=self.colors["dark"],
            anchor="w"
        )
        self.cpu_label.pack(fill=tk.X, padx=10, pady=2)
        
        self.memory_label = tk.Label(
            self.stats_frame,
            text="Memory: 0%",
            font=("Segoe UI", 8),
            fg=self.colors["light"],
            bg=self.colors["dark"],
            anchor="w"
        )
        self.memory_label.pack(fill=tk.X, padx=10, pady=2)
        
        # Start system monitoring
        self.update_system_stats()
        
        # Right content area
        self.content_area = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat display area with custom styling
        self.chat_frame = tk.Frame(self.content_area, bg=self.colors["bg"])
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chat history with custom styling
        self.textbox = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap="word",
            font=("Segoe UI", 11),
            bg=self.colors["dark"],
            fg=self.colors["fg"],
            insertbackground=self.colors["light"],
            selectbackground=self.colors["accent2"],
            bd=0,
            padx=10,
            pady=10
        )
        self.textbox.pack(fill=tk.BOTH, expand=True)
        self.textbox.insert(tk.END, "🤖 Welcome to NOVA AI Assistant! How can I help you today?\n")
        self.textbox.tag_configure("assistant", foreground=self.colors["accent1"])
        self.textbox.tag_configure("user", foreground=self.colors["success"])
        self.textbox.tag_configure("error", foreground=self.colors["error"])
        self.textbox.tag_configure("highlight", foreground=self.colors["warning"])
        self.textbox.configure(state="disabled")
        
        # Bottom control bar with input and buttons
        self.control_frame = tk.Frame(self.content_area, bg=self.colors["dark"], height=80)
        self.control_frame.pack(fill=tk.X)
        
        # Voice mode toggle
        self.voice_mode_var = tk.BooleanVar(value=False)
        self.voice_mode_check = tk.Checkbutton(
            self.control_frame,
            text="Voice Mode",
            variable=self.voice_mode_var,
            bg=self.colors["dark"],
            fg=self.colors["light"],
            selectcolor=self.colors["dark"],
            activebackground=self.colors["dark"],
            activeforeground=self.colors["accent1"],
            font=("Segoe UI", 9),
        )
        self.voice_mode_check.pack(side=tk.LEFT, padx=10)
        
        # Text input with placeholder
        self.input_frame = tk.Frame(self.control_frame, bg=self.colors["dark"], padx=5, pady=5)
        self.input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.text_input = tk.Entry(
            self.input_frame,
            font=("Segoe UI", 11),
            bg=self.colors["bg"],
            fg=self.colors["fg"],
            insertbackground=self.colors["light"],
            bd=0,
            relief=tk.FLAT
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, ipady=8, padx=10)
        self.text_input.bind("<Return>", lambda event: self.process_text_input())
        self.text_input.bind("<Up>", self.navigate_history_up)
        self.text_input.bind("<Down>", self.navigate_history_down)
        
        # Add placeholder text
        self.text_input.insert(0, "Type your command here...")
        self.text_input.bind("<FocusIn>", self.on_entry_click)
        self.text_input.bind("<FocusOut>", self.on_focus_out)
        
        # Button frame
        self.button_frame = tk.Frame(self.control_frame, bg=self.colors["dark"])
        self.button_frame.pack(side=tk.RIGHT, padx=10)
        
        # Speak button with microphone icon
        self.speak_button = ttk.Button(
            self.button_frame,
            text="🎤 Speak",
            command=self.voice_input,
            style="TButton"
        )
        self.speak_button.pack(side=tk.LEFT, padx=5)
        
        # Send button with send icon
        self.send_button = ttk.Button(
            self.button_frame,
            text="📤 Send",
            command=self.process_text_input,
            style="TButton"
        )
        self.send_button.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_frame = tk.Frame(self.root, bg=self.colors["dark"], height=25)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Ready",
            font=("Segoe UI", 8),
            bg=self.colors["dark"],
            fg=self.colors["light"],
            anchor="w",
            padx=10
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Add visualizer canvas for voice input
        self.visualizer_canvas = tk.Canvas(
            self.status_frame,
            width=100,
            height=20,
            bg=self.colors["dark"],
            highlightthickness=0
        )
        self.visualizer_canvas.pack(side=tk.RIGHT, padx=10)
        
        # Welcome the user
        self.add_welcome_message()

    def on_entry_click(self, event):
        """Clear placeholder text when entry is clicked"""
        if self.text_input.get() == "Type your command here...":
            self.text_input.delete(0, tk.END)
            self.text_input.configure(fg=self.colors["fg"])

    def on_focus_out(self, event):
        """Add placeholder text if entry is empty"""
        if self.text_input.get() == "":
            self.text_input.insert(0, "Type your command here...")
            self.text_input.configure(fg=self.colors["light"])

    def navigate_history_up(self, event):
        """Navigate command history upward"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            self.text_input.delete(0, tk.END)
            self.text_input.insert(0, self.command_history[self.history_index])
            return "break"  # Prevent default behavior

    def navigate_history_down(self, event):
        """Navigate command history downward"""
        if self.command_history and self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.text_input.delete(0, tk.END)
            self.text_input.insert(0, self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            # At the end of history, clear the input
            self.history_index = len(self.command_history)
            self.text_input.delete(0, tk.END)
        return "break"  # Prevent default behavior

    def update_system_stats(self):
        """Update system stats in sidebar"""
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        
        self.cpu_label.config(text=f"CPU: {cpu_percent}%")
        self.memory_label.config(text=f"Memory: {memory_percent}%")
        
        # Change color based on usage
        if cpu_percent > 80:
            self.cpu_label.config(fg=self.colors["error"])
        elif cpu_percent > 50:
            self.cpu_label.config(fg=self.colors["warning"])
        else:
            self.cpu_label.config(fg=self.colors["light"])
            
        if memory_percent > 80:
            self.memory_label.config(fg=self.colors["error"])
        elif memory_percent > 50:
            self.memory_label.config(fg=self.colors["warning"])
        else:
            self.memory_label.config(fg=self.colors["light"])
        
        self.root.after(5000, self.update_system_stats)  # Update every 5 seconds

    def show_category_commands(self, category, commands):
        """Display available commands for a category"""
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, f"\n🔍 Available {category} Commands:\n", "highlight")
        for cmd in commands:
            self.textbox.insert(tk.END, f"  • {cmd}\n")
        self.textbox.configure(state="disabled")
        self.textbox.see(tk.END)

    def add_welcome_message(self):
        """Add a welcome animation to the chat area"""
        welcome_text = [
            "Welcome to NOVA AI Assistant!",
            "I can help you with various tasks including:",
            "• System information and monitoring",
            "• Web searches and information retrieval",
            "• Media playback and face detection",
            "• Calculations and productivity tools",
            "Try saying 'show commands' to see what I can do!"
        ]
        
        # Display the welcome message with animation
        self.textbox.configure(state="normal")
        for line in welcome_text:
            self.display_with_typing_effect(line + "\n")
        self.textbox.configure(state="disabled")

    def display_with_typing_effect(self, text, tag=None):
        if not text:  # Guard clause for empty text
         return
        def type_text(remaining_text, index=0):
        # ... (existing logic)
            try:
                self.root.after(self.typing_effect_speed, lambda: type_text(remaining_text, index + 1))
            except Exception as e:
                print(f"Error in typing effect: {e}")  # Graceful error handling
        type_text(text)

    def process_text_input(self):
        """Process text input from the entry field"""
        command = self.text_input.get()
        
        # Skip if it's the placeholder text or empty
        if command == "Type your command here..." or command.strip() == "":
            return
            
        # Add to command history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Clear the input field
        self.text_input.delete(0, tk.END)
        
        # Display the command in the chat area
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, f"\n👤 You: {command}\n", "user")
        self.textbox.configure(state="disabled")
        self.textbox.see(tk.END)
        
        # Process the command
        threading.Thread(target=self.handle_command, args=(command,)).start()

    def handle_command(self, command):
        """Process the command in a separate thread"""
        # Update status
        self.update_status("Processing...")
        
        # Process the command
        response = self.process_command(command)
        
        # Display the response
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, f"🤖 NOVA: ", "assistant")
        
        # Use typing effect for responses
        self.display_with_typing_effect(response + "\n")
        
        self.textbox.configure(state="disabled")
        self.textbox.see(tk.END)
        
        # Speak the response if voice mode is enabled
        if self.voice_mode_var.get():
            threading.Thread(target=self.speak, args=(response,)).start()
            
        # Update status
        self.update_status("Ready")
        
        # Occasionally add a random compliment (1 in 10 chance)
        if random.random() < 0.1:
            self.root.after(3000, self.add_random_compliment)

    def add_random_compliment(self):
        """Add a random compliment to the chat"""
        compliment = random.choice(self.compliment_list)
        
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, f"🤖 NOVA: {compliment}\n", "assistant")
        self.textbox.configure(state="disabled")
        self.textbox.see(tk.END)

    def update_status(self, status):
        """Update status bar"""
        self.status_label.config(text=status)
        
    def voice_input(self):
        """Capture voice command with visualization"""
        if self.is_listening:
            return
            
        self.is_listening = True
        threading.Thread(target=self._listen_thread).start()
        
        # Start visualizer animation
        self.animate_voice_visualizer()

    def _listen_thread(self):
        """Background thread for voice recognition"""
        self.update_status("Listening...")
        
        try:
            with sr.Microphone() as source:
                self.textbox.configure(state="normal")
                self.textbox.insert(tk.END, "\n🎤 Listening...\n", "highlight")
                self.textbox.configure(state="disabled")
                self.textbox.see(tk.END)
                
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            command = self.recognizer.recognize_google(audio).lower()
            
            # Display and process the command
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"👤 You: {command}\n", "user")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)
            
            # Add to command history
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            
            # Process the command
            response = self.process_command(command)
            
            # Display the response
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"🤖 NOVA: ", "assistant")
            self.display_with_typing_effect(response + "\n")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)
            
            # Speak the response
            self.speak(response)
            
        except sr.UnknownValueError:
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, "🤖 NOVA: Sorry, I couldn't understand that.\n", "error")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)
            self.speak("Sorry, I couldn't understand that.")
            
        except sr.RequestError as e:
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"🤖 NOVA: Error with speech recognition service: {e}\n", "error")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)
            
        except Exception as e:
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"🤖 NOVA: An error occurred: {e}\n", "error")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)
            
        finally:
            self.is_listening = False
            self.update_status("Ready")
            
    def animate_voice_visualizer(self):
        """Animate the voice visualizer bars"""
        if not self.is_listening:
            # Clear the canvas
            self.visualizer_canvas.delete("all")
            return
            
        # Clear the canvas
        self.visualizer_canvas.delete("all")
        
        # Draw animated bars
        width = self.visualizer_canvas.winfo_width()
        height = self.visualizer_canvas.winfo_height()
        bar_width = 4
        gap = 2
        bars = 10
        total_width = bars * (bar_width + gap)
        start_x = (width - total_width) // 2
        
        for i in range(bars):
            # Random height for each bar
            bar_height = random.randint(5, height)
            x1 = start_x + i * (bar_width + gap)
            y1 = (height - bar_height) / 2
            x2 = x1 + bar_width
            y2 = y1 + bar_height
            
            # Gradient color based on height
            intensity = int(255 * (bar_height / height))
            color = f"#{intensity:02x}{intensity//2:02x}ff"
            
            self.visualizer_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            
        if self.is_listening:
            self.root.after(100, self.animate_voice_visualizer)

    def process_command(self, command):
        """Process and execute commands with enhanced functionality"""
        command = command.lower()
        
        # Easter egg
        if "hello" in command or "hi nova" in command:
            return random.choice([
                "Hello there! How can I assist you today?",
                "Hi! I'm NOVA, your friendly AI assistant.",
                "Greetings! What can I help you with?"
            ])
            
        # Help command
        if "help" in command or "what can you do" in command or "show commands" in command:
            help_text = "Here are some things I can do:\n"
            for category, cmds in self.command_categories.items():
                help_text += f"\n{category}:\n"
                for cmd in cmds:
                    help_text += f"  • {cmd}\n"
            return help_text
            
        # Standard commands
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
            threading.Thread(target=self.detect_face).start()
            return "Starting face detection. Press 'q' to stop."
        elif "open" in command:
            return self.open_application(command)
        elif "search" in command:
            return self.search_web(command)
        elif "wikipedia" in command:
            return self.search_wikipedia(command)
        elif "play" in command and "music" in command:
            return self.play_music()
        elif "time" in command:
            return self.get_current_time()
        elif "exit" in command or "quit" in command:
            self.root.after(1000, self.root.quit)
            return "Shutting down. Goodbye!"
        elif "voice" in command and "settings" in command:
            return self.change_voice_settings()
        elif "theme" in command or "color" in command:
            return self.change_ui_theme(command)
        elif "weather" in command:
            return self.get_weather(command)
        elif "cpu" in command or "memory" in command or "performance" in command:
            return self.show_system_performance()
        elif "clear" in command:
            self.clear_chat()
            return "Chat history cleared."
        else:
            return "I'm not sure how to help with that. Try saying 'help' to see what I can do."

    def speak(self, text):
        """Speak output with animation"""
        self.update_status("Speaking...")
        self.engine.say(text)
        self.engine.runAndWait()
        self.update_status("Ready")

    def get_system_info(self):
        """Return enhanced system information with formatting"""
        # Get basic system info
        info = [
            f"Operating System: {platform.system()} {platform.release()}",
            f"Version: {platform.version()}",
            f"Architecture: {platform.machine()}",
            f"Processor: {platform.processor()}",
            f"Hostname: {socket.gethostname()}",
            f"IP Address: {socket.gethostbyname(socket.gethostname())}",
            f"Python Version: {platform.python_version()}"
        ]
        
        # Add memory info
        memory = psutil.virtual_memory()
        info.append(f"Total Memory: {self.format_bytes(memory.total)}")
        info.append(f"Available Memory: {self.format_bytes(memory.available)}")
        info.append(f"Memory Usage: {memory.percent}%")
        
        # Add disk info
        disk = psutil.disk_usage('/')
        info.append(f"Total Disk Space: {self.format_bytes(disk.total)}")
        info.append(f"Free Disk Space: {self.format_bytes(disk.free)}")
        info.append(f"Disk Usage: {disk.percent}%")
        
        # Add CPU info
        info.append(f"CPU Cores: {psutil.cpu_count(logical=False)}")
        info.append(f"Logical CPUs: {psutil.cpu_count(logical=True)}")
        info.append(f"Current CPU Usage: {psutil.cpu_percent()}%")
        
        # Add uptime
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        info.append(f"System Uptime: {hours}h {minutes}m {seconds}s")
        
        # Show system performance graph
        self.show_system_performance_graph()
        
        return "\n".join(info)

    def format_bytes(self, bytes):
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024
        return f"{bytes:.2f} PB"

    def take_screenshot(self):
        """Capture and save a screenshot with preview"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        
        try:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            
            # Create thumbnail preview
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"\nScreenshot saved as {filename}\n")
            
            # Create thumbnail of screenshot
            thumbnail = screenshot.resize((320, 180))
            photo = ImageTk.PhotoImage(thumbnail)
            
            # Create a label to display the thumbnail
            img_label = tk.Label(self.textbox, image=photo)
            img_label.image = photo  # Keep a reference
            self.textbox.window_create(tk.END, window=img_label)
            self.textbox.insert(tk.END, "\n")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)
            
            return f"Screenshot saved as {filename}."
        except Exception as e:
            return f"Error taking screenshot: {e}"

    def get_battery_status(self):
        """Get the battery status of the device"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                power_plugged = battery.power_plugged
                
                # Estimate remaining time
                if power_plugged:
                    status = "Charging"
                    time_left = "N/A (Plugged in)"
                else:
                    status = "Discharging"
                    seconds_left = battery.secsleft
                    if seconds_left == psutil.POWER_TIME_UNLIMITED:
                        time_left = "Power time unlimited"
                    elif seconds_left == psutil.POWER_TIME_UNKNOWN:
                        time_left = "Unknown"
                    else:
                        hours, remainder = divmod(seconds_left, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        time_left = f"{hours}h {minutes}m {seconds}s"
                
                # Create a battery visualization
                self.create_battery_visualization(percent)
                
                return f"Battery Status: {percent}% ({status})\nEstimated Time Remaining: {time_left}"
            else:
                return "No battery detected on this device."
        except Exception as e:
            return f"Error getting battery status: {e}"

    def create_battery_visualization(self, percent):
        """Create a visual battery indicator"""
        self.textbox.configure(state="normal")
        
        # Create a frame for the battery visualization
        battery_frame = tk.Frame(self.textbox, bg=self.colors["dark"], padx=10, pady=5)
        
        # Battery outline
        battery_outline = tk.Canvas(battery_frame, width=200, height=30, bg=self.colors["dark"], highlightthickness=0)
        battery_outline.create_rectangle(0, 0, 180, 30, outline=self.colors["light"], width=2)
        battery_outline.create_rectangle(180, 8, 190, 22, fill=self.colors["light"], outline=self.colors["light"])
        
        # Battery fill
        fill_width = int(1.8 * percent)
        
        # Determine color based on percentage
        if percent <= 20:
            fill_color = self.colors["error"]
        elif percent <= 50:
            fill_color = self.colors["warning"]
        else:
            fill_color = self.colors["success"]
            
        battery_outline.create_rectangle(3, 3, fill_width, 27, fill=fill_color, outline="")
        
        # Add percentage text
        text_x = 195 + 10
        battery_outline.create_text(100, 15, text=f"{percent}%", fill=self.colors["light"])
        
        battery_outline.pack(side=tk.LEFT)
        
        # Add to textbox
        self.textbox.window_create(tk.END, window=battery_frame)
        self.textbox.insert(tk.END, "\n")
        self.textbox.configure(state="disabled")

    def generate_qr_code(self, command):
        """Generate a QR code for the given text"""
        # Extract the text after "qr code"
        try:
            query = command.split("qr code")[1].strip()
        except:
            return "Please specify the text for the QR code. For example: 'qr code https://example.com'"
            
        if not query:
            return "Please specify the text for the QR code. For example: 'qr code https://example.com'"
            
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(query)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save the QR code
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qrcode_{timestamp}.png"
            img.save(filename)
            
            # Display the QR code
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"\nQR Code for '{query}' saved as {filename}\n")
            
            # Convert PIL Image to Tkinter PhotoImage
            img_tk = ImageTk.PhotoImage(img)
            
            # Create a label for the QR code
            img_label = tk.Label(self.textbox, image=img_tk)
            img_label.image = img_tk  # Keep a reference
            self.textbox.window_create(tk.END, window=img_label)
            self.textbox.insert(tk.END, "\n")
            self.textbox.configure(state="disabled")
            
            return f"QR Code generated for: {query}"
        except Exception as e:
            return f"Error generating QR code: {e}"

    def calculate(self, command):
        """Simple calculator functionality"""
        # Extract the expression after "calculate"
        try:
            expression = command.split("calculate")[1].strip()
        except:
            return "Please provide a math expression to calculate."
            
        if not expression:
            return "Please provide a math expression to calculate."
            
        try:
            # Replace words with operators
            expression = expression.replace("plus", "+")
            expression = expression.replace("minus", "-")
            expression = expression.replace("times", "*")
            expression = expression.replace("divided by", "/")
            expression = expression.replace("divided", "/")
            expression = expression.replace("multiplied by", "*")
            expression = expression.replace("multiply", "*")
            expression = expression.replace("divide", "/")
            expression = expression.replace("modulo", "%")
            expression = expression.replace("mod", "%")
            
            # Safely evaluate the expression
            result = eval(expression)
            
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating: {e}"

    def get_local_news(self):
        """Get top headlines news"""
        try:
            # Use a free news API
            response = requests.get("https://news.google.com/rss")
            soup = BeautifulSoup(response.content, features="xml")
            items = soup.findAll('item')
            news_items = []
            
            # Get the first 5 news items
            for i, item in enumerate(items[:5]):
                title = item.title.text
                link = item.link.text
                pubDate = item.pubDate.text
                news_items.append(f"{i+1}. {title} ({pubDate})")
                
            return "Top Headlines:\n" + "\n".join(news_items)
        except Exception as e:
            return f"Error fetching news: {e}"

    def detect_face(self):
        """Real-time face detection using webcam"""
        try:
            # Open webcam
            cap = cv2.VideoCapture(0)
            
            while True:
                # Read frame
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                # Draw rectangles around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Face Detected", (x, y-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Display number of faces found
                cv2.putText(frame, f"Faces Found: {len(faces)}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                # Display the resulting frame
                cv2.imshow('Face Detection - Press q to quit', frame)
                
                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            # Release resources
            cap.release()
            cv2.destroyAllWindows()
            
            return f"Face detection completed. Found {len(faces)} faces in the last frame."
        except Exception as e:
            return f"Error in face detection: {e}"

    def open_application(self, command):
        """Open common applications"""
        try:
            app_name = command.split("open")[1].strip().lower()
            
            # Common applications
            apps = {
                "browser": ["chrome", "firefox", "safari", "msedge"],
                "notepad": ["notepad", "notepad++"],
                "calculator": ["calc"],
                "file explorer": ["explorer"],
                "music player": ["wmplayer", "spotify"],
                "word": ["winword"],
                "excel": ["excel"],
                "powerpoint": ["powerpnt"],
                "terminal": ["cmd", "powershell"],
                "settings": ["ms-settings:"],
                "camera": ["microsoft.windows.camera:"],
            }
            
            # Try to find the app in the dictionary
            opened = False
            if app_name in apps:
                for app in apps[app_name]:
                    try:
                        subprocess.Popen(app)
                        opened = True
                        return f"Opening {app_name}..."
                    except:
                        continue
            
            # If not found, try to open it directly
            if not opened:
                try:
                    subprocess.Popen(app_name)
                    return f"Opening {app_name}..."
                except:
                    return f"Could not open {app_name}. Application not found."
                    
        except Exception as e:
            return f"Error opening application: {e}"

    def search_web(self, command):
        """Search the web for a query"""
        try:
            # Extract the search query
            query = command.split("search")[1].strip()
            
            if query:
                # Format the query for URL
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(search_url)
                return f"Searching for '{query}'..."
            else:
                return "Please specify what to search for."
        except Exception as e:
            return f"Error searching the web: {e}"

    def search_wikipedia(self, command):
        """Search Wikipedia for information"""
        try:
            # Extract the query
            query = command.replace("wikipedia", "").strip()
            
            if not query:
                return "Please specify what to search for on Wikipedia."
                
            # Search Wikipedia
            results = wikipedia.search(query)
            
            if not results:
                return f"No Wikipedia results found for '{query}'."
                
            # Get the page summary
            try:
                page = wikipedia.page(results[0])
                summary = wikipedia.summary(results[0], sentences=3)
                return f"Wikipedia: {summary}\n\nMore info: {page.url}"
            except wikipedia.DisambiguationError as e:
                return f"Multiple matches found. Try one of these: {', '.join(e.options[:5])}"
                
        except Exception as e:
            return f"Error searching Wikipedia: {e}"

    def play_music(self):
        """Simple music player functionality"""
        # Ask user to select a music file
        file_path = filedialog.askopenfilename(
            title="Select a music file",
            filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")]
        )
        
        if file_path:
            try:
                # On Windows, use the default media player
                if platform.system() == "Windows":
                    os.startfile(file_path)
                # On macOS, use the 'afplay' command
                elif platform.system() == "Darwin":
                    subprocess.Popen(["afplay", file_path])
                # On Linux, try with 'xdg-open'
                else:
                    subprocess.Popen(["xdg-open", file_path])
                    
                return f"Playing music: {os.path.basename(file_path)}"
            except Exception as e:
                return f"Error playing music: {e}"
        else:
            return "No music file selected."

    def get_current_time(self):
        """Get current time and date information"""
        now = datetime.datetime.now()
        
        # Format time and date
        time_str = now.strftime("%I:%M:%S %p")
        date_str = now.strftime("%A, %B %d, %Y")
        
        # Add timezone information
        timezone = datetime.datetime.now().astimezone().tzinfo
        
        return f"Current Time: {time_str}\nDate: {date_str}\nTimezone: {timezone}"

    def change_voice_settings(self):
        """Change voice settings like rate and volume"""
        # Create a dialog window
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Voice Settings")
        settings_window.geometry("300x250")
        settings_window.configure(bg=self.colors["dark"])
        
        # Add voice rate slider
        tk.Label(
            settings_window, 
            text="Voice Rate:", 
            font=("Segoe UI", 10),
            bg=self.colors["dark"],
            fg=self.colors["light"]
        ).pack(pady=(20, 5))
        
        rate_var = tk.IntVar(value=self.engine.getProperty('rate'))
        rate_slider = tk.Scale(
            settings_window,
            from_=100,
            to=300,
            orient=tk.HORIZONTAL,
            length=200,
            variable=rate_var,
            bg=self.colors["dark"],
            fg=self.colors["light"],
            highlightthickness=0,
            troughcolor=self.colors["bg"]
        )
        rate_slider.pack()
        
        # Add voice selection
        tk.Label(
            settings_window, 
            text="Voice:", 
            font=("Segoe UI", 10),
            bg=self.colors["dark"],
            fg=self.colors["light"]
        ).pack(pady=(20, 5))
        
        voices = self.engine.getProperty('voices')
        voice_names = [voice.name for voice in voices]
        voice_var = tk.StringVar(value=voices[0].name)
        
        voice_menu = ttk.Combobox(
            settings_window,
            textvariable=voice_var,
            values=voice_names,
            state="readonly",
            width=30
        )
        voice_menu.pack(pady=5)
        
        # Set current voice
        current_voice_id = self.engine.getProperty('voice')
        for idx, voice in enumerate(voices):
            if voice.id == current_voice_id:
                voice_menu.current(idx)
                break
        
        # Add apply button
        tk.Button(
            settings_window,
            text="Apply Changes",
            font=("Segoe UI", 10),
            bg=self.colors["accent1"],
            fg=self.colors["dark"],
            activebackground=self.colors["accent2"],
            activeforeground=self.colors["light"],
            command=lambda: self.apply_voice_settings(rate_var.get(), voice_var.get(), voices, settings_window)
        ).pack(pady=20)
        
        return "Voice settings dialog opened."

    def apply_voice_settings(self, rate, voice_name, voices, window):
        """Apply the selected voice settings"""
        # Set voice rate
        self.engine.setProperty('rate', rate)
        
        # Set voice
        for voice in voices:
            if voice.name == voice_name:
                self.engine.setProperty('voice', voice.id)
                break
                
        # Close settings window
        window.destroy()
        
        # Provide feedback
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, "🤖 NOVA: Voice settings updated successfully.\n", "assistant")
        self.textbox.configure(state="disabled")
        self.textbox.see(tk.END)
        
        # Speak with new settings
        self.speak("Voice settings have been updated. This is how I sound now.")

    def change_ui_theme(self, command):
        """Change UI theme colors"""
        # Predefined themes
        themes = {
            "dark": {
                "bg": "#2E3440",
                "fg": "#ECEFF4",
                "accent1": "#88C0D0",
                "accent2": "#5E81AC",
                "success": "#A3BE8C",
                "warning": "#EBCB8B",
                "error": "#BF616A",
                "dark": "#3B4252",
                "light": "#D8DEE9"
            },
            "light": {
                "bg": "#ECEFF4",
                "fg": "#2E3440",
                "accent1": "#5E81AC",
                "accent2": "#81A1C1",
                "success": "#A3BE8C",
                "warning": "#EBCB8B",
                "error": "#BF616A",
                "dark": "#D8DEE9",
                "light": "#3B4252"
            },
            "blue": {
                "bg": "#1A2733",
                "fg": "#FFFFFF",
                "accent1": "#0078D4",
                "accent2": "#2B88D8",
                "success": "#0EA57A",
                "warning": "#FFC83D",
                "error": "#F03A17",
                "dark": "#2C3E50",
                "light": "#E0E0E0"
            },
            "purple": {
                "bg": "#2D2B55",
                "fg": "#FFFFFF",
                "accent1": "#9D65FF",
                "accent2": "#7E57C2",
                "success": "#4CD964",
                "warning": "#FFCC00",
                "error": "#FF5252",
                "dark": "#1E1E3F",
                "light": "#E0E0E0"
            }
        }
        
        # Check if a specific theme is requested
        theme_name = ""
        for theme in themes.keys():
            if theme in command:
                theme_name = theme
                break
                
        if not theme_name:
            # If no specific theme requested, show theme selection dialog
            theme_window = tk.Toplevel(self.root)
            theme_window.title("Select UI Theme")
            theme_window.geometry("400x300")
            theme_window.configure(bg=self.colors["dark"])
            
            tk.Label(
                theme_window, 
                text="Select a Theme:", 
                font=("Segoe UI", 12, "bold"),
                bg=self.colors["dark"],
                fg=self.colors["light"]
            ).pack(pady=(20, 15))
            
            # Create theme buttons with preview
            for theme_name, theme_colors in themes.items():
                frame = tk.Frame(theme_window, bg=theme_colors["dark"], padx=10, pady=5, relief=tk.RAISED, bd=1)
                frame.pack(fill=tk.X, padx=20, pady=5)
                
                btn = tk.Button(
                    frame,
                    text=f"{theme_name.title()} Theme",
                    font=("Segoe UI", 10),
                    bg=theme_colors["accent1"],
                    fg=theme_colors["bg"],
                    activebackground=theme_colors["accent2"],
                    activeforeground=theme_colors["fg"],
                    command=lambda t=theme_name: self.apply_theme(t, themes, theme_window)
                )
                btn.pack(fill=tk.X, ipady=5)
                
            return "Theme selection dialog opened."
            
        else:
            # Apply the selected theme directly
            self.apply_theme(theme_name, themes)
            return f"{theme_name.title()} theme applied successfully."

    def apply_theme(self, theme_name, themes, window=None):
        """Apply the selected theme to the UI"""
        if theme_name in themes:
            # Update color dictionary
            self.colors = themes[theme_name]
            
            # Update main window
            self.root.configure(bg=self.colors["bg"])
            self.main_container.configure(bg=self.colors["bg"])
            self.content_area.configure(bg=self.colors["bg"])
            
            # Update sidebar
            self.sidebar.configure(bg=self.colors["dark"])
            self.logo_frame.configure(bg=self.colors["dark"])
            self.title_label.configure(bg=self.colors["dark"], fg=self.colors["accent1"])
            self.subtitle_label.configure(bg=self.colors["dark"], fg=self.colors["light"])
            self.stats_frame.configure(bg=self.colors["dark"])
            self.cpu_label.configure(bg=self.colors["dark"], fg=self.colors["light"])
            self.memory_label.configure(bg=self.colors["dark"], fg=self.colors["light"])
            
            # Update sidebar buttons
            for category, btn in self.category_buttons.items():
                btn.configure(
                    bg=self.colors["dark"],
                    fg=self.colors["fg"],
                    activebackground=self.colors["accent2"],
                    activeforeground=self.colors["fg"]
                )
            
            # Update text area
            self.textbox.configure(
                bg=self.colors["dark"],
                fg=self.colors["fg"],
                insertbackground=self.colors["light"],
                selectbackground=self.colors["accent2"]
            )
            self.textbox.tag_configure("assistant", foreground=self.colors["accent1"])
            self.textbox.tag_configure("user", foreground=self.colors["success"])
            self.textbox.tag_configure("error", foreground=self.colors["error"])
            self.textbox.tag_configure("highlight", foreground=self.colors["warning"])
            
            # Update control frame
            self.control_frame.configure(bg=self.colors["dark"])
            self.voice_mode_check.configure(
                bg=self.colors["dark"],
                fg=self.colors["light"],
                selectcolor=self.colors["dark"],
                activebackground=self.colors["dark"],
                activeforeground=self.colors["accent1"]
            )
            self.input_frame.configure(bg=self.colors["dark"])
            self.text_input.configure(
                bg=self.colors["bg"],
                fg=self.colors["fg"],
                insertbackground=self.colors["light"]
            )
            self.button_frame.configure(bg=self.colors["dark"])
            
            # Update status bar
            self.status_frame.configure(bg=self.colors["dark"])
            self.status_label.configure(bg=self.colors["dark"], fg=self.colors["light"])
            self.visualizer_canvas.configure(bg=self.colors["dark"])
            
            # Update ttk styles
            self.style.configure(
                "TButton",
                background=self.colors["accent1"],
                foreground=self.colors["bg"],
                focuscolor=self.colors["accent2"]
            )
            self.style.map(
                "TButton",
                background=[("active", self.colors["accent2"])]
            )
            self.style.configure(
                "TProgressbar",
                troughcolor=self.colors["dark"],
                background=self.colors["accent1"]
            )
            
            # Close theme window if it exists
            if window:
                window.destroy()
                
            # Update textbox with theme change notification
            self.textbox.configure(state="normal")
            self.textbox.insert(tk.END, f"🤖 NOVA: {theme_name.title()} theme applied successfully.\n", "assistant")
            self.textbox.configure(state="disabled")
            self.textbox.see(tk.END)

    def get_weather(self, command):
        """Get weather information for a location"""
        try:
            # Extract location
            if "in" in command:
                location = command.split("in")[1].strip()
            elif "for" in command:
                location = command.split("for")[1].strip()
            else:
                location = command.replace("weather", "").strip()
                
            if not location:
                return "Please specify a location for weather information."
                
            # Make API request to a free weather service
            response = requests.get(f"https://wttr.in/{location}?format=j1")
            data = response.json()
            
            # Extract weather information
            current = data["current_condition"][0]
            temp_c = current["temp_C"]
            temp_f = current["temp_F"]
            desc = current["weatherDesc"][0]["value"]
            humidity = current["humidity"]
            wind_speed = current["windspeedKmph"]
            feels_like = current["FeelsLikeC"]
            
            # Format response
            weather_info = f"Weather in {location.title()}:\n"
            weather_info += f"Temperature: {temp_c}°C ({temp_f}°F)\n"
            weather_info += f"Condition: {desc}\n"
            weather_info += f"Feels like: {feels_like}°C\n"
            weather_info += f"Humidity: {humidity}%\n"
            weather_info += f"Wind speed: {wind_speed} km/h"
            
            # Show weather visualization
            self.show_weather_visualization(temp_c, desc, humidity)
            
            return weather_info
        except Exception as e:
            return f"Error getting weather information: {e}"

    def show_weather_visualization(self, temp, condition, humidity):
        """Create a simple weather visualization"""
        self.textbox.configure(state="normal")
        
        # Create a frame for weather visualization
        weather_frame = tk.Frame(self.textbox, bg=self.colors["dark"], padx=15, pady=10)
        
        # Temperature display
        if float(temp) > 30:
            temp_color = "#FF5252"  # Hot
        elif float(temp) > 20:
            temp_color = "#FFD740"  # Warm
        elif float(temp) > 10:
            temp_color = "#64B5F6"  # Cool
        else:
            temp_color = "#90CAF9"  # Cold
            
        temp_label = tk.Label(
            weather_frame,
            text=f"{temp}°C",
            font=("Segoe UI", 24, "bold"),
            bg=self.colors["dark"],
            fg=temp_color
        )
        temp_label.grid(row=0, column=0, rowspan=2, padx=(0, 20))
        
        # Condition icon
        condition_icon = "☀️"  # Default: sunny
        if "rain" in condition.lower():
            condition_icon = "🌧️"
        elif "cloud" in condition.lower():
            condition_icon = "☁️"
        elif "snow" in condition.lower():
            condition_icon = "❄️"
        elif "fog" in condition.lower() or "mist" in condition.lower():
            condition_icon = "🌫️"
        elif "thunder" in condition.lower() or "storm" in condition.lower():
            condition_icon = "⛈️"
            
        icon_label = tk.Label(
            weather_frame,
            text=condition_icon,
            font=("Segoe UI", 32),
            bg=self.colors["dark"]
        )
        icon_label.grid(row=0, column=1, rowspan=2)
        
        # Condition description
        condition_label = tk.Label(
            weather_frame,
            text=condition,
            font=("Segoe UI", 12),
            bg=self.colors["dark"],
            fg=self.colors["light"]
        )
        condition_label.grid(row=0, column=2, padx=20, sticky="s")
        
        # Humidity display
        humidity_label = tk.Label(
            weather_frame,
            text=f"Humidity: {humidity}%",
            font=("Segoe UI", 10),
            bg=self.colors["dark"],
            fg=self.colors["light"]
        )
        humidity_label.grid(row=1, column=2, padx=20, sticky="n")
        
        # Insert into textbox
        self.textbox.window_create(tk.END, window=weather_frame)
        self.textbox.insert(tk.END, "\n")
        self.textbox.configure(state="disabled")

    def show_system_performance(self):
        """Display system performance information"""
        # Get CPU and memory information
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Create performance visualization
        self.show_system_performance_graph()
        
        # Format response
        performance_info = "System Performance:\n"
        performance_info += f"CPU Usage: {cpu_percent}%\n"
        performance_info += f"Memory Usage: {memory.percent}% (Used: {self.format_bytes(memory.used)} of {self.format_bytes(memory.total)})\n"
        performance_info += f"Disk Usage: {disk.percent}% (Free: {self.format_bytes(disk.free)} of {self.format_bytes(disk.total)})"
        
        return performance_info

    def show_system_performance_graph(self):
        """Show a graph of system performance"""
        self.textbox.configure(state="normal")
        
        # Create a frame for the graph
        graph_frame = tk.Frame(self.textbox)
        
        # Create a figure for the graph
        fig, ax = plt.subplots(figsize=(5, 3))
        fig.patch.set_facecolor(self.colors["dark"])
        
        # Get CPU and memory data for last few seconds
        cpu_percents = [psutil.cpu_percent(interval=0.1) for _ in range(10)]
        memory_percents = [psutil.virtual_memory().percent for _ in range(10)]
        
        # Plot the data
        ax.plot(cpu_percents, 'r-', label='CPU')
        ax.plot(memory_percents, 'b-', label='Memory')
        ax.set_ylim(0, 100)
        ax.set_ylabel('Usage %')
        ax.set_xlabel('Time (last few seconds)')
        ax.set_title('System Resource Usage')
        ax.legend()
        
        # Set colors
        ax.set_facecolor(self.colors["dark"])
        ax.xaxis.label.set_color(self.colors["light"])
        ax.yaxis.label.set_color(self.colors["light"])
        ax.title.set_color(self.colors["light"])
        for spine in ax.spines.values():
            spine.set_color(self.colors["light"])
        
        # Create a canvas to display the figure
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Insert the graph into the textbox
        self.textbox.window_create(tk.END, window=graph_frame)
        self.textbox.insert(tk.END, "\n")
        self.textbox.configure(state="disabled")
        
        # Show the graph
        plt.close(fig)  # Close the figure to prevent it from displaying in a separate window

# Run the application
if __name__ == "__main__":
    assistant = ModernAIAssistant()
    assistant.root.mainloop()
