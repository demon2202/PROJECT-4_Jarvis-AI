# 🚀 Modern AI Assistant

## 📝 Description
Modern AI Assistant is an advanced voice-enabled virtual assistant built using Python. It integrates speech recognition, natural language processing, and AI-based responses to assist users with a variety of tasks such as fetching weather updates, providing news, translating languages, managing emails, controlling the system, and much more!

## 📥 Installation
Follow these steps to set up the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/ModernAI-Assistant.git
   cd ModernAI-Assistant
   ```


2. **Create a Virtual Environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

## 🎯 Usage
Once the assistant is running, you can interact with it using voice commands or text input. Here are some examples:

### 🔊 Voice Commands
-To activate voice commands, simply say **'Hey Assistant'** followed by your request:

-Weather: "weather [location]" - Get the current weather for a specific location.

-Reminder: "reminder [task] in [time]" - Set a reminder (e.g., "reminder drink water in 5 minutes").

-Email: "email [subject] to [recipient]" - Send an email (e.g., "email Hello to friend@gmail.com").

-Translate: "translate [text] to [language]" - Translate text to a specified language (e.g., "translate Hello to Spanish").

-Internet Speed: "internet speed" - Check the current internet speed.

-IP Address: "ip address" - Get your public IP address.

-YouTube: "youtube [query]" - Open YouTube or search for a video.

-Maps: "maps [location]" - Open Google Maps or search for a location.

-Social Media: "social media [platform]" - Open a social media platform (e.g., "social media facebook").

-Read File: "read file [filename]" - Read the contents of a text file.

-Write File: "write file [filename] with [content]" - Write text to a file.

-CPU/Memory Usage: "cpu" or "memory" - Get real-time CPU and memory usage.

### ⌨️ Text Input
If voice input is unavailable, type your command in the interface and press **Enter** to receive responses.

## 🛠 How to Use the Code
To modify or extend the assistant, follow these steps:

1. **Recognizing Voice Commands**
   - Modify `listen()` in `main.py` to handle additional commands.
   ```python
   with sr.Microphone() as source:
       print("Listening...")
       audio = self.recognizer.listen(source)
       command = self.recognizer.recognize_google(audio)
   ```

2. **Adding New Features**
   - Locate `process_command()` and add your custom functionality:
   ```python
   if "play music" in command:
       self.play_music()
   ```

3. **Fetching Weather Data**
   - Update `get_weather()` to adjust for different APIs or locations.
   ```python
   url = f"http://api.openweathermap.org/data/2.5/weather?q={self.settings['city']}&appid={self.settings['weather_api_key']}&units=metric"
   response = requests.get(url).json()
   ```

4. **Playing Music**
   - Modify `play_music()` to use a different music source or playlist.
   ```python
   pygame.mixer.init()
   pygame.mixer.music.load("song.mp3")
   pygame.mixer.music.play()
   ```

## 📦 Modules and Dependencies
The project makes use of various Python libraries to provide extensive functionality:

- **Speech Recognition:** `speech_recognition`, `pyttsx3`
- **Graphical Interface:** `customtkinter`, `tkinter`
- **AI & NLP:** `openai`, `wolframalpha`, `wikipedia`
- **System Utilities:** `platform`, `socket`, `psutil`, `pyautogui`
- **Web Scraping & APIs:** `requests`, `BeautifulSoup`, `newsapi`
- **Finance & Crypto:** `cryptocompare`, `yfinance`, `forex_python`
- **Security & Face Recognition:** `face_recognition`, `cv2`
- **Multimedia Processing:** `pyaudio`, `pygame`, `gtts`, `playsound`

## 🤝 Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## 📜 License
This project is licensed under the [MIT License](LICENSE).

## 🙌 Acknowledgments
- [OpenAI](https://openai.com/)
- [Wolfram Alpha](https://www.wolframalpha.com/)
- [NewsAPI](https://newsapi.org/)

🎉 Enjoy using Modern AI Assistant!

