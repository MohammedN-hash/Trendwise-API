import langdetect



def is_english(text):
    try:
        return langdetect.detect(text) == 'en'
    except langdetect.LangDetectException:
        return False