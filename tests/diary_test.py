import unittest
import tempfile
import logging
import datetime
from diary.diaryclass import Diary
import os, sys

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.level = logging.DEBUG

class TestDiary(unittest.TestCase):

    def setUp(self):
        self.debug = False
        self.database = tempfile.NamedTemporaryFile(prefix="diary", delete=False)
        logger.debug("\nCreating database file %r.", self.database.name)
        self.diary = Diary(db=self.database.name, debug=self.debug)

    def test(self):
        self.diary.add_entry(time=datetime.datetime.now(), entry="Test entry", tags=["test","foo"])
        self.assertEqual(1, len(self.diary.get_table("entries")))

    def tearDown(self):
        logger.debug("Removing temporary database file.")
        os.remove(self.database.name)

if __name__ == '__main__':
    unittest.main()

