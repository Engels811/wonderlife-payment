import os

INVOICE_BASE_PATH = "/home/discord/invoices"

def safe_invoice_path(path: str) -> str | None:
    """
    Schutz gegen Path Traversal
    """
    if not path:
        return None

    full = os.path.realpath(path)
    base = os.path.realpath(INVOICE_BASE_PATH)

    if not full.startswith(base):
        return None

    if not os.path.exists(full):
        return None

    return full
