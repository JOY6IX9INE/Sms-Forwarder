import os
import json
import datetime
import time
import re
import requests

webhook_url = "https://discord.com/api/v10/webhooks/1127219693850210344/cXnferwYNShJIf1x763iiLlrSFxdi9EA5il8Y8R-HMQ2CJEjF0cFjn5cueMuhTjn494o"  # Replace with your Discord webhook URL

print(f"Welcome to SMS forwarder")

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

# Defining function for forwarding SMS
def smsforward():
    lastSMS = datetime.datetime.now()
    tmpFile = "tmpLastTime.txt"
    filters = ["otp", "one time password", "OTP"]  # Add your filters here
    headers = {'Content-Type': 'application/json'}

    # Checking the existence of the temporary file containing the last forwarded SMS time
    if not os.path.exists(tmpFile):
        # Saved time not found. Setting it to the current date and time
        print(bcolors.WARNING + "[!] Last time not found. Setting it to the current date-time")
        tfile = open(tmpFile, "w")
        tfile.write(str(lastSMS))
        tfile.close()
    else:
        # Saved last SMS forward time found. Loading from that
        tfile = open(tmpFile, "r")
        lastSMS = datetime.datetime.fromisoformat(tfile.read())
        tfile.close()

    print(f"Last SMS forwarded on {lastSMS}")
    jdata = os.popen("termux-sms-list").read()  # Reading all SMSs using Termux API
    jd = json.loads(jdata)  # Storing JSON output
    #print(f"Reading {len(jd)} latest SMSs")

    for j in jd:
        if datetime.datetime.fromisoformat(j['received']) > lastSMS:  # Comparing SMS timing
            for f in filters:
                if f in j['body'].lower() and j['type'] == "inbox":  # Checking if the SMS is in the inbox and the filter(s) are matching
                    print(f"{f} found")
                    payload = {
                        "content": j['body']  # Sending the SMS body as content to Discord webhook
                    }
                    response = requests.post(webhook_url, headers=headers, json=payload)  # Sending the request to the Discord webhook
                    if response.status_code == 204:
                        print(bcolors.BOLD + bcolors.OKBLUE + "[+] Message forwarded to Discord successfully")
                        tfile = open(tmpFile, "w")
                        tfile.write(j['received'])
                        tfile.close()
                    else:
                        print(bcolors.FAIL + "[!] Failed to forward message to Discord")

# Calling the smsforward function for the first time
smsforward()

# Looping indefinitely to forward new SMS messages
while True:
    time.sleep(1)  # Delay of 1 second between checking for new SMS messages
    smsforward()
    
