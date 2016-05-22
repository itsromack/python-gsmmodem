# ==============================================================
# Issue Data Access Object
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since February 27, 2016
# ==============================================================
from Category import Category
import _mysql

class CategoryDAO:
    db = False

    def __init__(self, db):
        self.db = db

    def all(self):
        sql = 'SELECT * FROM categories WHERE active = 1'
        self.db.cursor.execute(sql)
        result = self.db.cursor.fetchall()
        categories = []
        for row in result:
            category = Category(row)
            categories.append(category)
        return categories

    # expects a Category object
    def create(self, categoryObject=None):
        if categoryObject != None:
            sql = 'INSERT INTO categories ' \
                  'SET name = "%s"' % _mysql.escape_string(categoryObject.name)
            self.db.cursor.execute(sql)
            return True
        return False

    def update(self, categoryObject=None):
        if categoryObject != None:
            sql = 'UPDATE categories SET ' \
                  ' name = "%s", ' \
                  'WHERE id = %d' % (
                _mysql.escape_string(categoryObject.name),
                int(categoryObject['id'])
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def activate(self, categoryObject=None):
        if categoryObject != None:
            sql = 'UPDATE categories SET ' \
                  ' active = %d, ' \
                  'WHERE id = %d' % (
                1,
                int(categoryObject['id'])
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def deactivate(self, categoryObject=None):
        if categoryObject != None:
            sql = 'UPDATE categories SET ' \
                  ' active = %d, ' \
                  'WHERE id = %d' % (
                0,
                int(categoryObject['id'])
            )
            self.db.cursor.execute(sql)
            return True
        return False

    def get_by_id(self, id):
        sql = 'SELECT * FROM categories WHERE id = %d' % id
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return Category(row)
        return False

    def get_by_category_name(self, category_name):
        sql = 'SELECT i.* FROM categories ' \
              'WHERE name = "%s" AND active = 1' % category_name
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        if row:
            return Category(row)
        return False
