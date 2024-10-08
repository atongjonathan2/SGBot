import json
from pymongo import MongoClient
from telebot import logging
from tgbot.config import DATABASE
from pymongo.errors import DuplicateKeyError


class Database:

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def start_db(self):
        # self.logger.info("Initialising database ...")
        try:
            client = MongoClient(DATABASE)
            db = client['sgbot']
            # self.logger.info("Database initialised successfully")
            return db
        except Exception as e:
            self.logger.error(
                f"Error occured when connecting to database: {e}")

    def insert_user(self, user):
        users_collection = self.start_db()['users']
        existing_user = users_collection.find_one({'chat_id': user['chat_id']})
        if existing_user:
            raise DuplicateKeyError(
                f"User with id {user['id']} already exists")
        else:
            users_collection.insert_one(user)
            self.logger.info(f"{user['first_name']} added to Database")

    def insert_json_data(self, json_data, media_type):
        if media_type == 'audio': collection = 'songs'
        if media_type == 'video': collection = 'canvas'
        json_data_collection = self.start_db()[collection]
        json_data_collection.insert_one(json_data)
        self.logger.info(f"{json_data['title']} added to Database")

    def get_all_data(self, collection_name: str) -> list:
        data_collection = self.start_db()[collection_name]
        cursor = data_collection.find()
        result = [item for item in cursor]
        return result

    def search_data(self, collection, performer, title):
        retrieved_data = self.get_all_data(collection)
        message_id = []
        for message in retrieved_data:
            try:
                if performer == message["performer"] and title == message["title"]:
                    message_id.append(message["message_id"])                   
            except Exception:
                self.logger.error(message)
        return message_id
                
        
