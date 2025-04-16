# Discord Bot : Snail

A bot designed to gather all messages and use them to perform various tasks, such as:

## Main Functions

* Catch each message in server
* Generating a weekly report of server

## Project Folder Structure

The structure and purpose of each folder in the project.

```bash
Discord_Bot-Snails/
├── Database/
│   ├── msgDB.py                    # Module with database functions
│   └── DB.db                       # SQLite database file for storing messages
├── Environment_Setting/
│   ├── environment.yml             # Conda environment configuration file
│   └── requirements.txt            # pip environment dependencies file
├── Main_Extensions/
│   ├── msgAnalyzer.py              # Module for analyzing messages
│   └── msgSaver.py                 # Module for saving messages
├── .gitignore                      # Specifies files and directories to be ignored by Git
├── main.py                         # Entry point for the Discord bot
├── config.json                     # Configuration file containing allowed channel and category IDs
└── README.md                       # Project overview and setup instructions
```

## Setup

### 🛠️ Step 1: Create config.json

Create a config.json file and add the following:

#### 🧩 Basic Configuration

```json
{
    "discord_token": "ABC12345678",
    "send_channel_id": 1234567812345678,
    "admin_id": 1234567812345678
}
```

| Key | Description |
|-|-|
| discord_token | Your Discord bot token |
| send_channel_id | Default channel ID for sending messages |
| admin_id | Discord ID of the admin user (for privileged access) |

#### ✅ Optional: Use when you don't fetch every channel

```json
{
    "discord_token": "ABC12345678",
    "send_channel_id" : 1234567812345678,
    "admin_id": 1234567812345678,
    "allow_category_ids": [
        "1234567812345678"
    ],
    "allow_channel_ids": [
        "1234567812345678"
    ]
}
```

| Key | Description |
|-|-|
| allow_category_ids | List of category IDs where the bot is allowed to fetch messages |
| allow_channel_ids | List of specific channel IDs where the bot can fetch messages |

### 🛠️ Step 2: Install Requirements

You can install the required packages using `pip` or `conda`.

#### 📦 Using pip

```bash
pip install -r requirements.txt
```

#### 🐍 Using conda

```bash
conda env create -f environment.yml
conda activate Snails
```

### 🛠️ Step 3: Run the Main Script

Make sure you're inside your virtual environment, then run:

```bash
python main.py
```
