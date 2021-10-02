import sqlite3
from bll.ErrorHandler import error_handler

class JarvisDB:

    def __init__(self, debug_trace=True):
        """
        Initializing JarvisDB object.
        Basically just returns connection and cursor objects to the database..
        """
        self.debug_trace = debug_trace


    #@error_handler(debug_mode=True,function_name="JarvisDB.restart_database")
    def restart_database(self):
        """
        THIS WILL REMOVE THE DATABASE. USE THIS ONLY TO RESTART FROM BEGINNING
        """
        # remove any previously existing db file
        try:
            os.remove("database/jarvisdb.db")
        except:
            pass

        # create the db file
        jarvisdb_conn = sqlite3.connect("database/jarvisdb.db", check_same_thread=False)
        jarvisdb_cur = jarvisdb_conn.cursor()
        
        return jarvisdb_conn, jarvisdb_cur

    #@error_handler(debug_mode=True,function_name="JarvisDB.return_database")
    def return_database(self):
        """
        Returns database connection
        """
        # create the db file
        jarvisdb_conn = sqlite3.connect("database/jarvisdb.db", check_same_thread=False)
        jarvisdb_cur = jarvisdb_conn.cursor()
        
        return jarvisdb_conn, jarvisdb_cur