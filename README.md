# SPINNINGMIXER_PROJECT
Repo for Data Science I project.

# PRJECT 01 TO DO LIST:

 - [ ] Enable a “bot” called Jarvis inside your team workspace using Slack’s API.
 - [ ] Create a Python script to power Jarvis that can receive messages from Slack, react to messages based on their contents, and send messages of its own back to Slack.
 - [ ] Instantiate the necessary behavior of Jarvis in your Python code. In particular, Jarvis must remember its current state (where it is in a conversation) when new messages are received and respond to messages with particular contents.
 - [ ] Devise a small database that Jarvis can store some of the data it receives during certain conversations.
 - [ ] Use the completed Jarvis to generate natural language (text) data and save this text to the
database.


DEVELOPER DOCUMENTATION:

    * Required Packages *
        - Required packages can be found in requirements/requirements.txt

    * Slack Tokens *
        - Slack API tokens are expected to be base64 encrypted and stored in two environment variables:
                - $ENCRYPTED_APP_TOKEN
                - $ENCRYPTED_API_TOKEN
        - To see encryption examples or encrypt your tokens, look at misc/excryption_example.py
        - *** Extra ***
            - Store the following in a .env file in the same directory as jarvis.py
                # Use the ENCRYPTED_APP_TOKEN token when starting the websocket connection. 
                    ENCRYPTED_APP_TOKEN = "Insert Base64 Encrypted APP token here>"

                # Use the ENCRYPTED_API_TOKEN token when posting a message.
                    ENCRYPTED_API_TOKEN = "<Insert Base64 API token here>"

    * Software Pattern *
        - Code follows fascade software application development pattern:
          (https://en.wikipedia.org/wiki/Facade_pattern)

        * Visual
            (Top):
                - Jarvis
                    (Business Logic Layer)
                        - WebSocketHandler
                        - Slack_API_Handler
                            (Data Access Object Layer)
                                - DAO (Data Access Object)
                                    (Database Layer)
                                        - JarvisDB (python)
                                        - jarvisdb.db (sqlite3) 
        * Description
            (Top)
            Jarvis --> jarvis.py:

                This is the main run file to start the Jarvis bot. It mostly just establishes a forever-listening
                WebSocketApp connection to our Slack channel.

            (Business Logic Layer)
            WebSocketHandler --> bll/web_socket_handler.py

                This file handles all logic involving the web socket connections:
                    - listening of Jarvis to the Slack channel
                    - establishing of the web socket connection
                    

            (Business Logic Layer)
            SlackAPIHandler --> bll/web_socket_handler.py

                This file handles all the action logic involving the Slack API connections in response to events
                flagged / identified from the WebSocketHandler:
                    - returning decrypted Slack API tokens 
                    - sending messages from Jarvis
                    - toggling Jarvis training mode
                    - Capturing training data and sending it to the DAO

            (DAO Layer)
            DAO (Data Access Object) --> DAO/DAO.py

                This file handles all queries to the jarvisdb sqlite3 database
                    -> Establises connection obects to database from JarvisDB

            (Database Layer)

                JarvisDB --> database/JarvisDB.py
                    -> Returns connection objects to the jarvisdb database
                jarvisdb --> database/jarvisdb.db
                    -> Sqlite3 database for Jarvis

      
Enjoy!
