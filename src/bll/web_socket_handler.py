import os
import time
import sys 
import websocket
import requests
import json
from bll.slack_api_handler import SlackAPIHandler
from bll.ErrorHandler import error_handler
try:
    import thread
except ImportError:
    import _thread as thread


class WebSocketHandler():
    """
    This file handles all logic to the web socket connection.
    Mostly handles the listening of Jarvis to our slack channel

    Inherits Jarvis
    """

    def __init__(self, __enableTrace__=False, __slack_app_key__=None, __slack_api_key__=None):
        """
        Initializing WebSocketHandler object
        """

        # This dictionary keeps track of the messages Jarvis receives
        # Useful for not sending any duplicate api calls that may be sent to
        # the web socket
        self.data = dict(())
        self.data['Message'] = [] # keeps track of the messages
        self.data['From']    = [] # keeps track of the senders of the messages
        self.num_received_messages = 0 # keeps

        # Getting any app tokens that may have been passed to the Jarvis constructor
        self.__slack_api_key__ = __slack_api_key__
        self.__slack_app_key__ = __slack_app_key__

        # Setting the websocket chatter (True=lots, False=little)
        self.__enableTrace__   = __enableTrace__
        websocket.enableTrace(self.__enableTrace__) 

        # Creating WebSocketHandler object attrbute to abstract Slack API stuff
        self.SlackAPIHandler = SlackAPIHandler(__enableTrace__  = self.__enableTrace__,  \
                                               __slack_app_key__= __slack_app_key__,     \
                                               __slack_api_key__= __slack_api_key__      )

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
        ws.send(str.encode(json.dumps(resp))) # send a response back to Slack acknowledging that you've received the event

        message_text = str(message["payload"]["event"]["text"])
        message_from = str(message["payload"]["event"]["user"])

        # # DEBUG INCOMING MESSAGE
        if str(message["payload"]["event"]["user"]).strip() != self.SlackAPIHandler.recipient2id["Jarvis"]:
            print("\nJARVIS-INFO: Message Received: ")
            print("\tTEXT: " + message_text)
            print("\tFROM: " + message_from) 

        # Print if someone sends a message to Jarvis (as long as it's not from Jarvis)
        if str(message["payload"]["event"]["type"]).strip() == "message" and \
           str(message["payload"]["event"]["user"]).strip() != self.SlackAPIHandler.recipient2id["Jarvis"]:

            # Recall the previous message received
            if ( len(self.data['Message']) > 0 and len(self.data['From']) > 0 ):
                last_message_text = str(self.data['Message'][self.num_received_messages-1]).strip()
                last_message_from = str(self.data['From'][self.num_received_messages-1]).strip()

            # Prevent duplicate websocket traffic from interfering with user experience
            if ( len(self.data['Message']) == 0 and len(self.data['From']) == 0 ) or \
               ( message_text != last_message_text ):

                # Cache the message to the data dictionary
                self.data['From'].append(message_from)
                self.data['Message'].append(message_text)
                self.num_received_messages += 1

                # # # DEBUG MESSAGE HISTORY
                print("\nJARVIS-INFO: Messages History Table ")
                count = 0 
                while count < len(self.data['Message']):
                    print("\n\t " + str(count+1) + ".) MESSAGE: " + self.data['Message'][count] )
                    print("\t "   + str(count+1) + ".) From: "    + self.data['From'][count]    )
                    count += 1

                # Handle the event response appropriately with SlackAPIHandler
                self.SlackAPIHandler.handle_message(message_text, message_from)
        return

    @error_handler(debug_mode=True,function_name="WebSocketHandler.on_error")
    def on_error(self, ws, error):
        """
        Prints any errors related to the websocket connection
        """
        if len(str(error)) > 0:
            print("\nJARVIS-ERROR: on_error")
            print(error)
            print("\n")

        return
            
    def on_close(self):
        """
        Handles the closing of the websocket connection
        """
        self.ws.close()
        return

    def on_open(self, ws):
        """
        Useless function from skeleton
        """
        return
    
    def return_websocket(self):
        """
        Returns websocket connection to Slack API
        """
        self.ws = websocket.WebSocketApp(url=self.SlackAPIHandler.get_connection_url(), 
                                      on_message = self.on_message,
                                      on_error = self.on_error,
                                      #on_close = self.on_close,
                                      on_open = self.on_open)
        self.ws.on_close = self.on_close()

        return self.ws


#EOF