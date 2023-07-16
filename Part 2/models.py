from mongoengine import Document, StringField, BooleanField, connect
import configparser

# -------- Connection to MongoDB ---------
config = configparser.ConfigParser()
config.read("../Part 1/config.ini")

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = "hw08_part2"

connect(db=db_name,
        host=f"mongodb+srv://{mongo_user}:{mongodb_pass}@stepanovdb.codnmzv.mongodb.net/?retryWrites=true&w=majority",
        ssl=True)
# ----------------------------------------------


class MyContacts(Document):
    fullname = StringField(max_length=30, required=True)
    email = StringField(max_length=40, required=True)
    message = StringField(required=True)
    preferred_sending = StringField(required=True)  # SMS or Email
    is_received = BooleanField(default=False)
