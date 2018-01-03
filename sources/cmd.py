import urllib.request
import urllib.error
import json
import time
from datetime import datetime, timedelta
from subprocess import check_output

class NotificationSource:
    def __init__(self, args):
        self.args = args

    def get_text(self):
        ret = check_output(self.args, shell=True)
        return ret.decode()

