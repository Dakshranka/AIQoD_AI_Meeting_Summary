import requests
import sys
import os

# Add the root directory to the Python path (for importing config.py)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# Import Trello API credentials from config.py (which is in the root directory)
from config import TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_LIST_ID

# Import action item extraction function from backend
from backend.action_item_extractor import extract_action_items

# Trello API URL
TRELLO_URL = "https://api.trello.com/1/cards"

def create_trello_task(task_name):
    """Create a task in Trello based on extracted action items."""
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "idList": TRELLO_LIST_ID,
        "name": task_name,
        "desc": "Auto-generated from meeting notes",
    }
    
    response = requests.post(TRELLO_URL, params=params)

    if response.status_code == 200:
        print(f"✅ Task Created: {task_name}")
    else:
        print(f"❌ Error Creating Task: {response.text}")

def assign_tasks_from_summary():
    """Read the latest summary file, extract action items, and create Trello tasks."""
    summary_folder = "summaries"

    if not os.path.exists(summary_folder) or not os.listdir(summary_folder):
        print("⚠ No summary files found!")
        return

    # Get the latest summary file
    latest_file = sorted(os.listdir(summary_folder))[-1]
    summary_path = os.path.join(summary_folder, latest_file)

    # Read summary content
    with open(summary_path, "r", encoding="utf-8") as file:
        summary_text = file.read()

    # Extract action items from summary
    action_items = extract_action_items(summary_path)

    if not action_items:
        print("⚠ No action items found!")
        return

    # Create Trello tasks for each action item
    for i, item in enumerate(action_items.split("\n"), 1):
        if item.strip():  # Ensure non-empty tasks
            create_trello_task(f"Task {i}: {item}")

if __name__ == "__main__":
    assign_tasks_from_summary()
