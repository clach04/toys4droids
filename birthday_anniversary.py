#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Simple birthday (anniversary) math
"""

import os
import sys
import datetime


import android


# http://developer.android.com/reference/android/provider/ContactsContract.CommonDataKinds.Event.html

EVENT_START_DATE = 'data1'  # ContactsContract.CommonDataKinds.Event.START_DATE
EVENT_TYPE = 'data2' # ContactsContract.CommonDataKinds.Event.TYPE
EVENT_MIMETYPE = 'vnd.android.cursor.item/contact_event'  # ContactsContract.CommonDataKinds.Event.MIMETYPE

EVENT_TYPE_ANNIVERSARY = '1'  # Event.TYPE_ANNIVERSARY
EVENT_TYPE_BIRTHDAY = '3'  # Event.TYPE_BIRTHDAY
EVENT_TYPE_OTHER = '2'  # Event.TYPE_OTHER

EVENT_MAPPING = {
    EVENT_TYPE_ANNIVERSARY: 'ANNIVERSARY',
    EVENT_TYPE_BIRTHDAY: 'BIRTHDAY',
    EVENT_TYPE_OTHER: 'OTHER',
}


def replace_year_handle_leap_year(in_date, year):
    """Replace year of date, if end up with invalid date due to leap year
    make the date the first of March.
    """
    try:
        result = in_date.replace(year=year)
    except ValueError:
        # only check for Feb 29th
        if in_date.month == 2 and in_date.day == 29:
            result = datetime.date(year, 3, 1)
        else:
            raise
    return result


def upcoming_date(the_date, today=datetime.date.today()):
    current_year = today.year
    next_date = replace_year_handle_leap_year(the_date, current_year)
    if today > next_date:
        next_date = replace_year_handle_leap_year(the_date, current_year + 1)
    return next_date

def doit():
    dates = []
    droid = android.Android()
    contacts = droid.queryContent(
        'content://com.android.contacts/data',  # uri
        ['display_name', EVENT_START_DATE, EVENT_TYPE],  # attributes
        'mimetype = ?',  # selection (WHERE clause)
        [EVENT_MIMETYPE, ],  # selectionArgs (bind parameters)
        None  # order (ORDER BY)
        ).result
    today = datetime.date.today()
    for contact in contacts:
        person_name, event_date, event_type = contact['display_name'], contact[EVENT_START_DATE], contact[EVENT_TYPE]
        event_type = EVENT_MAPPING[event_type]
        event_date = datetime.date(*map(int, event_date.split('-')))
        next_date = upcoming_date(event_date, today=today)
        years = next_date.year - event_date.year

        details = (next_date, event_type, years, person_name)
        dates.append(details)
    dates.sort()

    for date in dates:
        print date


def main(argv=None):
    if argv is None:
        argv = sys.argv

    doit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
