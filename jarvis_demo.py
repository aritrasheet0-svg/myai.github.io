"""
Jarvis AI Assistant - Modified Demo Version (without microphone)
This version uses text input instead of speech for testing purposes
"""

import pyttsx3
import requests
import json
import re
import os
import subprocess
import webbrowser

# Configuration
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://github.com/your-repo-name",
    "X-Title": "Jarvis Assistant"
}

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty("rate", 180)

def speak(text, allow_interruption=False):
    """Convert text to speech"""
    print(f"🗣️ Jarvis: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def listen():
    """Get user input from console instead of microphone"""
    user_input = input("\n👤 You: ").strip()
    return user_input if user_input else None

def clean_response(text):
    """Clean up AI response formatting"""
    text = re.sub(r'\\n|\n|\r', ' ', text)
    text = re.sub(r'[*_#>\[\]{}|]', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def chat_with_deepseek(prompt):
    """Send prompt to DeepSeek AI and get response"""
    try:
        data = {
            "model": "deepseek/deepseek-r1-zero:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Jarvis, an intelligent AI assistant. Keep responses concise and helpful."
                },
                {"role": "user", "content": prompt}
            ]
        }
        
        print("⏳ Jarvis is thinking...")
        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            raw_answer = result["choices"][0]["message"]["content"]
            print("✅ API Response received")
            return clean_response(raw_answer)
        else:
            print(f"❌ API Error: {response.status_code}")
            return "Sorry, I couldn't get a response from the AI."
    except requests.exceptions.Timeout:
        return "The AI is taking too long to respond. Please try again."
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return "There was a problem connecting to the AI."

# 💻 Control Functions
def shutdown():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

def open_chrome():
    speak("Opening Chrome.")
    try:
        path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        if os.path.exists(path):
            subprocess.Popen([path])
        else:
            speak("Chrome is not installed at the default location")
    except Exception as e:
        print(f"Error opening Chrome: {e}")

def search_google(query):
    speak(f"Searching Google for {query}")
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
    except Exception as e:
        print(f"Error searching: {e}")

def open_folder(folder_name):
    speak(f"Opening folder {folder_name}")
    try:
        # Use Documents folder as base instead
        folder_path = os.path.join(os.path.expanduser("~"), "Documents", folder_name)
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            speak(f"Sorry, I can't find the folder {folder_name}")
    except Exception as e:
        print(f"Error opening folder: {e}")

# 🔁 Main Loop
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 JARVIS AI ASSISTANT - Text Input Mode")
    print("=" * 50)
    
    speak("Hello, I am Jarvis. I'm ready to assist you.", allow_interruption=False)
    print("\nCommands: 'exit', 'shutdown', 'open chrome', 'search for [query]', 'open folder [name]'")
    print("Or ask me anything!\n")

    while True:
        command = listen()

        if command:
            command_lower = command.lower()

            # Exit commands
            if any(word in command_lower for word in ["exit", "quit", "stop", "bye"]):
                speak("Goodbye! Have a great day.", allow_interruption=False)
                break

            # Shutdown command
            elif "shutdown" in command_lower:
                response = input("Are you sure you want to shutdown? (yes/no): ")
                if response.lower() == "yes":
                    shutdown()
                    break
                else:
                    speak("Shutdown cancelled")

            # Open Chrome
            elif "open chrome" in command_lower:
                open_chrome()

            # Search Google
            elif "search for" in command_lower or "google" in command_lower:
                search_query = command_lower.replace("search for", "").replace("google", "").strip()
                if search_query:
                    search_google(search_query)
                else:
                    speak("What should I search for?")

            # Open folder
            elif "open folder" in command_lower:
                folder = command_lower.replace("open folder", "").strip()
                open_folder(folder)

            # General AI query
            else:
                response = chat_with_deepseek(command)
                if response:
                    speak(response, allow_interruption=False)
                else:
                    speak("I couldn't understand the response.", allow_interruption=False)
        else:
            speak("Sorry, I didn't hear that. Please try again.")
