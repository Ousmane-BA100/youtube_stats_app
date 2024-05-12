import streamlit as st
import pandas as pd
import requests

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
        # Récupérer les statistiques de la vidéo (y compris le nombre de vues)
        statistics = data['items'][0]['statistics']
        view_count = statistics['viewCount']
        return view_count
    else:
        return None

# Lire le fichier Excel et sélectionner les colonnes nécessaires
df = pd.read_excel(r'C:\Users\oba3994\Downloads\Nombre vue youtube\youtube-report-2024_new.xls', usecols=['Content', 'Video title', 'LINK'])

# Renommer la colonne 'Content' en 'video_id'
df.rename(columns={'Content': 'video_id'}, inplace=True)

# Interface utilisateur Streamlit
st.title('YouTube Video Views')

# Affichage du DataFrame
st.subheader('Contenu du fichier Excel :')
st.write(df)

# Création d'une liste pour stocker les données de vue de chaque vidéo
views_data = []

# Parcourir chaque ligne du DataFrame pour récupérer les vues de chaque vidéo
for index, row in df.iterrows():
    video_id = row['video_id']
    video_title = row['Video title']
    view_count = get_video_stats(video_id)
    if view_count is not None:
        views_data.append((video_title, view_count))

# Affichage des données de vue sous forme de tableau
if views_data:
    st.subheader('Vues de chaque vidéo :')
    st.table(pd.DataFrame(views_data, columns=['Video Title', 'View Count']))
else:
    st.write("Aucune donnée de vue disponible.")
