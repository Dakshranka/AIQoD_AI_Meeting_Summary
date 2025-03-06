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

st.title("🎙 AI-Powered Meeting Assistant & Task Manager")

# 📂 File Upload for Recorded Meetings
uploaded_file = st.file_uploader("📂 Upload a recorded meeting (.wav or .mp3)", type=["wav", "mp3"])

# 🎥 Live Meeting Detection
st.subheader("🎥 Live Meeting Recording")
live_meeting_detected = is_meeting_active()

if st.button("🔍 Detect & Start Recording Live Meeting"):
    if live_meeting_detected:
        st.success("✅ Live meeting detected! Recording in progress...")
        file_path = record_meeting_audio(os.path.join(DIRECTORIES["live_recordings"], "live_meeting.wav"))
        if not file_path:
            st.error("⚠ Recording failed. Ensure system audio is available.")
    else:
        st.warning("⚠ No live meeting detected.")
        file_path = None
else:
    file_path = None

# 🎯 Determine whether to process uploaded or live recording
if uploaded_file:
    file_path = os.path.join(DIRECTORIES["uploads"], uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded {uploaded_file.name} successfully!")

if file_path:
    # 📜 Transcription
    st.subheader("📜 Transcription")
    with st.spinner("Transcribing audio..."):
        transcript_text = (
            transcribe_audio(file_path) if uploaded_file else transcribe_live_audio(file_path)
        )
        time.sleep(2)  # Simulate processing delay
    
    transcript_file = os.path.join(
        DIRECTORIES["transcripts"],
        os.path.basename(file_path).replace(".wav", ".txt").replace(".mp3", ".txt"),
    )
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    st.text_area("Transcript", transcript_text, height=300)

    # 📌 Summarization
    st.subheader("📌 Summarization")
    with st.spinner("Summarizing transcript..."):
        summary_text = (
            summarize_transcript(transcript_file)
            if uploaded_file
            else summarize_live_transcript(transcript_file)
        )
        time.sleep(2)

    summary_file = os.path.join(
        DIRECTORIES["summaries"],
        os.path.basename(file_path).replace(".wav", "_summary.txt").replace(".mp3", "_summary.txt"),
    )
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_text)

    st.text_area("Summary", summary_text, height=200)

    # ✅ Extract Action Items
    st.subheader("✅ Action Items & Decisions")
    with st.spinner("Extracting action items..."):
        action_items_text = (
            extract_action_items(summary_file)
            if uploaded_file
            else extract_action_items_from_summary(summary_file)
        )
        time.sleep(2)

    action_items_file = os.path.join(
        DIRECTORIES["action_items"],
        os.path.basename(file_path).replace(".wav", "_actions.txt").replace(".mp3", "_actions.txt"),
    )
    with open(action_items_file, "w", encoding="utf-8") as f:
        f.write(action_items_text)

    st.text_area("Action Items", action_items_text, height=150)

    # 📌 Assign Tasks to Trello
    st.subheader("📌 Assign Tasks to Trello")
    if st.button("📤 Assign Tasks"):
        with st.spinner("Assigning tasks to Trello..."):
            if uploaded_file:
                assign_tasks_from_summary()
            else:
                assign_tasks_from_live_summary()
        st.success("✅ Tasks successfully assigned to Trello!")

    st.success("✅ Processing complete! View results above.")

else:
    st.warning("⚠ No file uploaded or live meeting detected.")
