#!/usr/bin/python3

from .diaryclass import Diary
import argparse
import sys
import json
import os
import re
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

    # If second arg is a number, it is a noteId
    id_desired = None
    print("len(sys.argv) = %d" % len(sys.argv))
    if len(sys.argv) > 1:
        try:
            id_desired = sys.argv[1]
            #del sys.argv[1]
        except:
            pass

    parser = argparse.ArgumentParser(prog="diary", description="Diary: a diary tool",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("FIXME: explain more here"))
    parser.add_argument("item", type=str, help="Diary item")
    parser.add_argument("categories", type=str, help="Category (use comma to separate)")
    parser.add_argument("--debug", type=int, default=0,
                        help="0 for quite action, 1 for information",
                        metavar="de")
    parser.add_argument("--database", type=str, default=None,
                        help="database location; defaults to %s" % defaultDatabase,
                        metavar="db")
    args = parser.parse_args()
    if not args.database:
        args.database = defaultDatabase
    print(args.item)
    print(args.categories)
    diary = Diary(debug=args.debug, db=args.database)
