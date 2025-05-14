# pyinstaller --onefile --noconsole --clean --hidden-import plyer.platforms.win.notification wifi.py
#    _____ ______          _   _ _____ _____ _____ _______ _____ ____  _   _          _______     __
#   / ____|  ____|   /\   | \ | |  __ \_   _/ ____|__   __|_   _/ __ \| \ | |   /\   |  __ \ \   / /
#  | (___ | |__     /  \  |  \| | |  | || || |       | |    | || |  | |  \| |  /  \  | |__) \ \_/ / 
#   \___ \|  __|   / /\ \ | . ` | |  | || || |       | |    | || |  | | . ` | / /\ \ |  _  / \   /  
#   ____) | |____ / ____ \| |\  | |__| || || |____   | |   _| || |__| | |\  |/ ____ \| | \ \  | |   
#  |_____/|______/_/    \_\_| \_|_____/_____\_____|  |_|  |_____\____/|_| \_/_/    \_\_|  \_\ |_| 
# Designed by SeanDictionary

import logging
from logging.handlers import RotatingFileHandler
import requests
import json
import subprocess
import time
from plyer import notification
from packaging import version
import pyperclip
import os


VERSION = version.parse("1.2")
REPO = "SeanDictionary/NJUPT-wifi"
default_set = """{
    "account": "account",
    "mode": "mode",
    "password": "password",
    "sleep": 5
}"""


def notify(title, msg, duration=8):
    try:
        notification.notify(title=title, message=msg, timeout=duration)
    except Exception as e:
        logger.error(f"[-] Notify Error: {e}")


def check_version():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    try:
        response = requests.get(url, proxies={"http": None, "https": None}, timeout=1)
        if response.status_code == 200:
            data = response.json()
            version = data["tag_name"]
            html_url = data["html_url"]
            if version.parse(version.strip("V")) > VERSION:
                pyperclip.copy(html_url)
                logger.info(f"[+] New version {version} available. Update URL {html_url}.")
                notify(title="NJUPT校园网", msg=f"发现新版本 {version}\n更新地址已复制到剪贴板")
        else:
            logger.warning(f"[-] Connect to Github API Error with State code: {response.status_code}")
    except Exception as e:
        logger.warning(f"[-] Check Version Error: {e}")


def scan_wifi():
    result_bytes = subprocess.check_output(
        ["netsh", "wlan", "show", "networks"],
        shell=True
    )
    try:
        result = result_bytes.decode('utf-8', errors='ignore')

        ssids = []
        for line in result.splitlines():
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
                if ssid and ssid not in ssids:
                    ssids.append(ssid)
        logger.info(f"[+] Scan Wifi: {','.join(ssids)}")
        return ssids
    except Exception as e:
        logger.warning(f"[-] Scan Wifi Error: {e}")
        notify(title="NJUPT校园网", msg="扫描Wifi时出错\n详细查看日志文件")
        return []


def whether_using_njupt_ethernet():
    # test whether user is using NJUPT ethernet
    command = ['powershell', '-Command', 'Get-NetConnectionProfile']
    result = subprocess.run(command, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).stdout.split("\n\n")
    for line in result:
        if "NJUPT" in line and ("以太网" in line or "Ethernet" in line):
            return True
    return False


def test(url="http://connectivitycheck.platform.hicloud.com/generate_204",timeout=1):
    try:
        response = requests.get(url, timeout=timeout, proxies={})
        code = response.status_code
        if code == 204:
            logger.info("[+] State code: 204")
            return True
        else:
            logger.warning(f"[+] State code: {code}")
            return False
    except Exception as e:
        logger.warning(f"[-] Test Error: {e}")
        return False


