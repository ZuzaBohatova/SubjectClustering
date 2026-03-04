# text_processor.py
import re
import unicodedata
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import config
import stopwordsiso


class TextProcessor:
    def __init__(self):
        self.stop_words = self._prepare_stopwords()

    def remove_accents(self, input_str):
        if not isinstance(input_str, str): return ""
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def czech_stemmer(self, word):
        if len(word) < 4: return word
        word = re.sub(r'(ických|ových|ského|ického|ickým|ický|ické|osti|ická|ých|ými|ého|ému|ách|ami|ová|ové|ový|ího|ech|ata|aty|ity|ité|ost|ích|ský|ské|ská|ie|ovi|ou|em|ím)$', '', word)
        if len(word) > 3:
            word = re.sub(r'(a|e|i|o|u|y|á|é|í|ý|ů|ě)$', '', word)
        if word.endswith('výuc'): word = word[:-1] + 'k'
        return word

    def clean_word_process(self, w):
        w_stem = self.czech_stemmer(w)
        return self.remove_accents(w_stem)

    def _prepare_stopwords(self):
        try:
            raw_stopwords_cs = list(stopwordsiso.stopwords("cs"))
        except ImportError:
            print("Knihovna stopwordsiso chybí")
        
        raw_stopwords = raw_stopwords_cs
        processed = []
        for w in raw_stopwords:
            w_proc = self.clean_word_process(w)
            if len(w_proc) >= 4:
                processed.append(w_proc)
        return list(set(processed))

    def clean_text_pipeline(self, text):
        if not isinstance(text, str): return ""
        text = text.lower()
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'[^a-záčďéěíňóřšťúůýž\s]', ' ', text)

        words = text.split()
        cleaned_words = []
        
        for w in words:
            if 'angličtin' in w: 
                w = 'anglický'
                cleaned_words.append(self.clean_word_process('jazyk'))
            if 'učitel' in w or 'didakt' in w: 
                w = 'pedagog'
            if 'němec' in w or 'němč' in w or 'francouz' in w or 'španěl' in w  or 'rusk' in w or 'rušti' in w:
                w = 'angl'
            if 'škol' in w:
                w = 'škola'
            if 'programov' in w:
                w = 'programování'
            if 'finan' in w:
                w = 'finance'
            if 'výzkum' in w:
                w = 'výzkum'
            if 'kombinator' in w:
                w = 'kombinatorika'
            if 'lingvist' in w:
                w = 'lingvistika'

            w_final = self.clean_word_process(w)
            
            if any(bad in w_final for bad in config.FORBIDDEN_SUBSTRINGS): continue
            if len(w_final) < 4: continue
                
            cleaned_words.append(w_final)

        return " ".join(cleaned_words)