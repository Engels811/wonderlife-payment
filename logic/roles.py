import discord
import os
import mysql.connector

# ============================================
# DATABASE
# ============================================

def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

# ============================================
# ROLE LOOKUP
# ============================================

def get_role_id_for_product(product_name: str) -> int | None:
    """
    Holt die Discord-Rolle für ein Produkt aus der DB
    """
    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute(
        "SELECT discord_role_id FROM payment_products WHERE product_name=%s",
        (product_name,)
    )

    row = cur.fetchone()
    cur.close()
    db.close()

    if row:
        return int(row["discord_role_id"])
    return None

# ============================================
# ROLE ASSIGNMENT
# ============================================

async def assign_role(
    bot: discord.Client,
    guild_id: int,
    discord_user_id: int,
    product_name: str
):
    """
    Vergibt automatisch die passende Rolle nach Zahlung
    """
    role_id = get_role_id_for_product(product_name)
    if not role_id:
        return

    guild = bot.get_guild(guild_id)
    if not guild:
        return

    member = guild.get_member(discord_user_id)
    if not member:
        return

    role = guild.get_role(role_id)
    if not role:
        return

    await member.add_roles(role, reason="WonderLife Payment erfolgreich")
