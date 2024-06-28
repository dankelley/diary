# diary

'diary' is a python script to handle diary entries.

Nothing works yet!  Here are some samples.

Get help.

    diary --help
    diary -h

Add an entry that has no categories.

    diary I ate breakfast.

Add an entry that has a single category.

    diary I ate a salad for lunch. : food

Add an entry that has a two categories.

    diary I ate a salad for lunch. : food healthy

Export all entries in CSV format

    diary --export > backup.csv

Import a previous export

    diary --import < backup.csv # FIXME: code this

See all entries

    diary --list

See entries with `salad` in the content(note coded yet)

    diary --list salad # FIXME: DOES NOT WORK YET

See entries with tag `food` (note coded yet)

    diary --list : food # FIXME: DOES NOT WORK YET

Export database to a csv file, then reread it into a new database.
This could be useful in transporting files. Note that the original
times of the entries are preserved in the new database.

    diary --writeCSV > ~/diary.csv
    diary --database ~/new.db --readCSV ~/diary.csv


Testing

    alias a='\rm ~/Dropbox/diary.db'
    alias b='PYTHONPATH=/Users/kelley/git/diary python3 -m diary '
    alias c='echo .dump|sqlite3 ~/Dropbox/diary.db'
    b tweet or caw : bird sound
    b meow : cat sound animal
    b dog with no categories
    c
    echo "select time,entry,category FROM entries JOIN categories ON entry_category.entryId = categories.categoryId;"|sqlite3 ~/Dropbox/diary.db
    b --list
    b --export

