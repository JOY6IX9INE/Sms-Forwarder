import os
import json
import datetime
import time
import re
import requests

webhook_url = "https://discord.com/api/webhooks/1127297653479317555/da85yxPHkXQfrYSvv2Ho8BhqqPg_h5qB1w034JVRJJuP-SOGhDyp9xmDaylppjHZbUGp"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    RESET = '\033[0m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

os.system('clear')
print( bcolors.OKCYAN + '''
     _  _____   __   ___ _____ ____  
    | |/ _ \ \ / /  / _ \_   _|  _ \ 
 _  | | | | \ V /  | | | || | | |_) |
| |_| | |_| || |   | |_| || | |  __/ 
 \___/ \___/ |_|    \___/ |_| |_|
''' + bcolors.RESET )
print(bcolors.BOLD + bcolors.OKGREEN + f"[!] Welcome To Joy SMS Forwarder\n" + bcolors.RESET)
print(bcolors.WARNING + "[!] You Can Press Ctrl + c To Exit The Script" + bcolors.RESET)

def smsforward():
    lastSMS = datetime.datetime.now()
    tmpFile = "tmpLastTime.txt"
    filters = ["otp", "one time password", "OTP"]  # Add your filters here
    headers = {'Content-Type': 'application/json'}

    if not os.path.exists(tmpFile):
        print(bcolors.WARNING + "[!] Last Time Not found, Setting It Up" + bcolors.RESET)
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
                    print(bcolors.HEADER + "[!] Found A Otp Message, Forwarding To Discord..." + bcolors.RESET)
                    fullmsg = j['body']
                    numbers = re.findall(r'\d+', j['body']) 
                    numbers_str = ', '.join(numbers)
                    embed = {
                        "title": f"> {fullmsg}",
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
                    payload = {
                        "embeds": [embed]
                    }
                    response = requests.post(webhook_url, headers=headers, json=payload) 
                    if response.status_code == 204:
                        print(bcolors.BOLD + bcolors.OKBLUE + "[+] Successfully Forwarded Message To Discord" + bcolors.RESET)
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()
                    else:
                        print(bcolors.FAIL + "[!] Failed To Forward Message To Discord\n[!] Please Double Check If Everything Is Ok" + bcolors.RESET)

smsforward()

while True:
    time.sleep(1)
    smsforward()
