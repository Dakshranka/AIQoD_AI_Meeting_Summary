from transformers import pipeline
import os

# Define directories
TRANSCRIPT_DIR = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\transcripts"
SUMMARY_DIR = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\summaries"

# Ensure summary directory exists
os.makedirs(SUMMARY_DIR, exist_ok=True)

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_live_transcript(filename="live_meeting.txt"):
    """Summarize the transcribed meeting text."""
    transcript_path = os.path.join(TRANSCRIPT_DIR, filename)

    if not os.path.exists(transcript_path):
        print(f"❌ Error: Transcript file {transcript_path} not found!")
        return None

    with open(transcript_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    print("📌 Summarizing transcript...")

    # Hugging Face models have a token limit (1024), so summarize in chunks if needed
    max_input = 1024  # BART has a limit of 1024 tokens
    transcript_chunks = [transcript_text[i:i+max_input] for i in range(0, len(transcript_text), max_input)]

    summary = ""
    for chunk in transcript_chunks:
        summary += summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]["summary_text"] + " "

    # Save summary
    summary_file = os.path.join(SUMMARY_DIR, filename.replace(".txt", "_summary.txt"))
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ Summary saved: {summary_file}")
    return summary

if __name__ == "__main__":
    summarize_live_transcript()
