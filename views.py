from webapp2 import RequestHandler, uri_for

import jinja2
import models
import os
import json
import logging

from getters import library

J_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def render_to_string(filename, context):
    template = J_ENV.get_template('templates/' + filename)
    return template.render(context)


def render_with_context(self, filename, context):
    context.update({
        'auth_user' : models.get_current_account(),
        'auth_url'  : models.get_logout_url(self.request.uri)
    })

    template = J_ENV.get_template('templates/' + filename)
    self.response.out.write(template.render(context))


class Update(RequestHandler):
    def get(self):
        k = long(self.request.get('key'))
        m = models.Membership.get_by_id(k)

        f = library.get(m.scheme.name, lambda x: "?")

        f(self, m)

        context = {
            'points'    : m.points,
            'content'   : m.content
        }
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(context))


class Home(RequestHandler):
    def get(self):

        schemes = []

        for s in models.Scheme.all():
            if s.memberships.count() == 0:
                schemes.append(s)

        context = {
            'schemes'       : schemes,
            'memberships'   : models.Membership().all(),
            'm'             : models.Membership().all()[0]
        }

        render_with_context(self, 'home.html', context)


class Save(RequestHandler):
    def post(self):
        logging.info(self.request)

        k = long(self.request.get('key'))

        if k:
            m = models.Membership().get_by_id(k)
            m.username = self.request.get('username')
            m.password = self.request.get('password')
            m.put()

        context = {

        }
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(context))


class Add(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))

        if k:
            m = models.Membership()
            m.scheme = models.Scheme.get_by_id(k)
            m.account = models.get_current_account()
            m.username = self.request.get('username')
            m.password = self.request.get('password')
            m.put()

        context = {
            'scheme'    : str(m.scheme.group),
            'row'       : render_to_string('row.html', {'m': m}),
            'group'     : render_to_string('group.html', {'ms': [m]})
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(context))


class Delete(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))

        m = models.Membership.get_by_id(k)

        context = {
            'id'        : m.scheme.key().id(),
            'name'      : m.scheme.name,
            'group'     : str(m.scheme.group)
        }

        m.delete()

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(context))


# class Loyalties(RequestHandler):
#     def get(self):

#         context = {
#             'ls'    : models.Scheme.all().filter(
#                 'account =', models.get_current_account()
#              )
#         }

#         render_with_context(self, 'loyalties.html', context)

#     def post(self):
#         r = self.request

#         l = models.Scheme() if not r.get('key') else models.Scheme.get_by_id(long(r.get('key')))

#         if self.request.get('submit_type') == 'Delete':
#             l.delete()

#         else:

#             l.name = r.get('name')
#             l.page = r.get('page')
#             l.form_name = r.get('form_name')
#             l.form_user = r.get('form_user')
#             l.form_pass = r.get('form_pass')
#             l.match = r.get('match')

#             l.put()

#         self.redirect(self.request.uri.partition('?')[0])


class Do(RequestHandler):
    def get(self):
        # x = models.Account()

        # x.user_id = users.get_current_user().user_id()
        # x.name = "Rob Johansen"

        # x.put()

        # for y in models.Membership.all():
        #     y.account = models.Account().all()[0]
        #     y.put()

        # for x in models.Scheme.all():
        #     delattr(x, 'verbose_name')
        #     x.put()

        # x = models.Membership()
        # x.loyalty = models.Loyalty.get_by_key_name('BritishAirways')
        # x.username = 'r.johansen@live.co.uk'
        # x.password = 'Rdtower19'
        # x.put()

        self.response.out.write('Done')