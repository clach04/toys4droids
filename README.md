Small utilities for Android written in [Python (py4a)](http://code.google.com/p/python-for-android/). If you are looking for a download some self assembly is required, SL4A and Python needs to be installed first.

Some tools are Android specific and require [SL4A (aka android scripting)](http://code.google.com/p/android-scripting/), others are generic and not limited to the Android platform. All known to work under Gingerbread 2.3 (Froyo and earlier will likely work but is untested).

  * [easy\_webserver.py](https://bitbucket.org/clach04/toys4droids/src/tip/easy_webserver.py) - portable web server, if easydialogs is available prompts for directory to serve. By default shares external SD card (/mnt/sdcard) under Android. For more information about easydialogs see [easydialogs-empty](http://code.google.com/p/easydialogs-empty/).

  * [silent\_interlude.py](https://bitbucket.org/clach04/toys4droids/src/tip//silent_interlude.py) - Android specific, ever switch into silent mode and forget to re-enable the ringer? Set how long to be silent and the phone auto switches out at the end. Note more of a demo, https://play.google.com/store/apps/details?id=com.publicobject.shush is far more practical.

  * [birthday\_anniversary.py](https://bitbucket.org/clach04/toys4droids/src/tip//birthday_anniversary.py) - Android specific, show upcoming birthday and anniversary dates. (As of July 2014) the SL4A Contacts API is very limited (for example, no access to Birthday information). The Android Contact store is simply a (sqlite3) database and the api to access Contact reflects this. However all the Android documentation make use of constants and the values for those constants are not obvious, thus includes a few bare-minimum constants for getting dates out of the contact store. NOTE this can be ran remotely against sl4a by setting environment variables AP\_HOST and AP\_PORT to point to Android device that is already running an SL4A server

  * [remote\_clipboard.py](https://bitbucket.org/clach04/toys4droids/src/tip//remote_clipboard.py) - portable mini web app that allows the clipboard to be reviewed and updated.
      * relies on xerox
          * Windows requires fix https://github.com/clach04/xerox/tree/win_no_crash
          * Linux requires `xclip` binary - `sudo apt install xclip`
      * optional QR Code generation for console/terminal, install one of:
          * https://github.com/pyqrcode/pyqrcodeNG
          * https://github.com/heuer/segno
