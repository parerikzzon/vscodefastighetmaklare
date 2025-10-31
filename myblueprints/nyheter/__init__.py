# myblueprints/nyheter/__init__.py
"""
📰 NYHETER BLUEPRINT - Initialiseringsfil (Instruktioner för att starta nyhetsmodulen)

SYFTE: Att definiera en modul som hanterar visning av nyhetsartiklar och inläggning av kommentarer.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera nyheter-blueprintet (Blueprint-objektet).
2. Importera nödvändiga repositories (nyhet_repo och kommentar_repo).
3. Importera routes (URL-hanterarna) som tillhör nyhets-delen.

url_prefix='/nyheter' betyder att alla URL:er här börjar med /nyheter.
"""
# Importera Blueprint-klassen från Flask
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
nyheter_bp = Blueprint(
    'nyheter_bp',                       # Internt namn/identifierare. Används för url_for().
    __name__,                         # Python-modulens namn. Säger var Flask ska leta efter resurser.
    template_folder='templates'       # Säger till Flask var HTML-mallarna för detta blueprint ligger.
)


# ============================================================
# 2. IMPORTERA REPOSITORY (Databaslagret)
# ============================================================
# Importera DE TVÅ repository-instanser som behövs. 
# Nyheter-routen kommer att använda båda för att visa nyheter OCH hantera kommentarer.
from dbrepositories.nyhet_repository import nyhet_repo
from dbrepositories.kommentar_repository import kommentar_repo


# ============================================================
# 3. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
# Denna import MÅSTE vara sist!
# Filen 'nyheter_routes.py' använder variablerna 'nyheter_bp', 'nyhet_repo' och 'kommentar_repo'
# som definierades i steg 1 och 2.
from . import nyheter_routes