from google.appengine.ext import ndb
from google.appengine.api import users
import logging


def current_account():
    u = users.get_current_user()

    if u:
        return Account.query(Account.user_id == u.user_id()).get() or Account().put().get()             # Adds two :)

    else:
        return None


def logout_url(uri):
    return users.create_logout_url(uri)


class Account(ndb.Model):
    name = ndb.StringProperty()
    user_id = ndb.StringProperty()
    order = ndb.IntegerProperty(repeated=True)

    def rows(self):
        return filter(lambda x: x is not None, [Group.get_by_id(r) or Membership.get_by_id(r)  for r in self.order])


class Group(ndb.Model):
    name = ndb.StringProperty(required=True, default="New Group")
    order = ndb.IntegerProperty(repeated=True)

    def rows(self):
        return filter(lambda x: x is not None, [Membership.get_by_id(r) for r in self.order])


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