# visualizer.py
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import plotly.express as px
import config
import colorcet

class ClusterVisualizer:
    def create_plot(self, df, X):
        print("Počítám vizualizaci (PCA + t-SNE)...")
        
        pca = PCA(n_components=50, random_state=42)
        X_pca = pca.fit_transform(X.toarray())
        
        tsne = TSNE(n_components=2, random_state=42, perplexity=40, init='pca', learning_rate='auto')
        X_embedded = tsne.fit_transform(X_pca)
        
        df['x'] = X_embedded[:, 0]
        df['y'] = X_embedded[:, 1]
        
        print("Generuji HTML...")
        fig = px.scatter(
            df, x='x', y='y', 
            color='cluster_name', 
            hover_data=['code', 'title', 'garant'],
            title=f'Mapa předmětů MFF UK',
            template='plotly_white',
            color_discrete_sequence=colorcet.glasbey
        )
        
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_traces(marker=dict(
            size=8, 
            opacity=0.8,
        ))
        
        fig.write_html(config.OUTPUT_HTML)
        print(f"Hotovo! Graf uložen do '{config.OUTPUT_HTML}'.")