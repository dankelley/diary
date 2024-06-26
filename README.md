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

## See entries with `caw` in the entry.

    diary --list caw

## See entries with tag `sound`.

    diary --list : sound

## Rename a tag.

    diary --rename-tag oldName newName

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

    alias ,a='\rm ~/Dropbox/diary.db'
    # rapid testing: do next if in diary directory
    #alias ,d='PYTHONPATH=/Users/kelley/git/diary python3 -m diary'
    # after-installation testing
    alias ,d='diary'
    alias ,c='echo .dump|sqlite3 ~/Dropbox/diary.db'
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
