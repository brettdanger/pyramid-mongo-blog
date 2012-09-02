class BlogData(object):
    def __init__(self, request, collection='posts'):
        self.settings = request.registry.settings
        if collection == 'posts':
            self.collection = request.db['blogPosts']
        elif collection == 'page':
            self.collection = request.db['blogPages']

    #get a list of  blog blogPosts
    def get_recent_posts(self, num_of_entries, page, titles_only=False):
        row = num_of_entries * (page - 1)
        entries = self.collection.find({'active': True}).sort('_id', -1)[row: row + num_of_entries]
        if titles_only:
            titles = []
            for entry in entries:
                this_entry = {'title': entry['title'], 'url': entry['url']}
                titles.append(this_entry)
            return titles
        else:
            return entries

    #get a single post by the url
    def get_post_by_url(self, url):
        post = self.collection.find_one({'url':  url})
        return post

    def get_recent_posts_by_category(self, category, num_of_entries, page):
        row = num_of_entries * (page - 1)
        entries = self.collection.find({'category': category, 'active': True}).sort('_id', -1)[row: row + num_of_entries]
        return entries

    #get a list of  blog ALL blogPosts without the bodyText
    def get_all_posts(self,  num_of_entries,  page):
        row = num_of_entries * (page - 1)
        entries = self.collection.find({}, {'bodyText': 0}).sort('_id', -1)[row: row + num_of_entries]
        return entries

    #get a list of  blog ALL blogPages without the bodyText
    def get_all_pages(self,  num_of_entries,  page):
        row = num_of_entries * (page - 1)
        entries = self.collection.find({}, {'body': 0}).sort('_id', -1)[row: row + num_of_entries]
        return entries

    #delete entries
    def delete_post(self, url):
        self.collection.remove({'url': url})

    #get the posts by tag
    def get_recent_posts_by_tag(self, category, num_of_entries, page):
        row = num_of_entries * (page - 1)
        entries = self.collection.find({'tags': category, 'active': True}).sort('_id', -1)[row: row + num_of_entries]
        return entries
