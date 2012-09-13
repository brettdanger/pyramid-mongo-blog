from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest
from pyramid.events import BeforeRender
import pymongo
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from brettsblog.blogdata import BlogData

from pyramid_beaker import session_factory_from_settings
import logging
from brettsblog.resources import Root


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """

    session_factory = session_factory_from_settings(settings)

    authn_policy = AuthTktAuthenticationPolicy('A@uth3ntic@t3')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=Root,  authentication_policy=authn_policy,  authorization_policy=authz_policy,  session_factory=session_factory)
    config.add_static_view('static', 'brettsblog:static')

    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db

    #create globals for data accross all events
    def inject_renderer_globals(event):

        request = event['request']
        #set the static site info
        settings = request.registry.settings

        #get the recent entries
        blog_data = BlogData(request)
        recent_titles = blog_data.get_recent_posts(10, 1, True)
        event['recent_titles'] = recent_titles
        # Build static info from the configuration file
        event['static_info'] = {'blog_title': settings['site_name'], 'site_motto': settings['site_tag_line']}
        event['google_analytics'] = request.registry.settings['google_analytics']

    db_uri = settings['mongodb.url']
    MongoDB = pymongo.Connection
    if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.Connection):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)
    conn = MongoDB(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)
    config.add_subscriber(inject_renderer_globals, BeforeRender)
    config.include('pyramid_jinja2')
    config.scan('brettsblog')
    return config.make_wsgi_app()
