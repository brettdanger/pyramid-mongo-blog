from pyramid.security import Authenticated
from pyramid.security import Allow


class Root(object):
    __name__ = ''
    __parent__ = None

    def __init__(self, request):
        pass

    def __getitem__(self, key):
        if key == 'post':
            return Post()
        elif key == 'category':
            return Category()
        elif key == 'my_admin':
            return Admin()
        elif key == 'page':
            return Page()
        elif key == 'tag':
            return Tag()
        raise KeyError


class Post(object):
    __name__ = ''
    __parent__ = Root

    def __init__(self):
        pass

    def __getitem__(self, key):
        if key:
            return PostName(key)
        raise KeyError


class PostName(object):
    def __init__(self, number):
        self.__name__ = number


class Category(object):
    __name__ = ''
    __parent__ = Root

    def __init__(self):
        pass

    def __getitem__(self, key):
        if key:
            return CategoryName(key)
        raise KeyError


class Page(object):
    __name__ = ''
    __parent__ = Root

    def __init__(self):
        pass

    def __getitem__(self, key):
        if key:
            return PageName(key)
        raise KeyError


class Tag(object):
    __name__ = ''
    __parent__ = Root

    def __init__(self):
        pass

    def __getitem__(self, key):
        if key:
            return TagName(key)
        raise KeyError


class CategoryName(object):
    def __init__(self, number):
        self.__name__ = number


class PageName(object):
    def __init__(self, number):
        self.__name__ = number


class TagName(object):
    def __init__(self, number):
        self.__name__ = number


class Admin(object):
    __name__ = ''
    __parent__ = Root
    __acl__ = [
        (Allow, Authenticated, 'admin')
    ]

    def __init__(self):
        pass
