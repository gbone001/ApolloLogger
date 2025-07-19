@bot.command()
async def who_didnt_respond(ctx, event_id: str):
    responded = set()
    event_name = None

    with open("apollo_event_log.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["event_id"] == event_id:
                responded.add(row["user"])
                event_name = row["event_name"]

    all_users = [m.name for m in ctx.guild.members if not m.bot]
    missing = [user for user in all_users if user not in responded]

    if event_name:
        embed = discord.Embed(
            title=f"🤷 Members Without Response: {event_name}",
            description="\n".join(missing) or "All accounted for!",
            color=0xffcc00
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❗ No data found for event ID `{event_id}`.")
