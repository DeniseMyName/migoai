import requests
import subprocess
import pkg_resources

def check_update():
    url = "https://pastebin.com/raw/VVGzt459"
    response = requests.get(url)

    if response.status_code == 200:
        latest_version = float(response.text.strip())        
        try:
            installed_version = float(pkg_resources.get_distribution("migoai").version)
        except pkg_resources.DistributionNotFound:
            installed_version = 0.0
            
        if latest_version > installed_version:
            subprocess.run(["pip", "install", "git+https://github.com/DeniseMyName/migoai.git"])
