# ==============================================================
# Message Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since March 5, 2016
# ==============================================================
class Message:
    sender_number = None
    sender = None
    receiver = None
    message = None
    created_at = None
    deleted_at = None

    def __init__(self, data):
        self.sender_number = data['sender_number']
        self.sender = data['sender']
        self.receiver_number = data['receiver_number']
        self.message = data['message']
        self.created_at = data['created_at']
        self.deleted_at = data['deleted_at']

    def display_message(self):
        return "(%s) [%s] %s: %s" % self.created_at, self.sender, self.sender_number, self.created_at

# ==============================================================
# OutgoingMessage Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since March 5, 2016
# ==============================================================
class OutgoingMessage:
	id = None
	message = None
	recipient = None
	event_trigger = None
	sent_at = None
	created_at = None

	def __init__(self, data):
		self.id = data['id']
		self.message = data['message']
		self.recipient = data['recipient']
		self.event_trigger = data['event_trigger']
		self.sent_at = data['sent_at']
		self.created_at = data['created_at']
