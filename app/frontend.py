import streamlit as st

def youtube_card(thumbnail_url, video_url, summary):
    # Custom CSS for the card
    st.markdown("""
        <style>
        .youtube-card {
            border: 2px solid #FF0000;
            border-radius: 15px;
            padding: 20px;
            margin: 20px auto;
            background-color: white;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        .thumbnail-container {
            position: relative;
            margin-bottom: 20px;
        }
        .thumbnail {
            width: 100%;
            border-radius: 12px;
            transition: transform 0.3s;
        }
        .youtube-link {
            color: #FF0000;
            text-decoration: none;
            font-weight: 500;
            font-size: 18px;
            display: flex;
            align-items: center;
            margin-bottom: 16px;
        }
        .summary-box {
            background-color: #f9f9f9;
            padding: 16px;
            border-radius: 10px;
            max-height: 240px;
            overflow-y: auto;
        }
        </style>
    """, unsafe_allow_html=True)

    # Card HTML
    st.markdown(f"""
        <div class="youtube-card">
            <div class="thumbnail-container">
                <img src="{thumbnail_url}" class="thumbnail" alt="Video thumbnail">
            </div>
            {summary}
        </div>
    """, unsafe_allow_html=True)

# Example usage
def main():
    st.set_page_config(page_title="YouTube Video Card", layout="wide")
    
    # You can replace these with your actual video details
    thumbnail_url = "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    summary = """This is an example summary of the video. It can be multiple lines long 
                and will be scrollable if it exceeds the maximum height. The text is easy 
                to read and the container has a subtle background."""
    
    # Add some padding and a title
    st.markdown("<h1 style='text-align: center;'>YouTube Video Summary</h1>", unsafe_allow_html=True)
    
    # Create columns for better centering
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        youtube_card(thumbnail_url, video_url, summary)

if __name__ == "__main__":
    main()
