import requests
import pandas as pd
import streamlit as st
from PIL import Image

# Configure the page layout to wide
st.set_page_config(layout="wide")

# Your YouTube Data API v3 key
API_KEY = 'AIzaSyBPXBNpYVDB-w2V8BmV9WqWzB7UANH4A6g'

# Load the logo image
logo_path = 'ALE-MICROSITE.jpg'  # Make sure this file is in the same directory as your script
logo = Image.open(logo_path)

# Function to get the videos in a playlist
def get_playlist_videos(playlist_id):
    videos = []
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&key={API_KEY}&part=snippet&maxResults=50"
    response = requests.get(url).json()

    if 'items' in response:
        videos.extend(response['items'])

    while 'nextPageToken' in response:
        nextPageToken = response['nextPageToken']
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&key={API_KEY}&part=snippet&maxResults=50&pageToken={nextPageToken}"
        response = requests.get(url).json()
        if 'items' in response:
            videos.extend(response['items'])

    return videos

# Function to get video stats
def get_video_stats(video_id):
    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={API_KEY}&part=statistics'
    response = requests.get(url).json()
    if 'items' in response and len(response['items']) > 0:
        statistics = response['items'][0]['statistics']
        return statistics.get('viewCount', '0')
    return '0'

# Playlist IDs to get data from (Example)
playlists = {
    "Spacewalkers": "PL-mHF9yP7tLC5aEgEP3z3cBXfFAKcB2OA",
    "Perfect Blend OVNA": "PL-mHF9yP7tLDRCNBKkwJc85vodgc7Kws4",
    "Networking IoT": "PL837C80A0F53215EF"
    # Add more playlists as needed
}

# Sidebar for selecting the playlist
st.sidebar.title("Select Playlist")
selected_playlist = st.sidebar.radio("Playlists", list(playlists.keys()))

# Main content with logo and title
col1, col2 = st.columns([1, 9])
with col1:
    st.image(logo, width=100)
with col2:
    st.title(f"{selected_playlist}")

# Get the videos for the selected playlist
playlist_id = playlists[selected_playlist]
videos = get_playlist_videos(playlist_id)

# Create a list to store video data
videos_data = []

for video in videos:
    video_id = video['snippet']['resourceId']['videoId']
    title = video['snippet']['title']
    published_at = video['snippet']['publishedAt']
    view_count = get_video_stats(video_id)
    videos_data.append({
        'Video Title': title,
        'View Count': int(view_count),
        'Video Publish Date': pd.to_datetime(published_at).date(),
        'LINK': f"https://www.youtube.com/watch?v={video_id}"
    })

# Convert the list to a DataFrame
df = pd.DataFrame(videos_data)

# Check if the 'LINK' column is present before applying the function
if 'LINK' in df.columns:
    # Function to make links clickable
    def make_clickable(link):
        return f'<a href="{link}" target="_blank">{link}</a>'

    # Apply the make_clickable function to the LINK column
    df['LINK'] = df['LINK'].apply(make_clickable)

# Verify the column name and sort the DataFrame by publication date in descending order
if 'Video Publish Date' in df.columns:
    df = df.sort_values(by='Video Publish Date', ascending=False)

# Reindex the DataFrame
df = df.reset_index(drop=True)

# Calculate the total view count
total_views = df['View Count'].sum()

# Display the total view count in bold
st.markdown(f"**Total View Count: {total_views}**")

# Apply alternating row colors
styled_df = df.style.apply(
    lambda x: ['background-color: #f9f9f9' if i % 2 == 0 else 'background-color: #f0f0f0' for i in range(len(x))],
    axis=0
)

# Display the video data in a styled table, making sure it fills the width of the page
st.write(styled_df.set_table_styles(
    [{'selector': 'table', 'props': [('width', '100%')]}]
).to_html(escape=False), unsafe_allow_html=True)
