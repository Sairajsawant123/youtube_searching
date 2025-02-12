import streamlit as st
import pandas as pd
from youtube_search import YoutubeSearch
import re

def search_youtube(topic, content):
    """
    Searches YouTube for the most relevant and viewed videos of a given topic and content.

    Args:
        topic (str): The main topic to search for (e.g., "Maharashtra State Board English").
        content (str): The specific content within the topic (e.g., "Chapter 1" or "Nouns").

    Returns:
        list: A list of dictionaries containing details of the top four videos sorted by views (title, channel, duration, views, and video link).
    """
    search_terms = f"{topic} {content}"
    try:
        results = YoutubeSearch(search_terms, max_results=4).to_dict()
        video_list = []

        for result in results:
            title = result['title']
            channel = result['channel']
            duration = result['duration']
            views = result['views']
            video_link = 'https://www.youtube.com' + result['url_suffix']

            # Convert views to integer by removing commas and non-numeric characters
            views_numeric = int(re.sub(r'[^\d]', '', views))  # Extract the number from '50,992 views'

            video_list.append({
                'title': title,
                'channel': channel,
                'duration': duration,
                'views': views_numeric,
                'video_link': video_link
            })

        # Sort the video list by views in descending order
        sorted_videos = sorted(video_list, key=lambda x: x['views'], reverse=True)
        return sorted_videos

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
def main():
    st.title("YouTube Video Search")

    # Input fields for topic and content
    topic = st.text_input("Enter the topic (e.g., Python for ChatGPT Agents):")
    content = st.text_input("Enter the content (e.g., AI agents):")

    if st.button("Search"):
        if topic and content:
            # Perform the search
            sorted_videos = search_youtube(topic, content)

            if sorted_videos:
                # Convert the list of dictionaries to a DataFrame
                df = pd.DataFrame(sorted_videos)

                # Make video links clickable
                df['video_link'] = df['video_link'].apply(lambda x: f'<a href="{x}" target="_blank">Watch Video</a>')

                # Display the DataFrame as an HTML table with clickable links
                st.write("Top 4 Videos Sorted by Views:")
                st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.warning("No videos found.")
        else:
            st.warning("Please enter both topic and content.")

if __name__ == "__main__":
    main()