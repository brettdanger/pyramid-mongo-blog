from pyramid.view import view_config, render_view
import brettsblog.resources
from brettsblog.blogdata import BlogData
from pyramid.httpexceptions import HTTPNotFound
from brettsblog.views.root import strip_tags


@view_config(context='brettsblog:resources.Post',  renderer='post.jinja2')
@view_config(context='brettsblog:resources.PostName', name='', renderer='post.jinja2')
def post(context, request):
    #get mongoDB posts
    blog_data = BlogData(request)
    post = blog_data.get_post_by_url(context.__name__)

    if post is None:
        raise HTTPNotFound('notfound').exception
    postDate = post[u'postDate'].strftime("%B %d %Y")
    return {'cur_page': '',
          'page_title': post[u'title'],
          'title': post[u'title'],
          'category': post[u'category'],
          'author': post[u'author'],
          'url': post[u'url'],
          'date': postDate,
          'blog_body': post[u'postText'],
          'tags': post[u'tags']}


@view_config(context='brettsblog:resources.PageName',  renderer='page.jinja2')
def page(context, request):
     #get mongoDB posts
    blog_data = BlogData(request, 'page')
    page = blog_data.get_post_by_url(context.__name__)
    if page is None:
        raise HTTPNotFound('notfound').exception
    return {'cur_page': page[u'shortname'],
          'page_title': page[u'title'],
          'url': page[u'url'],
          'body': page[u'body']
          }


@view_config(context='brettsblog:resources.Category',  renderer='home.jinja2')
@view_config(context='brettsblog:resources.CategoryName',  name='', renderer='home.jinja2')
def category_view(context, request):
     #get mongoDB posts
    blog_data = BlogData(request)
    posts = blog_data.get_recent_posts_by_category(context.__name__, 10, 1)

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
    if not entries:
        raise HTTPNotFound('notfound').exception
    return {'cur_page': 'home', 'page_title': 'Category: ' + context.__name__, 'entries': entries}


@view_config(context='brettsblog:resources.Tag',  renderer='home.jinja2')
@view_config(context='brettsblog:resources.TagName',  name='', renderer='home.jinja2')
def tag_view(context, request):
    #get mongoDB posts
    blog_data = BlogData(request)
    posts = blog_data.get_recent_posts_by_tag(context.__name__, 10, 1)

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
    if not entries:
        raise HTTPNotFound('notfound').exception
    return {'cur_page': 'home', 'page_title': 'Category: ' + context.__name__, 'entries': entries}
