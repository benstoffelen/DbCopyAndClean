from unittest import TestCase

from cleaner.cleaners import Cleaners


class TestCleaners(TestCase):
    def test_clean_multiple_punctuations(self):
        self.fail()

    def test_detect_language_langid(self):
        cleaner = Cleaners()
        with open("comments.txt") as f:
            for line in f:
                line = line.replace('"', "")
                lang = cleaner.check_language_langid(line)
                print line
                print lang
        self.fail()
