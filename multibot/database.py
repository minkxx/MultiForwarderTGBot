from pymongo.mongo_client import MongoClient
from pyrogram.types import Message

from multibot import MONGO_DB_URI


mongoClient = MongoClient(MONGO_DB_URI)


collection = mongoClient["chat_ids"]["ids"]

users_collection = mongoClient["users"]["user_ids"]


def set_chat_id(m: Message, from_chat_id: int, to_chat_id: int):
    user_id = str(m.from_user.id)
    data = {"from_chat_id": int(from_chat_id), "to_chat_id": int(to_chat_id)}
    obj_doc = {user_id: {"$exists": True}}
    obj = collection.find_one(obj_doc)
    if obj:
        all_datas = []
        for i in obj[user_id]:
            all_datas.append(i)
        if data not in all_datas:
            all_datas.append(data)
        updateQuery = {"$set": {user_id: all_datas}}
        collection.update_one(obj_doc, updateQuery)
    else:
        data = [{"from_chat_id": from_chat_id, "to_chat_id": to_chat_id}]
        toSendDoc = {user_id: data}
        collection.insert_one(toSendDoc)


def get_all_chats(get_only_key=False, get_only_value=False):
    all_documents = collection.find()
    all_ = []
    all_chats = []

    if get_only_value:
        for document in all_documents:
            last_key, last_value = list(document.items())[-1]
            all_.append(last_value)
        for i in all_:
            for j in i:
                all_chats.append(j)
        return all_chats

    elif get_only_key:
        for document in all_documents:
            last_key, last_value = list(document.items())[-1]
            all_.append(last_key)
        for i in all_:
            all_chats.append(i)
        return all_chats
    else:
        return False


def add_user_db(user_id):
    obj_doc = {"all_users_list": {"$exists": True}}
    obj = users_collection.find_one(obj_doc)
    if obj:
        all_datas = []
        for i in obj["all_users_list"]:
            all_datas.append(i)
        if user_id not in all_datas:
            all_datas.append(user_id)
        updateQuery = {"$set": {"all_users_list": all_datas}}
        users_collection.update_one(obj_doc, updateQuery)
    else:
        data = [user_id]
        toSendDoc = {"all_users_list": data}
        users_collection.insert_one(toSendDoc)


def remove_user_db(user_id: int):
    obj_doc = {"all_users_list": {"$exists": True}}
    obj = users_collection.find_one(obj_doc)
    if obj:
        all_datas = []
        for i in obj["all_users_list"]:
            all_datas.append(i)
        if user_id in all_datas:
            all_datas.remove(user_id)
        updateQuery = {"$set": {"all_users_list": all_datas}}
        users_collection.update_one(obj_doc, updateQuery)


def get_all_users():
    obj_doc = {"all_users_list": {"$exists": True}}
    obj = users_collection.find_one(obj_doc)
    if obj:
        all_datas = []
        for i in obj["all_users_list"]:
            all_datas.append(i)
        return all_datas
    else:
        return False


def chats_of_user(user_id):
    user_id = str(user_id)
    obj_doc = {user_id: {"$exists": True}}
    obj = collection.find_one(obj_doc)
    if obj:
        return obj[user_id]
    else:
        return False
