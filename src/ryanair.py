#!/usr/bin/env python

import getpass

from RyanairApi import RyanairApi


def main():
    try:
        print "Welcome!"

        username = raw_input("Please enter username: ")
        password = getpass.getpass("Please enter password:")

        ryanairApi = RyanairApi(username, password)
        ryanairApi.getAllSeats()
        exit(0)
    except KeyboardInterrupt:
        print "\nQuitting.."
        exit(0)
