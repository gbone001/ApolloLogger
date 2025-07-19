import csv
import os

def export_full_attendance_csv(event_id: str, guild_members, input_file="apollo_event_log.csv", output_file="full_attendance_export.csv"):
    responses = {}
    event_name = None

    # Read CSV and collect responses for event_id
    with open(input_file, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["event_id"] == event_id:
                responses[row["user"]] = row["status"]
                event_name = row["event_name"]

    if not event_name:
        print(f"❗ No data found for event ID `{event_id}`.")
        return

    all_usernames = [member.name for member in guild_members if not member.bot]

    # Prepare full list
    full_attendance = []
    for username in all_usernames:
        if username in responses:
            full_attendance.append({
                "username": username,
                "response": responses[username],
                "source": "CSV (logged response)"
            })
        else:
            full_attendance.append({
                "username": username,
                "response": "No Response",
                "source": "Guild-only"
            })

    # Export to CSV
    with open(output_file, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "response", "source"])
        writer.writeheader()
        writer.writerows(full_attendance)

    print(f"✅ Export complete: {output_file}")
