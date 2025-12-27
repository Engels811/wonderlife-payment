import discord
import os

WONDERLIFE_COLOR = 0x8E44FF


def paypal_payment_embed(
    user: discord.Member,
    product_name: str,
    amount_cents: int
) -> discord.Embed:
    """
    Erstellt die PayPal-Zahlungs-Embed-Nachricht für den User
    """

    amount_eur = amount_cents / 100
    paypal_email = os.getenv("PAYPAL_EMAIL", "payments@wonderlife-network.eu")

    embed = discord.Embed(
        title="🪙 WonderLife PayPal Zahlung",
        description=(
            f"Du hast dich für **PayPal** als Zahlungsmethode entschieden.\n\n"
            f"📦 **Produkt:** `{product_name}`\n"
            f"💰 **Betrag:** `{amount_eur:.2f} €`\n\n"
            f"### 🔐 Zahlungsinformationen\n"
            f"📧 **Empfänger:** `{paypal_email}`\n"
            f"💬 **Zahlungsart:** `Freunde & Familie`\n"
            f"✏️ **Kommentar:** `leer lassen`\n\n"
            f"⚠️ **Wichtig:**\n"
            f"- Zahlung **ohne Kommentar** senden\n"
            f"- Nach der Zahlung **unten bestätigen**\n"
            f"- Ein Teammitglied prüft die Zahlung\n\n"
            f"🔗 Deine Zahlung ist fest mit deiner **Discord-ID** verknüpft."
        ),
        color=WONDERLIFE_COLOR
    )

    embed.set_footer(
        text=f"WonderLife Network • Discord-ID: {user.id}"
    )

    return embed


class PayPalConfirmView(discord.ui.View):
    """
    Button-View für PayPal-Zahlung bestätigen
    """

    def __init__(self, user: discord.Member, product_name: str, amount_cents: int):
        super().__init__(timeout=600)
        self.user = user
        self.product_name = product_name
        self.amount_cents = amount_cents

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Stellt sicher, dass nur der richtige User interagieren kann
        """
        return interaction.user.id == self.user.id

    @discord.ui.button(
        label="✅ Zahlung gesendet",
        style=discord.ButtonStyle.green
    )
    async def confirm_payment(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        """
        Wird aufgerufen, wenn der User seine PayPal-Zahlung bestätigt
        """

        await interaction.response.send_message(
            "✅ **Zahlung gemeldet!**\n\n"
            "Ein Teammitglied prüft deine PayPal-Zahlung.\n"
            "Du erhältst dein Produkt nach erfolgreicher Bestätigung.",
            ephemeral=True
        )

        # Ab hier:
        # → Ticket-Erstellung
        # → Admin-Benachrichtigung
        # → spätere Rollenvergabe
        #
        # Das erfolgt zentral in tickets.py / admin-commands
