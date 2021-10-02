import os
from pathlib import Path
from dotenv import load_dotenv
import base64
from DAO.DAO import DAO
from bll.slack_api_handler import Slack_API_Handler
import websocket
import requests
import json
try:
    import thread
except ImportError:
    import _thread as thread
import time
import sys 

# Loading the enviornment variables from .env 
# Used for getting API and APP keys
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Bot:

    def on_message(self, ws, message):
        """
        ws = websocket
        message = json message string
        """
        message = json.loads(message)
        envelope_id = message['envelope_id']
        keys = message.keys()
        resp = {'envelope_id': envelope_id }

        # Print if someone sends a message to Jarvis
        if str(message["payload"]["event"]["type"]).strip() == "message":
            print("\n")
            print("Received message: " + str(message["payload"]["event"]["text"]))
            print("From: " + str(message["payload"]["event"]["user"]))
            print("\n")

            # DEBUG -- Send "testing" to general channel when Jarvis receives a message from someone
            self.Slack_API_Handler.send_message_to_channel(message="testing")

        ws.send(str.encode(json.dumps(resp))) # send a response back to Slack acknowledging that you've received the event

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        # def run(*args):
        #     for i in range(3):
        #         time.sleep(1)
        #         ws.send("Hello %d" % i)
        #     time.sleep(1)
        #     ws.close()
        #     print("thread terminating...")
        # thread.start_new_thread(run, ())
        pass

    def start(self):

        # Creating Bot object attrbute to abstract Slack API calls
        self.Slack_API_Handler = Slack_API_Handler() 
        
        # Starting the WebSockerApp
        ws = websocket.WebSocketApp(self.Slack_API_Handler.get_connection_url(), 
                                  on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        ws.on_open = self.on_open
        websocket.enableTrace(False) # Set to False for less chatter, set to True for ultimate chatter mode
        ws.run_forever()


### START HERE
self = Bot()
self.start()

#EOF