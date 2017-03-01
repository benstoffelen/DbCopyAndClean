# This Python file uses the following encoding: utf-8
import unittest
from utilities.utilities import Utilities


class TestCleaners(unittest.TestCase):
    def test_clean_multiple_punctuations(self):
        text1 = "schön zu sehen das sowas in coburg stattfindet...vielleicht besuche ich mal wieder die alte" + \
                " heimat.. gut zu wissen ;)"
        text2 = "Genau für Mich!!!!"
        cleaner = Utilities()
        result1 = "schön zu sehen das sowas in coburg stattfindet. vielleicht besuche ich mal wieder die alte" + \
                  " heimat. gut zu wissen ;)"
        result2 = "Genau für Mich!"
        self.assertEqual(cleaner.clean_multiple_punctuations(text1), result1)
        self.assertEqual(cleaner.clean_multiple_punctuations(text2), result2)

    def test_clean_url(self):
        text = "vom 13. bis 16. mai findet in Coburg das 34. BMW Veteranentreffen statt," + \
               "Infos auch unter http://www.facebook.com/TourismusCoburg?v=app_2344061033&ref=ts#!/event.php" + \
               "?eid=110512678986182&index=1"
        cleaner = Utilities()
        result = "vom 13. bis 16. mai findet in Coburg das 34. BMW Veteranentreffen statt,Infos auch unter"
        self.assertEqual(cleaner.clean_url(text), result)

    @unittest.skip("testing skipping")
    def test_detect_language_langid(self):
        cleaner = Utilities()
        with open("comments.txt") as f:
            for line in f:
                line = line.replace('"', "")
                lang = cleaner.check_language_langid(line)
                print line
                print lang
        pass

    @unittest.skip("testing skipping")
    def test_detect_language_langdetect(self):
        cleaner = Utilities()
        with open("comments.txt") as f:
            for line in f:
                line = line.replace('"', "")
                lang = cleaner.check_language_languagedetect(line)
                print line
                print lang
        pass

    def test_clean_smileys(self):
        cleaner = Utilities()
        test1 = ":o))"
        test2 = "UUU Nice Lets Play Rock n Roll  :))"
        self.assertEqual(cleaner.clean_smileys(test1), ":o)")
        self.assertEqual(cleaner.clean_smileys(test2), "UUU Nice Lets Play Rock n Roll  :)")

    def test_clean_multiple_whitespaces(self):
        cleaner = Utilities()
        test1 = "UUU Nice Lets Play Rock n Roll  :))"
        self.assertEqual(cleaner.clean_multiple_whitespaces(test1), "UUU Nice Lets Play Rock n Roll :))")

    def test_clean_beginning_punct(self):
        cleaner = Utilities()
        self.assertEqual("Sonnebrille und wech",cleaner.clean_dots_beginning_of_text("...Sonnebrille und wech"))

    def test_multiple_dots(self):
        cleaner = Utilities()
        self.assertEqual('dass auto ist traumhaft.', cleaner.clean_multiple_dots('dass auto ist traumhaft........'))
        test2 = "vom 13. bis 16. mai findet in Coburg das 34. BMW Veteranentreffen statt, Infos auch unter"
        self.assertEqual(test2, cleaner.clean_multiple_dots(test2))

    def test_clean_test(self):
        cleaner = Utilities()
        self.assertEqual('dass auto ist traumhaft.', cleaner.clean_text('dass auto ist traumhaft........'))