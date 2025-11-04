# shl/__init__.py
"""
🏒 SHL STATISTIK BLUEPRINT - Initialiseringsfil
Ansvarar för att definiera SHL-blueprintet.
"""
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
shl_bp = Blueprint(
    'shl_bp',                       # Internt namn/identifierare
    __name__,                         # Python-modulens namn
    template_folder='templates',      # Säger var HTML-mallarna för detta blueprint ligger (shl/templates)
)


# ============================================================
# 2. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
# Denna import MÅSTE vara sist eftersom routarna använder 'shl_bp'-objektet.
from . import shl_routes