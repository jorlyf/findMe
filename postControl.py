from functions import giveTime
from defs import Posts, Contacts
from dataBase import db
import os
import uuid


class CheckBeforePost:

    def __init__(self, current_user, form):
        self.__db = db
        self.__current_user = current_user
        self.__form = form

        self.__checkTime()

        self.__checkAdminRole()

        if self.__condition:
            self.__remaining_time = 0

    def __checkAdminRole(self):
        if self.__current_user.role == 'admin':
            self.__condition = True

    def __getLastPost(self):
        all_posts = self.__db.session.query(Posts).filter_by(author_id=self.__current_user.getId()).all()
        if not all_posts:
            return 0
        return all_posts[-1]

    def __checkTime(self):

        if bool(self.__getLastPost()):
            if (giveTime().timestamp() - self.__getLastPost().date.timestamp()) > 1200:
                self.__condition = True
            else:
                self.__condition = False
                self.__remaining_time = 1200 - (giveTime().timestamp() - self.__getLastPost().date.timestamp())

        else:
            self.__condition = True

    def get(self):
        return self.__condition, self.__remaining_time


def addPostToDB(form, current_user, root_path):
    if not checkHavingContacts(form.vk.data, form.instagram.data, form.otherContacts.data):
        return False
    if form.image.data:
        img = form.image.data
        extension = '.jpeg'
        filename = str(uuid.uuid4()) + extension
        img.save(os.path.join(f"{root_path}\\static\\images\\posts\\{filename}"))
    else:
        filename = None

    post = Posts(author_id=current_user.getId(), head_name=form.head.data,
                 description=form.description.data, images=filename)

    db.session.add(post)
    db.session.flush()
    contacts = Contacts(post_id=post.id, vk=form.vk.data, instagram=form.instagram.data, other=form.otherContacts.data)
    db.session.add(contacts)
    db.session.commit()
    return True


def delPostFromDB(post):
    try:
        contacts = post.contacts
        db.session.delete(contacts)
        db.session.delete(post)

        db.session.commit()
    except:
        print('error delPostFromDB')


def checkHavingContacts(*args):
    length = ''.join(args)
    if len(length) <= 0:
        return False
    return True
