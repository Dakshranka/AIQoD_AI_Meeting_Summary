import spacy
import os

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Directories
SUMMARY_DIR = "summaries"
ACTION_ITEMS_DIR = "action_items"

# Ensure action items directory exists
os.makedirs(ACTION_ITEMS_DIR, exist_ok=True)

def extract_action_items(file_path):
    """ Extract key action items and decisions from a summary file """
    with open(file_path, "r", encoding="utf-8") as f:
        summary_text = f.read()

    doc = nlp(summary_text)
    action_items = []

    # Identify action items based on verbs and named entities
    for sent in doc.sents:
        if any(token.pos_ == "VERB" for token in sent):  # Checks for actions (verbs)
            action_items.append(sent.text)

    # Save action items
    action_items_text = "\n".join(action_items)
    action_items_filename = os.path.join(ACTION_ITEMS_DIR, os.path.basename(file_path).replace("_summary.txt", "_actions.txt"))
    
    with open(action_items_filename, "w", encoding="utf-8") as f:
        f.write(action_items_text)

    print(f"Action items saved: {action_items_filename}")
    return action_items_text

# Example usage
if __name__ == "__main__":
    summary_file = os.path.join(SUMMARY_DIR, "audio1266319506_summary.txt")  # Change to actual file name
    extracted_actions = extract_action_items(summary_file)
    print("Extracted Action Items:\n", extracted_actions)
