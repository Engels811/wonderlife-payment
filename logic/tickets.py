import discord
import os
from datetime import datetime

# ============================================
# TICKET CREATION
# ============================================

async def create_payment_ticket(
    bot: discord.Client,
    guild_id: int,
    discord_user_id: int,
    product_name: str,
    provider: str,
    amount_cents: int
):
    guild = bot.get_guild(guild_id)
    if not guild:
        return

    member = guild.get_member(discord_user_id)
    if not member:
        return

    category = guild.get_channel(int(os.getenv("PAYMENT_CATEGORY_ID")))
    if not category:
        return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True),
    }

    channel = await guild.create_text_channel(
        name=f"zahlung-{member.name}",
        category=category,
        overwrites=overwrites
    )

    embed = discord.Embed(
        title="💎 WonderLife Zahlung abgeschlossen",
        color=0x8E44FF,
        timestamp=datetime.utcnow()
    )

    embed.add_field(name="👤 User", value=member.mention, inline=False)
    embed.add_field(name="📦 Produkt", value=product_name, inline=True)
    embed.add_field(name="🏦 Zahlungsart", value=provider.upper(), inline=True)
    embed.add_field(
        name="💰 Betrag",
        value=f"{amount_cents / 100:.2f} €",
        inline=True
    )

    embed.set_footer(text="WonderLife Network • Payment System")

    await channel.send(embed=embed)
