# pyinstaller --onefile --clean wifi.py
#    _____ ______          _   _ _____ _____ _____ _______ _____ ____  _   _          _______     __
#   / ____|  ____|   /\   | \ | |  __ \_   _/ ____|__   __|_   _/ __ \| \ | |   /\   |  __ \ \   / /
#  | (___ | |__     /  \  |  \| | |  | || || |       | |    | || |  | |  \| |  /  \  | |__) \ \_/ / 
#   \___ \|  __|   / /\ \ | . ` | |  | || || |       | |    | || |  | | . ` | / /\ \ |  _  / \   /  
#   ____) | |____ / ____ \| |\  | |__| || || |____   | |   _| || |__| | |\  |/ ____ \| | \ \  | |   
#  |_____/|______/_/    \_\_| \_|_____/_____\_____|  |_|  |_____\____/|_| \_/_/    \_\_|  \_\ |_| 
# Designed by SeanDictionary
# V1.0
import requests
import json

default_set = """{
    "account": "account",
    "mode": "mode",
    "password": "password"
}"""

def load_json():
    try:
        with open('account.json', 'r') as file:
            data = json.load(file)
            account = data.get('account')
            mode = "%40" + data.get('mode') if data.get('mode') else ""
            password = data.get('password')
        return account, mode, password
    except FileNotFoundError:
        with open('account.json', 'w') as file:
            file.write(default_set)
        print(f"Error: FileNotFoundError")
        print(f"Generated account.json.Change the information.")
        input("Press Enter to exit...")
        exit()
    except Exception as e:
        print(f"Error: {e}")

def fetch_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    account, mode, password = load_json()
    url = f"https://p.njupt.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{account}{mode}&user_password={password}"
    fetch_url_content(url)
    input("Press Enter to exit...")