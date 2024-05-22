import streamlit as st
import pandas as pd
import requests
import datetime as dt

# Remplacez 'YOUR_API_KEY' par votre clé API YouTube Data API v3
API_KEY = 'AIzaSyBPXBNpYVDB-w2V8BmV9WqWzB7UANH4A6g'

# Fonction pour récupérer les statistiques d'une vidéo depuis l'API YouTube
def get_video_stats(video_id):
    # URL de l'API YouTube Data API v3 pour récupérer les statistiques d'une vidéo
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=statistics'

    # Effectuer une requête GET à l'API
    response = requests.get(url)

    # Vérifier si la requête a réussi (code de statut 200)
    if response.status_code == 200:
        # Convertir la réponse en JSON
        data = response.json()
        # Vérifier si la clé 'items' existe dans la réponse et si elle contient des éléments
        if 'items' in data and len(data['items']) > 0:
            # Récupérer les statistiques de la vidéo (y compris le nombre de vues)
            statistics = data['items'][0]['statistics']
            view_count = statistics['viewCount']
            return view_count
        else:
            return None
    else:
        return None

# Lire le fichier Excel et sélectionner les colonnes nécessaires
df = pd.read_excel('https://github.com/Ousmane-BA100/youtube_stats_app/raw/main/youtube-report-2024_new.xlsx', sheet_name='Networking', usecols=['Content', 'Video title', 'Video publish time', 'LINK'], engine='openpyxl')

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
        # Si aucune statistique n'est disponible pour cette vidéo, ajoutez 0 comme valeur de vue
        views_data.append((video_title, 0))

# Ajouter les données de vue au DataFrame
df['View Count'] = [view[1] for view in views_data]

# Calculer les vues par trimestre pour l'année en cours
current_year = dt.datetime.now().year

df['views Q1'] = df.apply(lambda x: x['View Count'] if x['Video publish time'].year == current_year and x['Video publish time'].quarter == 1 else 0, axis=1)
df['views Q2'] = df.apply(lambda x: x['View Count'] if x['Video publish time'].year == current_year and x['Video publish time'].quarter == 2 else 0, axis=1)
df['views Q3'] = df.apply(lambda x: x['View Count'] if x['Video publish time'].year == current_year and x['Video publish time'].quarter == 3 else 0, axis=1)
df['views Q4'] = df.apply(lambda x: x['View Count'] if x['Video publish time'].year == current_year and x['Video publish time'].quarter == 4 else 0, axis=1)

# Trier le DataFrame par ordre décroissant en fonction du 'Video publish time'
df_sorted = df.sort_values(by='Video publish time', ascending=False)

# Réindexer le DataFrame dans l'ordre
df_sorted = df_sorted.reset_index(drop=True)

# Affichage des données de vue sous forme de tableau
if not df_sorted.empty:
    st.subheader('Vues de chaque vidéo (trié par date de publication) :')
    st.table(df_sorted)
else:
    st.write("Aucune donnée de vue disponible.")
