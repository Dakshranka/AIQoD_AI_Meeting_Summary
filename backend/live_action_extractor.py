import spacy
import os

# Define directories
SUMMARY_DIR = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\summaries"
ACTION_ITEMS_DIR = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\action_items"

# Ensure action items directory exists
os.makedirs(ACTION_ITEMS_DIR, exist_ok=True)

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

def extract_action_items_from_summary(filename="live_meeting_summary.txt"):
    """Extract key action items and decisions from a summarized transcript."""
    summary_path = os.path.join(SUMMARY_DIR, filename)

    if not os.path.exists(summary_path):
        print(f"❌ Error: Summary file {summary_path} not found!")
        return None

    with open(summary_path, "r", encoding="utf-8") as f:
        summary_text = f.read()

    print("✅ Extracting action items...")

    doc = nlp(summary_text)
    action_items = []

    # Identify action items based on verbs (e.g., assigned, discuss, finalize)
    for sent in doc.sents:
        if any(token.pos_ == "VERB" for token in sent):  # Checks for actions
            action_items.append(sent.text)

    # Save action items
    action_items_text = "\n".join(action_items)
    action_items_file = os.path.join(ACTION_ITEMS_DIR, filename.replace("_summary.txt", "_actions.txt"))

    with open(action_items_file, "w", encoding="utf-8") as f:
        f.write(action_items_text)

    print(f"✅ Action items saved: {action_items_file}")
    return action_items_text

if __name__ == "__main__":
    extract_action_items_from_summary()
