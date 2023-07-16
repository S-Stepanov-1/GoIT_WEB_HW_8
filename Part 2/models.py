from mongoengine import Document, StringField, BooleanField


class MyContacts(Document):
    fullname = StringField(max_length=30, required=True)
    email = StringField(max_length=40, required=True)
    is_received = BooleanField(default=False)
