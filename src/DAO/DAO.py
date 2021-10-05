import os
import glob
from database.JarvisDB import JarvisDB
from bll.ErrorHandler import error_handler
import pandas as pd

class DAO():
    """
    DAO: Data Access Object
    This file handles all queries to the sqlite3 database

    Inherits SlackAPIHandler
    """
    
    def __init__(self, __enableTrace__=False):
        """
        Initializing Jarvis DAO object
        """
        self.__enableTrace__   = __enableTrace__ # can be used as debug flag from here on out
        self.JarvisDB = JarvisDB(__enableTrace__=self.__enableTrace__)
        self.JarvisDB_conn, self.JarvisDB_cur = self.JarvisDB.return_database() # get connection objects to db
        self.create_training_data_table() # create the training data table if it doesn't exist

    @error_handler(debug_mode=True,function_name="DAO.create_training_data_table")
    def create_training_data_table(self):
        """
        Creates the training data table in the database if it doesn't exist
        """
        sql_string = "CREATE TABLE IF NOT EXISTS training_data (ACTION Text, TEXT Text);"
        self.JarvisDB_cur.execute(sql_string)
        self.JarvisDB_conn.commit()

        return

    @error_handler(debug_mode=True,function_name="DAO.create_training_data_table")
    def return_training_data_table(self):
        """
        Returns the training data table as a pandas dataframe
        """
        sql_string = "SELECT * FROM training_data;"
        df = pd.read_sql_query(sql_string, self.JarvisDB_conn)

        return df

    @error_handler(debug_mode=True,function_name="DAO.insert_training_data")
    def insert_training_data(self, action, text):
        """
        Inserts training data into the Jarvis database
        """
        # Check if data already exists in db
        sql_string = "SELECT * FROM training_data WHERE ACTION = '{}' AND TEXT = '{}';".format(action,text)
        df = pd.read_sql_query(sql_string, self.JarvisDB_conn)

        # If not, write SQL INSERT string
        if len(df) == 0:
            sql_string = "INSERT INTO training_data (ACTION, TEXT) VALUES ('{}', '{}');".format(action,text)
            
            # Insert data into the Jarvis database
            self.JarvisDB_cur.execute(sql_string)
            self.JarvisDB_conn.commit()

        return

#EOF