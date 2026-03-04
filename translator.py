# translator.py
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

class TranslatorService:
    def __init__(self):
        try:
            from deep_translator import GoogleTranslator
            self.translator = GoogleTranslator(source='auto', target='cs')
            self.active = True
        except ImportError:
            print("Knihovna deep-translator chybí.")
            self.active = False

    def is_text_english(self, text):
        if not isinstance(text, str) or not text.strip(): return False
        words = text.lower().split()
        eng_count = sum(1 for w in words if w in ENGLISH_STOP_WORDS)
        return (eng_count / len(words)) > 0.15

    def translate_if_needed(self, text, force=False):
        if not self.active or not isinstance(text, str) or len(text) < 4:
            return text
            
        text_clean = re.sub(r'<[^>]+>', ' ', text)
        should_translate = force or self.is_text_english(text_clean)
        
        if should_translate:
            try:
                translated = self.translator.translate(text)
                if translated: return translated
            except:
                pass
        return text