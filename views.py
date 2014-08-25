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
    from google.appengine.api import users

    context.update({
        'user'          : models.get_user_account()
    })

    template = J_ENV.get_template('templates/' + filename)
    self.response.out.write(template.render(context))


def json_response(self, context):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(context))












def menu_items():
    from operator import attrgetter

    schemes = []
    for s in models.Scheme.query():
        if s.memberships.count() == 0:
            schemes.append(s)

    return sorted(schemes, key=attrgetter('name'))









class Home(RequestHandler):
    def get(self):
        context = {
            'ms'        : menu_items()
        }

        render_with_context(self, 'home.html', context)


class AdminConsole(RequestHandler):
    def get(self):
        context = {

        }

        render_with_context(self, 'admin.html', context)



class Menu(RequestHandler):
    def get(self):
        context = {
            'menu'      : render_to_string('menu.html', { 'ms' : menu_items() })
        }

        json_response(self, context)


class Add(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))
        s = models.Scheme.get_by_id(k)

        m = models.Membership()
        m.scheme = s.key
        m.put()

        context = {
            'node'      : render_to_string('row.html', { 'r' : m })
        }

        json_response(self, context)


class AddGroup(RequestHandler):
    def post(self):
        m = models.Group()
        m.put()

        context = {
            'node'      : render_to_string('group.html', { 'r' : m })
        }

        json_response(self, context)


class Remove(RequestHandler):
    def post(self):
        k = long(self.request.get('key'))
        m = models.Membership.get_by_id(k) or models.Group.get_by_id(k)

        m.key.delete()

        context = {

        }

        json_response(self, context)


class Update(RequestHandler):
    def get(self):
        k = long(self.request.get('key'))
        m = models.Membership.get_by_id(k)

        from getters import updater
        rs = updater(self, m, self.request.get('p'))

        context = {

        }

        if rs.get('success'):
            m.content = unicode(rs.get('content'))
            m.put()

            s = models.Status(membership=m.key)
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
        m = models.Membership.get_by_id(k) or models.Group.get_by_id(k)

        m.name = self.request.get('name')
        
        if m.key.kind() == 'Membership':
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

        ks = json.loads(k)

        def _order(k):
            if k['isGroup']:
                g = models.Group.get_by_id(long(k['id']))
                g.order = map(_order, k['subs'])
                g.put()

            return long(k['id'])
                
        p = models.get_user_profile()
        p.order = map(_order, ks)
        p.put()


class Do(RequestHandler):
    def get(self):
        self.response.out.write('Done')