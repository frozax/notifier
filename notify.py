#!/usr/bin/env python3

import time
from datetime import datetime
import sys
import argparse
import importlib

def parse_args():
    parser = argparse.ArgumentParser(description="Sends notifications\nExample: ./notify --source helloworld \"cmd echo toto\" helloworld")
    parser.add_argument("--source", "-s", nargs="*", default="helloworld",
                        help="Data to send")
    parser.add_argument("--destination", "-d", type=str, default="stdout",
                       help="Where to send data")
    parser.add_argument("--cron", type=str, default="",
                        help="Notifier will be called every day at the time given (e.g: 1500)")

    return parser.parse_args()

def _err(s):
    print("FATAL ERROR")
    print(s)
    sys.exit(1)


def call(sources, dest):
    source_data = ""
    try:
        for source in sources:
            source_data += source.get_text() + "\n"
    except:
        source_data = "FATAL ERROR: Could not get data\n%s\n%s" % (sys.exc_info()[0].__name__,
                                                                   sys.exc_info()[1])

    dest.send(source_data)

if __name__ == '__main__':
    args = parse_args()
    sources = []
    try:
        for source in args.source:
            source_split = source.split()
            source_cmd, source_param = source_split[0], ' '.join(source_split[1:])
            source_module = importlib.import_module("sources." + source_cmd)
            if source_param:
                sources.append(source_module.NotificationSource(source_param))
            else:
                sources.append(source_module.NotificationSource())
    except ImportError:
        _err("Could not import " + args.source)

    try:
        dest_module = importlib.import_module("destinations." + args.destination)
        dest = dest_module.NotificationDestination()
    except ImportError:
        _err("Could not import " + args.destination)

    if args.cron:
        cur_time = datetime.time(datetime.now())
        cur_time_min = cur_time.minute + cur_time.hour * 60
        wished_time_min = int(args.cron[:2]) * 60 + int(args.cron[2:])
        initial_sleep = wished_time_min - cur_time_min
        day_min = 24 * 60
        if initial_sleep < 0:
            initial_sleep += day_min
        print("Initial sleep %d minutes" % initial_sleep)
        time.sleep(initial_sleep * 60)
        while True:
            call(sources, dest)
            print("Sleep %d seconds" % (day_min * 60))
            time.sleep(day_min * 60)
    else:
        call(sources, dest)
