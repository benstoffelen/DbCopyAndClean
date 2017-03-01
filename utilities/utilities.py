import langdetect
import re
from langid.langid import LanguageIdentifier, model

from utilities import urlmarker


class Utilities:
    def __init__(self):
        self._identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

    #Method to remove multiple punctuations. E.g. ..... --> .
    @staticmethod
    def clean_multiple_punctuations(text):
        doubles_removed = re.sub(r'[.!?\-)/\\:\']+(?=[.!?\-)/\\:\'])', '', text)
        return re.sub(r'([.?!])(\S)', r"\1 \2", doubles_removed)

    #Method to detect text language using the langid framewok
    def check_language_langid(self, text):
        return self._identifier.classify(text)[0]

    #Method to detect text language using the langdetect framework
    @staticmethod
    def check_language_languagedetect(text):
        return langdetect.detect(text)

    # Method to clean urls from text
    @staticmethod
    def clean_url(text):
        return re.sub(urlmarker.WEB_URL_REGEX, '', text).rstrip()

    # Method to reduce smileys to their general form. E.g. :-DDDDDDD --> :-D
    # TODO BeSt: maybe there is a database that can do this out of the box?
    @staticmethod
    def clean_smileys(text):
        return re.sub(r'([\[\]@{]?[:;8]+[o-]?)([D)XBbdSs"(O\)\[\\pP?])+(?<=[D)XBbdSs"(O\)\[\\pP?])', r"\1\2", text)

    # Method to remove multiple whitespaces from text
    @staticmethod
    def clean_multiple_whitespaces(text):
        return ' '.join(text.split())

    #Method to remove ... from beginning of text
    @staticmethod
    def clean_dots_beginning_of_text(text):
        return re.sub(r'^[.]+\s*(\w*)',r"\1", text)