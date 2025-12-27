import discord

async def notify_user(
    bot: discord.Client,
    user_id: int,
    title: str,
    message: str,
    success: bool = True
):
    user = bot.get_user(user_id)
    if not user:
        return

    embed = discord.Embed(
        title=title,
        description=message,
        color=0x2ecc71 if success else 0xe74c3c
    )

    try:
        await user.send(embed=embed)
    except discord.Forbidden:
        pass
