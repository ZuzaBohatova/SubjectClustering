# data_loader.py
import pandas as pd
import os
from sqlalchemy import create_engine
import config
from translator import TranslatorService

class DataLoader:
    def __init__(self):
        self.translator_service = TranslatorService()

    def _prepare_translations(self, df):
        print("Provádím překlady (RAW -> Translated)...")
        final_texts = []
        total = len(df)
        for index, row in df.iterrows():
            if index % 100 == 0: print(f"   ... {index}/{total}")
            
            ts = self.translator_service
            parts = [
                ts.translate_if_needed(row.get('title', '')),
                ts.translate_if_needed(row.get('annotation_cz', '')),
                ts.translate_if_needed(row.get('syllabus_cz', '')),
                ts.translate_if_needed(row.get('annotation_en', ''), force=True),
                ts.translate_if_needed(row.get('syllabus_en', ''), force=True)
            ]
            final_texts.append(" ".join([p for p in parts if p]))
        
        df['combined_text_translated'] = final_texts
        return df

    def load_data(self):
        if os.path.exists(config.TRANSLATED_FILE):
            print(f"Načítám přeložený soubor '{config.TRANSLATED_FILE}'...")
            df = pd.read_csv(config.TRANSLATED_FILE, sep=';').fillna("")
        
        elif os.path.exists(config.RAW_INPUT_FILE):
            print(f"Načítám surový export '{config.RAW_INPUT_FILE}'...")
            df = pd.read_csv(config.RAW_INPUT_FILE, sep=';').fillna("")
            df = self._prepare_translations(df)
            df.to_csv(config.TRANSLATED_FILE, index=False, sep=';', encoding='utf-8-sig')
        else:
            raise FileNotFoundError("Nenalezen žádný vstupní soubor!")

        return df