import requests
import subprocess
from .config import VERSION

def check_update():
    url = "https://pastebin.com/raw/VVGzt459"
    response = requests.get(url)

    if response.status_code == 200:
        version = float(response.text.strip())
        if version > VERSION:
            subprocess.run(["pip", "install", "git+https://github.com/DeniseMyName/migoai.git"])