import langdetect
from langid.langid import LanguageIdentifier, model


class Cleaners:
    def __init__(self):
        self._identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

    def clean_multiple_punctuations(self):
        pass

    def check_language_langid(self, text):
        return self._identifier.classify(text)

    @staticmethod
    def check_language_languagedetect(text):
        return langdetect.detect(text)
