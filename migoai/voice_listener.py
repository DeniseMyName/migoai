import subprocess
import speech_recognition as sr
import pyttsx3
import threading
import json
from pathlib import Path
import os
import signal

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_commands():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for commands...")
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.6  

        while True:
            try:
                audio = recognizer.listen(source, timeout=5) 
                command = recognizer.recognize_google(audio).lower()
                
                if any(phrase in command for phrase in ["hey migo", "hey amigo", "hey migo ai", "hey migoai", "hey amigoai", "hey amigo ai"]):
                    speak("Starting migo")
                    threading.Thread(target=start_migo).start()

            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service; {e}")
            except sr.WaitTimeoutError:
                pass

def start_migo():
    subprocess.Popen(
        ["cmd", "/k", "migoai startup"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def start_voice_listener():
    process = subprocess.Popen(
        ["pythonw", "migoai/voice_listener.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    HOME_DIR = str(Path.home())
    CONFIG_DIR = os.path.join(HOME_DIR, '.migoai')
    CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

    os.makedirs(CONFIG_DIR, exist_ok=True)

    config_data = {}

    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config_data.update(json.load(f))

    config_data["pid"] = process.pid

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)


def stop_voice_listener():
    HOME_DIR = str(Path.home())
    CONFIG_FILE = os.path.join(HOME_DIR, '.migoai', 'config.json')

    try:
        with open(CONFIG_FILE, "r") as f:
            config_data = json.load(f)
        
        pid = config_data.get("pid")
        if pid is None:
            return False

        os.kill(pid, signal.SIGTERM)

        del config_data["pid"]
        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

        return True

    except FileNotFoundError:
        print("Config file not found.")
    except ProcessLookupError:
        print("Voice listener process not found.")
    except Exception as e:
        print(f"Error stopping voice listener: {e}")
    
    return False

if __name__ == "__main__":
    listen_for_commands()
