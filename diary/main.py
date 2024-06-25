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
    parser = argparse.ArgumentParser(prog="diary", description="Diary: a diary tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("FIXME: explain more here"))
    parser.add_argument("action", type=str,
                        help="Action (either 'add' or 'show')")
    parser.add_argument("entry", type=str, help="Diary entry")
    parser.add_argument("categories", type=str, help="Category (use comma to separate)")
    parser.add_argument("--debug", type=int, default=0,
                        help="0 for quiet action, 1 for some debugging output",
                        metavar="level")
    parser.add_argument("--database", type=str, default=None,
                        help="database location (defaults to %s)" % defaultDatabase,
                        metavar="filename")
    args = parser.parse_args()
    if args.database:
        print("user gave database '%s'" % args.database)
    if not args.database:
        args.database = defaultDatabase
    #print("action '%s'" % args.action)
    if args.action == "add":
        #print("entry '%s'" % args.entry)
        #print("categories '%s'" % args.categories)
        diary = Diary(debug=args.debug, db=args.database)
        diary.add_entry(args.entry, args.categories)
    elif args.action == "show":
        print("FIXME: code for 'show'")
    else:
        print("action must be either 'add' or 'show', not '%s'" % args.action)
        exit(1)
