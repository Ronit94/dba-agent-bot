from pymongo import MongoClient
from app.config import database_url, database_name
from fastapi.logger import logger
# --- Setup MongoDB ---
client_mongo = MongoClient(database_url)
db = client_mongo[database_name]
session_col = db["sessions"]

async def save_session(email, token, user_info):
    logger.info(f"Saving session for user: {email}")
    session = session_col.find_one({"email": email})
    if session:
        session_col.update_one(
            {"email": email},
            {
                "$set": {
                    "user_id": email,
                    "token": token,
                    "expires_at": token.get("expires_at", 0),
                    "user_info": user_info
                }
            },
            upsert=True
        )
    else:
        session_col.insert_one({
            "user_id": email,
            "email": email,
            "expires_at": token.get("expires_at", 0),
            "user_info": user_info,
            "token": token
        })


async def add_conversation_session(email, chat_context):
    """
    Add a conversation session for a user.
    """
    logger.info(f"Adding conversation session for user: {email}")
    session = session_col.find_one({"email": email})
    if session:
        session_col.update_one(
            {"email": email},
            {"$push": {"chat_context": chat_context}}
        )
    else:
        session_col.insert_one({
            "email": email,
            "chat_context": [chat_context]
        })


async def get_saved_session(email):
    sessions = session_col.find_one({"email": email},{"_id":0})
    return sessions

async def load_intents():
    """
    Load intents from the database.
    """
    logger.info("Loading intents from the database")
    intents = []
    for intent in db.intents_data.find():
        intents.append(intent)
    return intents