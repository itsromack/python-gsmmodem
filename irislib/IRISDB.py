import MySQLdb
import sys
import time
from collections import namedtuple
from Message import Message

class IRISDB:
	""" IRISDB Class """
	conn = False
	cur = False
	conf = False

	def __init__(self, **kwargs):
		self.conf = kwargs
		self.conf["keep_alive"] = kwargs.get("keep_alive", False)
		self.conf["charset"] = kwargs.get("charset", "utf8")
		self.conf["host"] = kwargs.get("host", "localhost")
		self.conf["port"] = kwargs.get("port", 3306)
		self.conf["autocommit"] = kwargs.get("autocommit", False)

		self.connect()

	def connect(self):
		"""Connect to the mysql server"""
		try:
			self.conn = MySQLdb.connect(db=self.conf['db'], host=self.conf['host'],
										port=self.conf['port'], user=self.conf['user'],
										passwd=self.conf['passwd'],
										charset=self.conf['charset'])
			self.cur = self.conn.cursor()
			print self.conn
			self.conn.autocommit(self.conf["autocommit"])
		except:
			print ("MySQL connection failed")
			raise

	def get_all_sms(self):
		sql = "SELECT * FROM sms_messages"
		self.cur.execute(sql)
		result = self.cur.fetchall()
		messages = None
		if result:
			row = namedtuple("Message", [f[0] for f in self.cur.description])
			messages = [row(*r) for r in result]
		return messages

	def get_all_recipients(self):
		sql = "SELECT * FROM report_recipients WHERE active = 1"
		self.cur.execute(sql)
		result = self.cur.fetchall()
		recipients = None
		# if result:]

	def get_message_by_id(self, message_id):
		sql = "SELECT * FROM sms_messages WHERE id = %i" % message_id
		self.cur.execute(sql)
		row = self.cur.fetchone()
		row = namedtuple("Message", [f[0] for f in self.cur.description])
		message = Message(row.sender, row.message, row.created_at)
		return message

	def get_message_by_sender(self, sender):
		sql = "SELECT * FROM sms_messages WHERE sender = '%s'" % sender
		self.cur.execute(sql)
		row = self.cur.fetchone()
		return row

	def save_message(self, message):
		sql = "INSERT INTO sms_messages SET sender = %s, message = %s, created_at = %s"
		self.cur.execute(sql, (message.sender, message.message, message.created_at))
		
	def sync_message(self, message_id):
		sql = "UPDATE sms_messages SET sync=1, sync_date='%s' WHERE id = %i" % (time.strftime("%Y-%m-%d %H:%M:%S"), message_id)
		self.cur.execute(sql)
