import os
import json
import datetime
import time
import re
import requests

webhook_url = "https://discord.com/api/v10/webhooks/1127219693850210344/cXnferwYNShJIf1x763iiLlrSFxdi9EA5il8Y8R-HMQ2CJEjF0cFjn5cueMuhTjn494o"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print( bcolors.OKCYAN + '''
     _  _____   __   ___ _____ ____  
    | |/ _ \ \ / /  / _ \_   _|  _ \ 
 _  | | | | \ V /  | | | || | | |_) |
| |_| | |_| || |   | |_| || | |  __/ 
 \___/ \___/ |_|    \___/ |_| |_|
''')
print(bcolors.BOLD + f"[!] Welcome To Joy SMS Forwarder")


def smsforward():
    lastSMS = datetime.datetime.now()
    tmpFile = "tmpLastTime.txt"
    filters = ["otp", "one time password", "OTP"]  # Add your filters here
    headers = {'Content-Type': 'application/json'}

    if not os.path.exists(tmpFile):
        print(bcolors.WARNING + "[!] Last time not found. Setting it to the current date-time")
        tfile = open(tmpFile, "w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        tfile = open(tmpFile, "r")
        lastSMS = datetime.datetime.fromisoformat(tfile.read())
        tfile.close()

    jdata = os.popen("termux-sms-list").read() 
    jd = json.loads(jdata)

    for j in jd:
        if datetime.datetime.fromisoformat(j['received']) > lastSMS: 
            for f in filters:
                if f in j['body'].lower() and j['type'] == "inbox":  
                    print(f"{f} found")
                    fullmsg = j['body']
                    numbers = re.findall(r'\d+', j['body'])  # Extract numbers from the SMS body
                    numbers_str = ', '.join(numbers)  # Convert the numbers to a comma-separated string
                    embed = {
                        "title": fullmsg,
                        "description": f"```{numbers_str}```",
                        "author": {
                            "name": "Otp SmS Forwarder By Joy",
                            "icon_url": "https://cdn.discordapp.com/avatars/1116815519299940444/03a3d7c2cf901b4ee8905a42a53e703f.webp"
                        },
                        "footer": {
                            "text": "Forwarded From Smart Phone by SMS Forwarder"
                            "icon_url": "https://cdn.discordapp.com/avatars/1116815519299940444/03a3d7c2cf901b4ee8905a42a53e703f.webp"
                        }
                    }
                    payload = {
                        "embeds": [embed]
                    }
                    response = requests.post(webhook_url, headers=headers, json=payload) 
                    if response.status_code == 204:
                        print(bcolors.BOLD + bcolors.OKBLUE + "[+] Message forwarded to Discord successfully")
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()
                    else:
                        print(bcolors.FAIL + "[!] Failed to forward message to Discord")

smsforward()

while True:
    time.sleep(1)
    smsforward()
