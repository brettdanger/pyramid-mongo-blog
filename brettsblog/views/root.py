from pyramid.view import view_config
import brettsblog.resources
from brettsblog.blogdata import BlogData
from pyramid.httpexceptions import HTTPFound
import re


@view_config(context='brettsblog:resources.Root', renderer='brettsblog:templates/home_entry_list.pt')
@view_config(context='brettsblog:resources.Root', renderer='brettsblog:templates/home_entry_list.pt', name='home')
def my_view(request):
    #get mongoDB posts
    blog_data = BlogData(request)
    posts = blog_data.get_recent_posts(10, 1)

    entries = []
    for post in posts:
        postDate = post[u'postDate'].strftime("%B %d %Y")
        entry = {'title': post[u'title'],
               'url': post[u'url'],
               'date': postDate,
                        'author': post[u'author'],
                        'blog_body': strip_tags(post[u'postText'][:1000]) + '...',
                        'tags': post[u'tags']}
        entries.append(entry)
    return {'cur_page': 'home', 'page_title': 'Welcome to Brett\'s Blog', 'entries': entries}


@view_config(context='pyramid.httpexceptions.HTTPNotFound', renderer='brettsblog:templates/404_error.pt')
def not_found(request):
    return{'message': 'Error 404, Page Not Found',  'cur_page': '', 'page_title': 'Requested Page Not Found'}


def strip_tags(content):
    return re.sub('<[^<]*?>', '', content)
