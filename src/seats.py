# Seats are allocated with this order..
rows = [
    '33',
    '20',
    '19',
    '22',
    '15',
    '24',
    '12',
    '26',
    '10',
    '28',
    '08',
    '30',
    '18',
    '21',
    '14',
    '23',
    '11',
    '25',
    '09',
    '27',
    '29',
    '07',
    '06',
    '05',
    '04',
    '03',
    '02',
    '01',
    '17',
    '16',
    '31',
    '32'
]

# ...from A to F
order = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
]

# First row only has 3 seats
nonexistent = [
    '01D',
    '01E',
    '01F',
]

# Larger seats
morespace = [
    '01A',
    '01B',
    '01C',
    '02D',
    '02E',
    '02F',
]


def getFirstFree(unavailable):
    """ Return the seat that will be allocated next
    according to the seats already allocated (unavailable). """

    # FIXME: The row are separated in two groups (ABC + DEF)
    # If the first group is empty but the second is not, the single place
    # is allocated on the second group, instead of on the first.

    for row in rows:
        for place in order:
            seat = str(row) + place
            if seat not in unavailable and seat not in nonexistent:
                return seat
    return 'N/D'


def seatInfo(seat):
    """Give some informations about a seat."""

    info = ''
    if 'A' in seat:
        info += 'Close to the left window'
    if 'F' in seat:
        info += 'Close to the right window'
    if 'C' in seat or 'D' in seat:
        info += 'Middle seat'
    if seat in morespace:
        if info == '':
            info += 'More space for legs'
        else:
            info += ' and more space for legs'
    if '16' in seat or '17' in seat:
        if info == '':
            info += 'More space for legs, emergency exit in the middle'
        else:
            info += ' and more space for legs, emergency exit in the middle'
    if info != '':
        return '(' + info + ')'
    return info
