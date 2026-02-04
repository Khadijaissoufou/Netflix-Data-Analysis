# CODE FINAL - APPLICATION STREAMLIT COMPLÈTE

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import warnings
import os

warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Analyse Netflix - Évolution des Genres",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS minimaliste et professionnel
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        color: #E50914;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E50914;
    }
    .section-title {
        font-size: 1.5rem;
        color: #333333;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid #E50914;
        margin-bottom: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #E50914;
    }
    .stButton button {
        background-color: #E50914;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #B20710;
    }
</style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown('<div class="main-title">Analyse Netflix - Évolution des Genres par Pays</div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #666666; font-size: 1rem; margin-bottom: 2rem; line-height: 1.5;">
Étude de l'évolution des genres et comparaison des tendances entre pays (1925-2021)<br>
Base de données : Netflix Movies and TV Shows (Kaggle)
</div>
""", unsafe_allow_html=True)

# Fonction de chargement des données
@st.cache_data
def load_data():
    """Charge les données nettoyées depuis le fichier CSV"""
    try:
        # Essayer plusieurs chemins possibles
        possible_paths = [
            "netflix_titles_cleaned.csv",  # Même dossier
            os.path.join(os.path.dirname(__file__), "netflix_titles_cleaned.csv"),  # Dossier de l'app
            os.path.expanduser("~/Documents/Seminaire/netflix_titles_cleaned.csv"),  # Dossier utilisateur
            "C:/Users/Mahamadou.Is Khadija/OneDrive/Documents/Seminaire/netflix_titles_cleaned.csv"  # Chemin complet
        ]
        
        df = None
        for path in possible_paths:
            try:
                if os.path.exists(path):
                    df = pd.read_csv(path, encoding='utf-8')
                    st.sidebar.success(f"Données chargées depuis : {path}")
                    break
            except:
                continue
        
        if df is None:
            st.error("Fichier netflix_titles_cleaned.csv non trouvé.")
            st.info("""
            Veuillez :
            1. Placer le fichier dans le même dossier que cette application
            2. Vérifier le chemin d'accès au fichier
            """)
            return pd.DataFrame()
        
        # Conversion des types de données
        # Colonnes datetime
        date_columns = ['date_added']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Colonnes numériques
        numeric_columns = ['release_year', 'year_added', 'month_added', 
                          'duration_min', 'duration_seasons', 'decade']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Conversion des colonnes de listes
        def convert_to_list(value):
            if pd.isna(value):
                return []
            if isinstance(value, list):
                return value
            if isinstance(value, str):
                if value == '[]' or value == '':
                    return []
                try:
                    import ast
                    return ast.literal_eval(value)
                except:
                    items = [item.strip() for item in value.split(',')]
                    return [item for item in items if item]
            return []
        
        list_columns = ['genres_list', 'countries_list', 'cast_list', 'director_list']
        for col in list_columns:
            if col in df.columns:
                df[col] = df[col].apply(convert_to_list)
        
        return df
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        return pd.DataFrame()

# Chargement des données
with st.spinner('Chargement des données en cours...'):
    df = load_data()

if df.empty:
    st.stop()

# Barre latérale - Filtres
st.sidebar.title("Configuration de l'analyse")

# Informations sur le dataset
st.sidebar.markdown(f"""
**Caractéristiques du jeu de données :**
- **Nombre total d'entrées :** {len(df):,}
- **Nombre de colonnes :** {df.shape[1]}
- **Période couverte :** {int(df['release_year'].min())} - {int(df['release_year'].max())}
- **Types de contenu :** {df['type'].nunique()}
""")

# Sélection du type de contenu
st.sidebar.markdown("**Filtrage par type de contenu**")
content_type = st.sidebar.multiselect(
    "Sélectionner le type :",
    options=['Movie', 'TV Show'],
    default=['Movie', 'TV Show']
)

# Sélection de la période
st.sidebar.markdown("**Filtrage temporel**")
year_range = st.sidebar.slider(
    "Sélectionner la période d'analyse :",
    min_value=int(df['release_year'].min()),
    max_value=int(df['release_year'].max()),
    value=(2000, 2021)
)

# Extraction des pays pour le filtre
all_countries = []
for countries in df['countries_list']:
    all_countries.extend(countries)

country_counts = Counter(all_countries)
top_countries = sorted([country for country, _ in country_counts.most_common(20)])

st.sidebar.markdown("**Sélection des pays**")
selected_countries = st.sidebar.multiselect(
    "Choisir les pays à analyser :",
    options=top_countries,
    default=['United States', 'India', 'United Kingdom', 'Canada', 'France', 'Japan']
)

# Extraction des genres pour le filtre
all_genres = []
for genres in df['genres_list']:
    all_genres.extend(genres)

genre_counts = Counter(all_genres)
top_genres = sorted([genre for genre, _ in genre_counts.most_common(15)])

st.sidebar.markdown("**Sélection des genres**")
selected_genres = st.sidebar.multiselect(
    "Choisir les genres à analyser :",
    options=top_genres,
    default=['Dramas', 'Comedies', 'Action & Adventure', 'Documentaries', 'International Movies']
)

# Application des filtres
filtered_df = df.copy()

# Filtre par type
if content_type:
    filtered_df = filtered_df[filtered_df['type'].isin(content_type)]

# Filtre par période
filtered_df = filtered_df[
    (filtered_df['release_year'] >= year_range[0]) & 
    (filtered_df['release_year'] <= year_range[1])
]

# Filtre par pays
if selected_countries:
    mask = filtered_df['country'].apply(
        lambda x: any(country in str(x) for country in selected_countries) if pd.notna(x) else False
    )
    filtered_df = filtered_df[mask]

# Filtre par genres
if selected_genres:
    mask = filtered_df['listed_in'].apply(
        lambda x: any(genre in str(x) for genre in selected_genres) if pd.notna(x) else False
    )
    filtered_df = filtered_df[mask]

# Section 1 : Vue d'ensemble
st.markdown('<div class="section-title">Vue d\'ensemble des données filtrées</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-container'>
        <div style='font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;'>Productions totales</div>
        <div style='font-size: 2rem; font-weight: 700; color: #E50914;'>{len(filtered_df):,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    films_count = len(filtered_df[filtered_df['type'] == 'Movie'])
    st.markdown(f"""
    <div class='metric-container'>
        <div style='font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;'>Films</div>
        <div style='font-size: 2rem; font-weight: 700; color: #E50914;'>{films_count:,}</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.2rem;'>
            {films_count/len(filtered_df)*100:.1f}% du total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    series_count = len(filtered_df[filtered_df['type'] == 'TV Show'])
    st.markdown(f"""
    <div class='metric-container'>
        <div style='font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;'>Séries TV</div>
        <div style='font-size: 2rem; font-weight: 700; color: #E50914;'>{series_count:,}</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.2rem;'>
            {series_count/len(filtered_df)*100:.1f}% du total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_year = filtered_df['release_year'].mean()
    st.markdown(f"""
    <div class='metric-container'>
        <div style='font-size: 1.2rem; font-weight: 600; color: #333; margin-bottom: 0.5rem;'>Année moyenne</div>
        <div style='font-size: 2rem; font-weight: 700; color: #E50914;'>{int(avg_year)}</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 0.2rem;'>
            Période : {int(filtered_df['release_year'].min())} - {int(filtered_df['release_year'].max())}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Section 2 : Analyse temporelle
st.markdown('<div class="section-title">Analyse temporelle des productions</div>', unsafe_allow_html=True)

# Onglets pour différentes analyses temporelles
tab1, tab2, tab3 = st.tabs(["Évolution globale", "Comparaison par pays", "Analyse par genre"])

with tab1:
    # Évolution globale du nombre de productions
    yearly_counts = filtered_df['release_year'].value_counts().sort_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly_counts.index,
        y=yearly_counts.values,
        mode='lines+markers',
        line=dict(color='#E50914', width=3),
        marker=dict(size=6, color='#E50914'),
        name='Nombre de productions'
    ))
    
    fig.update_layout(
        title=f'Évolution du nombre de productions ({year_range[0]}-{year_range[1]})',
        xaxis_title="Année",
        yaxis_title="Nombre de productions",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Comparaison de l'évolution entre pays
    if selected_countries:
        fig = go.Figure()
        
        colors = ['#E50914', '#221F1F', '#564d4d', '#808080', '#A9A9A9']
        
        for i, country in enumerate(selected_countries[:5]):
            mask = filtered_df['country'].str.contains(country, na=False)
            country_counts = filtered_df[mask]['release_year'].value_counts().sort_index()
            
            fig.add_trace(go.Scatter(
                x=country_counts.index,
                y=country_counts.values,
                mode='lines+markers',
                name=country,
                line=dict(width=2, color=colors[i % len(colors)]),
                marker=dict(size=5)
            ))
        
        fig.update_layout(
            title='Évolution comparée par pays',
            xaxis_title="Année",
            yaxis_title="Nombre de productions",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veuillez sélectionner au moins un pays dans la barre latérale pour afficher cette comparaison.")

with tab3:
    # Évolution des genres
    if selected_genres:
        fig = go.Figure()
        
        for genre in selected_genres[:5]:
            mask = filtered_df['listed_in'].str.contains(genre, na=False)
            genre_counts = filtered_df[mask]['release_year'].value_counts().sort_index()
            
            fig.add_trace(go.Scatter(
                x=genre_counts.index,
                y=genre_counts.values,
                mode='lines+markers',
                name=genre,
                line=dict(width=2),
                marker=dict(size=5)
            ))
        
        fig.update_layout(
            title='Évolution de la popularité des genres',
            xaxis_title="Année",
            yaxis_title="Nombre de productions",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veuillez sélectionner au moins un genre dans la barre latérale pour afficher cette analyse.")

# Section 3 : Analyse comparative entre pays
if selected_countries and len(selected_countries) >= 2:
    st.markdown('<div class="section-title">Analyse comparative entre pays</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Heatmap de popularité des genres par pays
        heatmap_data = []
        
        for country in selected_countries[:6]:
            mask = filtered_df['country'].str.contains(country, na=False)
            country_df = filtered_df[mask]
            
            country_genres = []
            for genres in country_df['genres_list']:
                country_genres.extend(genres)
            
            genre_counts = Counter(country_genres)
            country_row = {'Pays': country}
            
            # Prendre les genres les plus populaires pour ce pays
            for genre, count in genre_counts.most_common(8):
                if genre in selected_genres[:8]:
                    country_row[genre] = count
            
            heatmap_data.append(country_row)
        
        if heatmap_data:
            heatmap_df = pd.DataFrame(heatmap_data).set_index('Pays').fillna(0)
            
            fig = px.imshow(
                heatmap_df,
                labels=dict(x="Genres", y="Pays", color="Nombre de productions"),
                title="Popularité des genres par pays",
                color_continuous_scale='Reds',
                aspect='auto'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Répartition Films vs Séries par pays
        type_data = []
        
        for country in selected_countries[:5]:
            mask = filtered_df['country'].str.contains(country, na=False)
            country_df = filtered_df[mask]
            
            movies = len(country_df[country_df['type'] == 'Movie'])
            shows = len(country_df[country_df['type'] == 'TV Show'])
            total = movies + shows
            
            if total > 0:
                type_data.append({
                    'Pays': country,
                    'Type': 'Films',
                    'Pourcentage': (movies / total) * 100
                })
                type_data.append({
                    'Pays': country,
                    'Type': 'Séries TV',
                    'Pourcentage': (shows / total) * 100
                })
        
        if type_data:
            type_df = pd.DataFrame(type_data)
            
            fig = px.bar(
                type_df,
                x='Pays',
                y='Pourcentage',
                color='Type',
                barmode='stack',
                color_discrete_map={'Films': '#E50914', 'Séries TV': '#221F1F'},
                title="Répartition Films vs Séries TV par pays",
                labels={'Pourcentage': 'Pourcentage (%)'}
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# Section 4 : Observations et tendances
st.markdown('<div class="section-title">Observations et tendances</div>', unsafe_allow_html=True)

# Calculer des statistiques intéressantes
observations = []

# 1. Genre dominant
if len(filtered_df) > 0:
    all_filtered_genres = []
    for genres in filtered_df['genres_list']:
        all_filtered_genres.extend(genres)
    
    if all_filtered_genres:
        genre_counter = Counter(all_filtered_genres)
        top_genre, top_count = genre_counter.most_common(1)[0]
        observations.append(f"**Genre le plus populaire** : {top_genre} ({top_count} occurrences)")

# 2. Pays dominant
if selected_countries:
    country_stats = []
    for country in selected_countries:
        mask = filtered_df['country'].str.contains(country, na=False)
        count = filtered_df[mask].shape[0]
        if count > 0:
            country_stats.append((country, count))
    
    if country_stats:
        top_country = max(country_stats, key=lambda x: x[1])
        observations.append(f"**Pays le plus représenté** : {top_country[0]} ({top_country[1]} productions)")

# 3. Tendance temporelle
if len(filtered_df) >= 2:
    earliest_year = filtered_df['release_year'].min()
    latest_year = filtered_df['release_year'].max()
    
    earliest_count = filtered_df[filtered_df['release_year'] == earliest_year].shape[0]
    latest_count = filtered_df[filtered_df['release_year'] == latest_year].shape[0]
    
    if earliest_count > 0:
        growth_rate = ((latest_count - earliest_count) / earliest_count) * 100
        observations.append(f"**Tendance** : {growth_rate:+.1f}% de variation entre {int(earliest_year)} et {int(latest_year)}")

# 4. Durée moyenne des films
films_df = filtered_df[filtered_df['type'] == 'Movie']
if len(films_df) > 0 and 'duration_min' in films_df.columns:
    avg_duration = films_df['duration_min'].mean()
    if not pd.isna(avg_duration):
        observations.append(f"**Durée moyenne des films** : {avg_duration:.1f} minutes")

# Afficher les observations
if observations:
    for obs in observations:
        st.markdown(f"""
        <div class='info-box'>
            {obs}
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Les filtres actuels ne permettent pas de générer des observations significatives.")

# Section 5 : Exploration des données
st.markdown('<div class="section-title">Exploration des données</div>', unsafe_allow_html=True)

with st.expander("Afficher les statistiques descriptives", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Distribution par année**")
        year_dist = filtered_df['release_year'].value_counts().sort_index()
        st.dataframe(
            year_dist.reset_index().rename(columns={'release_year': 'Année', 'count': 'Nombre'}).head(15),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        if selected_countries:
            st.markdown("**Distribution par pays**")
            country_dist = []
            for country in selected_countries:
                mask = filtered_df['country'].str.contains(country, na=False)
                count = filtered_df[mask].shape[0]
                if count > 0:
                    country_dist.append((country, count))
            
            if country_dist:
                country_df = pd.DataFrame(country_dist, columns=['Pays', 'Nombre'])
                st.dataframe(
                    country_df.sort_values('Nombre', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )

with st.expander("Afficher un échantillon des données filtrées", expanded=False):
    display_cols = ['title', 'type', 'release_year', 'country', 'rating', 'duration', 'listed_in']
    available_cols = [col for col in display_cols if col in filtered_df.columns]
    
    st.dataframe(
        filtered_df[available_cols].head(30),
        use_container_width=True,
        height=400
    )

# Section 6 : Export des résultats
st.markdown('<div class="section-title">Export des résultats</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Téléchargement des données**")
    st.markdown("""
    Exportez les données filtrées au format CSV pour une analyse ultérieure
    ou pour les intégrer dans d'autres outils.
    """)
    
    # Conversion en CSV
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Télécharger les données filtrées",
        data=csv_data,
        file_name=f"donnees_netflix_filtrees_{year_range[0]}_{year_range[1]}.csv",
        mime="text/csv",
        help="Cliquez pour télécharger les données au format CSV"
    )

with col2:
    st.markdown("**Synthèse de l'analyse**")
    st.markdown("""
    Cette analyse interactive permet d'explorer :
    
    - L'évolution temporelle des productions Netflix
    - Les différences entre pays producteurs
    - La popularité des genres et son évolution
    - Les tendances du catalogue Netflix
    
    Les visualisations sont interactives et peuvent être zoomées,
    filtrées et exportées directement depuis l'interface.
    """)

# Pied de page
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666666; font-size: 0.9rem; padding: 1rem 0;">
    <div style="font-weight: 600; margin-bottom: 0.5rem;">Analyse Netflix - Projet d'analyse de données</div>
    <div>Source des données : Dataset Kaggle "Netflix Movies and TV Shows"</div>
    <div style="margin-top: 0.5rem;">Technologies utilisées : Python, Pandas, Streamlit, Plotly</div>
</div>
""", unsafe_allow_html=True)