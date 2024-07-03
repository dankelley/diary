import unittest
import tempfile
import logging
import datetime
from diarydek.diarydekclass import Diarydek
import os
import sys

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.level = logging.DEBUG


class TestDiary(unittest.TestCase):

    def setUp(self):
        self.database = tempfile.NamedTemporaryFile(prefix="diary", delete=False)
        logger.debug("\nCreating database file %r.", self.database.name)
        self.diarydek = Diarydek(db=self.database.name, debug=False)

    def test(self):
        self.diarydek.add_entry(
            time=datetime.datetime.now(), entry="Test entry", tags=["test", "foo"]
        )
        self.assertEqual(1, len(self.diarydek.get_table("entries")))
        tagNames = [tag[1] for tag in self.diarydek.get_table("tags")]
        self.assertEqual(["test", "foo"], tagNames)
        self.diarydek.rename_tag("foo", "bar")
        tagNames = [tag[1] for tag in self.diarydek.get_table("tags")]
        self.assertEqual(["test", "bar"], tagNames)

    def tearDown(self):
        logger.debug("Removing temporary database file.")
        os.remove(self.database.name)


if __name__ == "__main__":
    unittest.main()
