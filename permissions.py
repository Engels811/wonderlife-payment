import discord
import os

# ============================================
# WONDERLIFE PERMISSIONS
# ============================================

# Rollen, die Zahlungsprozesse STARTEN dürfen
# (z. B. /payment Command)
PAYMENT_TEAM_ROLE_IDS = [
    1329371549052043328,  # Shop-Team
    111111111111111111,   # Support
    222222222222222222    # Admin
]

# Rollen, die Zahlungen BESTÄTIGEN dürfen
# (PayPal / PaySafeCard Freigabe)
PAYMENT_ADMIN_ROLE_IDS = [
    222222222222222222,   # Admin
    333333333333333333    # Projektleitung
]


def has_any_role(member: discord.Member, role_ids: list[int]) -> bool:
    """
    Prüft, ob ein Member mindestens eine der angegebenen Rollen besitzt
    """
    return any(role.id in role_ids for role in member.roles)


def can_start_payment(member: discord.Member) -> bool:
    """
    Darf der User eine Zahlung starten?
    """
    return has_any_role(member, PAYMENT_TEAM_ROLE_IDS)


def can_confirm_payment(member: discord.Member) -> bool:
    """
    Darf der User eine Zahlung bestätigen / freigeben?
    """
    return has_any_role(member, PAYMENT_ADMIN_ROLE_IDS)


def is_payment_user(interaction: discord.Interaction, target_user: discord.Member) -> bool:
    """
    Sicherheitscheck:
    Stellt sicher, dass nur der richtige User mit seiner Zahlung interagiert
    """
    return interaction.user.id == target_user.id
