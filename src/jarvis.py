import websocket
from pathlib import Path
from bll.web_socket_handler import WebSocketHandler


class Jarvis():
    """
    Run file to start the Jarvis Bot
    """
    def __init__(self, enableTrace=False, slack_api_key=None, slack_app_key=None):

        # Creating Jarvis object attrbute to abstract WebSocketApp and Slack API stuff
        # Set enableTrace to True or False to give lots of vs little chatter 
        self.__enableTrace__    = enableTrace

        # Getting any app tokens that may have been passed to the Jarvis constructor
        self.__slack_api_key__  = slack_api_key
        self.__slack_app_key__  = slack_app_key

        # Creating Web Socket Handler object from web_socket_api.py
        self.Web_Socket_Handler = WebSocketHandler(__enableTrace__  = self.__enableTrace__,   \
                                                   __slack_app_key__= self.__slack_app_key__, \
                                                   __slack_api_key__= self.__slack_api_key__  )

    def start(self):

        # Starting the WebSocketApp with return_websocket function in web_socket_handler.py
        self.ws = self.Web_Socket_Handler.return_websocket()        

        # Keep the web socket listening forever (without timeout)
        self.ws.run_forever()


### START HERE ###

# Loading Jarvis
self = Jarvis(slack_api_key=None, slack_app_key=None, enableTrace=False)
self.start()

#EOF