#!/bin/env python3
"""
Create random pairs from a list of participants, e.g. for xmas 
"""

import sys
import re
import random
import smtplib, ssl
from getpass import getpass


# Make a regular expression for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
# configure Mailbackend
port = 587 #starttls
smtp_server = "smtp.example.com"
sender = "sender@example.com"

def main():
    args = sys.argv[1:]

    if not args:
        # e.g. python main.py a@example.com b@example.com c@example.com
        print('usage: [inputs] ')
        sys.exit(1)

    maillist = []
    pair = []
    for arg in args:
        if check(arg):
            arg = arg.strip().lower()
        else:
            print(arg + " is not a valid E-Mail. Only valid E-Mails are excepted as args.")
            sys.exit(1)
        if arg not in maillist:
            maillist.append(arg)
    password = getpass( 'Type your Mailserver password an press enter: ' )
    # Create a secure SSL context
    #context = ssl.create_default_context()
    context = ssl._create_unverified_context() # self-signed cert

    print("Used: E-Mails: " + ", ".join(maillist))
    print("Result:")
    for p in pairlist(maillist):
        sendmail(donor=p[0], donee=p[1], password=password, context=context, sender=sender)

def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def pairlist(shufflelist):
    # shuffle the list pop first, shuffle if necessary
    pairlist = []
    orderlist = shufflelist.copy()
    orderlist.sort()
    random.shuffle(shufflelist)
    for k in orderlist:
        while k == shufflelist[0]:
            random.shuffle(shufflelist)
        pairlist.append((k, shufflelist.pop(0)))
    return pairlist

def sendmail(donor, donee, password, context, sender):
    message = """Subject: Xmas Roulette
To: {recipient}
From : {sender}
Hi {name}, thanks for participating! you are selected to present {recipient} with something appropriate!"""
    sender = sender
    with smtplib.SMTP(smtp_server, port) as server:
        # Try to log in to server and send email
        try:
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender, password)
            # Send email here
            server.sendmail(sender, donor, message.format(name=donor, recipient=donee, sender=sender))
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit() 
        print(f'Sent to {donor}')


if __name__ == '__main__':
    main()
