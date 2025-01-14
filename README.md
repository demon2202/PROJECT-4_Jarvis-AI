🤖 Jarvis AI

Jarvis AI is a 🐍 Python-based voice assistant 🎙️ that can perform various tasks such as fetching 📰 news, checking ☁️ weather updates, managing 🗒️ reminders, playing 🎵 music, and setting ⏳ timers. It leverages libraries like speech_recognition, pyttsx3, and APIs for enhanced functionality.

🌟 Features

1. 🎤 Voice Commands

Recognizes and processes voice commands using the speech_recognition library.

The takeCommand function captures 🔊 audio input, processes it with Google Speech Recognition API, and returns the recognized text in lowercase.

If recognition fails, it provides a fallback to prompt the user again.

Provides real-time feedback using pyttsx3 for text-to-speech 🗣️ conversion, handled by the say function.

2. 📰 News Updates

Fetches top 5 news 🗞️ headlines for 🇮🇳 India using the News API.

The get_news function sends a request to the News API endpoint using the requests library.

Parses the response JSON to extract and read the top 5 headlines.

Prompts the user with voice feedback for each headline.

3. 🌦️ Weather Updates

Retrieves current weather 🌡️ information for a specified city 🏙️ using OpenWeather API.

The get_weather function sends a request with the API key and city name.

Extracts temperature 🌡️ and weather description from the JSON response.

Provides a detailed weather report via TTS.

4. 🗓️ Reminders

Manages a list of reminders 📋 using an in-memory list.

add_reminder adds a user-specified reminder to the list.

list_reminders lists all saved reminders.

Notifies the user via TTS when a reminder is added or displayed.

5. 🎶 Music Player

Plays .mp3 and .wav files from a user-specified directory 📂.

Scans the specified folder (music_dir) for supported music files.

The play_music function opens the selected music file using os.startfile().

Supports commands for playing the next ⏭️ or previous ⏮️ song.

6. ⏲️ Timer

Sets a countdown timer ⌛ in seconds.

The set_timer function pauses execution for the specified duration using time.sleep().

Notifies the user via TTS when the timer ends 🛎️.

7. 🤝 Interactive Interface

Handles various commands through natural language queries 📣.

Matches keywords like "news," "weather," "play music," and others to trigger specific functions.

Provides a graceful fallback for unrecognized commands, ensuring a smooth 🧈 user experience.

⚙️ Installation and Setup

📋 Prerequisites

🐍 Python 3.7 or higher

Install required Python libraries:

pip install speechrecognition pyttsx3 requests

🛠️ Setup

Clone this repository:

git clone https://github.com/your-username/jarvis-ai.git

Navigate to the project directory:

cd jarvis-ai

Replace placeholders in the code with your API keys 🔑:

News API key: Replace "key" in the get_news function.

OpenWeather API key: Replace "your_openweather_api_key" in the get_weather function.

City: Replace "your_city" in the get_weather function.

▶️ Usage

Run the program 🖥️:

python jarvis.py

Speak 🎙️ commands such as:

"What's the news?"

"What's the weather like?"

"Add reminder to buy groceries."

"Play music."

"Set timer for 10 seconds."

"Next song."

To exit 🚪, say "exit" or "quit."

🗂️ File Structure

jarvis-ai/
├── jarvis.py  # Main script
└── README.md  # Project documentation

🔍 Key Code Explanation

1. 🗣️ say Function

Initializes a pyttsx3 engine for text-to-speech conversion.

Outputs spoken feedback for the user’s actions or system messages.

2. 🎤 takeCommand Function

Captures audio input using the speech_recognition library.

Uses Google’s Speech Recognition API to convert audio to text.

Handles exceptions gracefully when recognition fails.

3. 📰 get_news Function

Sends an HTTP GET request to the News API.

Parses the response JSON to retrieve the top 5 articles 📰.

Provides spoken feedback for each headline using the say function.

4. 🌦️ get_weather Function

Sends an HTTP GET request to OpenWeather API with a city name.

Extracts temperature 🌡️ and weather conditions from the response JSON.

Provides a spoken weather report.

5. 🗓️ add_reminder and list_reminders Functions

add_reminder: Adds a user-specified string 📌 to a global reminders list.

list_reminders: Iterates through the reminders list and reads each item aloud.

6. 🎶 Music Functionality

Scans the specified directory for .mp3 and .wav files.

Plays the selected music file using the os.startfile() method.

Supports navigation to the next ⏭️ or previous ⏮️ song by adjusting an index variable.

7. ⏳ set_timer Function

Converts a user-specified duration (in seconds) to an integer.

Pauses execution using time.sleep and announces when the timer expires 🛎️.

8. 🔄 Main Loop

Continuously listens for user commands and matches them with predefined actions.

Gracefully handles invalid or unsupported commands with a fallback message.

🔮 Future Improvements

Add support for more voice commands 🛠️.

Integrate additional APIs for extended functionality 🌐.

Create a GUI 🖼️ for a better user experience.

Add persistent storage 📂 for reminders.

📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.

🤝 Contribution

Contributions are welcome! Feel free to open issues 🐞 or submit pull requests for improvements or bug fixes 🛠️.
