import requests
import subprocess
import pkg_resources

def check_update():
    url = "https://raw.githubusercontent.com/DeniseMyName/migoai/refs/heads/main/setup.py"
    response = requests.get(url)
    if response.status_code == 200:
        setup_content = response.text
        version_start = setup_content.find('version="') + len('version="')
        version_end = setup_content.find('"', version_start)
        latest_version = float(setup_content[version_start:version_end])
        try:
            installed_version = float(pkg_resources.get_distribution("migoai").version)
        except pkg_resources.DistributionNotFound:
            installed_version = 0.0
        if latest_version > installed_version:
            subprocess.run(["pip", "install", "git+https://github.com/DeniseMyName/migoai.git"])
            subprocess.run(["migoai"])