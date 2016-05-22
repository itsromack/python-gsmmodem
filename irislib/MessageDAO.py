# ==============================================================
# Message Data Access Object
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since march 5, 2016
# ==============================================================
from datetime import date
import _mysql

class MessageDAO:
    db = False

    def __init__(self, db):
        self.db = db

    def save_message(self, message, sender, receiver):
        sql = 'INSERT INTO sms_messages SET ' \
              ' message = "%s", ' \
              ' sender = "%s", ' \
              ' receiver = "%s"' % (message, sender, receiver)
        self.db.cursor.execute(sql)
        return True

    def is_exists(self, message, sender):
        sql = 'SELECT id FROM sms_messages ' \
              'WHERE sender = "%s" AND message = "%s"' % (sender, message)
        self.db.cursor.execute(sql)
        row = self.db.cursor.fetchone()
        print sql
        print row
        if row != None:
            return True
        return False