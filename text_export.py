import pandas as pd
from sqlalchemy import create_engine
import config

class CourseExporter:
    def __init__(self):
        self.db_connection = config.DB_CONNECTION
        self.output_file = config.RAW_INPUT_FILE 

    def _get_sql_query(self):
        return """
        SELECT 
            p.povinn AS code,
            p.pnazev AS title,
            p.pgarant AS garant, -- PŘIDÁNO: Garant předmětu
            
            -- České verze
            anot_cz.memo AS annotation_cz,
            syl_cz.memo AS syllabus_cz,

            -- Anglické verze
            anot_en.memo AS annotation_en,
            syl_en.memo AS syllabus_en

        FROM recommender.povinn p
        
        JOIN recommender.searchable_povinn sp 
            ON p.povinn = sp.povinn
            
        -- 1. Anotace CZE
        LEFT JOIN recommender.pamela anot_cz 
            ON p.povinn = anot_cz.povinn 
            AND anot_cz.typ = 'A' 
            AND anot_cz.jazyk = 'CZE'

        -- 2. Anotace ENG
        LEFT JOIN recommender.pamela anot_en 
            ON p.povinn = anot_en.povinn 
            AND anot_en.typ = 'A' 
            AND anot_en.jazyk = 'ENG'

        -- 3. Sylabus CZE
        LEFT JOIN recommender.pamela syl_cz 
            ON p.povinn = syl_cz.povinn 
            AND syl_cz.typ = 'S' 
            AND syl_cz.jazyk = 'CZE'

        -- 4. Sylabus ENG
        LEFT JOIN recommender.pamela syl_en 
            ON p.povinn = syl_en.povinn 
            AND syl_en.typ = 'S' 
            AND syl_en.jazyk = 'ENG'
        """

    def run_export(self):
        print(f"Připojuji se k DB ({self.db_connection})...")
        
        try:
            engine = create_engine(self.db_connection)
            query = self._get_sql_query()
            
            print("⏳ Stahuji data...")
            df = pd.read_sql(query, engine)
            
            # Vyčištění NULL hodnot
            df.fillna("", inplace=True)

            print(f"\nStaženo {len(df)} předmětů.")
            print("-" * 50)
            print("Ukázka prvních 5 řádků:")
            print(df.head())
            print("-" * 50)
            
            # Uložení do CSV
            df.to_csv(self.output_file, index=False, encoding='utf-8-sig', sep=';')
            print(f"Data úspěšně uložena do souboru: '{self.output_file}'")
            
        except Exception as e:
            print(f"Chyba při exportu dat: {e}")

if __name__ == "__main__":
    exporter = CourseExporter()
    exporter.run_export()