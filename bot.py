import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

from permissions import can_start_payment
from ui.payment_embed import build_payment_embed
from ui.payment_view import PaymentView
from ui.tebex_view import TebexShopView

# ============================================
# INITIAL SETUP
# ============================================

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.dm_messages = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ============================================
# READY EVENT
# ============================================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("✅ WonderLife Payment Bot ist online")

# ============================================
# /payment COMMAND (TEAM ONLY)
# ============================================

@bot.tree.command(
    name="payment",
    description="💎 Starte eine WonderLife-Zahlung für einen User"
)
async def payment(
    interaction: discord.Interaction,
    user: discord.Member,
    product: str,
    price_eur: float,
    tebex_product: bool = False
):
    """
    Slash-Command:
    /payment user:<User> product:<Name> price_eur:<Preis> tebex_product:<True/False>
    """

    # ----------------------------
    # PERMISSION CHECK
    # ----------------------------
    if not can_start_payment(interaction.user):
        await interaction.response.send_message(
            "❌ Dieser Command ist nur für das WonderLife-Team.",
            ephemeral=True
        )
        return

    # ----------------------------
    # PREPARE DATA
    # ----------------------------
    amount_cents = int(price_eur * 100)

    # ----------------------------
    # BUILD EMBED
    # ----------------------------
    embed = build_payment_embed(
        user=user,
        product_name=product,
        amount_cents=amount_cents,
        started_by=interaction.user
    )

    # ----------------------------
    # SEND TO USER (DM)
    # ----------------------------
    try:
        if tebex_product:
            # Tebex-Sonderfall → NUR Tebex erlaubt
            view = TebexShopView(user)
        else:
            # Normale Zahlung → Stripe / PayPal / PSC
            view = PaymentView(
                user=user,
                product_name=product,
                amount_cents=amount_cents,
                allow_tebex=False
            )

        await user.send(
            embed=embed,
            view=view
        )

        await interaction.response.send_message(
            f"✅ Zahlungsanfrage wurde erfolgreich an {user.mention} gesendet.",
            ephemeral=True
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Der User hat DMs deaktiviert. Zahlung konnte nicht gesendet werden.",
            ephemeral=True
        )

# ============================================
# BOT START
# ============================================

bot.run(DISCORD_TOKEN)
