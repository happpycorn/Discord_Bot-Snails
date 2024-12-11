# Discord Bot : Snail

A bot designed to gather all messages and use them to perform various tasks, such as:

## Main Functions

* Catch each message in server
* Generating a weekly report of server

## Project Folder Structure

The structure and purpose of each folder in the project.

```bash
discord_bot/
├── Asset/
│   ├── stopWords.txt                # Font file for generating wordcloud
│   └── config.json                  # Generated wordcloud image
├── Database/
│   ├── db.py                        # Database functions
│   └── Message.db                   # Database file, may include multiple versions
├── Main_Extensions/
│   ├── msgAnalyzer.py               # Analyzes messages
│   └── magSaver.py                  # Saves messages
├── Other_Extensions/
│   └── *.py                         # The other extensions who have be deloveing
├── Environment_Setting/
│   ├── environment.yml              # Environment for conda
│   └── requirements.txt             # Environment for pip
├── .env                             # Environment variables file (create manually; see setup)
├── .gitignore                       # List of files to ignore in version control
├── main.py                          # Main program entry point
└── README.md                        # Project overview
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
    conda install conda-forge::discord.py
    conda install conda-forge::python-dotenv
    conda install conda-forge::wordcloud
    conda install conda-forge::tqdm
    conda install conda-forge::sumy
    conda install conda-forge::pandas
    ```

    but ckip_transformers still need install by pip:

    ```bash
    pip install ckip-transformers
    ```

3. Run `main.py`:

    ```bash
    python main.py
    ```
