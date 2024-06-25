#!/usr/bin/python3

import sys
import sqlite3 as sqlite
#import datetime
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
            print("Initializing database; run 'diary' again to use it.")
            self.initialize()
            return(None)
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

    def add_entry(self, entry, categories):
        categories = [category.strip() for category in categories.split(',')]
        print("add_entry...")
        print("  entry:%s" % entry)
        print("  categories:%s" % categories)
        self.cur.execute("INSERT INTO entries(entry) VALUES(?);", (entry,))
        self.con.commit()
        categoriesOriginal = []
        categoriesOriginal.extend((self.cur.execute("SELECT category FROM categories;"),))
        q = self.cur.execute("SELECT category from categories;").fetchall()
        categoriesOld = [category[0] for category in q]
        print("  existing categories: %s" % categoriesOld)
        for category in categories:
            if category in categoriesOld:
                print("%s: already in db" % category)
            else:
                print("%s: adding to db" % category)
                self.cur.execute("INSERT INTO categories(category) VALUES(?);", (category,))
                self.con.commit()
        print("done adding")

    def create_category(self, category):
        """Create a new category"""
        category = category.strip()
        if not len(category):
            self.error("Cannot have a blank book name")
        if category.find(",") >= 0:
            self.error("Cannot have a ',' in a category")
        existing = self.list_categories()
        if not category in existing:
            try:
                self.cur.execute("INSERT INTO category(category) VALUES(?);", (category))
                self.con.commit()
            except:
                self.fyi("Error adding a category named '%s'" % category)


    def initialize(self):
        ''' Initialize the database.  This is dangerous since it removes any existing content. '''
        self.cur.execute("CREATE TABLE version(major, minor, subminor);")
        self.cur.execute("INSERT INTO version(major, minor, subminor) VALUES (?,?,?);",
                (self.appversion[0], self.appversion[1], self.appversion[2]))
        self.cur.execute("CREATE TABLE categories(categoryId integer primary key autoincrement, category);")
        self.cur.execute("CREATE TABLE entries(entryId integer primary key autoincrement, entry);")
        self.cur.execute("CREATE TABLE entry_category(entryCategoryId integer primary key autoincrement, entryId, categoryId);")
        self.con.commit()

    def list_categories(self):
        ''' Return alphabetized list of categories '''
        names = []
        try:
            for n in self.cur.execute("SELECT category FROM categories;").fetchall():
                # Strip out leading and trailing whitespaces (can be artifacts of old data)
                k = n[0].strip()
                if len(k):
                    names.extend([k])
        except:
            self.error("ERROR: cannot find database table 'categories'")
        names = list(set(names)) # remove duplicates
        names = sorted(names, key=lambda s: s.lower())
        return(names)
