#!/usr/bin/env python

import requests
import json
import seats
import utils
import logging


class RyanairApi(object):
    logging.basicConfig(filename='/dev/null', level=logging.NOTSET)

    basicApiUrl = 'https://api.ryanair.com/'
    bookingApiUrl = 'https://nativeapps.ryanair.com/'

    customerId = ""
    authToken = ""
    sessionToken = ""

    def __init__(self, username, password):
        """Get the auth token and the customer ID"""
        url = 'userprofile/rest/api/v1/login'
        headers = utils.getHeaders()
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Lenght': '53'
            })
        params = {
            'password': password,
            'username': username
        }
        response = requests.post(
            self.basicApiUrl + url,
            headers=headers,
            params=params)

        if response.status_code != 200:
            logging.error('Impossible to login')
            print('Login error.')
            exit(1)
        data = response.json()

        self.customerId = data['customerId']
        self.authToken = data['token']
        logging.debug('User logged in')

    def getProfile(self):
        """Return user profile, printing a description"""
        url = 'userprofile/rest/api/v1/secure/users/' + \
            self.customerId + \
            '/profile/full'
        headers = utils.getHeaders()
        headers.update({
            'X-Auth-Token': self.authToken
        })
        response = requests.get(
            self.basicApiUrl + url,
            headers=headers)
        if response.status_code != 200:
            logging.error('Impossible to fetch profile')
            print('Impossible to fetch profile!')
            exit(1)
        user = response.json()
        print 'So....'
        print 'You\'re ' + user['firstName'] + ' ' + user['lastName']
        print 'Your nationality is ' + user['nationality']
        print 'Phone = ' + user['countryCallingCode'] + user['phoneNumber']
        print '--------------------------'
        return user

    def getUpcomingBookings(self):
        """Get the list of all upcoming bookings"""
        url = 'userprofile/rest/api/v1/secure/users/' + \
            self.customerId + \
            '/bookings/upcoming/all'
        headers = utils.getHeaders()
        headers.update({
            'X-Auth-Token': self.authToken
        })
        response = requests.get(self.basicApiUrl + url, headers=headers)
        if response.status_code != 200:
            logging.error('Impossible to fetch upcoming bookings')
            print('Impossible to fetch upcoming bookings!')
            exit(1)
        return response.json()

    def getAllSeats(self):
        bookings = self.getUpcomingBookings()
        print 'You have %s travel booked!' % bookings['count']
        # Display every booking
        for travel in bookings['Bookings']:
            self.infoBooking(travel['BookingId'])
        return

    def infoBooking(self, bookingId):
        """ Get and display information about one booking:
        - Print informations about the flights on the booking
        - Print informations about the passengers of the flights
        - Print a guess of the seat it will be allocated to the passengers
        """
        url = 'v4/Booking'
        headers = utils.getHeaders()
        headers.update({
            'Content-Type': 'application/json',
            'Content-Length': '52',
            'X-Auth-Token': self.authToken
        })
        data = {
            'surrogateId': self.customerId,
            'bookingId': bookingId
        }
        response = requests.post(
            self.bookingApiUrl + url,
            headers=headers,
            data=json.dumps(data))

        if response.status_code != 200:
            logging.error('Impossible to fetch bookings')
            print('Impossible to fetch bookings!')
            exit(1)
        result = response.json()

        # Save the received sessionToken
        self.sessionToken = response.headers['X-Session-Token']
        # Get informations about seats for this booking
        seatsList = self.infoSeats()
        if seatsList is False:
            logging.error('Impossible to fetch seats')
            print('Impossible to fetch seats!')
            exit(1)

        # Flight info
        print 'Prenotation number: %s (Status of the flight: %s)' % (
            utils.bclr.OKBLUE + result['info']['pnr'] + utils.bclr.ENDC,
            utils.bclr.OKGREEN + result['info']['status'] + utils.bclr.ENDC)
        numberofSeats = len(result['passengers'])
        print 'Number of passengers: %s' % numberofSeats
        c = 0
        # Print information about passengers
        for passenger in result['passengers']:
            c += 1
            print '  %i: %s %s' % (
                c,
                utils.bclr.HEADER + passenger['name']['first'],
                passenger['name']['last'] + utils.bclr.ENDC)
        c = 0
        for journey in result['journeys']:

            print '   [%s] %s -> %s (%s)' % (
                utils.bclr.OKBLUE + journey['flt'] + utils.bclr.ENDC,
                utils.bclr.WARNING + journey['orig'] + utils.bclr.ENDC,
                utils.bclr.WARNING + journey['dest'] + utils.bclr.ENDC,
                utils.parseDate(journey['depart']))

            if 'reasonCode' in journey['changeInfo'] and \
               journey['changeInfo']['reasonCode'] == 'PassengerCheckedIn':
                print '   Already checked-in'
            else:
                allocation = self.getSeat(
                    seatsList[c]['unavailableSeats'],
                    numberofSeats)
                if (allocation['status'] == 'error'):
                    print allocation['message']
                else:
                    print '   If you do check-in now, you will have \
seat %s %s' % (
                        utils.bclr.OKGREEN +
                        allocation['seat'] +
                        utils.bclr.ENDC,
                        seats.seatInfo(allocation['seat']))
            c += 1
        return

    def infoSeats(self):
        """ Show informations about seats for the booking
        - Return also the list of unavailable (already allocated) seats
        """
        url = 'v4/Seat'
        headers = utils.getHeaders()
        headers.update({
            'X-Session-Token': self.sessionToken
        })
        response = requests.get(self.bookingApiUrl + url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return False

    def getSeat(self, unavailable, numberofSeats):
        """ Return the seat that will be allocated during check-in"""
        response = dict()
        if utils.MAXPASSENGERS > numberofSeats:
            response['status'] = 'error'
            response['message'] = '   We are sorry but we currently \
don\'t support seat prediction for flights \
with %s passengers.' % numberofSeats
        else:
            response['status'] = 'ok'
            response['seat'] = seats.getFirstFree(unavailable)

        return response
