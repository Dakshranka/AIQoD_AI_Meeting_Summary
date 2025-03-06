from transformers import pipeline
import os

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Directory where transcripts are stored
TRANSCRIPT_DIR = "transcripts"
SUMMARY_DIR = "summaries"

# Ensure summary directory exists
os.makedirs(SUMMARY_DIR, exist_ok=True)

def summarize_transcript(file_path):
    """ Summarize the given transcript file and save the summary """
    with open(file_path, "r", encoding="utf-8") as f:
        transcript_text = f.read()

    # Hugging Face models have a token limit, so summarize in chunks if needed
    max_input = 1024  # BART has a limit of 1024 tokens
    transcript_chunks = [transcript_text[i:i+max_input] for i in range(0, len(transcript_text), max_input)]

    summary = ""
    for chunk in transcript_chunks:
        summary += summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]["summary_text"] + " "

    # Save summary to a file
    summary_filename = os.path.join(SUMMARY_DIR, os.path.basename(file_path).replace(".txt", "_summary.txt"))
    with open(summary_filename, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Summary saved: {summary_filename}")
    return summary

# Example usage
if __name__ == "__main__":
    transcript_file = os.path.join(TRANSCRIPT_DIR, "audio1266319506.txt")  # Change to the actual file name
    summary_text = summarize_transcript(transcript_file)
    print("Summary:\n", summary_text)
