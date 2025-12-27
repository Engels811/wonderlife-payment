from fpdf import FPDF
import os
from datetime import datetime

INVOICE_DIR = "/home/discord/invoices"
AGB_URL = "https://wonderlife-network.eu/agb"

def create_invoice(discord_id, product, amount_cents, customer, vat_info):
    invoice_number = f"WL-{int(datetime.utcnow().timestamp())}"
    path = f"{INVOICE_DIR}/{invoice_number}.pdf"

    os.makedirs(INVOICE_DIR, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.cell(0, 8, "WonderLife Network", ln=True)
    pdf.cell(0, 8, "Rechnung", ln=True)
    pdf.ln(4)

    pdf.cell(0, 8, f"Rechnung: {invoice_number}", ln=True)
    pdf.cell(0, 8, f"Datum: {datetime.utcnow().strftime('%d.%m.%Y')}", ln=True)
    pdf.ln(6)

    pdf.multi_cell(0, 6, customer["address"])
    pdf.ln(4)

    pdf.cell(0, 8, f"Produkt: {product}", ln=True)
    pdf.cell(0, 8, f"Nettobetrag: {amount_cents/100:.2f} EUR", ln=True)
    pdf.cell(0, 8, f"MwSt ({vat_info['vat_rate']}%): {vat_info['vat_amount']/100:.2f} EUR", ln=True)
    pdf.cell(0, 8, f"Gesamt: {vat_info['gross']/100:.2f} EUR", ln=True)

    pdf.ln(6)
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(
        0, 5,
        f"Es gelten unsere AGB: {AGB_URL}"
    )

    pdf.output(path)
    return invoice_number, path
