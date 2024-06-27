#!/usr/bin/python3

from .diaryclass import Diary
import argparse
import sys
import json
import os
from re import split
import textwrap
import datetime
import tempfile
from random import randint, seed
from time import strptime
import subprocess

indent = "  "
showRandomHint = False
defaultDatabase = "~/Dropbox/diary.db"

def diary():
    #print("len(sys.argv) = %d" % len(sys.argv))
    #print("sys.argv = %s" % sys.argv)
    parser = argparse.ArgumentParser(prog="diary", description="Diary: a diary tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("FIXME: explain more here"))
    parser.add_argument("--debug", action="store_true", help="turn on tracer information")
    parser.add_argument("--database", type=str, default=None,
                        help="database location (defaults to %s)" % defaultDatabase,
                        metavar="filename")
    parser.add_argument("-l", "--list", type=str, nargs="*", help="list entries", metavar="")
    parser.add_argument("words", type=str, nargs="*",
                        help="Entry words, perhaps followed by : and then tags")
    args = parser.parse_args()
    if ":" in args.words:
        start = args.words.index(":") + 1
        tags = args.words[start:len(args.words)]
        entry = ' '.join(map(str, args.words[0:start-1]))
    else:
        entry = ' '.join(map(str, args.words))
        tags = []
    if args.debug:
        print("  entry: %s" % entry)
        print("  tags:  %s" % tags)
        if args.database:
            print("user gave database '%s'" % args.database)
    if not args.database:
        args.database = defaultDatabase
    diary = Diary(debug=args.debug, db=args.database)
    if args.list:
        print(diary.list_all())
        exit(1)
    diary.add_entry(entry, tags)
