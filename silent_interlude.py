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

import android

droid = android.Android()
silent_mode_func = droid.toggleRingerSilentMode  # NOTE NOT a vibrate mode
#silent_mode_func = droid.toggleVibrateMode  # NOTE Doesn't work 


def sleep_for(num_secs):
    """Currently a simple os.sleep wrapper to sleep for num_secs.
    time.sleep() should suspend and be light on battery usage.
    Ideally using android WaitFor so changed to ring mode can be detected
    Returns True if sleep was 100% complete.
    """
    time.sleep(num_secs)
    return True


def on_silentmode_start():
    global droid
    #silent_mode_func(True)
    droid.toggleRingerSilentMode(True)
    # toggleVibrateMode() fails with java.lang.NullPointerException if ringer (2nd) param is missing
    #droid.toggleVibrateMode(True, True)
    droid.makeToast('silent mode engaged')
    # TODO add notification with ETA for silent mode end time


def on_silentmode_stop():
    global droid
    
    #silent_mode_func(False)
    droid.toggleRingerSilentMode(False)
    #droid.toggleVibrateMode(False, True)
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
        num_secs = 10
        on_silentmode_start()
        sleep_for(num_secs)
        on_silentmode_stop()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    doit()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
