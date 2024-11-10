import sys
from typing import Tuple, Optional
from .voice_listener import start_voice_listener, stop_voice_listener
from colorama import init, Fore, Style
from .voice_listener import start_voice_listener, stop_voice_listener
from .config import save_config, AVAILABLE_MODELS, load_config
from .chat_history import ChatHistoryManager

history_manager = ChatHistoryManager()
config = load_config()

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

    if "--startvoice" in args:
        start_voice_listener()
        print(f"\n{Fore.GREEN}Voice command for migo started{Style.RESET_ALL}")
        sys.exit(0)
    elif "--stopvoice" in args:
        if not stop_voice_listener():
            print(f"{Fore.RED}Voice command failed to stop:{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}Voice command for migo stopped{Style.RESET_ALL}")
        sys.exit(0)
    
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

    if (view_history or view_modals) and (set_default or set_default_modal or character or modal):
        print(f"{Fore.RED}Error: {Style.RESET_ALL}You cannot use view commands with other commands that set values.")
        sys.exit(0)

    if view_history:
        histories = history_manager.list_chat_histories()
        if histories:
            print(f"{Fore.CYAN}Available chat histories:{Style.RESET_ALL}")
            for idx, hist in enumerate(histories, 1):
                print(f"{Fore.GREEN}{idx}. {hist}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No saved chat histories found.{Style.RESET_ALL}")
        sys.exit(0)

    if view_modals:
        print(f"{Fore.CYAN}Available modal models:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{', '.join(AVAILABLE_MODELS)}{Style.RESET_ALL}")
        sys.exit(0)
    
    if set_default and character:
        config["default_character"] = character
        save_config(config)
        print(f"{Fore.GREEN}Default character set successfully!{Style.RESET_ALL}")
        sys.exit(0)
    
    if set_default_modal and modal:
        if modal not in AVAILABLE_MODELS:
            print(f"{Fore.RED}Error: {Fore.YELLOW}'{modal}'{Fore.RED} is not a valid model. {Fore.YELLOW}Available models are: {Fore.GREEN}{', '.join(AVAILABLE_MODELS)}{Style.RESET_ALL}")
            return
        config["default_modal"] = modal
        save_config(config)
        print(f"{Fore.GREEN}Default model set to '{modal}' successfully!{Style.RESET_ALL}")
        sys.exit(0)
    
    if modal and modal not in AVAILABLE_MODELS:
        print(f"{Fore.RED}Error: {Fore.YELLOW}'{modal}'{Fore.RED} is not a valid model. {Fore.YELLOW}Available models are: {Fore.GREEN}{', '.join(AVAILABLE_MODELS)}{Style.RESET_ALL}")
        sys.exit(0)

    return character, modal, chat_name
