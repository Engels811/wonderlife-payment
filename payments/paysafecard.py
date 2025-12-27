import discord
import os

WONDERLIFE_COLOR = 0x8E44FF


def paysafecard_intro_embed(
    user: discord.Member,
    product_name: str,
    amount_cents: int
) -> discord.Embed:
    """
    Erstellt die Einbettung für PaySafeCard-Zahlungen
    """

    amount_eur = amount_cents / 100

    embed = discord.Embed(
        title="🎟️ WonderLife PaySafeCard Zahlung",
        description=(
            f"Du hast dich für **PaySafeCard** als Zahlungsmethode entschieden.\n\n"
            f"📦 **Produkt:** `{product_name}`\n"
            f"💰 **Betrag:** `{amount_eur:.2f} €`\n\n"
            f"### 🔐 Wichtige Hinweise\n"
            f"- Du kannst **bis zu 5 Codes** eingeben\n"
            f"- Jeder Code wird **manuell geprüft**\n"
            f"- Ungültige Codes führen zur **Ablehnung**\n\n"
            f"🔗 Deine Zahlung ist fest mit deiner **Discord-ID** verknüpft."
        ),
        color=WONDERLIFE_COLOR
    )

    embed.set_footer(
        text=f"WonderLife Network • Discord-ID: {user.id}"
    )

    return embed


class PaySafeCardModal(discord.ui.Modal):
    """
    Modal für die Eingabe von bis zu 5 PaySafeCard-Codes
    """

    def __init__(
        self,
        user: discord.Member,
        product_name: str,
        amount_cents: int
    ):
        super().__init__(title="🎟️ PaySafeCard Codes eingeben")

        self.user = user
        self.product_name = product_name
        self.amount_cents = amount_cents

        self.code_1 = discord.ui.TextInput(
            label="Code 1",
            placeholder="XXXX-XXXX-XXXX",
            required=True,
            max_length=30
        )

        self.code_2 = discord.ui.TextInput(
            label="Code 2 (optional)",
            placeholder="XXXX-XXXX-XXXX",
            required=False,
            max_length=30
        )

        self.code_3 = discord.ui.TextInput(
            label="Code 3 (optional)",
            placeholder="XXXX-XXXX-XXXX",
            required=False,
            max_length=30
        )

        self.code_4 = discord.ui.TextInput(
            label="Code 4 (optional)",
            placeholder="XXXX-XXXX-XXXX",
            required=False,
            max_length=30
        )

        self.code_5 = discord.ui.TextInput(
            label="Code 5 (optional)",
            placeholder="XXXX-XXXX-XXXX",
            required=False,
            max_length=30
        )

        self.add_item(self.code_1)
        self.add_item(self.code_2)
        self.add_item(self.code_3)
        self.add_item(self.code_4)
        self.add_item(self.code_5)

    async def on_submit(self, interaction: discord.Interaction):
        """
        Wird aufgerufen, wenn der User das Formular abschickt
        """

        # Sammle alle eingegebenen Codes
        codes = [
            code.value.strip()
            for code in [
                self.code_1,
                self.code_2,
                self.code_3,
                self.code_4,
                self.code_5
            ]
            if code.value
        ]

        await interaction.response.send_message(
            "✅ **PaySafeCard Codes übermittelt!**\n\n"
            "Unser Team prüft deine Codes manuell.\n"
            "Du erhältst dein Produkt nach erfolgreicher Bestätigung.",
            ephemeral=True
        )

        # ⬇⬇⬇ WICHTIGE STELLE ⬇⬇⬇
        # Ab hier KEINE automatische Verarbeitung!
        #
        # Hier passiert später:
        # - Ticket-Erstellung (tickets.py)
        # - Weitergabe der Codes an das Team
        # - Admin bestätigt / lehnt ab
        # - Rollenvergabe + Rechnung
        #
        # Die Codes sollten NUR intern geloggt werden,
        # niemals öffentlich oder in Logs!
