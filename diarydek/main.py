#!/usr/bin/python3

from .diarydekclass import Diarydek
import argparse
import sys
from csv import reader
import textwrap
import datetime
import json
from os import path


rcfile = "~/.diardekyrc"  # can define next 2 items
defaultDatabase = "~/diarydek.db"
separator = ":"
try:
    f = open(path.expanduser(rcfile))
    rc = json.load(f)
    try:
        tmp = rc["database"]
        defaultDatabase = tmp
    except KeyError:
        pass
    try:
        tmp = rc["separator"]
        separator = tmp
    except KeyError:
        pass
    # defaultDatabase
except IOError:
    pass

overallHelp = """

# Customization

Some features of how diary works can be customized with a file in the
user's top-level directory, called `.diaryrc`. This file must be
written in JSON format, as in the example below. So far, the only
element that can be altered is the default database name.

    {
        "database": "~/Dropbox/diarydek.db"
    }

Another way to specify the database is by using a unix alias, e.g. the
author uses the following to isolate some diary items to a personal
database, by typing `,dp` instead of `diary` in the command-line
interface.

    alias ',dp'='diary --database=~/Documents/diary/personal.db'

# Advanced usage

## Merging two databases

The following creates a new database that contains the contents of two
other databases.

    diary --database ~/a.db --export > a.csv
    diary --database ~/b.db --export > b.csv
    diary --database ~/ab.db import < a.csv
    diary --database ~/ab.db import < b.csv

"""


