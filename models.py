from google.appengine.ext import ndb
from google.appengine.api import users


############
# ORDERING #
############
class OrderingBase(ndb.Model):
    order = ndb.IntegerProperty(repeated=True)

    def rows(self):
        return filter(lambda x: x, [Group.get_by_id(r) or Membership.get_by_id(r)  for r in self.order])


########
# USER #
########

class UserProfile(OrderingBase):
    pass


class UserModel(ndb.Model):
    @classmethod
    def __user_key(self):
        return ndb.Key(UserProfile, users.get_current_user().user_id())

    def __init__(cls, **kwargs):
        return super(UserModel, cls).__init__(parent=UserModel.__user_key(), **kwargs)

    @classmethod
    def get_by_id(cls, id, **kwargs):
        return super(UserModel, cls).get_by_id(id, parent=UserModel.__user_key(), **kwargs)

    @classmethod
    def query(cls, *args, **kwargs):
        return super(UserModel, cls).query(ancestor=UserModel.__user_key(), *args, **kwargs)


def get_user_profile():
    return UserProfile.get_or_insert(users.get_current_user().user_id())


def get_user_account():
    user = users.get_current_user()

    if user:
        user.profile = get_user_profile()

        user.is_admin = users.is_current_user_admin()
        user.logout_url = users.create_logout_url('/')
    
    return user


#########
# GROUP #
#########

class Group(UserModel, OrderingBase):
    name = ndb.StringProperty(required=True, default='New Group')


##############
# MEMBERSHIP #
##############
class Membership(UserModel):
    name = ndb.StringProperty()
    scheme = ndb.KeyProperty(kind='Scheme')
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
    membership = ndb.KeyProperty(kind='Membership')
    points = ndb.StringProperty(default='0')
    level = ndb.StringProperty(default='Member')
    created = ndb.DateTimeProperty(auto_now_add=True)




class Type(ndb.Model):
    name = ndb.StringProperty(required=True)
    
    @property
    def schemes(self):
        return Scheme.query(Scheme.type == self.key)


class Scheme(ndb.Model):
    name = ndb.StringProperty()
    type = ndb.KeyProperty(kind='Type')
    page = ndb.StringProperty()
    match = ndb.StringProperty()
    form_name = ndb.StringProperty()
    form_user = ndb.StringProperty()
    form_pass = ndb.StringProperty()

    @property
    def memberships(self):
        return Membership.query(Membership.scheme == self.key)

