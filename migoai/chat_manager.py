import json
import requests
from colorama import Fore, Style
from .text_utils import clean_text, wrap_text
from .aws_token import get_token
import re
import os
from .config import HEADERRS

class ChatManager:
    
    @staticmethod
    def submit_chat(model, user_input, history, system_prompt):
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
        response = requests.post(
                'https://prod-backend-k8s.flowgpt.com/v3/chat', 
                headers=HEADERRS, 
                json=json_data
            )
        response.encoding = 'utf-8'
        return response
        
    @staticmethod
    def is_create_file(response):
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