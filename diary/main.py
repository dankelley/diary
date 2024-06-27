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
        tags = diary.get_table("tags")
        print("tags: ", end="")
        print(tags)
        print("entries: ", end="")
        entries = diary.get_table("entries")
        print(entries)
        print("entry_tags: ", end="")
        entry_tags = diary.get_table("entry_tag")
        print(entry_tags)
        taglist = {}
        for tag in tags:
            taglist[tag[0]] = tag[1]
        #print(taglist)
        for entry in entries:
            #print(entry)
            entryId = entry[0]
            #print("  entryId %d" % entryId)
            #print(tags[0])
            #print("  ", tags[0][0])
            #print("  ", tags[0][1])
            tags = []
            for entry_tag in entry_tags:
                if entry_tag[1] == entryId:
                    tags.append(taglist[entry_tag[2]])
                    #matchingtag = next((x[2] for x in entry_tags if x[1] == entryId), 0)
                    #print("matchingtag follows")
                    #print(matchingtag)
                    #tagId = entry_tag[2]
                    #print("  tagId=%d" % tagId)
                    ##print("  %s" % tags[tagId][1])
                    #print("  %s" % tags[tagId][1])
            print(entry, end = "")
            print(tags)
        exit(3)
        rows = diary.list_all()
        print("FIXME: --list")
        tags = []
        for row in rows:
            if row[0] == idLast:
                tags.append(tag)
            else:
                print("  tags: ", tags, end="\n")
                (id, time, item, tag) = row
                tags = []
            idLast = row[0]
    else:
        diary.add_entry(entry, tags)
