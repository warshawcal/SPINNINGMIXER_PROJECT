import websocket
from pathlib import Path
from dotenv import load_dotenv
from bll.ErrorHandler import error_handler
from bll.web_socket_handler import WebSocketHandler

class Jarvis:

    #@error_handler(debug_mode=True, function_name="Jarvis.start")
    def start(self):

        # Creating Jarvis object attrbute to abstract WebSocketApp and Slack API stuff
        # Set enableTrace to True or False to give lots of vs little chatter 
        self.Web_Socket_Handler = WebSocketHandler(enableTrace=False)

        # Starting the WebSocketApp with return_websocket function in web_socket_handler.py
        self.ws = self.Web_Socket_Handler.return_websocket()        

        # Keep the web socket listening forever (without timeout)
        self.ws.run_forever()


### START HERE ###

# Loading the enviornment variables from .env 
# Used for getting encrypted API and APP keys
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Loading Jarvis
self = Jarvis()
self.start()

#EOF