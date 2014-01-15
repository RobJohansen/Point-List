from google.appengine.ext import db
from google.appengine.api import users


def get_current_account():
    i = users.get_current_user().user_id()
    cs = Account().all().filter('user_id =', i)

    if cs.count() == 0:
        a = Account()
        a.name = 'Name'
        a.user_id = i
        a.put()

    else:
        a = cs[0]

    return a


def get_logout_url(uri):
    return users.create_logout_url(uri)


class UserModel(db.Model):
    def all(cls, order=None):
    
        result = super(UserModel, cls).all().filter('account =', get_current_account())

        return result

    # def all(cls):
    #     a = super(UserModel, cls)

    #     # a = a.all(cls)

    #     # a = a

    #     return a.all(cls)


class Type(db.Model):
    name = db.StringProperty()

class Scheme(db.Model):
    name = db.StringProperty(required=True)
    type = db.ReferenceProperty(Type, collection_name='schemes')
    page = db.StringProperty()
    match = db.StringProperty()
    form_name = db.StringProperty()
    form_user = db.StringProperty()
    form_pass = db.StringProperty()


class Account(db.Model):
    name = db.StringProperty()
    user_id = db.StringProperty()



class Group(UserModel):
    name = db.StringProperty()
    account = db.ReferenceProperty(Account, collection_name='groups')

class Membership(UserModel):
    name = db.StringProperty()
    scheme = db.ReferenceProperty(Scheme, collection_name='memberships')
    group = db.ReferenceProperty(Group, collection_name='memberships')
    account = db.ReferenceProperty(Account, collection_name='memberships')
    username = db.StringProperty()
    password = db.StringProperty()
    points = db.StringProperty(default='0')
    content = db.TextProperty()