import discord
import os
import requests
from permissions import is_payment_user

WONDERLIFE_COLOR = 0x8E44FF
WONDERLIFE_LOGO = "https://i.ibb.co/cK47x2fF/Wonder-Life-Network-ohne-hintergrund.png"


def get_tebex_packages() -> list[dict]:
    """
    Lädt alle aktiven Tebex-Produkte live aus dem Shop
    """
    headers = {
        "Authorization": f"Bearer {os.getenv('TEBEX_PUBLIC_TOKEN')}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        "https://headless.tebex.io/api/accounts/me/packages",
        headers=headers,
        timeout=10
    )

    response.raise_for_status()
    return response.json().get("data", [])


class TebexShopView(discord.ui.View):
    """
    Zeigt alle Tebex-Produkte als Buttons an.
    """

    def __init__(self, user: discord.Member):
        super().__init__(timeout=600)
        self.user = user

        packages = get_tebex_packages()

        if not packages:
            self.add_item(TebexDisabledButton())
            return

        for package in packages:
            self.add_item(TebexProductButton(package, user))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Nur der Ziel-User darf interagieren
        """
        if not is_payment_user(interaction, self.user):
            await interaction.response.send_message(
                "❌ Diese Tebex-Zahlung ist nicht für dich.",
                ephemeral=True
            )
            return False
        return True


class TebexProductButton(discord.ui.Button):
    """
    Einzelnes Tebex-Produkt
    """

    def __init__(self, package: dict, user: discord.Member):
        label = f"{package['name']} – {package['price']:.2f}€"

        super().__init__(
            label=label,
            style=discord.ButtonStyle.green
        )

        self.package = package
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        store_id = os.getenv("TEBEX_STORE_ID")
        package_id = self.package["id"]

        checkout_url = f"https://{store_id}.tebex.io/package/{package_id}"

        embed = discord.Embed(
            title="🛒 WonderLife Tebex Checkout",
            description=(
                f"📦 **Produkt:** `{self.package['name']}`\n"
                f"💰 **Preis:** `{self.package['price']:.2f} €`\n\n"
                f"🔗 Klicke auf den Link, um die Zahlung über **Tebex** abzuschließen.\n\n"
                f"⚠️ Dieses Produkt ist **ausschließlich über Tebex** verfügbar."
            ),
            color=WONDERLIFE_COLOR
        )

        embed.set_thumbnail(url=WONDERLIFE_LOGO)
        embed.set_footer(
            text=f"WonderLife Network • Discord-ID: {interaction.user.id}"
        )

        await interaction.response.send_message(
            embed=embed,
            content=checkout_url,
            ephemeral=True
        )


class TebexDisabledButton(discord.ui.Button):
    """
    Fallback, falls keine Tebex-Produkte gefunden wurden
    """

    def __init__(self):
        super().__init__(
            label="❌ Tebex aktuell nicht verfügbar",
            style=discord.ButtonStyle.gray,
            disabled=True
        )
