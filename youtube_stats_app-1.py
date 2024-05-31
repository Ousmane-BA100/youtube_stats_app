import streamlit as st
import pandas as pd
import requests
import datetime as dt

# Configure the page layout to wide
st.set_page_config(layout="wide")

# Replace 'YOUR_API_KEY' with your YouTube Data API v3 key
API_KEY = 'AIzaSyBPXBNpYVDB-w2V8BmV9WqWzB7UANH4A6g'

# Function to get video stats from YouTube API
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
            st.write(f"No statistics found for video_id: {video_id}")
            return None
    else:
        st.write(f"Failed to fetch data for video_id: {video_id}, status code: {response.status_code}")
        return None

# Load the Excel file and create a dropdown to select the sheet
sheet_name = st.selectbox('**Select the worksheet**', ['Networking', 'Spacewalkers'], key='worksheet')

df = pd.read_excel(
    'https://github.com/Ousmane-BA100/youtube_stats_app/raw/main/youtube-report-2024_new.xls', 
    sheet_name=sheet_name, 
    usecols=['Content', 'Video title', 'Video publish time', 'LINK'], 
    engine='xlrd'
)

# Rename the 'Content' column to 'video_id'
df.rename(columns={'Content': 'video_id'}, inplace=True)

# Rename the 'Video publish time' column to 'video publication date'
df.rename(columns={'Video publish time': 'video publication date'}, inplace=True)

# Convert 'video publication date' column to datetime
df['video publication date'] = pd.to_datetime(df['video publication date']).dt.date

# Create a list to store view data for each video
views_data = []

# Iterate over each row in the DataFrame to get views for each video
for index, row in df.iterrows():
    video_id = row['video_id']
    video_title = row['Video title']
    view_count = get_video_stats(video_id)
    if view_count is not None:
        views_data.append((video_title, int(view_count)))
    else:
        views_data.append((video_title, 0))
    st.write(f"Fetched views for {video_title}: {view_count}")  # Debugging output

# Add view data to the DataFrame
df['View Count'] = [view[1] for view in views_data]

# Rearrange columns to place 'View Count' after 'Video title'
df_sorted = df[['Video title', 'View Count', 'video publication date', 'LINK']]

# Sort the DataFrame by publication date in descending order
df_sorted = df_sorted.sort_values(by='video publication date', ascending=False)

# Reindex the DataFrame in order
df_sorted = df_sorted.reset_index(drop=True)

# Apply alternating row colors
styled_df = df_sorted.style.apply(
    lambda x: ['background-color: #f9f9f9' if i % 2 == 0 else 'background-color: #f0f0f0' for i in range(len(x))],
    axis=0
)

# Function to make links clickable
def make_clickable(link):
    return f'<a href="{link}" target="_blank">{link}</a>'

# Apply the make_clickable function to the LINK column
df_sorted['LINK'] = df_sorted['LINK'].apply(make_clickable)

# Layout with columns for the image and title
col1, col2 = st.columns([1, 9])

with col1:
    st.image('https://github.com/Ousmane-BA100/youtube_stats_app/raw/main/ALE-MICROSITE.jpg', use_column_width=True)

with col2:
    st.title('NBD - YouTube Video Views')

# Display view data in a styled table
if not df_sorted.empty:
    st.subheader('Video views (sorted by publication date descending):')
    # Set table width to 1000 pixels
    st.write(styled_df.to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("No view data available.")
