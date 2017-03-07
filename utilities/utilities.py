import langdetect
import re

import language_check
from langid.langid import LanguageIdentifier, model
import nltk.tokenize as nlp

import urlmarker


class Utilities:
    def __init__(self):
        self._identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

    # Method to remove multiple punctuations. E.g. !!!!!! --> !
    @staticmethod
    def clean_multiple_punctuations(text):
        doubles_removed = re.sub(r'[!?/\\:\']+(?=[!?/\\:\'])', '', text)
        return re.sub(r'([?!])(\S)', r"\1 \2", doubles_removed)

    # Method to remove multiple dots but keeping , ...
    @staticmethod
    def clean_multiple_dots(text):
        # remove whitespaces between dots
        text = re.sub(r'([.]+)\s+([.]+)', r"\1\2", text)
        # reduce dots
        text = re.sub(r'(\w)\s*[.]{2,}\Z', r'\1.', text)
        text = re.sub(r'(\w)\s*[.]{2,}\s*', r'\1. ', text)
        return text

    # Method to detect text language using the langid framework
    def check_language_langid(self, text):
        return self._identifier.classify(text)[0]

    # Method to detect text language using the langdetect framework
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
        text = re.sub(r'([\[\]@{]?[:;8]+[o-]?)([D)XBbdSs"(O\)\[\\pP?])+(?<=[D)XBbdSs"(O\)\[\\pP?])', r" \1\2 ", text)
        myre = re.compile((u'('
                           u'\ud83c[\udf00-\udfff]|'
                           u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
                           u'[\u2600-\u26FF\u2700-\u27BF])+'),
                          re.UNICODE)
        text = re.sub(myre, r' \1 ', text)
        return re.sub(r'<3', ' <3 ', text)


    # Method to remove multiple whitespaces from text
    @staticmethod
    def clean_multiple_whitespaces(text):
        return ' '.join(text.split())

    # Method to remove ... from beginning of text
    @staticmethod
    def clean_dots_beginning_of_text(text):
        return re.sub(r'^[.]+\s*(\w*)', r"\1", text)

    # Method to split into sentences. Returns list
    @staticmethod
    def split_into_sentences(text):
        return nlp.sent_tokenize(text, language='german')

    @staticmethod
    def clean_apostrophes(text):
        return text.replace('"', "")

    @staticmethod
    def correct_spelling(text):
        print text
        tool = language_check.LanguageTool('de-DE')
        matches = tool.check(text)
        text = language_check.correct(text, matches)
        print text


    def clean_for_model(self, text):
        text = re.sub(r",", " , ", text)
        text = re.sub(r"!", " ! ", text)
        text = re.sub(r"\?", " ? ", text)
        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r"\^\^", " ^^", text)
        text = re.sub("\.", " . ", text)
        self.clean_multiple_whitespaces(text)
        return text.strip().lower()

    def clean_text(self, text):
        text = self.clean_url(text)
        text = self.clean_multiple_punctuations(text)
        text = self.clean_multiple_dots(text)
        text = self.clean_smileys(text)
        text = self.clean_dots_beginning_of_text(text)
        text = self.clean_multiple_whitespaces(text)
        #text = self.clean_for_model(text)
        return text
