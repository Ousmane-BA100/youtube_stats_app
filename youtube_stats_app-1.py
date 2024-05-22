import streamlit as st
import pandas as pd
import requests
import plotly.express as px

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
            view_count = int(statistics['viewCount']) # Convertir en entier
            return view_count
        else:
            return None
    else:
        return None

# Lire le fichier Excel et sélectionner les colonnes nécessaires
df = pd.read_excel(r'C:\Users\oba3994\Downloads\Nombre vue youtube\youtube-report-2024_new.xls', sheet_name='Networking', usecols=['Content', 'Video title', 'LINK'])

# Renommer la colonne 'Content' en 'video_id'
df.rename(columns={'Content': 'video_id'}, inplace=True)

# Création d'une colonne pour stocker les vues de chaque vidéo
df['View Count'] = df['video_id'].apply(lambda x: get_video_stats(x))

# Supprimer les lignes avec des vues manquantes
df = df.dropna(subset=['View Count'])

# Identifier le nombre maximal de vues parmi toutes les vidéos
max_view_count = 30000

# Filtrer le DataFrame pour exclure les vidéos avec un nombre de vues supérieur au maximum
filtered_df = df[df['View Count'] < max_view_count]

# Affichage du DataFrame filtréSS
st.write("Données après filtrage des vidéos avec plus de vues que toutes les autres :")
st.write(filtered_df)

# Création du graphique à barres avec une taille de barre augmentée
fig = px.bar(filtered_df, x='Video title', y='View Count', title='Nombre de vues par vidéo', range_y=[0, filtered_df['View Count'].max()*1.1], barmode='group', width=10) # Valeur modifiée à 10
st.plotly_chart(fig, use_container_width=True)




