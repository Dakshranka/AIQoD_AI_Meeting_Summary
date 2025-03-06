import streamlit as st
import os
import time
from backend.live_meeting_recorder import record_meeting_audio, is_meeting_active
from backend.live_transcriber import transcribe_live_audio  
from backend.live_summarizer import summarize_live_transcript
from backend.live_action_extractor import extract_action_items_from_summary
from backend.live_assign_tasks import assign_tasks_from_live_summary  

# Define Directories
DIRECTORIES = {
    "transcripts": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\transcripts",
    "summaries": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\summaries",
    "action_items": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\action_items",
    "live_recordings": r"C:\Users\Daksh\Downloads\Ai-meeting-summary\live_recordings"
}

# Ensure necessary directories exist
for directory in DIRECTORIES.values():
    os.makedirs(directory, exist_ok=True)

st.title("🎙 Live AI-Powered Meeting Assistant")

# 🎥 Live Meeting Detection
st.subheader("🎥 Live Meeting Recording")

if st.button("🔍 Detect & Start Recording Live Meeting"):
    live_meeting_detected = is_meeting_active()
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

if file_path:
    # 📜 Transcription
    st.subheader("📜 Transcription")
    with st.spinner("Transcribing live audio..."):
        transcript_text = transcribe_live_audio(file_path)
        time.sleep(2)  # Simulate processing delay
    
    transcript_file = os.path.join(DIRECTORIES["transcripts"], "live_meeting.txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    st.text_area("Transcript", transcript_text, height=300)

    # 📌 Summarization
    st.subheader("📌 Summarization")
    with st.spinner("Summarizing transcript..."):
        summary_text = summarize_live_transcript(transcript_file)
        time.sleep(2)

    summary_file = os.path.join(DIRECTORIES["summaries"], "live_summary.txt")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary_text)

    st.text_area("Summary", summary_text, height=200)

    # ✅ Extract Action Items
    st.subheader("✅ Action Items & Decisions")
    with st.spinner("Extracting action items..."):
        action_items_text = extract_action_items_from_summary(summary_file)
        time.sleep(2)

    action_items_file = os.path.join(DIRECTORIES[r"C:\Users\Daksh\Downloads\Ai-meeting-summary\action_items"], "live_actions.txt")
    with open(action_items_file, "w", encoding="utf-8") as f:
        f.write(action_items_text)

    st.text_area("Action Items", action_items_text, height=150)

    # 📌 Assign Tasks to Trello
    st.subheader("📌 Assign Tasks to Trello")
    if st.button("📤 Assign Tasks"):
        with st.spinner("Assigning tasks to Trello..."):
            assign_tasks_from_live_summary()
        st.success("✅ Tasks successfully assigned to Trello!")

    st.success("✅ Live meeting processing complete! View results above.")
