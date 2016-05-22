import smtplib

GMAIL_HOST = 'smtp.gmail.com:587'

class GMailer:
    smtp = None
    is_logged_in = False

    def __init__(self, username, password):
        self.smtp = smtplib.SMTP(GMAIL_HOST)
        if self.smtp.login(username, password):
            self.is_logged_in = True
            self.smtp.starttls()

    def send_message(self, sender, recipient, message):
        if self.is_logged_in:
            self.smtp.sendmail(sender, recipient, message)
            self.smtp.quit()
        else:
            print "Unable to connect to GMail SMTP"
            return False
