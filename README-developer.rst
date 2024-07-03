Developer notes
===============

New instructions as of July 2024
--------------------------------


I have used the following alias for local work (or something similar).
The idea is to skip the funky details of packaging.

::
    alias ",dd"="PYTHONPATH=/Users/kelley/git/diarydek python3 -m diarydek"

The following builds locally, so I'm focussing on that for now.

::
    python3 -m pip install . --break-system-packages

When things seem okay, do as follows.

::
    python3 -m build

This builds the sources in a form that is suitable for upload to pypi.
these are stored in the `dist/` directory.  Manually remove any old
files that predate the ones you just made.  If you are sure things are
okay, upload to pypi by using the following (either seems to work)

::
    python3 -m twine upload dist/*
    # twine upload dist/*

If this complains about it already being there, that likely means that
you forgot to bump the version number.  So, do that in both the
`pyproject.toml` file, and in `diarydek/diarydek.py`, where it
appears in the definition of `self.appversion`, which is a tuple.

Once this is done, you should pop over to pypi.org and remove the old
version.  Then do
::
    pip uninstall diarydek --break-system-packages
    pip install diarydek --break-system-packages

And then?  Well, I don't know how to make it work.  It does not seem
to install the main program or, if it does, it's not in my PATH.
Frustrating...

References
----------

1. https://packaging.python.org/tutorials/packaging-projects/ provides information on packaging.

Setup
-----

Of course, you need python3 to be installed.

Then, make sure that ``pip`` is installed; if not, do

::

    easy_install-3.8 pip

to install it. Next, install ``wheel``

::

    pip3.8 install wheel

Note: the steps listed above need only be done once.

Increasing the version number
-----------------------------

Several manual steps are required.

1. Alter the 'version=' line in `setup.py`.
2. Ensure that `README.md` has an entry for the version.
3. Ensure that the version numbers in the present document are updated, so that
   cut/paste will work for local installations.
4. Update the `self.appversion =` line in `diary/diarydek.py` for the new version. Look
   carefully at the nearby code, if changes have been made to the database.
5. Remove old files from the `dist/` directory.
6. Perform the steps listed under "Packaging" and "Installing package locally" below.
7. Use it for a while, only updating to pypi (see "Installing package on pypi.python" below)
   when it is clear that this new version is good.

Testing before packaging
------------------------


::

    PYTHONPATH=/Users/kelley/git/diarydek python3 -m diarydek

Packaging
---------

Each time the ``diarydek`` source is updated, do the following to test and package
it:

::

    python3 setup.py test
    python3 setup.py sdist
    python3 setup.py bdist_wheel --universal

After this, the ``dist`` directory will contain some packages.

Installing package locally
--------------------------

To install a local test version, do e.g. (with the up-to-date version number, if the line below has the wrong one)

::

    sudo -H pip3 install dist/diarydek-0.0.1.tar.gz --upgrade


Installing package on pypi.python
---------------------------------

To submit to ``pypi.python.org`` remove old versions from ``dist`` and
then do:

::

    pip3.9 install twine
    twine upload dist/*


**Reminder** After uploading, be sure to increment the version number (a) in
line 4 of setup.py, (b) in the present file and (c) in diarydek/diarydek.py where
self.appversion is define. Then add a blank entry for this new version, in
README.rst.


Suggested aliases for diarydek
-----------------------------

The developer uses the following, so that ``n`` runs the packaged version and
``nn`` runs the new (source-code) version.

::

    alias ,d='diarydek' # or, for debugging, 'PYTHONPATH=~/git/diarydek python3 -m diarydek'