def diary():
    time = datetime.datetime.now()  # can be over-written by --time
    parser = argparse.ArgumentParser(
        prog="diary",
        description="Diary: a commandline tool for adding entries to a diary database.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(overallHelp),
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Turn on tracer information.",
    )
    parser.add_argument(
        "--database",
        type=str,
        default=None,
        help="database location (defaults to %s)" % defaultDatabase,
        metavar="filename",
    )
    parser.add_argument(
        "--version", action="store_true", help="Show application version number."
    )
    parser.add_argument(
        "--time",
        type=str,
        default=None,
        help="time of item (defaults to present time if not given).",
        metavar="\"yyyy-mm-dd\" or \"yyyy-mm-ddThh:mm:ss\"",
    )
    parser.add_argument(
        "--showTags", action="store_true", help="Show tags in database, with counts."
    )
    parser.add_argument("--list", action="store_true", help="Print entries")
    parser.add_argument(
        "--since",
        type=str,
        nargs=1,
        help="Restrict --list to a recent time interval, as yyyy-mm-dd or 'yyyy-mm-dd HH:MM:SS'",
        metavar="yyyy-mm-dd",
    )
    parser.add_argument(
        "--writeCSV",
        action="store_true",
        help="Write entries to a CSV format that can be read with --readCSV.",
    )
    parser.add_argument(
        "--readCSV",
        type=str,
        default=None,
        help="Read CSV information into database, reversing --writeCSV action.",
        metavar="file.csv",
    )
    parser.add_argument(
        "--renameTag",
        type=str,
        nargs=2,
        help="Rename a tag.",
        metavar=("old", "new"),
    )
    parser.add_argument(
        "words",
        type=str,
        nargs="*",
        help="Diary entry, in the form of words that are optionally followed by tags, following a ':' character.",
    )
    args = parser.parse_args()
    if args.words:
        if separator in args.words:
            start = args.words.index(separator) + 1
            tags = args.words[start : len(args.words)]
            entry = " ".join(map(str, args.words[0 : start - 1]))
        else:
            entry = " ".join(map(str, args.words))
            tags = []
    else:
        entry = []
        tags = []
    if args.debug:
        print("  separator %s" % separator)
        print("  defaultDatabase %s" % defaultDatabase)
        print("  entry: %s" % entry)
        print("  tags:  %s" % tags)
    if not args.database:
        args.database = defaultDatabase
    diary = Diarydek(debug=args.debug, db=args.database)

    if args.renameTag:
        if args.words:
            diary.error("extra words after '--rename-tags old new'")

        diary.rename_tag(args.renameTag[0], args.renameTag[1])
        exit(0)

    if args.debug:
        print("  database: '%s'" % args.database)

    if args.version:
        (major, minor, subminor) = diary.appversion
        print("diary version %d.%d.%d" % (major, minor, subminor))
        sys.exit(0)
    if args.showTags:
        print("Tags in database, with counts:")
        for row in diary.get_tags_with_counts():
            print(" %10s: %d" % (row[0], row[1]))
        sys.exit(0)  # handle --showTags
    if args.time:
        tmp = args.time
        if args.debug:
            print("FIXME: handle --time %s" % args.time[0])
        if len(tmp) == 10:
            time = datetime.datetime.strptime(tmp, "%Y-%m-%d")
        elif len(tmp) == 19:
            time = datetime.datetime.strptime(tmp, "%Y-%m-%d %H:%M:%S")
        else:
            diary.error("must give time as \"yyyy-mm-dd\" or \"yyyy-mm-dd HH:MM:SS\"")
            sys.exit(1)
    since = None
    if args.since:
        tmp = args.since[0]
        if len(tmp) == 10:
            since = datetime.datetime.strptime(tmp, "%Y-%m-%d")
        else:
            since = datetime.datetime.strptime(tmp, "%Y-%m-%d %H:%M:%S")
        if args.debug:
            print("  --since with cutoff time %s" % since)

    if args.readCSV:
        with open(args.readCSV) as csv:
            rows = reader(csv)
            for row in rows:
                (time, entry, tagsWithCommas) = row
                # print("<%s> <%s> <%s>" % (time, entry, tagsWithCommas))
                tags = tagsWithCommas.split(",")
                # print(tags)
                diary.add_entry(time, entry, tags)
        sys.exit(0)  # handle --readCSV

    # Write whole database to CSV
    if args.writeCSV:
        tags = diary.get_table("tags")
        entries = diary.get_table("entries")
        entry_tags = diary.get_table("entry_tags")
        if args.debug:
            print("tags: ", end="")
            print(tags)
            print("entries: ", end="")
            print(entries)
            print("entry_tags: ", end="")
            print(entry_tags)
        # put tags in a dictionary, for easier lookup
        taglist = {}
        for tag in tags:
            taglist[tag[0]] = tag[1]
        for entry in entries:
            entryId = entry[0]
            tags = []
            for entry_tag in entry_tags:
                if entry_tag[1] == entryId:
                    tags.append(taglist[entry_tag[2]])
            print('"%s","%s"' % (entry[1], entry[2]), end="")
            if tags:
                print(',"', end="")
                print(",".join(tags), end="")
                print('"', end="")
            else:
                print(',""', end="")
            print("")
        sys.exit(0)  # handle --writeCSV

    if args.list:
        if args.debug:
            print("handling --list with --since=%s" % since)
        tagSearch = []
        entrySearch = ""
        if args.words:
            if separator in args.words:
                start = args.words.index(separator) + 1
                tagSearch = args.words[start : len(args.words)]
                entrySearch = " ".join(map(str, args.words[0 : start - 1]))
            else:
                entrySearch = " ".join(map(str, args.words))
            if args.debug:
                print("  args.words:  %s" % args.words)
                print("  entrySearch: '%s'" % entrySearch)
                print("  tagSearch:   %s" % tagSearch)
            if tagSearch and len(tagSearch) > 1:
                diary.error(
                    "cannot have more than 1 tag to search, but got: %s" % tagSearch
                )
            # un-tuple it
            if len(tagSearch) == 1:
                tagSearch = tagSearch[0]
        tags = diary.get_table("tags")
        entries = diary.get_table("entries")
        entry_tags = diary.get_table("entry_tags")
        if args.debug:
            print("tags: ", end="")
            print(tags)
            print("entries: ", end="")
            print(entries)
            print("entry_tags: ", end="")
            print(entry_tags)
        # put tags in a dictionary, for easier lookup
        taglist = {}
        for tag in tags:
            taglist[tag[0]] = tag[1]
        if args.debug:
            print("len(entrySearch): %s" % len(entrySearch))
            print("len(tagSearch): %s" % len(tagSearch))
            print("entrySearch: %s" % entrySearch)
            print("tagSearch: %s" % tagSearch)
        for entry in entries:
            entryId = entry[0]
            tags = []
            for entry_tag in entry_tags:
                if entry_tag[1] == entryId:
                    tags.append(taglist[entry_tag[2]])
            showAll = 0 == len(entrySearch) and 0 == len(tagSearch)
            showBasedOnEntry = 0 < len(entrySearch) and entrySearch in entry[2]
            showBasedOnTag = 0 < len(tagSearch) and tagSearch in tags
            tmp = entry[1]
            if len(tmp) == 10:
                entryTime = datetime.datetime.strptime(tmp, "%Y-%m-%d")
            else:
                tmp = tmp.split(".")[0]
                entryTime = datetime.datetime.strptime(tmp, "%Y-%m-%d %H:%M:%S")
            showBasedOnTime = (not since) or entryTime > since
            show = (showAll or showBasedOnEntry or showBasedOnTag) and showBasedOnTime
            if args.debug:
                print("  entrySearch:", entrySearch)
                print("  entry: ", entry[2])
                print("  tagSearch:", tagSearch)
                print("  tags: ", tags)
                print("  showAll: %d" % showAll)
                print("  showBasedOnEntry: %d" % showBasedOnEntry)
                print("  showBasedOnTag: %d" % showBasedOnTag)
                print("  show: %d" % show)
            if show:
                print("%s %s" % (entry[1], entry[2]), end="")
                if tags:
                    print(" : ", end="")
                    for tag in tags:
                        print(tag, end=" ")
                print()
        sys.exit(0)  # handle --list

    # Database insertion
    elif args.words:
        diary.add_entry(time, entry, tags)
    else:
        print("Try -h to learn how to use this")
