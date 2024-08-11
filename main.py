import websocket
import os
import json
import pymongo
import sys

mongoClientConnectionString = os.environ.get('MONGODB_URL')
apiKey = os.environ.get("Api_Key")
apiSecret = os.environ.get("Api_Secret")
wsUrl = os.environ.get("Ws_Url")

stockTickersToFeed = sys.argv[1:]

client = pymongo.MongoClient(mongoClientConnectionString)
db = client["stock"]
collection = db["stock_val"]


def on_message(ws, message):
    print(f"Received message: {message}")
    msgDct = json.loads(message)
    
    for msg in msgDct:
        if 'msg' in msg and msg['msg'] == 'authenticated':
            ws.send(json.dumps({
            "action":"subscribe",
            "bars": stockTickersToFeed
            }))
        if msg['T']  == 'subscription':
            print("subscribed.")

        if msg['T']  == 'b':
            print("Bar data recived")
            feed_mongo(msgDct)

def on_error(ws, error):
    print(f"Error: {error}")

def feed_mongo(msg):
    collection.insert_many(msg)

def on_close(ws, close_status_code, close_msg):
    print(f"Connection closed: {close_status_code}, {close_msg}")
    

def on_open(ws):
    print("Connected")
    authenticate(ws)

def authenticate(ws):
    authMsg = {
        "action": "auth",
        "key": apiKey,
        "secret": apiSecret
    }
    ws.send(json.dumps(authMsg))

if __name__ == "__main__":
    ws = websocket.WebSocketApp(wsUrl,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

