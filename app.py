import streamlit as st
import os
import time
from backend.transcriber import transcribe_audio
from backend.sumarrizer import summarize_transcript
from backend.action_item_extractor import extract_action_items
from backend.assign_tasks import assign_tasks_from_summary
from backend.live_meeting_recorder import record_meeting_audio, is_meeting_active
from backend.live_transcriber import transcribe_live_audio  
from backend.live_summarizer import summarize_live_transcript
from backend.live_action_extractor import extract_action_items_from_summary
from backend.live_assign_tasks import assign_tasks_from_live_summary  

# Custom CSS for UI enhancements
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        div.stButton > button {
            width: 100%;
            border-radius: 10px;
            font-size: 16px;
        }
        div.stTextArea > textarea {
            font-size: 14px;
        }
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# 📂 Define Directories
DIRECTORIES = {
    "transcripts": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\transcripts",
    "summaries": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\summaries",
    "action_items": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\action_items",
    "uploads": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\uploads",
    "live_recordings": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\live_recordings"
}

# 🔹 Ensure necessary directories exist
for directory in DIRECTORIES.values():
    os.makedirs(directory, exist_ok=True)

st.title("🎙 AI-Powered Meeting Assistant")

# 📂 File Upload for Recorded Meetings
with st.sidebar:
    st.subheader("📂 Upload Meeting Recording")
    uploaded_file = st.file_uploader("Upload (.wav or .mp3)", type=["wav", "mp3"])

# 🎥 Live Meeting Detection
st.subheader("🎥 Live Meeting Recorder")
live_meeting_detected = is_meeting_active()

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Detect & Start Live Recording"):
        if live_meeting_detected:
            st.success("✅ Live meeting detected! Recording in progress...")
            file_path = record_meeting_audio(os.path.join(DIRECTORIES["live_recordings"], "live_meeting.wav"))
        else:
            st.warning("⚠ No live meeting detected.")
            file_path = None
    else:
        file_path = None

# 🎯 Process Uploaded or Live Recording
if uploaded_file:
    file_path = os.path.join(DIRECTORIES["uploads"], uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded {uploaded_file.name} successfully!")

if file_path:
    tab1, tab2, tab3, tab4 = st.tabs(["📜 Transcription", "📌 Summary", "✅ Action Items", "📤 Assign Tasks"])

    # 📜 Transcription
    with tab1:
        with st.spinner("Transcribing audio..."):
            transcript_text = transcribe_audio(file_path) if uploaded_file else transcribe_live_audio(file_path)
            time.sleep(2)
        st.text_area("Transcript", transcript_text, height=300)

    # 📌 Summarization
    with tab2:
        with st.spinner("Summarizing transcript..."):
            summary_text = summarize_transcript(file_path) if uploaded_file else summarize_live_transcript(file_path)
            time.sleep(2)
        st.text_area("Summary", summary_text, height=200)

    # ✅ Extract Action Items
    with tab3:
        with st.spinner("Extracting action items..."):
            action_items_text = extract_action_items(file_path) if uploaded_file else extract_action_items_from_summary(file_path)
            time.sleep(2)
        st.text_area("Action Items", action_items_text, height=150)

    # 📤 Assign Tasks to Trello
    with tab4:
        if st.button("📤 Assign Tasks to Trello"):
            with st.spinner("Assigning tasks..."):
                assign_tasks_from_summary() if uploaded_file else assign_tasks_from_live_summary()
            st.success("✅ Tasks successfully assigned!")

else:
    st.warning("⚠ No file uploaded or live meeting detected.")
