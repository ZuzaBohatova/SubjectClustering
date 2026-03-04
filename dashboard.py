# dashboard.py
import pandas as pd
import plotly.express as px
import config
from dash import Dash, dcc, html, Input, Output
import colorcet


# --- NAČTENÍ DAT ---
try:
    df = pd.read_csv(config.OUTPUT_CSV)
    available_garants = sorted(df['garant'].dropna().astype(str).unique())
except:
    print("Chyba: Soubor "+config.OUTPUT_CSV+" nenalezen. Spusťte nejprve main.py!")
    exit()

# --- INICIALIZACE APLIKACE ---
app = Dash(__name__)
app.title = "Mapa předmětů MFF UK"

# Definice stylů
styles = {
    'fontFamily': 'Arial, sans-serif',
    'containerPadding': '20px',
    'sidebarWidth': '300px',
    'controlMargin': '20px'
}

# --- ROZLOŽENÍ (LAYOUT) ---
app.layout = html.Div(style={'fontFamily': styles['fontFamily'], 'padding': styles['containerPadding']}, children=[
    
    # Hlavní nadpis - zarovnán doleva
    html.H1("Interaktivní mapa předmětů MFF UK", 
            style={'textAlign': 'left', 'marginBottom': '30px', 'color': '#333'}),
    
    # Hlavní kontejner s Flexboxem (Sidebar vlevo, Graf vpravo)
    html.Div(style={'display': 'flex', 'flexDirection': 'row', 'gap': '30px'}, children=[
        
        # ---- LEVÝ POSTŘANNÍ PANEL (OVLÁDÁNÍ) ----
        html.Div(style={'width': styles['sidebarWidth'], 'flexShrink': 0}, children=[
            
            # Vyhledávání
            html.Div(style={'marginBottom': styles['controlMargin']}, children=[
                html.Label("🔍 Hledat předmět (název nebo kód):", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Input(
                    id='search-input', 
                    type='text', 
                    placeholder='Např. NPRG013 nebo Java', 
                    style={'width': '100%', 'padding': '10px', 'boxSizing': 'border-box', 'borderRadius': '5px', 'border': '1px solid #ccc'}
                )
            ]),
            
            # Filtr Garantů (pod sebou)
            html.Div(children=[
                html.Label("🎓 Filtrovat podle garanta:", style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='garant-dropdown',
                    options=[{'label': g, 'value': g} for g in available_garants],
                    placeholder="Vyberte garanty...",
                    multi=True,
                    style={'width': '100%'} 
                )
            ]),
        ]),

        # ---- GRAF ----
        html.Div(style={'flexGrow': 1, 'height': '85vh', 'border': '1px solid #eee', 'borderRadius': '5px', 'padding': '5px'}, children=[
            dcc.Graph(id='cluster-graph', style={'height': '100%'}, config={'displayModeBar': True})
        ])
    ])
])

# --- LOGIKA  ---
@app.callback(
    Output('cluster-graph', 'figure'),
    [Input('search-input', 'value'),
     Input('garant-dropdown', 'value')]
)
def update_graph(search_term, selected_garants):
    filtered_df = df.copy()
    
    # 1. Filtrace podle garanta
    if selected_garants:
        filtered_df = filtered_df[filtered_df['garant'].astype(str).isin(selected_garants)]
    
    # 2. Filtrace podle vyhledávání
    if search_term:
        search_term = search_term.lower()
        mask = (
            filtered_df['title'].fillna('').str.lower().str.contains(search_term) | 
            filtered_df['code'].fillna('').str.lower().str.contains(search_term)
        )
        filtered_df = filtered_df[mask]

    # Vytvoření grafu
    if filtered_df.empty:
        fig = px.scatter(title="Žádná data nenalezena pro zadaná kritéria.")
        fig.update_layout(xaxis={'visible': False}, yaxis={'visible': False}, template='plotly_white')
    else:
        # Určení barevné palety
        n_clusters = filtered_df['cluster_name'].nunique()
        palette = colorcet.glasbey
        
        fig = px.scatter(
            filtered_df, x='x', y='y',
            color='cluster_name',
            hover_data={'x': False, 'y': False, 'code': True, 'title': True, 'garant': True},
            template='plotly_white', 
            title=f"Nalezeno {len(filtered_df)} předmětů",
            color_discrete_sequence=palette
        )
        
        fig.update_traces(marker=dict(size=8, opacity=0.8, line=dict(width=0)))
        
        # Skrytí os a mřížky
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        
        fig.update_layout(margin=dict(r=200))
    return fig

# --- SPUŠTĚNÍ ---
if __name__ == '__main__':
    print("Spouštím dashboard na http://127.0.0.1:8050/")
    app.run(debug=True)