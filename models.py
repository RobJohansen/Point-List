from google.appengine.ext import db
from google.appengine.api import users


def current_account():
    u = users.get_current_user()

    if u:
        cs = Account.all().filter('user_id =', u.user_id())

        if cs.count() > 0:
            return cs[0]

        else:
            # Create Account
            return None

    else:
        return None

def logout_url(uri):
    return users.create_logout_url(uri)



class UserModel(db.Model):
    @classmethod
    def all(cls, **kwds):
        return super(UserModel, cls).all(**kwds).filter('account =', current_account())


class Account(db.Model):
    name = db.StringProperty()
    user_id = db.StringProperty()
    order = db.ListProperty(long)

class Group(db.Model):
    name = db.StringProperty()
    account = db.ReferenceProperty(Account, collection_name='groups')


class Type(db.Model):
    name = db.StringProperty(required=True, default='Name')


class Scheme(db.Model):
    name = db.StringProperty(required=True, default='Name')
    type = db.ReferenceProperty(Type, collection_name='schemes')
    page = db.StringProperty()
    match = db.StringProperty()
    form_name = db.StringProperty()
    form_user = db.StringProperty()
    form_pass = db.StringProperty()


class Membership(UserModel):
    name = db.StringProperty(required=True, default='Name')
    scheme = db.ReferenceProperty(Scheme, collection_name='memberships')
    group = db.ReferenceProperty(Group, collection_name='memberships')
    account = db.ReferenceProperty(Account, collection_name='memberships', default=current_account())
    username = db.StringProperty()
    password = db.StringProperty()
    points = db.StringProperty(default='0')
    content = db.TextProperty(default='')