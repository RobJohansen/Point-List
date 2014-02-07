from webapp2 import RequestHandler, uri_for

import jinja2
import models
import os
import logging
import json

J_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


def render_to_string(filename, context):
    template = J_ENV.get_template('templates/' + filename)
    return template.render(context)


def render_with_context(self, filename, context):
    context.update({
        'auth_user' : models.current_account(),
        'auth_url'  : models.logout_url(self.request.uri)
    })

    template = J_ENV.get_template('templates/' + filename)
    self.response.out.write(template.render(context))


def json_response(self, context):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(context))


class Home(RequestHandler):
    def get(self):
        from operator import attrgetter

        schemes = []
        for s in models.Scheme.query():
            if s.memberships.count() == 0:
                schemes.append(s)




        ms = sorted(schemes, key=attrgetter('name'))

        f = lambda xs: dict(map(lambda x: (x.key.id(), x), xs))

        xs = f(models.Membership.query())
        xs.update(f(models.Group.query()))

        rs = filter(lambda x: x is not None, map(lambda i: xs.get(i), models.current_account().order))




        context = {
            'ms'        : ms,
            'rs'        : rs
        }

        render_with_context(self, 'home.html', context)


class Add(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))
        s = models.Scheme.get_by_id(k)

        m = models.Membership()
        m.scheme = s.key
        m.put()

        context = {
            'row'       : render_to_string('row.html', { 'r' : m })
        }

        json_response(self, context)


class Remove(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))
        m = models.Membership.get_by_id(k)

        m.key.delete()

        context = { }

        json_response(self, context)


class Update(RequestHandler):
    def get(self):
        k = long(self.request.get('key'))
        m = models.Membership.get_by_id(k)

        from getters import updater
        rs = updater(self, m)

        context = {}

        if rs.get('success'):
            m.content = unicode(rs.get('content'))
            m.put()

            s = models.Status(membership=m)
            s.points = unicode(rs.get('points').replace(',', '').strip())
            s.put()

            context = {
                'points'    : s.points,
                'content'   : m.content
            }

        context.update({
            'success'   : rs.get('success')
        })
        
        json_response(self, context)


class Save(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))
        m = models.Membership().get_by_id(k)

        m.name = self.request.get('name')
        m.username = self.request.get('username')
        m.password = self.request.get('password')
        m.put()

        context = {
            'name'      : m.name
        }
        
        json_response(self, context)


class Order(RequestHandler):
    def post(self):
        k = self.request.get('keys')

        rs = []

        for r in json.loads(k):
            if isinstance(r, (list)):
                g = models.Group.query().get()
                g.order = map(long, r[1:])
                g.put()

            else:
                rs.append(r)
        
        a = models.current_account()
        a.order = map(long, rs)
        a.put()


class Do(RequestHandler):
    def get(self):
        self.response.out.write('Done')