import os
import json
import sys
import time
import threading
import textwrap
import requests
import signal  # Import the signal module
from colorama import init, Fore, Style
from typing import Tuple, Optional
from .config import load_config, save_config, AVAILABLE_MODELS, MAX_WIDTH, TOKEN_DATA, TOEKN
from .chat_history import ChatHistoryManager
import subprocess

init()

def start_voice_listener():
    subprocess.Popen(
        ["pythonw", "migoai/voice_listener.pyw"],
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

class Spinner:
    def __init__(self):
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.stop_spinner = False
        self.spinner_thread = None

    def spin(self):
        while not self.stop_spinner:
            for char in self.spinner_chars:
                sys.stdout.write(f"\r{Fore.CYAN}Thinking {char}{Style.RESET_ALL}")
                sys.stdout.flush()
                time.sleep(0.1)
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

def wrap_text(text, width=MAX_WIDTH):
    """Wrap text to specified width."""
    return '\n'.join(textwrap.wrap(text, width=width, replace_whitespace=False))

def clean_text(text):
    """Clean and normalize text to handle special characters.""" 
    return text.encode('utf-8').decode('utf-8', 'replace')

def parse_args() -> Tuple[Optional[str], bool, Optional[str], bool, Optional[str], bool, bool]:
    """Parse command line arguments."""
    args = sys.argv[1:]
    character = None
    modal = None
    chat_name = None
    set_default = False
    set_default_modal = False
    view_history = False
    view_modals = False

    if "--activatevoice" in args:
        start_voice_listener()
        print(f"\n{Fore.GREEN}Voice command for migo activated{Style.RESET_ALL}")
        return

    i = 0
    while i < len(args):
        if args[i] == "--character":
            character = args[i + 1]
            i += 2
        elif args[i] == "--defaultcharacter":
            character = args[i + 1]
            set_default = True
            i += 2
        elif args[i] == "--modal":
            modal = args[i + 1]
            i += 2
        elif args[i] == "--defaultmodal":
            modal = args[i + 1]
            set_default_modal = True
            i += 2
        elif args[i] == "--chat":
            chat_name = args[i + 1]
            i += 2
        elif args[i] == "--viewchats":
            view_history = True
            i += 1
        elif args[i] == "--viewmodals":
            view_modals = True
            i += 1
        else:
            i += 1
            
    return character, set_default, modal, set_default_modal, chat_name, view_history, view_modals

def get_token():
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'text/plain;charset=UTF-8',
        'origin': 'https://studio.flowgpt.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://studio.flowgpt.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }
    response = requests.post(
        'https://1816e4d6cd83.ba5a2ce6.us-east-2.token.awswaf.com/1816e4d6cd83/d1d994412487/verify',
        headers=headers,
        data=TOKEN_DATA,
    )
    return response.json().get("token")

def save_and_exit(history_manager, history, chat_name=None):
    """Function to save history and exit gracefully."""
    if chat_name:
        history_manager.save_history(history, chat_name)
    else:
        history_manager.save_history(history)
    print(f"\n{Fore.YELLOW}Chat saved and exiting...{Style.RESET_ALL}")
    sys.exit(0)

def chat_with_migoai():
    character, set_default, modal, set_default_modal, chat_name, view_history, view_modals = parse_args()
    config = load_config()
    spinner = Spinner()
    history_manager = ChatHistoryManager()

    if (view_history or view_modals) and (set_default or set_default_modal or character or modal):
        print(f"{Fore.RED}Error: {Style.RESET_ALL}You cannot use view commands like --viewchats or --viewmodals with other commands that set values.")
        return
    
    if view_history:
        histories = history_manager.list_chat_histories()
        if histories:
            print(f"{Fore.CYAN}Available chat histories:{Style.RESET_ALL}")
            for hist in histories:
                print(f"{Fore.GREEN}- {hist}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No saved chat histories found.{Style.RESET_ALL}")
        return

    if view_modals:
        print(f"{Fore.CYAN}Available modal models:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{', '.join(AVAILABLE_MODELS)}{Style.RESET_ALL}")
        return
    
    if set_default and character:
        config["default_character"] = character
        save_config(config)
        print(f"{Fore.GREEN}Default character set successfully!{Style.RESET_ALL}")
        return
    
    if set_default_modal and modal:
        if modal not in AVAILABLE_MODELS:
            print(f"{Fore.RED}Error: {Fore.YELLOW}'{modal}'{Fore.RED} is not a valid model. {Fore.YELLOW}Available models are: {Fore.GREEN}{', '.join(AVAILABLE_MODELS)}{Style.RESET_ALL}")
            return
        config["default_modal"] = modal
        save_config(config)
        print(f"{Fore.GREEN}Default model set to '{modal}' successfully!{Style.RESET_ALL}")
        return
    
    if modal and modal not in AVAILABLE_MODELS:
        print(f"{Fore.RED}Error: {Fore.YELLOW}'{modal}'{Fore.RED} is not a valid model. {Fore.YELLOW}Available models are: {Fore.GREEN}{', '.join(AVAILABLE_MODELS)}{Style.RESET_ALL}")
        return
    
    model = modal if modal else config.get("default_modal", "FlowGPT-Ares")
    system_prompt = character if character else config.get("default_character", "")
    
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {TOEKN}',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://studio.flowgpt.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://studio.flowgpt.com/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-aws-waf-token': get_token(),
        'x-flow-device-id': 'QmR2wbof9cOrxkRwXlhqu',
        'x-nonce': 'f511cff4304785287c9d7b406838d408',
        'x-signature': 'edc4bdbae160dfa6e2cc1adfec0ee3e8',
        'x-timestamp': '1731054192',
    }

    history = history_manager.load_history(chat_name)
    
    def signal_handler(signal, frame):
        """Handle Ctrl + C signal."""
        print(f"\n{Fore.RED}Detected Ctrl + C! Saving and exiting...{Style.RESET_ALL}")
        save_and_exit(history_manager, history, chat_name)

    signal.signal(signal.SIGINT, signal_handler)

    if chat_name:
        print(f"{Fore.CYAN}Loaded chat history: {chat_name}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}Chat started! Type 'migoai-exit' to end the conversation.{Style.RESET_ALL}")
    if system_prompt:
        print(f"{Fore.YELLOW}Using character: {wrap_text(system_prompt)}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Using model: {model}{Style.RESET_ALL}\n")

    while True:
        user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}")
        
        if user_input.lower() == "migoai-exit":
            if chat_name:
                history_manager.save_history(history, chat_name)
            else:
                history_manager.save_history(history)
            print(f"\n{Fore.YELLOW}Chat saved and exiting...{Style.RESET_ALL}")
            break
        
        json_data = {
            'model': model, 
            'nsfw': False,
            'question': user_input,
            'history': history,
            'system': system_prompt,
            'promptId': 'kZ4dDpl17xudKnSdr2Wdv',
            'temperature': 0.7,
            'userId': 'lns3JHoPZ9t_TUlUuQfOT',
            'documentIds': [],
            'generateImage': False,
            'generateAudio': False,
        }

        print()
        spinner.start()

        response = requests.post(
            'https://prod-backend-k8s.flowgpt.com/v3/chat', 
            headers=headers, 
            json=json_data
        )
        response.encoding = 'utf-8'

        spinner.stop()

        if response.status_code == 200:
            response_text = ''
            for line in response.text.splitlines():
                if not line.strip():
                    continue
                try:
                    response_json = json.loads(line)
                    text = response_json.get('data', '')
                    response_text += clean_text(text)
                except json.JSONDecodeError:
                    response_text = "Error occurred"

            wrapped_response = wrap_text(response_text)
            print(f"{Fore.BLUE}Migo AI: {Style.BRIGHT}{wrapped_response}{Style.RESET_ALL}\n")

            history.append({
                'role': 'user',
                'content': user_input,
            })
            history.append({
                'role': 'assistant',
                'content': response_text,
            })

            if chat_name:
                history_manager.save_history(history, chat_name)
            else:
                history_manager.save_history(history)

        else:
            print(f"{Fore.RED}Error: {response.status_code}{Style.RESET_ALL}")
