import urllib.request
import urllib.error
import json
import time
from datetime import datetime, timedelta
from subprocess import check_output, CalledProcessError

class NotificationSource:
    def __init__(self, args):
        self.args = args

    def get_text(self):
        try:
            ret = check_output(self.args, shell=True).decode()
        except CalledProcessError as e:
            ret = "CalledProcessError: %s" % (str(e))
            ret += "\nOutput:\n" + e.output.decode()
        return ret

