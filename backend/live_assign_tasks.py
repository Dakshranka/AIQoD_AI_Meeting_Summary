import requests
import os
import sys

# Add root directory to Python path (for config.py import)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))

# Import Trello credentials
from config import TRELLO_API_KEY, TRELLO_TOKEN, TRELLO_LIST_ID
from backend.live_action_extractor import extract_action_items_from_summary

TRELLO_URL = "https://api.trello.com/1/cards"

def create_trello_task(task_name):
    """Create a task in Trello based on extracted action items."""
    params = {
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "idList": TRELLO_LIST_ID,
        "name": task_name,
        "desc": "Auto-generated from live meeting notes",
    }
    
    response = requests.post(TRELLO_URL, params=params)

    if response.status_code == 200:
        print(f"✅ Task Created: {task_name}")
    else:
        print(f"❌ Error Creating Task: {response.text}")

def assign_tasks_from_live_summary(filename="live_meeting_summary.txt"):
    """Read the latest live meeting summary, extract action items, and create Trello tasks."""
    action_items_folder = r"C:\Users\Daksh\Downloads\Ai-meeting-summary\action_items"

    if not os.listdir(action_items_folder):  # Check if folder is empty
        print("⚠ No action items found!")
        return
    
    latest_file = sorted(os.listdir(action_items_folder))[-1]  # Get latest action item file
    action_items_path = os.path.join(action_items_folder, latest_file)

    with open(action_items_path, "r", encoding="utf-8") as file:
        action_items = file.readlines()

    if not action_items:
        print("⚠ No action items found!")
        return

    for i, item in enumerate(action_items, 1):
        if item.strip():  # Ensure it's not empty
            create_trello_task(f"Task {i}: {item.strip()}")

if __name__ == "__main__":
    assign_tasks_from_live_summary()
