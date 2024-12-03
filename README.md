# Telegram Bot for IMDb API

## Project Description

This Telegram bot interacts with the IMDb API and provides users with access to movie information. The bot allows users to query the list of movies with the lowest and highest ratings, as well as query movies within a custom rating range. It also keeps a history of the last 10 queries for each user.

## Main Functionality

The bot supports the following commands:
- `/start` - Welcome message and information about the commands.
- `/help` - Description of available commands.
- `/low` - Get movies with the lowest rating.
- `/high` - Get movies with the highest rating.
- `/custom <start> <end>` - Get movies in a specified range of positions.
- `/history` - Show the last 10 user queries.

## Installation

1. Clone the project repository:
   ```bash
   git clone <URL_of_your_repository>
   cd TelegramBot


2. Create a virtual environment: 
    ```bash
    python -m venv venv

3. Activate the virtual environment:

    For Windows: venv\Scripts\activate

    For Linux/Mac: source venv/bin/activate

4. Install the dependencies::
    ```bash
    pip install -r requirements.txt

# Configuration

Before running the bot, make sure you set up the environment file (e.g., `.env` or `config`), 
which contains your API key for interacting with IMDb. Example variables:
```
token=Your_Bot_Token
RAPIDAPI_KEY=Your_API_Key

```

# Running the bot 
To run the bot, use the following command:
```bash
python main.py
```
 
# Usage

Once the bot is running, send the `/start` command in Telegram to get a list of available commands. 
You can query movies using `/low`, `/high` or use a custom range with `/custom`.

Example Commands:

    - /low —  Get movies with the lowest ratings.
    - /high — Get movies with the highest ratings.
    - /custom 1 10 — Get movies from position 1 to 10 in the rating list.
    - /history — View the last 10 user queries.

