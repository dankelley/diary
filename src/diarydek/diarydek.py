#!/usr/bin/python3

from __future__ import print_function
import sys
import sqlite3 as sqlite
import os.path

authorId = "Dan Kelley"


class Diarydek:
    def __init__(self, db="~/Dropbox/diarydek.db", debug=0, quiet=False):
        """
        A class used for the storing and searching diary notes.
        """
        self.debug = debug
        self.quiet = quiet
        self.db = db
        self.fyi("Database '%s' (before path expansion)." % self.db)
        self.db = os.path.expanduser(self.db)
        self.fyi("Database '%s' (after path expansion)." % self.db)
        mustInitialize = not os.path.exists(self.db)
        if mustInitialize:
            print('Creating new database named "%s".' % self.db)
        else:
            dbsize = os.path.getsize(self.db)
            self.fyi("Database file size %s bytes." % dbsize)
            mustInitialize = not dbsize
        try:
            con = sqlite.connect(self.db)
            con.text_factory = str  # permit accented characters
        except Exception:
            self.error("Error opening connection to database named '%s'" % db)
            raise
        self.con = con
        self.cur = con.cursor()
        self.authorId = authorId
        # DEVELOPER: next line must match version in toml file
        self.appversion = [0, 0, 14]
        self.dbversion = self.appversion
        if mustInitialize:
            self.initialize()
        try:
            self.dbversion = self.cur.execute("""SELECT * FROM version;""").fetchone()
        except Exception:
            self.warning("cannot get version number in database")
            self.dbversion = [0, 1, 0]
        appversion = "%s.%s.%s" % (
            self.appversion[0],
            self.appversion[1],
            self.appversion[2],
        )
        dbversion = "%s.%s.%s" % (
            self.dbversion[0],
            self.dbversion[1],
            self.dbversion[2],
        )
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
        return "diarydek version %d.%d.%d" % (
            self.appversion[0],
            self.appversion[1],
            self.appversion[2],
        )

    def rename_tag(self, old, new):
        self.fyi("rename_tag with old='%s' and new='%s'" % (old, new))
        tagNames = [tag[1] for tag in self.get_table("tags")]
        if old not in tagNames:
            self.error('There is no tag named "%s"' % old)
        else:
            q = "UPDATE tags SET tag = '%s' WHERE tag = '%s';" % (new, old)
            self.fyi(q)
            self.cur.execute(q)
            self.con.commit()

    def add_entry(self, time, entry, tags):
        self.fyi("add_entry...")
        self.fyi("  entry: %s" % entry)
        self.fyi("  tags:  %s" % tags)
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
            if tag not in tagsOld:
                self.fyi("%s: adding to db" % tag)
                self.cur.execute("INSERT INTO tags(tag) VALUES(?);", (tag,))
                self.con.commit()
        # add linkages
        for tag in tags:
            self.fyi("tag %s" % tag)
            tagId = self.cur.execute(
                "SELECT tagId FROM tags WHERE tag='%s';" % tag
            ).fetchall()[0]
            self.con.commit()
            self.fyi("tagId %d" % tagId)
            self.cur.execute(
                "INSERT INTO entry_tags(entryId,tagId) VALUES(?,?);",
                (entryId, tagId[0]),
            )
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
        if tag not in existing:
            try:
                self.cur.execute("INSERT INTO tags(tag) VALUES(?);", (tag))
                self.con.commit()
            except Exception:
                self.error("Cannot add tag '%s'" % tag)

    def initialize(self):
        """Initialize the database"""
        self.cur.execute("CREATE TABLE version(major, minor, subminor);")
        self.cur.execute(
            """INSERT INTO version(major, minor, subminor) VALUES (?,?,?);
            """,
            (self.appversion[0], self.appversion[1], self.appversion[2]),
        )
        self.cur.execute(
            """CREATE TABLE tags(
                tagId integer primary key autoincrement,
                tag);
            """
        )
        self.cur.execute(
            """CREATE TABLE entries(
                entryId integer primary key autoincrement,
                time,
                entry);
            """
        )
        self.cur.execute(
            """
            CREATE TABLE entry_tags(
                entryTagId integer primary key autoincrement,
                entryId, tagId);
            """
        )
        self.con.commit()

    def list_all(self):
        """list all"""
        q = """
        SELECT entries.entryId, entries.time, entries.entry, tags.tag
        FROM entries
        JOIN entry_tags
          ON entry_tags.entryId = entries.entryId
        JOIN tags
          ON entry_tags.tagId = tags.tagId
        ORDER BY entries.time;
        """
        self.fyi(q)
        res = self.cur.execute(q).fetchall()
        self.con.commit()
        return res  # list_all

    def get_table(self, tablename):
        if tablename == "entries":
            res = self.cur.execute(
                "SELECT * from %s ORDER BY time;" % tablename
            ).fetchall()
        else:
            res = self.cur.execute("SELECT * from %s;" % tablename).fetchall()
        self.con.commit()
        return res

    def get_tags_with_counts(self):
        """Get tags, with counts."""
        q = """
        SELECT tags.tag,count(tags.tag)
        FROM tags
        JOIN entry_tags
        ON tags.tagId = entry_tags.tagId
        GROUP BY tags.tagId, entry_tags.tagId
        """
        res = self.cur.execute(q).fetchall()
        res = sorted(res, key=lambda res: res[0])
        self.con.commit()
        return res

    def list_tags(self):
        """Return alphabetized list of tags"""
        names = []
        try:
            for n in self.cur.execute("SELECT tag FROM tags;").fetchall():
                k = n[0].strip()
                if len(k):
                    names.extend([k])
        except Exception:
            self.error("ERROR: cannot find database table 'tags'")
        names = list(set(names))  # remove duplicates
        names = sorted(names, key=lambda s: s.lower())
        return names
