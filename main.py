#!/bin/env python3
"""
Create random pairs from a list of participants, e.g. for xmas 
"""

import sys
import re
import random

# Make a regular expression for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

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
    print("Used: E-Mails: " + ", ".join(maillist))
    print("Result:")
    for p in pairlist(maillist):
        print(p[0] + " beschenkt " + p[1])

 
# Define a function for for validating an Email
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


if __name__ == '__main__':
    main()
