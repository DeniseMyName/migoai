import os
import json
import signal
from colorama import init, Fore, Style
from .config import load_config, HEADERRS
from .chat_history import ChatHistoryManager
from .aityping import TypingSpinner
from .argument_parser import parse_args
from .text_utils import wrap_text, clean_text
from .chat_manager import ChatManager
import sys


init()

class ChatWithMigoAI:
    def __init__(self):
        self.config = load_config()
        self.typing = TypingSpinner()
        self.history_manager = ChatHistoryManager()
        self.chat_manager = ChatManager()
        self.character, self.modal, self.chat_name = parse_args()
        self.model = self.modal or self.config.get("default_modal", "FlowGPT-Ares")
        self.system_prompt = self.character or self.config.get("default_character", "")
        self.history = self.history_manager.load_history(self.chat_name)
        signal.signal(signal.SIGINT, self.signal_handler)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def signal_handler(self, signal, frame):
        print(f"\n{Fore.RED}Detected Ctrl + C! Saving and exiting...{Style.RESET_ALL}")
        self.history_manager.save_and_exit(self.history, self.chat_name)
    
    def display_initial_info(self):
        chat_name = "Default Chat"
        if self.chat_name:
            chat_name = self.chat_name
        print(f"{Fore.CYAN}Chat started! Type 'migoai-exit' to end the conversation.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Loaded chat history: {chat_name}{Style.RESET_ALL}")
        if self.system_prompt:
            print(f"{Fore.YELLOW}Using character: {wrap_text(self.system_prompt)}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Using model: {self.model}{Style.RESET_ALL}\n")
        for entry in self.history:
            role = entry['role']
            content = wrap_text(entry['content'])
            if role == "user":
                print(f"{Fore.GREEN}You: {Style.RESET_ALL}{content}\n")
            elif role == "assistant":
                print(f"{Fore.BLUE}Migo AI: {Style.BRIGHT}{content}{Style.RESET_ALL}\n")

    def run(self):
        self.clear_screen()
        self.display_initial_info()

        while True:
            sys.stdout.write(f"{Fore.GREEN}You: {Style.RESET_ALL}")
            sys.stdout.flush()
            user_input = input()

            if not user_input:
                continue

            print()

            if user_input.lower() == "migoai-exit":
                self.save_chat()
                print(f"\n{Fore.YELLOW}Chat saved and exiting...{Style.RESET_ALL}")
                break

            self.typing.start()
            response = self.chat_manager.submit_chat(self.model, user_input, self.history, self.system_prompt)
            self.typing.stop()

            if response.status_code == 200:
                response_text = self.process_response(response.text)
                self.display_response(response_text)
                self.update_history(user_input, response_text)
            else:
                print(f"{Fore.RED}Error: {response.text}{Style.RESET_ALL}")

    def process_response(self, response_text):
        processed_text = ''
        for line in response_text.splitlines():
            if not line.strip():
                continue
            try:
                response_json = json.loads(line)
                text = response_json.get('data', '')
                processed_text += clean_text(text)
            except json.JSONDecodeError:
                processed_text = "Error occurred"
        return processed_text

    def display_response(self, response_text):
        self.chat_manager.is_create_file(response_text)
        wrapped_response = wrap_text(response_text)
        print(f"{Fore.BLUE}Migo AI: {Style.BRIGHT}{wrapped_response}{Style.RESET_ALL}\n")

    def update_history(self, user_input, response_text):
        self.history.append({'role': 'user', 'content': user_input})
        if response_text.strip():
            self.history.append({'role': 'assistant', 'content': response_text})
        self.save_chat()

    def save_chat(self):
        if self.chat_name:
            self.history_manager.save_history(self.history, self.chat_name)
        else:
            self.history_manager.save_history(self.history)