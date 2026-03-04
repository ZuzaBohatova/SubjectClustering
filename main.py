# main.py
from data_loader import DataLoader
from text_processor import TextProcessor
from clustering import ClusteringEngine
from visualizer import ClusterVisualizer
import warnings
import config

# Ignorovat varování o nekonzistenci stop-slov
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn.feature_extraction.text')

def main():
    # 1. Načtení dat (automaticky řeší raw/translated/completed i DB)
    loader = DataLoader()
    df = loader.load_data()

    # 2. Čištění textu
    processor = TextProcessor()
    print("Čistím texty pro AI...")
    df['clean_text'] = df['combined_text_translated'].apply(processor.clean_text_pipeline)
    
    # Filtr prázdných
    df = df[df['clean_text'].str.len() > 10].copy()

    # 3. Clusterizace
    engine = ClusteringEngine(processor.stop_words)
    X = engine.vectorize(df['clean_text'])
    df['cluster'] = engine.run_kmeans(df, X)
    df['cluster_name'] = engine.name_clusters(df, X)

    # 4. Vizualizace
    viz = ClusterVisualizer()
    viz.create_plot(df, X)
    
    print("Ukládám data pro dashboard...")
    df.to_csv(config.OUTPUT_CSV, index=False)

if __name__ == "__main__":
    main()