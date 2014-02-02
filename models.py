from google.appengine.ext import ndb
from google.appengine.api import users
import logging

def current_account():
    u = users.get_current_user()

    if u:
        cs = Account.query(Account.user_id == u.user_id())

        if cs.count() > 0:
            return cs.get()

        else:
            # Create Account
            return None

    else:
        return None

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


class UserModel(ndb.Model):
    account = ndb.KeyProperty(Account, default=current_account())

    @classmethod
    def query(cls, *args, **kwds):
        return super(UserModel, cls).query(UserModel.account == current_account().key, *args, **kwds)


class Group(UserModel):
    name = ndb.StringProperty(required=True)

    @property
    def memberships(self):
        return Membership.query(Membership.group == self.key)


class Type(ndb.Model):
    name = ndb.StringProperty(required=True)
    
    @property
    def schemes(self):
        return Scheme.query(Scheme.type == self.key)


class Scheme(ndb.Model):
    name = ndb.StringProperty(required=True, default='Name')
    type = ndb.KeyProperty(Type)
    page = ndb.StringProperty()
    match = ndb.StringProperty()
    form_name = ndb.StringProperty()
    form_user = ndb.StringProperty()
    form_pass = ndb.StringProperty()

    @property
    def memberships(self):
        return Membership.query(Membership.scheme == self.key)


class Membership(UserModel):
    name = ndb.StringProperty(required=True, default='Name')
    scheme = ndb.KeyProperty(Scheme)
    group = ndb.KeyProperty(Group)
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    content = ndb.TextProperty()

    @property
    def statuses(self):
        return Status.query(Status.membership == self.key)

    @property
    def latest(self):
        return self.statuses.order(-Status.created).get()

    def chart_data(self):
        from datetime import datetime
        default = datetime(1970, 1, 1)

        return map(lambda x: [(x.created - default).total_seconds() * 1000, int(x.points)], self.statuses.order(Status.created))


class Status(ndb.Model):
    membership = ndb.KeyProperty(Membership)
    points = ndb.StringProperty(default='0')
    level = ndb.StringProperty(default='Member')
    created = ndb.DateTimeProperty(auto_now_add=True)