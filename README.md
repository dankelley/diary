# diary

'diary' is a python script to handle diary entries.

Nothing works yet!  Here are some samples.

# Sample Usage

## Get help.

    diary --help
    diary -h

## Add an entry that has no categories.

    diary I ate breakfast.

## Add an entry that has a single category.

    diary I ate a salad for lunch. : food

## Add an entry that has a two categories.

    diary I ate a salad for lunch. : food healthy

## Export all entries in CSV format

    diary --export > backup.csv

## Import a previous export

    diary --import < backup.csv

## See all entries

    diary --list

## See entries with `salad` in the content(note coded yet)

    diary --list salad # FIXME: DOES NOT WORK YET

## See entries with tag `food` (note coded yet)

    diary --list : food # FIXME: DOES NOT WORK YET

## Exporting to csv (and importing back)

Export database to a csv file, then reread it into a new database.
This could be useful in transporting files. Note that the original
times of the entries are preserved in the new database.

    diary --writeCSV > ~/diary.csv
    diary --database ~/new.db --readCSV ~/diary.csv

## Find tag usage

    diary --tags

# Developer's test code

During testing, the following proved helpful. Note that it starts by
destroying the database!!

    alias a='\rm ~/Dropbox/diary.db'
    alias b='PYTHONPATH=/Users/kelley/git/diary python3 -m diary'
    alias c='echo .dump|sqlite3 ~/Dropbox/diary.db'
    b tweet or caw : bird sound
    b meow : cat sound animal
    b dog with no categories
    c
    b --list
    b --export
    b --tags
    b --writeCSV > ~/diary.csv
    b --database ~/new.db --readCSV ~/diary.csv

