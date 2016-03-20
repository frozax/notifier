import urllib.request
import urllib.error
import json
import time
from datetime import datetime, timedelta

PATH_TO_LATEST_BUILD = "http://localhost:8010/json/builders/%s/builds/-1?as_text=0"

class NotificationSource:
    def get_text(self):
        try:
            data = urllib.request.urlopen(PATH_TO_LATEST_BUILD % "backup").read()
        except urllib.error.URLError:
            return "FATAL: Buildbot NOT running"

        j = json.loads(data.decode('utf8'))
        build_number = j["number"]
        end_date = datetime.fromtimestamp(j["times"][1])
        diff_date = datetime.fromtimestamp(time.time()) - end_date
        too_long = diff_date > timedelta(hours=24)

        steps = j["steps"]
        success = 0
        skipped = 0
        failed = []
        for step in steps:
            name = step["text"][0]
            res = step["results"][0]
            if res == 0:
                success += 1
            elif res == 3:
                skipped += 1
            else:
                failed.append(name)

        if too_long:
            res = "ATTENTION: Dernier backup de + de 24h"
        else:
            res = ""
        res = "Dernier backup le %s\n" % (end_date.strftime("%d %b à %H:%M"))
        if len(failed) > 0:
            res += "%d ECHEC: %s" % (len(failed), ",".join(failed))
        res += "\n"
        res += "succes: %d, ignorés: %d" % (success, skipped)

        return res
