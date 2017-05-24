# Headers
CLIENT_VERSION = '3.27.1'
CLIENT_OS = 'ios'
CLIENT_V_OS = '10.1.1'
USER_AGENT = 'RyanairApp/3.27.1 (iPhone; iOS 10.1.1; Scale/2.00)'

# Max passengers supported at the moment
MAXPASSENGERS = 1


def getHeaders():
    """ Basic headers to set-up a request"""
    headers = {
        'Accept': '*/*',
        'Connection': 'close',
        'client-version': CLIENT_VERSION,
        'client': CLIENT_OS,
        'Accept-Language': 'en-GB;q=1',
        'User-Agent': USER_AGENT,
        'client-os': CLIENT_V_OS
    }
    return headers


class bclr:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parseDate(string):
    """Parse that string."""
    # TODO: Give some format based on timezone, please :D
    date = string.split('T')[0]
    time = string.split('T')[1]
    datef = date.split('-')
    datep = datef[2] + '/' + datef[1] + '/' + datef[0]
    timef = time.split(':')
    timep = timef[0] + ':' + timef[1]
    return bclr.WARNING + \
        datep + bclr.ENDC + ' - ' + bclr.WARNING + timep + bclr.ENDC
