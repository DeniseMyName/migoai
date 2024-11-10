import os
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from colorama import init, Fore, Style
import sys

class ChatHistoryManager:
    def __init__(self):
        HOME_DIR = str(Path.home())
        self.history_dir = Path(HOME_DIR) / '.migoai' / "histories"
        self.history_dir.mkdir(exist_ok=True)  
        self.current_history_file = self.history_dir / "default.json"
        
    def save_history(self, history: List[Dict], chat_name: Optional[str] = None) -> None:
        """Save chat history to a file."""
        if chat_name:
            filename = f"{chat_name}.json"
            filepath = self.history_dir / filename
        else:
            filepath = self.current_history_file
            
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
            
    def load_history(self, chat_name: Optional[str] = None) -> List[Dict]:
        """Load chat history from a file."""
        if chat_name:
            matching_files = list(self.history_dir.glob(f"{chat_name}.json"))
            if not matching_files:
                return []
            filepath = max(matching_files, key=os.path.getctime)
        else:
            filepath = self.current_history_file
            
        if not filepath.exists():
            return []
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
            
    def list_chat_histories(self) -> List[str]:
        """List all available chat histories."""
        histories = []
        for file in self.history_dir.glob("*.json"):
            chat_name = file.stem
            if chat_name not in histories:
                histories.append(chat_name)
        return histories

    def save_and_exit(self, history, chat_name=None):
        """Function to save history and exit gracefully."""
        if chat_name:
            self.save_history(history, chat_name)
        else:
            self.save_history(history)
        print(f"\n{Fore.YELLOW}Chat saved{Style.RESET_ALL}")
        sys.exit(0)