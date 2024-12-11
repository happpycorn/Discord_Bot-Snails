# Discord Bot : Snail

A bot designed to gather all messages and use them to perform various tasks, such as:

## Main Functions

* Catch each message in server
* Generating a weekly report of server

## Project Folder Structure

The structure and purpose of each folder in the project.

```bash
Discord_Bot-Snails/
├── Asset/
│   ├── stopWords.txt               # List of stop words for LDA analysis
│   └── config.json                 # Configuration file containing allowed channel and category IDs
├── Database/
│   ├── db.py                       # Module with database functions
│   └── Message.db                  # SQLite database file for storing messages
├── Main_Extensions/
│   ├── msgAnalyzer.py              # Module for analyzing messages
│   └── msgSaver.py                 # Module for saving messages
├── Environment_Setting/
│   ├── environment.yml             # Conda environment configuration file
│   └── requirements.txt            # pip environment dependencies file
├── .env                            # Environment variables file (manually created; see setup instructions)
├── .gitignore                      # Specifies files and directories to be ignored by Git
├── main.py                         # Entry point for the Discord bot
└── README.md                       # Project overview and setup instructions
```

## Setup

1. Create a `.env` file and add the following:

    ```bash
    DISCORD_TOKEN=<Your_DC_Bot_Token>
    ```

2. Install requirements from `requirement.txt`

    You can use Pip:

    ```bash
    pip install -r requirements.txt
    ```

    or use Conda:

    ```bash
    conda env create -f environment.yml
    conda activate Snails
    ```

3. Run `main.py`:

    ```bash
    python main.py
    ```
