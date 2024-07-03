# diary

'diarydek' is a python script to handle diary entries.  This file is a
sort of sandbox for the author.  Perhaps some of this content will
appear later in a vignette or whatever is the python equivalent of an
R vignette.  Please do not rely on anything in this document actually
working at this time, and please do not expect that any behaviour
sketched here will continue to work.  It's a sandbox after all.


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

# Developer's test code

During testing, the following proved helpful. Note that it starts by
destroying the database!!

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
