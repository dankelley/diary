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
    parser.add_argument("--list", action="store_true", help="list entries")
    parser.add_argument("words", type=str, nargs="*",
                        help="Entry, optionally with tags following ':'")
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
    if not args.database:
        args.database = defaultDatabase
    diary = Diary(debug=args.debug, db=args.database)
    if args.debug:
        print("  database: '%s'" % args.database)
    if args.list:
        if args.words:
            print("FIXME: --list needs to handle words and tags.  FYI, words are:")
            print(args.words)
            start = args.words.index(":") + 1
            tags = args.words[start:len(args.words)]
            entry = ' '.join(map(str, args.words[0:start-1]))
            print("entry:")
            print(entry)
            print("tags:")
            print(tags)
        tags = diary.get_table("tags")
        entries = diary.get_table("entries")
        entry_tags = diary.get_table("entry_tag")
        if args.debug:
            print("tags: ", end="")
            print(tags)
            print("entries: ", end="")
            print(entries)
            print("entry_tags: ", end="")
            print(entry_tags)
        taglist = {}
        for tag in tags:
            taglist[tag[0]] = tag[1]
        for entry in entries:
            entryId = entry[0]
            tags = []
            for entry_tag in entry_tags:
                if entry_tag[1] == entryId:
                    tags.append(taglist[entry_tag[2]])
            print("%s %s" % (entry[1], entry[2]), end = "")
            if tags:
                print(" : ", end="")
                for tag in tags:
                    print(tag, end=" ")
            print()
    else:
        diary.add_entry(entry, tags)
