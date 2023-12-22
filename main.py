import os
import json
import datetime
import time
import re
import requests

class SMSForwarder:
    def __init__(self):
        self.webhook_url = "https://discord.com/api/webhooks/XXXX/XXXX"
        self.last_sms_time = self._get_last_sms_time()
        self.filters = ["otp", "one time password", "OTP"]

    def _get_last_sms_time(self):
        tmp_file = "tmpLastTime.txt"
        if os.path.exists(tmp_file):
            with open(tmp_file, "r") as file:
                return datetime.datetime.fromisoformat(file.read())
        else:
            last_sms = datetime.datetime.now()
            with open(tmp_file, "w") as file:
                file.write(str(last_sms))
            return last_sms

    def _update_last_sms_time(self, timestamp):
        tmp_file = "tmpLastTime.txt"
        with open(tmp_file, "w") as file:
            file.write(timestamp)

    def _send_to_discord(self, message, numbers):
        headers = {'Content-Type': 'application/json'}
        full_message = f"> {message}"
        numbers_str = ', '.join(numbers)
        embed = {
            "title": full_message,
            "description": f"```{numbers_str}```",
            "author": {
                "name": "OTP SMS FORWARDER BY JOY",
                "icon_url": "https://cdn.discordapp.com/emojis/1052840053950402600.png"
            },
            "thumbnail": {
                "url": "https://cdn.discordapp.com/emojis/1127296081710039180.png"
            },
            "footer": {
                "text": "Forwarded From Smart Phone by SMS Forwarder",
                "icon_url": "https://cdn.discordapp.com/emojis/1095997599036739594.png"
            },
            "color": 0x00FF00
        }
        payload = {"embeds": [embed]}
        response = requests.post(self.webhook_url, headers=headers, json=payload)
        return response

    def process_sms(self, sms):
        if datetime.datetime.fromisoformat(sms['received']) > self.last_sms_time:
            for f in self.filters:
                if f in sms['body'].lower() and sms['type'] == "inbox":
                    print("[!] Found an OTP Message, Forwarding to Discord...")
                    response = self._send_to_discord(sms['body'], re.findall(r'\d+', sms['body']))
                    if response.status_code == 204:
                        print("[+] Successfully Forwarded Message to Discord")
                        self._update_last_sms_time(sms['received'])
                    else:
                        print("[!] Failed to Forward Message to Discord\n[!] Please Double Check if Everything is OK")

def main():
    os.system('clear')
    print("""
     _  _____   __   ___ _____ ____  
    | |/ _ \ \ / /  / _ \_   _|  _ \ 
 _  | | | | \ V /  | | | || | | |_) |
| |_| | |_| || |   | |_| || | |  __/ 
 \___/ \___/ |_|    \___/ |_| |_|""")
    print("[!] Welcome to Joy SMS Forwarder")
    print("[!] You Can Press Ctrl + c To Exit The Script")

    forwarder = SMSForwarder()

    while True:
        time.sleep(1)
        jdata = os.popen("termux-sms-list").read()
        jd = json.loads(jdata)

        for j in jd:
            forwarder.process_sms(j)

if __name__ == "__main__":
    main()
