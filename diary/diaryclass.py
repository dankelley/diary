#!/usr/bin/python3

import sys
import sqlite3 as sqlite
import datetime
import os.path
#import difflib
#from distutils.version import StrictVersion
#import re
#import tempfile
#import subprocess
#import hashlib
#import random
#import string
#from math import trunc

#reload(sys)
#sys.setdefaultencoding('utf8')
authorId = "Dan Kelley"

class Diary:
    def __init__(self, db="~/Dropbox/diary.db", debug=0, quiet=False):
        '''
        A class used for the storing and searching diary notes.
        '''
        self.debug = debug
        self.quiet = quiet
        self.db = db
        self.fyi("Database '%s' (before path expansion)." % self.db)
        self.db = os.path.expanduser(self.db)
        self.fyi("Database '%s' (after path expansion)." % self.db)
        mustInitialize = not os.path.exists(self.db)
        if mustInitialize:
            print("Creating new database named \"%s\"." % self.db)
        else:
            try:
                dbsize = os.path.getsize(self.db)
                self.fyi("Database file size %s bytes." % dbsize)
                mustInitialize = not dbsize
            except:
                pass
        try:
            con = sqlite.connect(self.db)
            con.text_factory = str # permit accented characters
        except:
            self.error("Error opening connection to database named '%s'" % db)
            exit(1)
        self.con = con
        self.cur = con.cursor()
        self.authorId = authorId
        ## 0.3: add note.modified column
        self.appversion = [0, 1, 0] # db schema changes always yield first or second digit increment
        self.dbversion = self.appversion
        if mustInitialize:
            self.initialize()
        try:
            self.dbversion = self.cur.execute("SELECT * FROM version;").fetchone()
        except:
            self.warning("cannot get version number in database")
            self.dbversion = [0, 1, 0]
            pass
        appversion = "%s.%s.%s" % (self.appversion[0], self.appversion[1], self.appversion[2])
        dbversion = "%s.%s.%s" % (self.dbversion[0], self.dbversion[1], self.dbversion[2])
        self.fyi("appversion: %s" % appversion)
        self.fyi("dbversion: %s" % dbversion)
        self.fyi("self.dbversion: %s" % [self.dbversion])


    def fyi(self, msg, prefix="  "):
        if self.debug:
            print(prefix + msg, file=sys.stderr)


    def warning(self, msg, prefix="Warning: "):
        if not self.quiet:
            print(prefix + msg, file=sys.stderr)


    def error(self, msg, level=1, prefix="Error: "):
        if not self.quiet:
            print(prefix + msg, file=sys.stderr)
        sys.exit(level)


    def version(self):
        return("nota version %d.%d.%d" % (self.appversion[0], self.appversion[1], self.appversion[2]))

    def add_entry(self, entry, tags):
        self.fyi("add_entry...")
        self.fyi("  entry: %s" % entry)
        self.fyi("  tags:  %s" % tags)
        time = datetime.datetime.now()
        self.cur.execute("INSERT INTO entries(time,entry) VALUES(?,?);", (time, entry))
        entryId = self.cur.lastrowid
        self.fyi("entryID %d" % entryId)
        self.con.commit()
        # add tags to known list
        q = self.cur.execute("SELECT tag from tags;").fetchall()
        self.con.commit()
        tagsOld = [tag[0] for tag in q]
        self.fyi("  existing tags: %s" % tagsOld)
        for tag in tags:
            if not tag in tagsOld:
                self.fyi("%s: adding to db" % tag)
                self.cur.execute("INSERT INTO tags(tag) VALUES(?);", (tag,))
                self.con.commit()
        # add linkages
        for tag in tags:
            self.fyi("tag %s" % tag)
            tagId = self.cur.execute("SELECT tagId FROM tags WHERE tag='%s';" % tag).fetchall()[0]
            self.con.commit()
            self.fyi("tagId %d" % tagId)
            self.cur.execute("INSERT INTO entry_tag(entryId,tagId) VALUES(?,?);", (entryId, tagId[0]))
            self.con.commit()
        self.fyi("done adding")

    def create_tag(self, tag):
        """Create a new tag"""
        tag = tag.strip()
        if not len(tag):
            self.error("Cannot have a blank book name")
        if tag.find(",") >= 0:
            self.error("Cannot have a ',' in a tag")
        existing = self.list_tags()
        if not tag in existing:
            try:
                self.cur.execute("INSERT INTO tags(tag) VALUES(?);", (tag))
                self.con.commit()
            except:
                self.fyi("Error adding a tag named '%s'" % tag)


    def initialize(self):
        ''' Initialize the database.  This is dangerous since it removes any existing content. '''
        self.cur.execute("CREATE TABLE version(major, minor, subminor);")
        self.cur.execute("INSERT INTO version(major, minor, subminor) VALUES (?,?,?);",
                (self.appversion[0], self.appversion[1], self.appversion[2]))
        self.cur.execute("CREATE TABLE tags(tagId integer primary key autoincrement, tag);")
        self.cur.execute("CREATE TABLE entries(entryId integer primary key autoincrement, time, entry);")
        self.cur.execute("CREATE TABLE entry_tag(entryTagId integer primary key autoincrement, entryId, tagId);")
        self.con.commit()

    def list_all(self):
        ''' list all '''
        q = '''
        SELECT entries.time, entries.entry, tags.tag
        FROM entries
        JOIN entry_tag
          ON entry_tag.entryId = entries.entryId
        JOIN tags
          ON entry_tag.tagId =
        tags.tagId;
        '''
        self.fyi(q)
        res = self.cur.execute(q).fetchall()
        self.con.commit()
        return(res)

    def list_tags(self):
        ''' Return alphabetized list of tags '''
        names = []
        try:
            for n in self.cur.execute("SELECT tag FROM tags;").fetchall():
                # Strip out leading and trailing whitespaces (can be artifacts of old data)
                k = n[0].strip()
                if len(k):
                    names.extend([k])
        except:
            self.error("ERROR: cannot find database table 'tags'")
        names = list(set(names)) # remove duplicates
        names = sorted(names, key=lambda s: s.lower())
        return(names)
