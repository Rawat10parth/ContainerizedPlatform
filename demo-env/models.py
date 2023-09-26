from . import db


class Users(db.Documenrt):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    email = db.StringField(required=True)
    dob = db.StringField(required=True)