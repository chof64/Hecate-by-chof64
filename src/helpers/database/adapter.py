
"""
    Adapters in connecting to database.
"""

import os

import motor.motor_asyncio
from dotenv import load_dotenv


load_dotenv()


class MongoConn():
    """
        All connecting functions to the database.
    """
    def __init__(self, auth:dict = "default"):
        """
            Authentication and related variables used to connect to the database.

            TODO: Add auth checks to see if the credentials exists or all arguments are given.
        """
        # 0: Argument checks and processing.
        if auth != "default":
            parsed_auth = auth
        else:
            parsed_auth = {
                "username": "DEFAULT_MONGO_USERNAME",
                "password": "DEFAULT_MONGO_PASSWORD",
                "uri": "DEFAULT_MONGO_URI"
            }
        # 1: Variables
        self.db_username = os.getenv(parsed_auth['username'])
        self.db_password = os.getenv(parsed_auth['password'])
        self.db_uri = os.getenv(parsed_auth['uri'])


    async def database_conn(self, database_name:str, collection_name:str):
        """
            Connects to the database and returns the connection.
        """
        # 0: Authentication credentials, processing and merging.
        db_login_user = f'{self.db_username}:{self.db_password}'
        db_address = f'{self.db_uri}/{database_name}'
        db_login_string = f'mongodb+srv://{db_login_user}@{db_address}?retryWrites=true&w=majority'

        client = motor.motor_asyncio.AsyncIOMotorClient(db_login_string)
        return client[database_name][collection_name]
