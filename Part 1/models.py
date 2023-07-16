from mongoengine import ListField, Document, StringField, ReferenceField


class Authors(Document):
    fullname = StringField(max_length=30, required=True)
    born_date = StringField(max_length=20)
    born_location = StringField(max_length=50)
    description = StringField(required=True)


class Quotes(Document):
    tags = ListField(StringField(max_length=20))
    author = ReferenceField(Authors)
    quote = StringField(required=True)
