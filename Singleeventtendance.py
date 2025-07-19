@bot.command()
async def attendance(ctx, event_id: str):
    counts = {"Going": [], "Tentative": [], "Not Going": []}
    event_name = None

    with open("apollo_event_log.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["event_id"] == event_id:
                status = row["status"]
                counts[status].append(row["user"])
                event_name = row["event_name"]

    if event_name:
        responded_users = set(counts["Going"] + counts["Tentative"] + counts["Not Going"])
        all_members = [m.name for m in ctx.guild.members if not m.bot]
        not_responded = [user for user in all_members if user not in responded_users]

        embed = discord.Embed(title=f"📋 Attendance for: {event_name} (ID: {event_id})", color=0x00b2ff)
        embed.add_field(name="✅ Going", value="\n".join(counts["Going"]) or "None", inline=False)
        embed.add_field(name="❌ Not Going", value="\n".join(counts["Not Going"]) or "None", inline=False)
        embed.add_field(name="🤔 Tentative", value="\n".join(counts["Tentative"]) or "None", inline=False)
        embed.add_field(name="🤷 No Response", value="\n".join(not_responded) or "None", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❗ No data found for event ID `{event_id}`.")
