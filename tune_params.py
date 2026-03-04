from data_loader import DataLoader
from text_processor import TextProcessor
from optimizer import ClusterOptimizer
import pandas as pd
import warnings
import config

warnings.filterwarnings("ignore", category=UserWarning, module='sklearn.feature_extraction.text')

def main():
    print("Načítám data...")
    loader = DataLoader()
    df = loader.load_data()

    processor = TextProcessor()
    print("Čistím texty...")
    df['clean_text'] = df['combined_text_translated'].apply(processor.clean_text_pipeline)
    df = df[df['clean_text'].str.len() > 10].copy()

    param_grid = {
        'n_clusters': [55,60,65,70,75,80,90,95,100 ],
        'max_features': [5000, 7000, 10000],
        'min_df': [2, 5, 7, 10],
        'max_df': [0.11, 0.15, 0.2, 0.25, 0.3],
        'merge_small': [True],
        'min_cluster_size': [15, 20, 25, 30]
    }

    optimizer = ClusterOptimizer(df, processor.stop_words)
    results = optimizer.run_grid_search(param_grid)

    print("\nTop 10 konfigurací podle Silhouette Score:")
    print(results.head(10))

    results.to_csv(config.EXPERIMENT_RESULTS_CSV, index=False)
    
    best = results.iloc[0]
    print(f"\nVítězná konfigurace:")
    print(f"Clusters: {best['n_clusters']} (Final: {best['n_clusters_final']})")
    print(f"Silhouette: {best['silhouette']:.4f}")

if __name__ == "__main__":
    main()