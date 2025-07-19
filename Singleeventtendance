@bot.command()
async def attendance(ctx, event_id: str):
    counts = {"Going": 0, "Tentative": 0, "Not Going": 0}
    event_name = None

    with open("apollo_event_log.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["event_id"] == event_id:
                counts[row["status"]] += 1
                event_name = row["event_name"]

    if event_name:
        embed = discord.Embed(
            title=f"📋 Attendance for: {event_name} (ID: {event_id})", color=0x00b2ff
        )
        embed.add_field(name="✅ Going", value=str(counts["Going"]), inline=True)
        embed.add_field(name="🤔 Tentative", value=str(counts["Tentative"]), inline=True)
        embed.add_field(name="❌ Not Going", value=str(counts["Not Going"]), inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❗ No data found for event ID `{event_id}`.")
