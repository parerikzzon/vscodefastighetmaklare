# myblueprints/kontor/__init__.py
"""
🏢 KONTOR BLUEPRINT - Initialiseringsfil
"""
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
kontor_bp = Blueprint(
    'kontor_bp',                       # Internt namn/identifierare.
    __name__,                          # Python-modulens namn.
    url_prefix='/kontor',              # Sätter bas-URL:en till /kontor
    template_folder='templates'        # Säger var HTML-mallarna ligger
)


# ============================================================
# 2. IMPORTERA REPOSITORY (Databaslagret)
# ============================================================
from dbrepositories.kontor_repository import kontor_repo


# ============================================================
# 3. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
from . import kontor_routes