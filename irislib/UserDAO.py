# ==============================================================
# User Data Access Object
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
from User import User
from datetime import date
import _mysql
import hashlib

class UserDAO:
    db = False

    def __init__(self, db):
        self.db = db

    def result_to_users(self, result):
        users = []
        for row in result:
            user = User(row)
            users.append(user)
        return users

    # expects a User object
    def create(self, userObject=None):
        if userObject != None:
            sql = 'INSERT INTO users ' \
                  'SET level = "%s", ' \
                  ' full_name = "%s", ' \
                  ' login = "%s", ' \
                  ' password = "%s", ' \
                  ' contact_number = "%s"' % (
                _mysql.escape_string(userObject.level),
                _mysql.escape_string(userObject.full_name),
                _mysql.escape_string(userObject.login),
                _mysql.escape_string(hashlib.sha224(userObject.password).hexdigest()),
                _mysql.escape_string(userObject.contact_number)
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def update(self, userObject=None):
        if userObject != None:
            now = date.today()
            userObject['updated_at'] = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE users ' \
                  ' SET level = "%s", ' \
                  ' full_name = "%s", ' \
                  ' login = "%s", ' \
                  ' password = "%s", ' \
                  ' updated_at = "%s" ' \
                  'WHERE id = %d' % (
                userObject['level'],
                userObject['full_name'],
                userObject['login'],
                userObject['password'],
                userObject['updated_at'],
                userObject['id']
            )
            return True
        return False

    def delete(self, user_id=None):
        if user_id != None:
            now = date.today()
            updated_at = now.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'UPDATE users ' \
                  'SET deleted_at = "%s" ' \
                  'WHERE id = %d' % (updated_at, user_id)
            self.db.cursor.execute(sql)
            return True
        return False

    def all(self):
        sql = 'SELECT * FROM users WHERE deleted_at IS NULL'
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        users = []
        for row in result:
            user = User(row)
            users.append(user)
        return users

    def get_by_id(self, id):
        sql = 'SELECT * FROM users WHERE id = %d AND deleted_at IS NULL' % id
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return User(row)
        return False

    def get_by_full_name(self, full_name):
        sql = 'SELECT * FROM users WHERE full_name = "%s" AND deleted_at IS NULL LIMIT 1' % full_name
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        row = self.db.cursor.fetchone()
        if row:
            return User(row)
        return False

    def get_by_login(self, login):
        sql = 'SELECT * FROM users WHERE login = "%s" AND deleted_at IS NULL LIMIT 1' % login
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return User(row)
        return False

    def login(self, username, password):
        sql = 'SELECT * FROM users WHERE login = "%s" AND password = "%s" AND deleted_at IS NULL' % (username, password)
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return True
        return False