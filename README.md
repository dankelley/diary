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

See all entries

    diary --list

See entries with category `food`

    diary --list food

Testing

    a='\rm ~/Dropbox/diary.db'
    b='PYTHONPATH=/Users/kelley/git/diary python3 -m diary '
    c='echo .dump|sqlite3 ~/Dropbox/diary.db'
    b item without categories
    b item with two categories : cat1 cat2

