from pyramid.view import view_config, render_view
import brettsblog.resources
from brettsblog.blogdata import BlogData
from brettsblog.AdminUser import AdminUser
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from brettsblog.views.root import strip_tags
from pyramid.security import remember
from pyramid.security import forget
from pyramid.security import authenticated_userid
import datetime
import pymongo


@view_config(context='brettsblog:resources.Admin', name='', renderer='brettsblog:templates/admin.pt', permission='admin')
def admin(context, request):
    logged_in = authenticated_userid(request)
    url = request.path_info
    return {'cur_page': '', 'page_title': 'Admin', 'username': logged_in, 'url': url}


@view_config(context='pyramid.httpexceptions.HTTPForbidden', renderer='brettsblog:templates/login.pt')
@view_config(context='brettsblog:resources.Admin', name='login', renderer='brettsblog:templates/login.pt')
def login(context, request):
    url = ''
    if request.scheme == 'http':
        request.scheme = 'https'
        #return HTTPFound(location=request.url)
    return {'message': 'login', 'cur_page': '', 'page_title': 'Welcome to Brett\'s Blog', 'url': url}


@view_config(context='brettsblog:resources.Admin', name='login',  request_method='POST', renderer='brettsblog:templates/login.pt')
def login_post(context, request):
    referrer = '/my_admin'

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']

        admin_user = AdminUser(login, request)

        if admin_user.validate_user(password):
                headers = remember(request, login)
                return HTTPFound(location=referrer,  headers=headers)
        message = 'Failed login'
        return {'message': message,  'cur_page': '', 'page_title': 'Failed Login'}


@view_config(context='brettsblog:resources.Admin', name='logout', renderer='brettsblog:templates/admin.pt')
def logout(context, request):
    headers = forget(request)
    return HTTPFound(location='/my_admin/login',
                     headers=headers)


#handle all the CRUD actions on the backend
@view_config(context='brettsblog:resources.Admin',  renderer='json', xhr=True, permission='admin')
def new_post(context, request):

    post_data = dict()
    blog_data = BlogData(request)

    #This handles the New entry post
    if 'postBlog' in request.params:
        if request.params['action_type'] == 'add':
            for key, value in request.params.items():
                if key == 'tags':
                    value = value.split(', ')
                if key != 'postBlog' or key != 'action_type':
                    post_data[key] = value
            post_data['author'] = 'Brett Dangerfield'
            post_data['postDate'] = datetime.datetime.utcnow()

            #check to see if the post is active
            if 'active' in post_data.keys():
                post_data['active'] = True
            else:
                post_data['active'] = False

            #insert the post into mongo
            collection = request.db['blogPosts']
            try:
                collection.insert(post_data, safe=True)
                return {'success': True, 'message': 'Post Saved'}
            except pymongo.errors.DuplicateKeyError:
                return {'success': False, 'message': 'Duplicate URL'}

        #we are editing an existing post
        elif request.params['action_type'] == 'edit':
            for key, value in request.params.items():
                if key == 'tags':
                    value = value.split(', ')
                if key != 'postBlog' or key != 'action_type':
                    post_data[key] = value
            post_data['author'] = 'Brett Dangerfield'
            post_data['postDate'] = datetime.datetime.utcnow()

            #check to see if the post is active
            if 'active' in post_data.keys():
                post_data['active'] = True
            else:
                post_data['active'] = False

            #insert the post into mongo
            collection = request.db['blogPosts']
            try:
                collection.update({'url': post_data['url']}, post_data)
                return {'success': True, 'message': 'Post Saved'}
            except pymongo.errors.DuplicateKeyError:
                return {'success': False, 'message': 'Duplicate URL'}

    #now let's handle the list of entries
    elif 'listPosts' in request.params:
        posts = blog_data.get_all_posts(50, 1)

        entries = []
        for post in posts:
            postDate = post[u'postDate'].strftime("%B %d %Y")
            tags = post[u'tags'] if u'tags' in post else ''
            entry = {'title': post[u'title'],
                   'url': post[u'url'],
                   'date': postDate,
                    'category': post[u'category'],
                    'tags': tags,
                    'active': post[u'active']}
            entries.append(entry)
        return {'entries': entries}

    #get a single post for editing
    elif 'editPost' in request.params:
        post = blog_data.get_post_by_url(request.params['id'])
        return {'title': post[u'title'],
          'category': post[u'category'],
          'author': post[u'author'],
          'url': post[u'url'],
          'author': post[u'author'],
          'blog_body': post[u'postText'],
          'active': post[u'active'],
          'tags': post[u'tags']}


#handle all the CRUD actions on the backend for the pages editing
@view_config(context='brettsblog:resources.Admin', name='pages',  renderer='json', xhr=True, permission='admin')
def pages(context, request):
    print 'pages'
    blog_data = BlogData(request, 'page')

    #now let's handle the list of entries
    if 'listPages' in request.params:
        pages = blog_data.get_all_pages(50, 1)

        entries = []
        for page in pages:
            entry = {'title': page[u'title'],
                   'url': page[u'url'],
                   'order': page[u'order'],
                   'shortname': page[u'shortname'],
                    'active': page[u'active']}
            entries.append(entry)
        return {'entries': entries}


#handle all the CRUD actions on the backend
@view_config(context='brettsblog:resources.Admin',  name='delete', request_method='DELETE', renderer='json', xhr=True, permission='admin')
def delete_post(context, request):
    blog_data = BlogData(request)
    blog_data.delete_post(request.params['id'])
    return {'result': True}
