import discord

WONDERLIFE_COLOR = 0x8E44FF
WONDERLIFE_LOGO = "https://i.ibb.co/cK47x2fF/Wonder-Life-Network-ohne-hintergrund.png"


def build_payment_embed(
    user: discord.Member,
    product_name: str,
    amount_cents: int,
    started_by: discord.Member
) -> discord.Embed:
    """
    Erstellt die zentrale WonderLife-Payment-Embed,
    die der User erhält, nachdem ein Teamler /payment ausführt.
    """

    amount_eur = amount_cents / 100

    embed = discord.Embed(
        title="💎 WonderLife Network – Payment Center",
        description=(
            f"Hallo {user.mention},\n\n"
            f"ein Teammitglied hat für dich eine Zahlung erstellt.\n\n"
            f"📦 **Produkt:** `{product_name}`\n"
            f"💰 **Preis:** `{amount_eur:.2f} €`\n\n"
            f"⬇️ **Bitte wähle unten deine gewünschte Zahlungsart aus.**\n\n"
            f"🔒 Deine Zahlung wird **sicher verarbeitet** und ist fest mit "
            f"deiner **Discord-ID** verknüpft."
        ),
        color=WONDERLIFE_COLOR
    )

    embed.set_thumbnail(url=WONDERLIFE_LOGO)

    embed.add_field(
        name="🏦 Verfügbare Zahlungsarten",
        value=(
            "💳 **Stripe** – Klarna, Sofortüberweisung, Visa, Mastercard\n"
            "🪙 **PayPal** – Freunde & Familie\n"
            "🎟️ **PaySafeCard** – bis zu 5 Codes\n"
            "🛒 **Tebex** – offizieller WonderLife Shop (falls verfügbar)"
        ),
        inline=False
    )

    embed.add_field(
        name="ℹ️ Hinweise",
        value=(
            "• Zahlungen ohne Kommentar durchführen\n"
            "• Ungültige Angaben können zur Ablehnung führen\n"
            "• Bei Fragen wende dich an unser Team"
        ),
        inline=False
    )

    embed.set_footer(
        text=(
            f"WonderLife Network • Zahlung gestartet von "
            f"{started_by.display_name}"
        )
    )

    return embed
