#!/usr/bin/env python3

import sys
import argparse
import importlib

def parse_args():
    parser = argparse.ArgumentParser(description="Sends notifications")
    parser.add_argument("--source", "-s", type=str, default="helloworld",
                        help="Data to send")
    parser.add_argument("--params", "-p", type=str, default="",
                        help="argument to source")
    parser.add_argument("--destination", "-d", type=str, default="stdout",
                       help="Where to send data")

    return parser.parse_args()

def _err(s):
    print("FATAL ERROR")
    print(s)
    sys.exit(1)

if __name__ == '__main__':
    args = parse_args()
    try:
        source_module = importlib.import_module("sources." + args.source)
        if args.params:
            source = source_module.NotificationSource(args.params)
        else:
            source = source_module.NotificationSource()
    except ImportError:
        _err("Could not import " + args.source)

    try:
        dest_module = importlib.import_module("destinations." + args.destination)
        dest = dest_module.NotificationDestination()
    except ImportError:
        _err("Could not import " + args.destination)

    try:
        source_data = source.get_text()
    except:
        source_data = "FATAL ERROR: Could not get data\n%s" % sys.exc_info()[0].__name__
        raise

    dest.send(source_data)
