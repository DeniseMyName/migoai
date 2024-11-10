from colorama import init, Fore, Style
import sys
import time
import threading

class TypingSpinner:
    def __init__(self):
        self.typing_message = "Typing."
        self.stop_spinner = False
        self.spinner_thread = None

    def spin(self):
        while not self.stop_spinner:
            for i in range(4):
                sys.stdout.write(f"\r{Fore.CYAN}{self.typing_message}{'.' * i}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.5)
                if self.stop_spinner:
                    break
            sys.stdout.write("\r" + " " * 20 + "\r")
            sys.stdout.flush()

    def start(self):
        self.stop_spinner = False
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self):
        self.stop_spinner = True
        if self.spinner_thread:
            self.spinner_thread.join()
