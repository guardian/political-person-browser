#!/usr/bin/env python

# Always prefer a newer version of django, for at least the auto-escape ability of
# the template functions
from google.appengine.dist import use_library
use_library('django', '1.1')

from google.appengine.ext.webapp import WSGIApplication, RequestHandler
from google.appengine.ext.webapp.util import run_wsgi_app

# Local imports
import settings
import helpers
import models
import logging

class MainHandler(RequestHandler):
    def get(self):
        logging.info("Got request for /")
        helpers.render_template(self, 'index.html', {})

class LoadMPHandler(RequestHandler):
    def post(self):
        id = self.request.get('id')
        api_url = self.request.get('api_url')
        json = helpers.load_from_json_endpoint(api_url)
        #Do Something with the returned information
        logging.info('Got information on MP %s from %s' % (json['person']['name'], api_url))

class LoadFeedHandler(RequestHandler):
    def get(self):
        json = helpers.load_from_json_endpoint('http://www.guardian.co.uk/politics/api/general-election/2010/results/json')
        for constituency in json['results']['called-constituencies']:
            mp_id = constituency['result']['winning-mp']['aristotle-id']
            api_url = constituency['result']['winning-mp']['json-url']
            helpers.add_task('feed', '/tasks/loadmp', {'id':mp_id, 'api_url':api_url})

def main():
    application = WSGIApplication([
        ('/', MainHandler),
        ('/feeds/import', LoadFeedHandler),
        ('/tasks/loadmp', LoadMPHandler),
    ],
    debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
