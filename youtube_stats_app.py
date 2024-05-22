import streamlit as st
import pandas as pd
import requests
import datetime as dt

# Remplacez 'YOUR_API_KEY' par votre clé API YouTube Data API v3
API_KEY = 'AIzaSyBPXBNpYVDB-w2V8BmV9WqWzB7UANH4A6g'

# Fonction pour récupérer les statistiques d'une vidéo depuis l'API YouTube
def get_video_stats(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=statistics'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            statistics = data['items'][0]['statistics']
            view_count = statistics['viewCount']
            return view_count
        else:
            return None
    else:
        return None

# Lire le fichier Excel et sélectionner les colonnes nécessaires
df = pd.read_excel(
    'https://github.com/Ousmane-BA100/youtube_stats_app/raw/main/youtube-report-2024_new.xls', 
    sheet_name='Networking', 
    usecols=['Content', 'Video title', 'Video publish time', 'LINK'], 
    engine='xlrd'
)

# Renommer la colonne 'Content' en 'video_id'
df.rename(columns={'Content': 'video_id'}, inplace=True)

# Interface utilisateur Streamlit
st.title('YouTube Video Views')

# Convertir la colonne 'Video publish time' en datetime
df['Video publish time'] = pd.to_datetime(df['Video publish time'])

# Création d'une liste pour stocker les données de vue de chaque vidéo
views_data = []

# Parcourir chaque ligne du DataFrame pour récupérer les vues de chaque vidéo
for index, row in df.iterrows():
    video_id = row['video_id']
    video_title = row['Video title']
    view_count = get_video_stats(video_id)
    if view_count is not None:
        views_data.append((video_title, int(view_count)))
    else:
        views_data.append((video_title, 0))

# Ajouter les données de vue au DataFrame
df['View Count'] = [view[1] for view in views_data]

# Trier le DataFrame par ordre décroissant en fonction de la date de publication
df_sorted = df.sort_values(by='Video publish time', ascending=False)

# Réindexer le DataFrame dans l'ordre
df_sorted = df_sorted.reset_index(drop=True)

# Affichage des données de vue sous forme de tableau
if not df_sorted.empty:
    st.subheader('Vues de chaque vidéo (trié par date de publication décroissante) :')
    st.table(df_sorted)
else:
    st.write("Aucune donnée de vue disponible.")
