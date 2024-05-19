import util
from androguard.misc import AnalyzeAPK
import os
import datetime
import subprocess

avd_manager_command = [
    'avdmanager',
    'create','avd',
    '--name','my_avd',
    '--package','system-images;android-29;google_apis;x86',
    '--abi','google-apix/x86',
    '--device','pixel',
    '--force'
]
subprocess.run(avd_manager_command)
