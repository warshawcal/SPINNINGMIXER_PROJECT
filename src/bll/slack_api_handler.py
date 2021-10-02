import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import base64
import requests
import json
import sys
"""
This file handles all calls to the Slack API
"""

class Slack_API_Handler:

    def send_message_to_channel(self, message, channel="C02F17T7CK1"):
        """
        Deafult channel is the "general" channel
        """
        headers = {
                    "Authorization": "Bearer " + self.return_slack_api_token(),
                    "Content-type": "application/x-www-form-urlencoded",
                }
        url = "https://slack.com/api/chat.postMessage"
        data = {"channel":channel,"text":message}
        response = requests.post(url, headers=headers, data=data)
        response = json.loads(str(response.text))

    def return_slack_app_token(self):
        """
        @TODO: Load the encrypted slack app token from the env, decrypts it, and returns the 
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
        @TODO: Load the encrypted slack api token from the env, decrypts it, and returns the 
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
        some curl command: 
            curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' https://hooks.slack.com/services/asdfasdfasdf

        equivalent python code:
            headers = {
                'Content-type': 'application/json',
            }

            data = '{"text":"Hello, World!"}'

            response = requests.post('https://hooks.slack.com/services/asdfasdfasdf', headers=headers, data=data)

        (https://stackoverflow.com/questions/25491090/how-to-use-python-to-execute-a-curl-command/48005899)
        """

        # To get web socket URL, read the following: https://api.slack.com/apis/connections/socket-implement
        headers = {
                    'Content-type': 'application/x-www-form-urlencoded"',
                    "Authorization": "Bearer " + self.return_slack_app_token(),
                }
        url = "https://slack.com/api/apps.connections.open"
        response = requests.post(url, headers=headers)
        response = json.loads(str(response.text))
        
        return response["url"]
