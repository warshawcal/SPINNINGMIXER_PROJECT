import os
import time
import sys 
import websocket
import requests
import json
from bll.slack_api_handler import SlackAPIHandler
try:
    import thread
except ImportError:
    import _thread as thread


class WebSocketHandler:

    def __init__(self, enableTrace=False):
        """
        Initializing WebSocketHandler object
        Mostly handles the listening of Jarvis to our slack channel
        """
        websocket.enableTrace(enableTrace) 

        # Creating WebSocketHandler object attrbute to abstract Slack API stuff
        self.SlackAPIHandler = SlackAPIHandler()

    def on_message(self, ws, message):
        """
        Reads incoming messages from the websocket connection
        Args:
            ws = websocket
            message = json message string
        """
        message = json.loads(message)
        envelope_id = message['envelope_id']
        keys = message.keys()
        resp = {'envelope_id': envelope_id }

        # Print if someone sends a message to Jarvis (as long as it's not from Jarvis)
        if str(message["payload"]["event"]["type"]).strip() == "message" and \
           str(message["payload"]["event"]["user"]).strip() != self.SlackAPIHandler.recipient2id["Jarvis"]:

            message_text = str(message["payload"]["event"]["text"])
            message_from = str(message["payload"]["event"]["user"])

            # Check if the message should trigger the training mode ON/OFF
            if self.SlackAPIHandler.trigger_training_mode_ON(message_text, message_from):
                # DO SOMETHING IF TRAINING MODE TRIGGERED ON --> @TODO
                pass
            elif self.SlackAPIHandler.trigger_training_mode_OFF(message_text, message_from):
                # DO SOMETHING IF TRAINING MODE TRIGGERED OFF --> @TODO
                pass
            else:
                # IF NOT TRAINING MODE RELATED, HANDLE THE MESSAGE OTHERWISE
                self.SlackAPIHandler.handle_message(message_text, message_from)

        ws.send(str.encode(json.dumps(resp))) # send a response back to Slack acknowledging that you've received the event

    def on_error(self, ws, error):
        """
        Prints any errors related to the websocket connection
        """
        if len(str(error)) > 0:
            print("\nJARVIS-ERROR:")
            print(error)
            print("\n")
            
    def on_close(self):
        """
        Handles the closing of the websocket connection
        """
        self.ws.close()

    def on_open(self, ws):
        """
        Useless function from skeleton
        """
        pass
    
    def return_websocket(self):
        """
        Returns websocket connection to Slack API
        """
        self.ws = websocket.WebSocketApp(self.SlackAPIHandler.get_connection_url(), 
                                      on_message = self.on_message,
                                      on_error = self.on_error,
                                      #on_close = self.on_close,
                                      on_open = self.on_open)
        self.ws.on_close = self.on_close()

        return self.ws


#EOF