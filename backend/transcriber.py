import whisper
import subprocess
import os

# Ensure the transcript directory exists
TRANSCRIPT_DIR = "transcripts"
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def convert_audio(input_file, output_file="converted_audio.wav"):
    """ Convert audio to 16kHz, mono PCM format """
    command = [
        "ffmpeg", "-i", input_file,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_file, "-y"
    ]
    subprocess.run(command, check=True)
    return output_file

def transcribe_audio(file_path):
    """ Transcribe the given audio file and save the transcript """
    model = whisper.load_model("base")
    
    # Convert the audio before transcription
    converted_file = convert_audio(file_path)

    # Now transcribe
    result = model.transcribe(converted_file)
    transcript_text = result["text"]

    # Save transcript to a file
    transcript_filename = os.path.join(TRANSCRIPT_DIR, os.path.basename(file_path).replace(".wav", ".txt"))
    with open(transcript_filename, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print(f"Transcription saved: {transcript_filename}")
    return transcript_text

# Example usage
if __name__ == "__main__":
    file_path = "backend/audio1266319506.wav"
    transcript = transcribe_audio(file_path)
    print("Transcription:\n", transcript)
