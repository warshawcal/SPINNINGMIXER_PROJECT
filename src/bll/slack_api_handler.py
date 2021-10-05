import os
import base64
import requests
import json
import sys
import pandas as pd
import time
from DAO.DAO import DAO
from bll.ErrorHandler import error_handler


class SlackAPIHandler():
    """
    This file handles all logic to the Slack API.
    Mostly handles the action logic of Jarvis in response to events.

    Inherits WebSocketHander
    """
    def __init__(self, __enableTrace__=False, __slack_app_key__=None, __slack_api_key__=None):
        """
        Initializing SlackAPIHandler object.
        """

        # recipient:id map for Slack API Handler
        self.recipient2id = {
            "Nicholas Hella" : "U02FCUM64NR",
            "John"           : "U02G5KRTC8Y",
            "Cal"            : "U02GADB06D6",
            "Nick Knudson"   : "U02FGDFJQ78",
            "Jarvis"         : "U02G827ANEA",
            "general"        : "C02F17T7CK1"
        }

        # Data from conversation
        self.data = dict(())        

        # Boolean for whether Jarvis is in training mode
        self.in_training_mode = False
        self.print_the_training_data = True

        # Getting any app tokens that may have been passed to the Jarvis constructor
        self.__slack_api_key__ = __slack_api_key__
        self.__slack_app_key__ = __slack_app_key__
        self.__enableTrace__   = __enableTrace__ # can be used as debug flag from here on out

        # Creating Slack_API_Handler object attrbute to abstract Sqlite3 database stuff
        self.DAO = DAO(__enableTrace__=self.__enableTrace__) # No need to pass tokens from here on out

    def handle_message(self, message, received_from):
        """
        Handles responses to messages received by Jarvis from recipient
        """

        # Toggle Jarvis training mode if necessary with appropriate handling
        if self.trigger_training_mode_ON(message, received_from):
            pass # Handling done in trigger_training_mode_ON function
        elif self.trigger_training_mode_OFF(message, received_from):
            pass # Handling done in trigger_training_mode_ON function
        # Handling for training mode
        elif self.in_training_mode:
            # Handle the message appropriately if in training mode --> @TODO: Pump data into jarvisdb
            self.handle_training(message,received_from)
        else:
            # Handle the message appropriately if not in training mode --> @TODO: Everything else..
            message = "Hello, I'm not in training mode. Enter \"training time\" to enable training mode " + \
                      "and enter \"done\" to disable training mode"
            self.send_message_to_recipient(message=message, recipient=received_from)
            pass

        return

    def handle_training(self, message, received_from):
        """
        Handles Jarvis's training response
        """
        # Get the subject, if Jarvis hasn't already gotten it
        if self.data['training_data']['ACTION'] is None:
            self.data['training_data']['ACTION'] = str(message).strip()
            message = "Ok, let's call this ACTION `" + str(message).strip() + "`. " \
                    + "Now give me some training text!"
            self.send_message_to_recipient(message=message, recipient=received_from)
        # Else, get some training text!
        else:
            if str(self.data['training_data']['ACTION']).strip() != message:
                self.data['training_data']['TEXT'].append(str(message).strip())
            message = "Ok, I've got it! What else?"
            self.send_message_to_recipient(message=message, recipient=received_from)

        return

    def trigger_training_mode_ON(self, message, received_from):
        """
        Returns True/False if Jarvis should be in training mode
        """
        if str(message).strip() == "training time" and self.in_training_mode == False:
            # Mimicing the training data table in jarvisdb in the data dictionary
            self.data['training_data'] = dict(())
            self.data['training_data']['ACTION'] = None
            self.data['training_data']['TEXT'] = []
            self.in_training_mode = True # Activating Jarvis training mode
            message = "OK, I'm ready for training. What NAME should this ACTION be?"
            self.send_message_to_recipient(message=message, recipient=received_from)
            return self.in_training_mode
        
        return False

    def print_training_data(self):
        """
        Returns the training data Jarvis has stored
        """
        print("\nJARVIS-INFO: TRAINING DATA TABLE")
        print("\tACTION: " + str(self.data['training_data']['ACTION']))
        print("\tTRAINING TEXT:")
        count = 1
        for message in self.data['training_data']['TEXT']:
            print("\t\t* " + str(count) + ") " + str(message))
            count += 1
        print("\n")

        return


    def trigger_training_mode_OFF(self, message, received_from):
        """
        Returns True/False if Jarvis should be in training mode
        """
        if str(message).strip() == "done" and self.in_training_mode:
            message = "OK, I'm done training. Saving results.."
            self.in_training_mode = False
            self.send_message_to_recipient(message=message, recipient=received_from)
            self.save_training_data_to_jarvis_database()
            return True
        
        return False

    def save_training_data_to_jarvis_database(self):
        # @TODO: Finish
        if self.print_the_training_data:
                self.print_training_data()

        for message in self.data['training_data']['TEXT']:
            self.DAO.insert_training_data(action=self.data['training_data']['ACTION'],
                                                 text=message)
        print("Saving training data to Jarvis database!")
        
        return

    @error_handler(debug_mode=True,function_name="SlackAPIHandler.send_message_to_recipient")
    def send_message_to_recipient(self, message, recipient):
        """
        Send message to a receipient on Slack
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

        return

    @error_handler(debug_mode=True,function_name="SlackAPIHandler.return_slack_app_token")
    def return_slack_app_token(self):
        """
        Load the encrypted slack app token from the env, decrypts it, and returns the 
        decrypted token
        """

        if str(self.__slack_app_key__).strip() == "None":
            # Getting encrypted app token from .encrypted_api_keys file
            for line in open('.env', 'r').readlines():
                line = line.replace(" ", "") # Removing all spaces
                if line.startswith("#") is False and line.startswith("ENCRYPTED_APP_TOKEN") is True:
                        ENCRYPTED_APP_TOKEN = line.replace("ENCRYPTED_APP_TOKEN=", "").strip()
                        ENCRYPTED_APP_TOKEN = ENCRYPTED_APP_TOKEN.replace("\"", "").strip()

            # Decrypting the b64 encoded token
            base64_encrypted_output = ENCRYPTED_APP_TOKEN.encode('ascii')
            b64_output_bytes = base64.b64decode(base64_encrypted_output)
            base64_decrypted_app_token = b64_output_bytes.decode('ascii')
            self.__slack_app_key__ =  str(base64_decrypted_app_token)

            return self.__slack_app_key__

    @error_handler(debug_mode=True,function_name="SlackAPIHandler.return_slack_api_token")
    def return_slack_api_token(self):
        """
        Load the encrypted slack api token from the env, decrypts it, and returns the 
        decrypted token
        """
        if str(self.__slack_api_key__).strip() == "None":
            # Getting encrypted app token from .encrypted_api_keys file
            for line in open('.env', 'r').readlines():
                line = line.replace(" ", "") # Removing all spaces
                if line.startswith("#") is False and line.startswith("ENCRYPTED_API_TOKEN") is True:
                        ENCRYPTED_API_TOKEN = line.replace("ENCRYPTED_API_TOKEN=", "").strip()
                        ENCRYPTED_API_TOKEN = ENCRYPTED_API_TOKEN.replace("\"", "").strip()

            base64_encrypted_output = ENCRYPTED_API_TOKEN.encode('ascii')
            b64_output_bytes = base64.b64decode(base64_encrypted_output)
            base64_decrypted_api_token = b64_output_bytes.decode('ascii')
            self.__slack_api_key__ = str(base64_decrypted_api_token)

            return self.__slack_api_key__

    @error_handler(debug_mode=True,function_name="SlackAPIHandler.get_connection_url")
    def get_connection_url(self):
        """
        Returns the opening connection from Slack API for the web socket
        """

        # To get web socket URL, read the following: https://api.slack.com/apis/connections/socket-implement
        headers = {
                    'Content-type' : 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer ' + self.return_slack_app_token(),
                }
        url = "https://slack.com/api/apps.connections.open"
        response = requests.post(url, headers=headers)
        response = json.loads(str(response.text))

        # print("\n\nConnection Establishment Response: ")
        # print(response)
        # print("\n\n")

        if "url" not in response.keys():
            print("\n\nJARVIS-ERROR:")
            print("*** COULD NOT ESTABLISH CONNECTION TO SLACK API ***")
            print("\n\t * TRY REINSTALLING JARVIS APP TO WORKSPACE AND REGENERATED ENCRYPTED KEYS")
            print("\n\t * See misc/encryption_example.py to encrypt tokens!")
            print("\nEXITING... Bye!")
            sys.exit()

        return response["url"]


#EOF