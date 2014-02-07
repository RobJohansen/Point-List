from google.appengine.ext import ndb
from google.appengine.api import users
import logging


def current_account():
    u = users.get_current_user()

    if u:
        cs = Account.query(Account.user_id == u.user_id())

        return cs.get()

    else:
        return None

def current_account_key():
    c = current_account()

    return None if not c else c.key

def logout_url(uri):
    return users.create_logout_url(uri)


class Account(ndb.Model):
    name = ndb.StringProperty()
    user_id = ndb.StringProperty()
    order = ndb.IntegerProperty(repeated=True)

    @property
    def groups(self):
        return Group.query(Group.account == self.key)

    @property
    def memberships(self):
        return Membership.query(Membership.account == self.key)


# class UserModel(ndb.Model):
#     account = ndb.KeyProperty(Account, default=current_account_key())

#     @classmethod
#     def all(cls, *args, **kwds):
#         return super(UserModel, cls).query(*args, **kwds)

#     @classmethod
#     def query(cls, *args, **kwds):
#         return super(UserModel, cls).query(UserModel.account == current_account_key(), *args, **kwds)



class Group(ndb.Model):
    name = ndb.StringProperty(required=True)
    order = ndb.IntegerProperty(repeated=True)


class Type(ndb.Model):
    name = ndb.StringProperty(required=True)
    
    @property
    def schemes(self):
        return Scheme.query(Scheme.type == self.key)


class Scheme(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.KeyProperty(Type)
    page = ndb.StringProperty()
    match = ndb.StringProperty()
    form_name = ndb.StringProperty()
    form_user = ndb.StringProperty()
    form_pass = ndb.StringProperty()

    @property
    def memberships(self):
        return Membership.query(Membership.scheme == self.key)


class Membership(ndb.Model):
    name = ndb.StringProperty()
    scheme = ndb.KeyProperty(Scheme)
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    content = ndb.TextProperty()

    @property
    def statuses(self):
        return Status.query(Status.membership == self.key)

    @property
    def latest(self):
        return self.statuses.order(-Status.created).get()

    @property
    def verbose_name(self):
        return self.name or self.scheme.get().name

    def chart_data(self):
        from datetime import datetime
        default = datetime(1970, 1, 1)

        return map(lambda x: [(x.created - default).total_seconds() * 1000, int(x.points)], self.statuses.order(Status.created))


class Status(ndb.Model):
    membership = ndb.KeyProperty(Membership)
    points = ndb.StringProperty(default='0')
    level = ndb.StringProperty(default='Member')
    created = ndb.DateTimeProperty(auto_now_add=True)