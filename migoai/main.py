import os
import json
import sys
import time
import threading
import textwrap
import requests
import signal 
from colorama import init, Fore, Style
from typing import Tuple, Optional
from .config import load_config, save_config, AVAILABLE_MODELS, MAX_WIDTH, TOEKN
from .aws_token import get_token
from .chat_history import ChatHistoryManager
from .voice_listener import start_voice_listener, stop_voice_listener
import os
import re
from .aityping import TypingSpinner

init()


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
    startvoice = False
    stopvoice = False

    if "--startvoice" in args:
        start_voice_listener()
        startvoice = True
    elif "--stopvoice" in args:
        if not stop_voice_listener():
            print(f"{Fore.RED}Voice command failed to stop:{Style.RESET_ALL}")
        else:
            stopvoice = True

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
            
    return character, set_default, modal, set_default_modal, chat_name, view_history, view_modals, startvoice, stopvoice

def save_and_exit(history_manager, history, chat_name=None):
    """Function to save history and exit gracefully."""
    if chat_name:
        history_manager.save_history(history, chat_name)
    else:
        history_manager.save_history(history)
    print(f"\n{Fore.YELLOW}Chat saved{Style.RESET_ALL}")
    sys.exit(0)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def execute_action_based_on_ai_response(response):
    filename_match = re.search(r"Filename:\s*(.+)", response)

    if filename_match:
        filename = filename_match.group(1).strip()

        if filename:
            code_blocks = re.findall(r'```.*?\n(.*?)```', response, re.DOTALL)

        if code_blocks:
            code_content = code_blocks[0].strip()

            dir_path = os.path.dirname(filename)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)

            with open(filename, 'w') as file:
                file.write(code_content)

            return True
    
    return False

def chat_with_migoai():
    clear_screen()
    character, set_default, modal, set_default_modal, chat_name, view_history, view_modals, startvoice, stopvoice = parse_args()
    config = load_config()
    typing = TypingSpinner()
    history_manager = ChatHistoryManager()

    if (view_history or view_modals) and (set_default or set_default_modal or character or modal):
        print(f"{Fore.RED}Error: {Style.RESET_ALL}You cannot use view commands like --viewchats or --viewmodals with other commands that set values.")
        return
    
    if startvoice:
        print(f"\n{Fore.GREEN}Voice command for migo started{Style.RESET_ALL}")
        return

    if stopvoice:
        print(f"\n{Fore.GREEN}Voice command for migo stopped{Style.RESET_ALL}")
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
            'system': f"if a file needs to be create. Example I say, create index.html and code hello world in python, then your response should begin with Filename: index.html and also specify path if asked before you give me your actual response. Another example, Filename: index.html or Filename: website/index.html this is the code for hello world.\n{system_prompt}",
            'promptId': 'kZ4dDpl17xudKnSdr2Wdv',
            'temperature': 0.7,
            'userId': 'lns3JHoPZ9t_TUlUuQfOT',
            'documentIds': [],
            'generateImage': False,
            'generateAudio': False,
        }

        print()
        typing.start()

        response = requests.post(
            'https://prod-backend-k8s.flowgpt.com/v3/chat', 
            headers=headers, 
            json=json_data
        )
        response.encoding = 'utf-8'

        typing.stop()

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

            file_creation = execute_action_based_on_ai_response(response_text)
            wrapped_response = wrap_text(response_text)
            print(f"{Fore.BLUE}Migo AI: {Style.BRIGHT}{wrapped_response}{Style.RESET_ALL}\n")
            if file_creation is not None and file_creation:
                print(f"{Fore.BLUE}Migo AI: {Style.BRIGHT}Make Sure to check the created files{Style.RESET_ALL}\n")

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
            print(f"{Fore.RED}Error: {response.text}{Style.RESET_ALL}")
