import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
import ollama
import requests
import re
import urllib.request
from gtts import gTTS
import tempfile
import uuid  # To create a unique key for each summary

summary_id = str(uuid.uuid4())[:8]  # 


# Prompt template
prompt_template = """
You are a YouTube video summarizer. Given the full transcript of a video, summarize it in only maximum 5 bullet points within 250 words. Do not write any other text like "Here is the summary" or "Here is the transcript".
Here is the transcript:
"""

model = "deepseek-r1:1.5b"

# Extract transcript (English only)
def extract_transcript_details(video_id):
    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        transcript = " ".join([item["text"] for item in transcript_data])
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript):
        return None
    except Exception as e:
        raise e

# Generate summary
def generate_summary_with_ollama(transcript_text, prompt):
    full_prompt = prompt + transcript_text
    response = ollama.chat(model=model, messages=[{"role": "user", "content": full_prompt}])
    # return response['message']['content']
    content = response.message.content
    return re.sub(r'^.*?</think>\s*', '', content, flags=re.DOTALL) 

def get_summary_audio(summary_text):
    tts = gTTS(summary_text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

def preprocess_text(text):
    # Remove extra whitespace and newlines
    text = re.sub(r'\n+', '\n', text)     # normalize multiple newlines
    text = re.sub(r'[ \t]+', ' ', text)   # normalize spaces/tabs
    
    text = re.sub(r'\[.*?\]', '', text)  # removes [Music], [Applause], etc.

    text = re.sub(r"[^a-zA-Z0-9.,!?'\s]", '', text)

    text = text.strip()

    return text


# Streamlit UI
st.set_page_config(page_title="YouTube Video Summarizer")
st.markdown("<h1 style='text-align: center;'>▶️ YouTube Video Summarizer</h1>", unsafe_allow_html=True)

if f"open_{summary_id}" not in st.session_state:
    st.session_state[f"open_{summary_id}"] = False

query = st.text_input("🔍 Enter your search query:")
search = query.replace(" ","+")
youtube_search="https://www.youtube.com/results?search_query="+search
if query:
    html = urllib.request.urlopen(youtube_search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_ids = list(set(video_ids))  # Remove duplicates

    st.info(f"Found {len(video_ids)} video candidates. Searching for transcripts...")

    count = 0
    col_index = 0
    columns = st.columns(3)  # Three columns for card display

    for video_id in video_ids:
        if count >= 9:  # 3 rows (3x3 layout)
            break

        transcript_text = extract_transcript_details(video_id)
        if not transcript_text:
            continue

        try:
            cleaned_transcript = preprocess_text(transcript_text)
            summary = generate_summary_with_ollama(cleaned_transcript, prompt_template)
            summary = preprocess_text(summary)
            # summary = "hello"
            audio_path = get_summary_audio(summary)

            video_url = f"https://www.youtube.com/watch?v={video_id}"
            embed_url = f"https://www.youtube.com/embed/{video_id}"

            with columns[col_index]:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 15px; padding: 15px; margin-bottom: 25px;
                            box-shadow: 0 4px 8px rgba(0,0,0,0.1); background-color: #ffffff;">
                    <iframe width="100%" height="300" src="{embed_url}" 
                            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; 
                            clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
                    </iframe>
                    <h4 style="margin: 10px 0 5px;"><a href="{video_url}" target="_blank">🔗 Watch on YouTube</a></h4>
                    <div style="font-size: 14px; line-height: 1.5; color: black; max-height: 250px; min-height: 250px; overflow-y: auto; white-space: pre-wrap;
                                background-color: #f8f8f8; padding: 10px; border-radius: 10px;">
                        {summary}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.audio(audio_path, format="audio/mp3")

            count += 1
            col_index = (col_index + 1) % 3  # Move to next column cyclically

        except Exception as e:
            st.warning(f"⚠️ Error with video {video_id}: {str(e)}")