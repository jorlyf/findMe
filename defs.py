from datetime import datetime
from pytz import timezone
from flask_login import UserMixin
from dataBase import db


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(20), default='user')
    date = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Moscow')))

    def __repr__(self):
        return f"<users {self.id}>"


    def getId(self):
        return self.id


    def getPosts(self):
        return db.session.query(Posts).filter_by(author_id=self.id).all()


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    vk = db.Column(db.String(50))
    instagram = db.Column(db.String(50))
    other = db.Column(db.String(100))

    def __repr__(self):
        return f"<contacts {self.id}>"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    head_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contacts = db.relationship('Contacts', backref='posts', uselist=False)
    images = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Moscow')))

    def __repr__(self):
        return f"<posts {self.id}>"

    def toJson(self):
        post = {}
        if hasattr(self, 'id'):
            post['id'] = self.id
        if hasattr(self, 'date'):
            post['date'] = str(self.date)
        if hasattr(self, 'description'):
            post['description'] = self.description
        if hasattr(self, 'head_name'):
            post['head_name'] = self.head_name
        if hasattr(self, 'contacts'):
            if hasattr(self.contacts, 'vk'):
                post['vk'] = self.contacts.vk
            if hasattr(self.contacts, 'instagram'):
                post['instagram'] = self.contacts.instagram
            if hasattr(self.contacts, 'other'):
                post['otherContacts'] = self.contacts.other
        if hasattr(self, 'images'):
            post['images'] = self.images

        return post
