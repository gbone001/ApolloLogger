🧠 Phase 1: Bot Setup & Environment
1. Create a Discord Application
Go to Discord Developer Portal

Click "New Application" → Name it (e.g., ApolloLogger)

Navigate to the Bot tab → Add bot → Customize avatar and settings

2. Set Permissions
For reading event commands and member data:

MESSAGE CONTENT INTENT: Enabled

SERVER MEMBERS INTENT: Enabled

Add to server with OAuth2 URL:

plaintext
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=274877975552
(This scope allows message reading and writing, member access)

🛠️ Phase 2: Logging Apollo Events
Apollo Bot uses /event commands and structured embeds. Since it doesn’t expose a public API, your bot needs to:

1. Use Discord.py (or nextcord/pycord)
bash
pip install discord.py
2. Listen for Apollo Event Embeds
python
import discord
from discord.ext import commands
import json
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    if message.author.name == "Apollo" and "event" in message.embeds[0].title.lower():
        embed = message.embeds[0]
        data = {
            "event_title": embed.title,
            "description": embed.description,
            "timestamp": datetime.utcnow().isoformat()
        }
        with open(f"logs/apollo_event_{datetime.utcnow().date()}.json", "a") as f:
            f.write(json.dumps(data) + "\n")
    await bot.process_commands(message)

bot.run("YOUR_BOT_TOKEN")
🔁 You can extend this to track reactions or button clicks (like RSVP responses) by handling on_reaction_add or interaction responses.

🗄️ Phase 3: Store Responses
Option A: JSON File Logging
Bot appends structured logs to /var/data/apollo_events/

Easily backed up by Elastio

Option B: PostgreSQL Storage
python
import psycopg2

conn = psycopg2.connect("dbname=gareth_apollo user=gareth_user password=your_secure_password")
cur = conn.cursor()
cur.execute("INSERT INTO event_logs (event_title, description, timestamp) VALUES (%s, %s, %s)",
            (embed.title, embed.description, datetime.utcnow()))
conn.commit()
🔐 Phase 4: Backing Up with Elastio
Once logs are stored:

Option A: File Backup
bash
elastio backup /var/data/apollo_events/ --tag "discord-events"
Option B: PostgreSQL Dump + Backup
bash
pg_dump gareth_apollo > /var/backups/apollo.sql
elastio backup /var/backups/apollo.sql --tag "postgres-apollo-backup"
You can automate this via:

Cron jobs

Airflow DAGs

📦 Step-by-Step: Export to CSV
1. Install Required Module
Python’s built-in CSV module handles this nicely:

bash
pip install pandas  # Optional for advanced formatting
2. CSV Writing Example
Modify your bot to append to a CSV file whenever it logs a response:

python
import csv
from datetime import datetime

def log_to_csv(event_data, filename="apollo_event_log.csv"):
    headers = ["event_id", "event_name", "user", "status", "timestamp"]
    file_exists = os.path.isfile(filename)

    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not file_exists:
            writer.writeheader()

        for response in event_data["responses"]:
            writer.writerow({
                "event_id": event_data["event_id"],
                "event_name": event_data["event_name"],
                "user": response["user"],
                "status": response["status"],
                "timestamp": event_data["timestamp"]
            })
3. CSV Output Format
Here’s what your CSV might look like:

event_id,event_name,user,status,timestamp
12345,Weekly Strategy Brief,Gareth,Going,2025-07-20T03:00:00Z
12345,Weekly Strategy Brief,Alex,Tentative,2025-07-20T03:00:00Z
If you're backing up with Elastio, this file can now be protected using your backup policy:

bash
elastio backup /path/to/apollo_event_

🕰️ Option 1: Automation via Cron
📁 Directory Structure
plaintext
/apollo_bot/
  ├── bot.py
  ├── data/
  │   └── daily_event_log.csv
  ├── backup/
  │   └── elastio_backup.sh
🧾 elastio_backup.sh
bash
#!/bin/bash
DATE=$(date +"%Y-%m-%d")
CSV_PATH="/apollo_bot/data/daily_event_log.csv"
TAG="apollo-${DATE}"

elastio backup "$CSV_PATH" --tag "$TAG"
Make it executable: chmod +x elastio_backup.sh

🕗 Cron Job Setup
Edit your crontab with:

bash
crontab -e
Then add:

bash
0 23 * * * python3 /apollo_bot/bot.py >> /apollo_bot/log.txt 2>&1
5 23 * * * /apollo_bot/backup/elastio_backup.sh >> /apollo_bot/backup/backup.log 2>&1
🕐 This runs your bot at 11:00 PM daily, then backs up 5 minutes later.

⚙️ Option 2: Airflow DAG
1. Task Flow
log_apollo_responses_task: Executes bot logic and flushes to CSV

backup_elastio_task: Triggers Elastio CLI for that CSV file

2. Python DAG
python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG("apollo_backup_dag", start_date=datetime(2025, 7, 20), schedule_interval="@daily") as dag:

    log_apollo_responses = BashOperator(
        task_id="log_apollo_responses",
        bash_command="python3 /apollo_bot/bot.py"
    )

    backup_elastio = BashOperator(
        task_id="backup_elastio",
        bash_command="/apollo_bot/backup/elastio_backup.sh"
    )

    log_apollo_responses >> backup_ela

    

Elastio policies (snapshot schedules + ransomware detection)
