import subprocess
import speech_recognition as sr
import pyttsx3
import threading

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

if __name__ == "__main__":
    listen_for_commands()
