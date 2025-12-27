import discord
from permissions import is_payment_user
from payments.stripe import stripe_link
from payments.paypal import paypal_payment_embed, PayPalConfirmView
from payments.paysafecard import (
    paysafecard_intro_embed,
    PaySafeCardModal
)

WONDERLIFE_COLOR = 0x8E44FF


class PaymentView(discord.ui.View):
    """
    Zentrale Zahlungsarten-Auswahl für WonderLife Network

    - Stripe
    - PayPal (F&F)
    - PaySafeCard
    - OPTIONAL: Tebex (separat!)
    """

    def __init__(
        self,
        user: discord.Member,
        product_name: str,
        amount_cents: int,
        allow_tebex: bool = False
    ):
        super().__init__(timeout=600)

        self.user = user
        self.product_name = product_name
        self.amount_cents = amount_cents
        self.allow_tebex = allow_tebex

        # Tebex ist ein Sonderfall:
        # Wenn allow_tebex=True → Stripe/PayPal/PSC NICHT anzeigen
        if allow_tebex:
            self.clear_items()
            self.add_item(self.tebex_only_button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Sicherheitscheck: nur der Ziel-User darf interagieren
        """
        if not is_payment_user(interaction, self.user):
            await interaction.response.send_message(
                "❌ Diese Zahlungsanfrage ist nicht für dich.",
                ephemeral=True
            )
            return False
        return True

    # ==========================================================
    # STRIPE
    # ==========================================================

    @discord.ui.button(
        label="💳 Stripe",
        style=discord.ButtonStyle.green
    )
    async def stripe_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        checkout_url = stripe_link(
            discord_id=self.user.id,
            product=self.product_name,
            price=self.amount_cents
        )

        embed = discord.Embed(
            title="💳 Stripe Zahlung",
            description=(
                f"📦 **Produkt:** `{self.product_name}`\n"
                f"💰 **Betrag:** `{self.amount_cents / 100:.2f} €`\n\n"
                "🔗 Klicke auf den Link, um die Zahlung abzuschließen:"
            ),
            color=WONDERLIFE_COLOR
        )

        await interaction.response.send_message(
            embed=embed,
            content=checkout_url,
            ephemeral=True
        )

    # ==========================================================
    # PAYPAL
    # ==========================================================

    @discord.ui.button(
        label="🪙 PayPal",
        style=discord.ButtonStyle.secondary
    )
    async def paypal_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        embed = paypal_payment_embed(
            user=self.user,
            product_name=self.product_name,
            amount_cents=self.amount_cents
        )

        view = PayPalConfirmView(
            user=self.user,
            product_name=self.product_name,
            amount_cents=self.amount_cents
        )

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )

    # ==========================================================
    # PAYSAFECARD
    # ==========================================================

    @discord.ui.button(
        label="🎟️ PaySafeCard",
        style=discord.ButtonStyle.blurple
    )
    async def paysafecard_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        embed = paysafecard_intro_embed(
            user=self.user,
            product_name=self.product_name,
            amount_cents=self.amount_cents
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

        await interaction.followup.send_modal(
            PaySafeCardModal(
                user=self.user,
                product_name=self.product_name,
                amount_cents=self.amount_cents
            )
        )

    # ==========================================================
    # TEBEX (SONDERFALL)
    # ==========================================================

    @discord.ui.button(
        label="🛒 Weiter zu Tebex",
        style=discord.ButtonStyle.green
    )
    async def tebex_only_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        # Diese View wird nur benutzt,
        # wenn allow_tebex=True gesetzt wurde
        await interaction.response.send_message(
            "🛒 **Dieses Produkt wird ausschließlich über Tebex verkauft.**\n"
            "Bitte nutze den Tebex-Shop zur Zahlung.",
            ephemeral=True
        )
