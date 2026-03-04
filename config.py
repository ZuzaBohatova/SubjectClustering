# config.py

# Soubory
RAW_INPUT_FILE = "./data/courses_export_cs_en.csv"
TRANSLATED_FILE = "./data/courses_translated.csv"
OUTPUT_HTML = "cluster_map_params.html"
OUTPUT_CSV = "./data/clustering_data_params.csv"
EXPERIMENT_RESULTS_CSV = "./data/clustering_results.csv"


# Databáze
DB_CONNECTION = "postgresql://postgres:postgres@localhost:5432/recsis"

# Parametry clusterizace
NUM_CLUSTERS = 95
MIN_CLUSTER_SIZE = 15 # Sloučit clustery menší než toto číslo
MAX_FEATURES = 7000
TFIDF_MAX_DF = 0.3
TFIDF_MIN_DF = 10

# Zakázané podřetězce (balast)
FORBIDDEN_SUBSTRINGS = [
    'magist', 'bakalar', 'seminar', 'doktor', 'kurz', 'kurs', 'aktualn', 
    'diplom', 'kredit', 'zkousk', 'zapocet', 'anotac', 'sylabus', 'univerzit',
    'prednas', 'student', 'zapis', 'kapacit', 'duvod', 'soucasn', 'pasov',
    'vyberov', 'vyber', 'hodin', 'ukazk', 'rozbor', 'vysled', 'oblast', 
    'referat', 'stanoven', 'part', 'vybran', 'vyuk', 'zadan', 'tem', 'zapsat',
    'predmet', 'prac', 'event', 'lektor', 'pisemn', 'fakult', 'semestr', 'ruzn',
    'samostatn', 'ucitel', 'zkousek', 'vcetn', 'omezen', 'teoret', 'ucebn', 'odborn'
    'urcen', 'nejnovejs', 'cvicen', 'katedr', 'ustav', 'venovan', 'temat', 'rocnik',
    'prakt', 'studijn', 'voliteln', 'prubeh', 'obsah', 'konzultac', 'vedouc', 'prax'
]

# Změna váhy slov
KEYWORD_WEIGHTS = {
    'pedagog': 2.0,
}