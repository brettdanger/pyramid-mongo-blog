from passlib.hash import sha256_crypt


class AdminUser(object):
    def __init__(self, username, request):
        self.settings = request.registry.settings
        self.collection = request.db['admin']
        self.__get_stored_hash(username)

    def __get_stored_hash(self, username):
        record = self.collection.find_one({'username':  username})
        if record is None:
            self.stored_hash = None
        else:
            self.stored_hash = record[u'password']

    def  validate_user(self, password):
        if self.stored_hash is not None:
            return sha256_crypt.verify(password, self.stored_hash)
        return False
