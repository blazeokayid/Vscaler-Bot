from pymongo import MongoClient
from Vscaler import DATABASE_URL

vsc = MongoClient(DATABASE_URL)
db = vsc.vscale
user_settings = db["user_settings"]

def save_user_settings(user_id, settings):
    user_settings.update_one(
        {"_id": user_id,
        "$set": settings},
        upsert=True
        )
    
def get_user_settings(user_id):
    return user_settings.find_one("_id",user_id)