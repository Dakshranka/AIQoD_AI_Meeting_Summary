# 🎧 AI-Powered Meeting Summary & Task Manager

## 🚀 Overview

AI-Powered Meeting Summary & Task Manager is a real-time and recorded meeting assistant that:

✅ Records live meetings (Zoom & Google Meet)

✅ Transcribes speech into text using Whisper AI

✅ Summarizes key points using NLP

✅ Extracts action items automatically

✅ Assigns tasks to Trello for better productivity

## 📌 Features

🔹 **Live & Recorded Meeting Support** – Works with both uploaded audio and live meetings

🔹 **Automatic Transcription** – Uses Whisper AI to convert speech to text

🔹 **Smart Summarization** – Generates concise summaries using NLP

🔹 **Action Item Extraction** – Identifies key takeaways & decisions

🔹 **Trello Integration** – Automatically creates tasks from action items

## 🛠 Installation

### Clone the Repository
```sh
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Setup Trello API (For Task Assignment)
Create a `config.py` file in the project root:
```python
TRELLO_API_KEY = "your-trello-api-key"
TRELLO_TOKEN = "your-trello-token"
TRELLO_LIST_ID = "your-trello-list-id"
```
🛑 **Important:** Add `config.py` to `.gitignore` to prevent exposing credentials.

### Run the Streamlit App
```sh
streamlit run app.py
```

## 📂 Project Structure
```bash
📁 Ai-meeting-summary/
│── 📁 backend/              # Core backend logic
│   ├── transcriber.py       # Transcription using Whisper AI
│   ├── summarizer.py        # Summarization using NLP
│   ├── action_item_extractor.py  # Extracts action items
│   ├── assign_tasks.py      # Assigns tasks to Trello
│   ├── live_meeting_recorder.py  # Records live meetings
│   ├── live_transcriber.py  # Transcribes live meetings
│   ├── live_summarizer.py   # Summarizes live transcripts
│   ├── live_action_extractor.py  # Extracts live meeting action items
│   ├── live_assign_tasks.py # Assigns live meeting tasks to Trello
│── 📁 transcripts/          # Stores meeting transcripts
│── 📁 summaries/            # Stores meeting summaries
│── 📁 action_items/         # Stores extracted action items
│── 📁 live_recordings/      # Stores live meeting recordings
│── app.py                   # Main Streamlit app
│── requirements.txt          # Required dependencies
│── .gitignore                # Files to ignore in Git
│── README.md                 # Project documentation
```

## 🎯 Usage

⸿ **Upload a recorded meeting or start live recording**

⸿ **Wait for transcription & summarization**

⸿ **Review extracted action items**

⸿ **Assign tasks to Trello with one click**

## 🤖 Technologies Used

🕽 **Whisper AI** – Transcription

📝 **SpaCy / NLP** – Summarization

✅ **Trello API** – Task automation

🎥 **SoundDevice** – Live meeting recording

🖥 **Streamlit** – Frontend

## 🛠 Future Enhancements

✅ **Speaker Identification**

✅ **Multiple Language Support**

✅ **Slack Integration for Notifications**

✅ **Email Reminders for Action Items**

## 💜 License

MIT License. Free to use & modify! 🚀

## ⭐ Contribute

Want to improve this project? Fork it & submit a PR! 💡

## 📌 Next Steps

⸿ **Copy & Paste the above content into a `README.md` file**

⸿ **Commit & Push to GitHub:**
```sh
git add README.md
git commit -m "Added project README"
git push origin main
```


