#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""silent_interlude - automatically switch out of silent mode.
Ever switch n silent mode and forget to switch it back? This enters
silent mode for an hour, 2 hours, etc. and auto exits silent mode.
"""

import os
import sys
import time
import datetime

import android

droid = android.Android()


def sleep_for(num_secs):
    """Currently a simple os.sleep wrapper to sleep for num_secs.
    time.sleep() should suspend and be light on battery usage.
    Ideally use android WaitFor so changed to ring mode can be detected,
    assuming there is a ringer change event.
    Returns True if sleep was 100% complete.
    """
    time.sleep(num_secs)
    #droid.eventRegisterForBroadcast('silent_interlude.pigsfly')
    #droid.eventWaitFor('sleeptest_wait.pigsfly', num_secs * 1000)
    return True


def on_silentmode_start(num_secs):
    global droid
    #silent_mode_func(True)
    droid.toggleRingerSilentMode(True)
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=num_secs)
    end_time_str = end_time.strftime('%H:%M:%S (%Y-%m-%d )')
    droid.notify('Phone in silent mode', 'ringer will be enabled at %s' % end_time_str)
    droid.makeToast('silent mode engaged')


def on_silentmode_stop():
    global droid
    
    #silent_mode_func(False)
    droid.toggleRingerSilentMode(False)
    ## TODO consider using setMediaVolume()
    droid.makeToast('silent mode dis-engaged')


def doit():
    global droid
    
    # TODO Check checkRingerSilentMode() and getVibrateMode()
    
    # Get silence period
    ENTER_CUSTOM = 'Custom'
    mins_list = ['60', '90', '120', ENTER_CUSTOM]  # TODO optional config file
    
    droid.dialogCreateAlert('Silent mode time', 'select number of minutes')
    droid.dialogSetItems(mins_list)
    droid.dialogSetNegativeButtonText('Cancel')
    droid.dialogShow()
    response = droid.dialogGetResponse().result
    droid.dialogDismiss()
    button_pressed = response.get('which')
    if button_pressed:
        num_mins = None
    else:
        item = response.get('item')
        if item is None:
            num_mins = None
        num_mins = mins_list[item]
    if num_mins == ENTER_CUSTOM:
        # Enter in custom time
        droid.dialogCreateInput('Silent mode time', 'enter number of minutes', '', 'number')
        droid.dialogSetPositiveButtonText('OK')
        droid.dialogSetNegativeButtonText('Cancel')
        droid.dialogShow()
        result = droid.dialogGetResponse().result
        num_mins = None
        if result.get('which') == 'positive':
            try:
                num_mins = int(result['value'])
            except ValueError:
                pass
    elif num_mins:
        num_mins = int(num_mins)

    if num_mins:
        num_secs = 60 * num_mins
        # ensure python script works when screen is off
        droid.wakeLockAcquirePartial()
        on_silentmode_start(num_secs)
        sleep_for(num_secs)
        on_silentmode_stop()
        droid.wakeLockRelease() 


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    doit()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
