#!/usr/bin/env python
from __future__ import print_function

from gsmmodem.modem import GsmModem
from gsmmodem.exceptions import InterruptedException
from gsmmodem.exceptions import TimeoutException
from irislib import DB, MessageDAO, Message
from collections import namedtuple
from time import strftime
import time
import logging
import sys


#PORT = '/dev/ttyUSB2'
PORT = '/dev/tty.usbserial-1421A'
# PORT = '/dev/tty.usbserial'
BAUDRATE = 115200
PIN = None # SIM card PIN (if any) 
GSM_NUMBER = "09208255700"

# REPLY_TO_SENDER_MESSAGE = 'Thank you for sending an incident report. We will respond immediately, please standby. ~ I.R.I.S. Framework\n\n This SIM card is currently in integration testing mode\n\nPlease visit http://iris-framework.com'
REPLY_TO_SENDER_MESSAGE = 'Thank you, we have received your incident report. We will respond immediately, please standby.\nIRIS Framework\nhttp://iris-framework.com'
db = DB(
    host="localhost",
    db="iris_tmbb",
    user="root",
    passwd="secret",
    autocommit=True
)
messageDao = MessageDAO(db)

def handleSms(sms):
    print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    print('Replying to SMS...')
    if messageDao.is_exists(sms.text, sms.number):
        print('Message already exists')
    else:
        messageDao.save_message(sms.text, sms.number, GSM_NUMBER)
    sms.reply(u'Thank you, we have received your incident report. We will respond immediately, please standby.\nIRIS Framework\nhttp://iris-framework.com')
    print('SMS sent.\n')

modem = GsmModem(PORT, BAUDRATE, smsReceivedCallbackFunc=handleSms)

def main():
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem.smsTextMode = False 
    modem.connect(PIN)
    print('Waiting for SMS message... OR incoming calls...')
    try:    
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close()

if __name__ == '__main__':
    main()

