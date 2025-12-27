import os
from logic.subscriptions import (
    get_expired_auto_renew_subscriptions,
    extend_subscription,
    disable_subscription
)
from logic.invoices import create_invoice
from logic.mail import send_invoice_email
from logic.vat import calculate_vat

def process_auto_renewals():
    subs = get_expired_auto_renew_subscriptions()

    for sub in subs:
        try:
            # -----------------------------------
            # VAT
            # -----------------------------------
            vat = calculate_vat(
                sub["price_cents"],
                country_code="DE"  # später dynamisch
            )

            # -----------------------------------
            # INVOICE
            # -----------------------------------
            invoice_number, pdf_path = create_invoice(
                sub["discord_id"],
                sub["product"],
                sub["price_cents"],
                customer={
                    "address": "Auto-Renew Kunde\nDiscord ID: " + str(sub["discord_id"])
                },
                vat_info=vat
            )

            # -----------------------------------
            # EMAIL (optional)
            # -----------------------------------
            send_invoice_email(
                to_email="customer@example.com",  # später aus DB
                invoice_number=invoice_number,
                pdf_path=pdf_path
            )

            # -----------------------------------
            # EXTEND SUBSCRIPTION
            # -----------------------------------
            extend_subscription(
                sub_id=sub["id"],
                days=sub["billing_interval_days"]
            )

            print(
                f"[RENEW] OK | Sub {sub['id']} | "
                f"{sub['product']} verlängert"
            )

        except Exception as e:
            # Fehler → Abo pausieren
            disable_subscription(sub["id"])
            print(
                f"[RENEW] FAILED | Sub {sub['id']} | {e}"
            )
