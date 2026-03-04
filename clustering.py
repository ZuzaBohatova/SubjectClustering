# clustering.py
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import config

class ClusteringEngine:
    def __init__(self, stop_words):
        self.stop_words = stop_words
        self.vectorizer = None
        self.kmeans = None

    def vectorize(self, texts):
        print("Vektorizace (TF-IDF)...")
        self.vectorizer = TfidfVectorizer(
            max_features=config.MAX_FEATURES,
            stop_words=self.stop_words,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=config.TFIDF_MIN_DF,
            max_df=config.TFIDF_MAX_DF
        )
        X = self.vectorizer.fit_transform(texts)
        
        # aplikace vah
        X = self._apply_custom_weights(X)
        
        return X

    def _apply_custom_weights(self, X):
        if not config.KEYWORD_WEIGHTS:
            return X

        print("Aplikuji manuální váhy slov...")
        feature_names = self.vectorizer.get_feature_names_out()

        # Vytvoříme mapu: slovo -> index sloupce v matici
        vocab_map = {word: idx for idx, word in enumerate(feature_names)}
        
        # Upravíme váhy
        for word, weight in config.KEYWORD_WEIGHTS.items():
            # Slovo musí být malými písmeny
            clean_word = word.lower()
            
            if clean_word in vocab_map:
                col_idx = vocab_map[clean_word]
                print(f"   -> Boosting '{clean_word}': {weight}x")
                
                # Vynásobení celého sloupce v matici danou vahou
                X[:, col_idx] *= weight
            else:
                pass 
                
        return X

    def _merge_small_clusters(self, df, X, labels):
        df['cluster'] = labels
        counts = df['cluster'].value_counts()
        small = counts[counts < config.MIN_CLUSTER_SIZE].index.tolist()
        
        if not small: return labels

        print(f"Rozpouštím {len(small)} malých clusterů...")
        large_clusters = counts[counts >= config.MIN_CLUSTER_SIZE].index.tolist()
        large_centers = self.kmeans.cluster_centers_[large_clusters]
        
        new_labels = labels.copy()
        for cid in small:
            indices = np.where(labels == cid)[0]
            vectors = X[indices].toarray()
            for i, vec in zip(indices, vectors):
                dists = np.linalg.norm(large_centers - vec, axis=1)
                new_labels[i] = large_clusters[np.argmin(dists)]
        return new_labels

    def run_kmeans(self, df, X):
        print(f"Clusterizace do {config.NUM_CLUSTERS} skupin...")
        self.kmeans = KMeans(n_clusters=config.NUM_CLUSTERS, random_state=42, n_init=10)
        labels = self.kmeans.fit_predict(X)
        final_labels = self._merge_small_clusters(df, X, labels)
        return final_labels

    def name_clusters(self, df, X):
        print("Pojmenování clusterů...")
        active_clusters = sorted(df['cluster'].unique())
        
        new_centers = []
        for cid in active_clusters:
            idx = np.where(df['cluster'] == cid)[0]
            new_centers.append(X[idx].mean(axis=0).A1)
        new_centers = np.array(new_centers)

        terms = self.vectorizer.get_feature_names_out()
        order_centroids = new_centers.argsort()[:, ::-1]
        labels_map = {}

        for i, cid in enumerate(active_clusters):
            # Získáme 3 nejčastější slova
            top_terms = [terms[ind] for ind in order_centroids[i, :3]]
            keywords = ", ".join(top_terms) 
            
            # Najdeme centroid (reprezentativní předmět)
            idx = np.where(df['cluster'] == cid)[0]
            vecs = X[idx].toarray()
            dists = np.linalg.norm(vecs - new_centers[i], axis=1)
            
            # Použijeme název předmětu
            rep_title = df.iloc[idx[np.argmin(dists)]]['title']
            
            if rep_title == "Matematika pro chemiky I":
                rep_title = "Matematická analýza 3"
            # zkrácení názvu na 40 znaků
            if len(rep_title) > 40:
                rep_title = rep_title[:40] + "..."
            
            # Sestavíme nový název: Předmět (slovo1, slovo2, slovo3)
            labels_map[cid] = f"{rep_title} ({keywords})"
            print(f"Cluster {cid}: {labels_map[cid]}")
            
        return df['cluster'].map(labels_map)