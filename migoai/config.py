import json
import os
from pathlib import Path
from .aws_token import get_token

HOME_DIR = str(Path.home())
CONFIG_DIR = os.path.join(HOME_DIR, '.migoai')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')
AVAILABLE_MODELS = ["magnum-12b-v2", "FlowGPT-Ares", "nemomix-v4"]
MAX_WIDTH = 80

def ensure_config_dir():
    """Ensure the config directory exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config():
    """Load configuration from JSON file in user's home directory."""
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"default_character": ""}
    return {"default_character": ""}

VERSION = 1.0

def save_config(config):
    """Save configuration to JSON file in user's home directory."""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)


TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImxuczNKSG9QWjl0X1RVbFV1UWZPVCIsImVtYWlsIjoiZGVuaXNlbXluYW1lOUBnbWFpbC5jb20iLCJzdWIiOiJsbnMzSkhvUFo5dF9UVWxVdVFmT1QiLCJpYXQiOjE3MzExMDM5MDUuOTAzLCJleHAiOjE3MzE3MDg3MDV9.jexGq7soYRjU0_SNs8I-BWtQVz49olJZ8_WtWrhhR6yvOpXfWiv1T3JoaIITLsUmeazu7enZPjB5f-R7RXWec3oPk11frjxodvkqZjwqyRMdaogVdy8o_hKxkT4ulzeXAl7tQL0fZQN9azH80h4OxebaNov_4aICDdJjpMRrGgJCSqU_O-Gld2JdrQJLWi6JBEQYaQIrefvkzziyUMzJ6x1jBhpe6-KNGNtCXGEXUt_G6hOpMVIu7l7ySDw-TUav8jiZq89C0RBh8pbSSfQgoBz-pdpcSgjmtBkSGnicsPuJEtFvzjphOR2h8y4oE8FD6IkwLy0M_rivFABLIF1TzA"

HEADERRS = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {TOKEN}',
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