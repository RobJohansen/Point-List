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


def json_response(self, context):
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(context))


class Home(RequestHandler):
    def get(self):
        context = {
            'm'         : models.Membership().all()[0]
        }

        render_with_context(self, 'home.html', context)


class Add(RequestHandler):
    def post(self):
        context = {
            'row'       : render_to_string('row.html', {'m': models.Membership().all()[1]})
        }

        json_response(self, context)


class Remove(RequestHandler):
    def post(self):
        context = {
            
        }

        json_response(self, context)


class Update(RequestHandler):
    def get(self):
        context = {
            'points'    : "0",
            'content'   : "Hotel Information"
        }
        
        json_response(self, context)


class Save(RequestHandler):
    def post(self):
        context = {

        }
        
        json_response(self, context)


class Do(RequestHandler):
    def get(self):
        self.response.out.write('Done')