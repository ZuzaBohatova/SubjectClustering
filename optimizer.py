import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import itertools
from tqdm import tqdm 

class ClusterOptimizer:
    def __init__(self, df, stop_words):
        self.df = df
        self.stop_words = stop_words
        self.results = []

    def run_grid_search(self, param_grid):
        keys, values = zip(*param_grid.items())
        combinations = [dict(zip(keys, v)) for v in itertools.product(*values)]
        
        print(f"Spouštím testování {len(combinations)} kombinací...")

        for params in tqdm(combinations):
            result = self._evaluate_params(params)
            self.results.append(result)

        results_df = pd.DataFrame(self.results)
        return results_df.sort_values(by="silhouette", ascending=False)

    def _evaluate_params(self, params):
        try:
            vectorizer = TfidfVectorizer(
                max_features=params['max_features'],
                stop_words=self.stop_words,
                ngram_range=(1, 2),
                sublinear_tf=True,
                min_df=params.get('min_df', 5),
                max_df=params.get('max_df', 0.5)
            )
            X = vectorizer.fit_transform(self.df['clean_text'])

            kmeans = KMeans(
                n_clusters=params['n_clusters'], 
                random_state=42, 
                n_init=10
            )
            labels = kmeans.fit_predict(X)

            if params.get('merge_small', False):
                labels = self._simulate_merge_small(self.df, X, labels, kmeans, params.get('min_cluster_size', 20))

            unique_labels = np.unique(labels)
            if len(unique_labels) < 2:
                return {**params, "silhouette": -1, "n_clusters_final": len(unique_labels)}

            # Výpočet Silhouette Score
            sil = silhouette_score(X, labels)

            return {
                **params,
                "n_clusters_final": len(unique_labels),
                "silhouette": sil
            }

        except Exception as e:
            print(f"Chyba při parametrech {params}: {e}")
            return {**params, "error": str(e)}

    def _simulate_merge_small(self, df, X, labels, kmeans, min_size):
        df_temp = df.copy()
        df_temp['cluster'] = labels
        counts = df_temp['cluster'].value_counts()
        small = counts[counts < min_size].index.tolist()
        
        if not small: return labels

        large_clusters = counts[counts >= min_size].index.tolist()
        if not large_clusters: return labels

        large_centers = kmeans.cluster_centers_[large_clusters]
        new_labels = labels.copy()
        
        for cid in small:
            indices = np.where(labels == cid)[0]
            # Výpočet vzdáleností k centrům velkých clusterů
            vectors = X[indices].toarray()
            for i, vec in zip(indices, vectors):
                dists = np.linalg.norm(large_centers - vec, axis=1)
                new_labels[i] = large_clusters[np.argmin(dists)]
        
        return new_labels