def load_json():
    try:
        with open('account.json', 'r') as file:
            data = json.load(file)
            account = data.get('account')
            mode = "%40" + data.get('mode') if data.get('mode') else ""
            password = data.get('password')
            sleep = int(data.get('sleep',5))
        logger.info(f"[+] Load json file.")
        return account, mode, password, sleep
    except FileNotFoundError:
        with open('account.json', 'w') as file:
            file.write(default_set)
        logger.error(f"[-] Error: FileNotFoundError.")
        logger.error(f"[-] Generated account.json. Remember to change the information.")
        notify(title="NJUPT校园网", msg="第一次运行或未找到json文件\n已生成json文件，请修改账号密码\n并重新运行")
        os._exit(0)
    except Exception as e:
        logger.error(f"[-] Load json Error: {e}")
        notify(title="NJUPT校园网", msg="加载json文件出错\n详细查看日志文件")


def fetch_url_content(url):
    time.sleep(1) # wait for 1 second for the connection to be established
    try:
        response = requests.get(url, proxies={})
        logger.info(f"[+] Login Response: {response.text}")
        if "Portal协议认证成功！" in response.text:
            logger.info("[+] Connected NJUPT")
            notify(title="NJUPT校园网", msg="已成功连接NJUPT校园网")
            check_version()
        elif "AC999" in response.text:
            logger.info("[+] Already Connected NJUPT")
            # notify(title="NJUPT校园网", msg="正在使用NJUPT校园网")
        elif "当前时间禁止上网" in response.text:
            logger.warning("[-] Current time is not allowed to login to the internet.")
            while True:
                current = time.localtime()
                if current.tm_hour >= 7 and current.tm_hour < 23:
                    logger.info("[+] Current time is allowed to login to the internet.")
                    break
                else:
                    time.sleep(60)
        else:
            logger.error("[-] Authentication failed. Please check your account and password.")
            notify(title="NJUPT校园网", msg="登陆信息出错\n请检查json文件中的账号和密码确保正确\n并重新运行")
            os._exit(0)
    except Exception as e:
        logger.error(f"[-] Login Request Error: {e}")
        notify(title="NJUPT校园网", msg="登陆请求出错\n详细查看日志文件")


if __name__ == "__main__":
    log_handler = RotatingFileHandler(
        filename='wifi.log',
        mode='a',
        maxBytes=50 * 1024 * 1024,  # 50MB
        backupCount=5,              # 5 backup files
        encoding='utf-8'
    )

    formatter = logging.Formatter('%(asctime)s - %(levelname)-7s - %(message)s')
    log_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    
    logger.info(f"[+] ===================START VERSION {VERSION}===================")
    logger.info("[+] Start NJUPT Auto Login Script")
    notify(title="NJUPT校园网", msg="校园网自动登陆服务启动")
    while True:
        try:
            account, mode, password, step = load_json()
        except:
            continue
        url = f"https://p.njupt.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{account}{mode}&user_password={password}"

        if not any(test() for _ in range(1)):
            wifi_list = scan_wifi()
            if {"NJUPT","NJUPT-CMCC","NJUPT-CHINANET"} & set(wifi_list):
                logger.info("[+] NJUPT wifi environment detected.")
                if whether_using_njupt_ethernet():
                    # using ethernet
                    logger.info("[+] Connecting Ethernet.")
                    fetch_url_content(url)
                else:
                    # using wifi
                    for wifi_name in ["NJUPT","NJUPT-CMCC","NJUPT-CHINANET"]:
                        try:
                            tmp = subprocess.run(["netsh", "wlan", "connect", f"name={wifi_name}"])
                            print(f"[+] Connecting Wifi {wifi_name}")
                            break
                        except Exception as e:
                            logger.info(f"[-] Connecting Wifi {wifi_name} Error: {e}")
                            notify(title="NJUPT校园网", msg=f"连接Wifi {wifi_name} 时出错\n详细查看日志文件")
                    fetch_url_content(url)
            else:
                # if not in NJUPT wifi environment, sleep for 1 hrs
                logger.info("[-] Not in NJUPT wifi environment.")
                time.sleep(60*60)
        time.sleep(step)
