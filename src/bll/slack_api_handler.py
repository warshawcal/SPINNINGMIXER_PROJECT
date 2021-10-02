import os
import base64
import requests
import json
import sys
import pandas as pd
from DAO.DAO import DAO


class SlackAPIHandler:
    """
    This file handles all calls to the Slack API.
    Mostly handles the action logic of Jarvis in response to events.
    """

    def __init__(self, enableTrace=False):

        # recipient:id map for Slack API Handler
        self.recipient2id = {
            "Nicholas Hella" : "U02FCUM64NR",
            "John"           : "U02G5KRTC8Y",
            "Cal"            : "U02GADB06D6",
            "Nick Knudson"   : "U02FGDFJQ78",
            "Jarvis"         : "U02G827ANEA",
            "general"        : "C02F17T7CK1"
        }

        # Boolean for whether Jarvis is in training mode
        self.in_training_mode = False

        # Creating Slack_API_Handler object attrbute to abstract Sqlite3 database stuff
        self.Jarvis_DAO = DAO()


    def handle_message(self, message, received_from):
        """
        Handles responses to messages recieved by Jarvis from receipient
        """

        if self.in_training_mode:
            # Handle the message appropriately if in training mode --> @TODO
            message = "Responding while I'm in training mode!"
            self.send_message_to_recipient(message=message, recipient=received_from)
            pass
        else:
            # Handle the message appropriately if in training mode --> @TODO
            message = "Hello, I'm not in training mode. This is an automated response."
            self.send_message_to_recipient(message=message, recipient=received_from)
            pass

    def trigger_training_mode_ON(self, message, received_from):
        """
        Returns True/False if Jarvis should be in training mode
        """
        if str(message).strip() == "training time" and self.in_training_mode == False:
            message = "OK, I'm ready for training. What NAME should this ACTION be?"
            self.send_message_to_recipient(message=message, recipient=received_from)
            self.in_training_mode = True
            return self.in_training_mode
        
        return False

    def trigger_training_mode_OFF(self, message, received_from):
        """
        Returns True/False if Jarvis should be in training mode
        """
        if str(message).strip() == "done" and self.in_training_mode:
            message = "OK, I'm done training."
            self.in_training_mode = False
            self.send_message_to_recipient(message=message, recipient=received_from)
            return True
        
        return False

    def send_message_to_recipient(self, message, recipient="Jarvis"):
        """
        Deafult channel is the "general" channel
        """
        headers = {
                    "Authorization": "Bearer " + self.return_slack_api_token(),
                    "Content-type": "application/x-www-form-urlencoded",
                }
        url = "https://slack.com/api/chat.postMessage"
        if recipient in self.recipient2id.keys(): 
            recipient = self.recipient2id[recipient]
        data = {"channel":recipient,"text":message}
        response = requests.post(url, headers=headers, data=data)
        response = json.loads(str(response.text))

    def return_slack_app_token(self):
        """
        Load the encrypted slack app token from the env, decrypts it, and returns the 
        decrypted token
        """
        # Decrypting the ECRYPTED_SLACK_TOKEN env variable
        ENCRYPTED_APP_TOKEN = os.environ['ENCRYPTED_APP_TOKEN']
        base64_encrypted_output = ENCRYPTED_APP_TOKEN.encode('ascii')
        b64_output_bytes = base64.b64decode(base64_encrypted_output)
        base64_decrypted_output = b64_output_bytes.decode('ascii')
        
        return str(base64_decrypted_output)

    def return_slack_api_token(self):
        """
        Load the encrypted slack api token from the env, decrypts it, and returns the 
        decrypted token
        """
        # Decrypting the ECRYPTED_SLACK_TOKEN env variable
        ENCRYPTED_API_TOKEN = os.environ['ENCRYPTED_API_TOKEN']
        base64_encrypted_output = ENCRYPTED_API_TOKEN.encode('ascii')
        b64_output_bytes = base64.b64decode(base64_encrypted_output)
        base64_decrypted_output = b64_output_bytes.decode('ascii')
        
        return str(base64_decrypted_output)

    def get_connection_url(self):
        """
        Returns the opening connection from Slack API for the web socket
        """

        # To get web socket URL, read the following: https://api.slack.com/apis/connections/socket-implement
        headers = {
                    'Content-type': 'application/x-www-form-urlencoded"',
                    "Authorization": "Bearer " + self.return_slack_app_token(),
                }
        url = "https://slack.com/api/apps.connections.open"
        response = requests.post(url, headers=headers)
        response = json.loads(str(response.text))

        # print("\n\nConnection Establishment Response: ")
        # print(response)
        # print("\n\n")

        if "url" not in response.keys():
            print("\n\nJARVIS-ERROR:")
            print("COULD NOT ESTABLISH CONNECTION TO SLACK API!!!")
            print("\n\t * TRY REINSTALLING JARVIS APP TO WORKSPACE AND REGENERATED ENCRYPTED KEYS")
            print("\n\t * See misc/encryption_example.py to encrypt tokens!")
            print("\nEXITING... Bye!")
            sys.exit()

        return response["url"]


#EOF