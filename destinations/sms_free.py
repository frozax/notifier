import os
import json
import urllib.request
import urllib.parse

URL = "https://smsapi.free-mobile.fr/sendmsg?user=%s&pass=%s&msg=%s"

class NotificationDestination:
    def send(self, text):
        params = json.load(open(os.path.expanduser("~/.free_notification_key")))
        encoded_text = urllib.parse.quote_plus(text)
        url = URL % (params["user"], params["pass"], encoded_text)
        print("URL=%s" % url)
        request = urllib.request.urlopen(url)
        if request.status != 200:
            print("ERROR SENDING SMS: %d" % request.status)
