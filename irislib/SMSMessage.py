# ==============================================================
# Message Class
# IRIS Framework
#
# @author Romack L. Natividad <romacknatividad@gmail.com>
# @since May 13, 2016
# ==============================================================
class SMSMessage:
    sender = None
    receiver = None
    message = None
    created_at = None

    def __init__(self, data):
        self.sender = data['sender']
        self.receiver = data['receiver']
        self.message = data['message']
        self.created_at = data['created_at']

    def display_message(self):
        return "(%s) [%s] %s: %s" % self.sender, self.reciver, self.message, self.created_at
