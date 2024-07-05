# diarydek

'diarydek' is a python script to handle diary entries.  It is still in
an Alpha stage of development, meaning that anything you see here
might change in the future.  Heck, some of it may be wrong even as you
read this!


# Sample Usage

## Get help.

    diarydek --help
    diarydek -h

## Add an entry that has no categories.

    diarydek I ate breakfast.

## Add an entry that has a single category.

    diarydek I ate a salad for lunch. : food

## Add an entry that has a two categories.

    diarydek I ate a salad for lunch. : food healthy

## Export all entries in CSV format

    diarydek --export > backup.csv

## Import a previous export

    diarydek --import < backup.csv

## See all entries

    diarydek --list

## See entries with `caw` in the entry.

    diarydek --list caw

## See entries with tag `sound`.

    diarydek --list : sound

## Rename a tag.

    diarydek --rename-tag oldName newName

## Exporting to csv (and importing back)

Export database to a csv file, then reread it into a new database.
This could be useful in transporting files. Note that the original
times of the entries are preserved in the new database.

    diarydek --writeCSV > ~/diary.csv
    diarydek --database ~/new.db --readCSV ~/diary.csv

## Find tag usage

    diarydek --tags

# Developer's notes

During testing, the following proved helpful. Note that it starts by
destroying the database!!

    # build and install local version (not touching pypi, no need to
    # bump version number)
    python3 -m pip install . --break-system-packages
    # below are from VERY early stages, and should be deleted
    alias ,a='\rm ~/Dropbox/diarydek.db'
    # rapid testing: do next if in diary directory
    #alias ,d='PYTHONPATH=/Users/kelley/git/diarydek python3 -m diarydek'
    # after-installation testing
    alias ,d='diarydek'
    alias ,c='echo .dump|sqlite3 ~/Dropbox/diarydek.db'
    ,a # clean database
    ,d tweet or caw : bird sound
    ,d meow : cat sound animal
    ,d dog with no categories
    ,c
    ,d --list
    ,d --list caw
    ,d --list : sound
    ,d --tags
    ,d --writeCSV > ~/diary.csv
    ,d --database ~/new.db --readCSV ~/diary.csv


# Developer notes


The following builds locally, when run from the source directory.

    python3 -m pip install . --break-system-packages

If this works in testing, consider uploading to pypi.  Be sure to bump
the version number first to avoid conflict with a version on pypi.  Do
this in two steps:

1. Edit the `pyproject.toml` file, altering the line defining
   `version`.

2. Edit the `src/diarydek/diarydek.py` file, altering
   the definition of `self.appversion`.

With this done, it is possible to upload to pypi, which is done with
the following.  (The first step just ensures that you don't try to
upload any old sources that you might have built up previously with
twine.)

    rm dist/*                      # remove any existing files
    python3 -m build               # build, installing 2 files in dist
    python3 -m twine upload dist/* # upload to pypi

Once this is done, you can install the pypi version using the
following.  If it works, then you can have some assurance that users
can install it (using the second step).

    pip uninstall diarydek --break-system-packages # remove any existing version
    pip install diarydek --break-system-packages   # install new, from pypi

# Suggested aliases

Although you can use a single diary for all your work, it can
sometimes help to have multiple databases, e.g. for privacy.  I do
things like the following.

    alias ',dp'='diarydek --database=~/Documents/diary/personal.db'
    alias ',dw'='diarydek --database=~/Documents/diary/work.db'


References
----------

1. https://packaging.python.org/tutorials/packaging-projects/ provides
   information on packaging.

