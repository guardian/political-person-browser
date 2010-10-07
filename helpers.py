import os
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api.urlfetch import fetch
from google.appengine.api.labs import taskqueue

import logging

try:
    import json
except ImportError:
    from django.utils import json

def load_from_json_endpoint(url):
    logging.info('Requesting "%s"' % (url))
    response = fetch(url)
    logging.info('Got "%d"' % (response.status_code))
    if response.status_code == 200:
        return json.loads(response.content)
    return None

def add_task(queue_name, url, params):
    logging.info('Adding task for "%s" with params "%s"' % (url, params))
    taskqueue.add(queue_name=queue_name, url=url, params=params)

def render_admin_template(self, end_point, template_values):
    user = users.get_current_user()
    if user:
        template_values['greeting'] = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                    (user.nickname(), users.create_logout_url("/admin/")))

    render_template(self, end_point, template_values)

def render_template(self, end_point, template_values):
    path = os.path.join(os.path.dirname(__file__), "templates", end_point)
    self.response.out.write(template.render(path, template_values))
    
def slugify(word):
    return word.replace(' ', "-").lower()
