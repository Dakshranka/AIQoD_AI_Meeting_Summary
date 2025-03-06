import whisper
import os

# Define directories
AUDIO_DIR = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\live_recordings"
TRANSCRIPT_DIR = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\transcripts"

# Ensure transcript directory exists
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def transcribe_live_audio(filename="live_meeting.wav"):
    """Transcribe recorded meeting audio using Whisper AI."""
    audio_path = os.path.join(AUDIO_DIR, filename)
    
    if not os.path.exists(audio_path):
        print(f"❌ Error: Audio file {audio_path} not found!")
        return None

    print("📝 Transcribing meeting audio...")

    # Load Whisper model
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    transcript_text = result["text"]

    # Save transcript
    transcript_file = os.path.join(TRANSCRIPT_DIR, filename.replace(".wav", ".txt"))
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print(f"✅ Transcript saved: {transcript_file}")
    return transcript_text

if __name__ == "__main__":
    transcribe_live_audio()
