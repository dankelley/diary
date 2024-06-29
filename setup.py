import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(name='diary',
      version='0.0.1',
      description='Diary application',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/dankelley/diary',
      author='Dan Kelley',
      author_email='kelley.dan@gmail.com',
      license='GPL3',
      packages=['diary'],
      python_requires='>=3.6',
      classifiers=['Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Topic :: Utilities',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
      test_suite="tests",
      entry_points={ 'console_scripts':
          [ 'diary = diary.main:diary' ]
          },
      zip_safe=True)
