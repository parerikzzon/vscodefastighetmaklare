# myblueprints/maklare/__init__.py
"""
🤵 MÄKLARE BLUEPRINT - Initialiseringsfil (Instruktioner för att starta mäklar-modulen)

SYFTE: Att definiera en modul som hanterar visning av mäklarlistor och enskilda mäklarprofiler.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera maklare-blueprintet (Blueprint-objektet).
2. Importera nödvändigt repository (maklare_repo).
3. Importera routes (URL-hanterarna) som tillhör mäklar-delen.

url_prefix='/maklare' betyder att alla URL:er som definieras i maklare_routes.py
automatiskt får prefixet /maklare (t.ex. /maklare/anna-stahl).

VIKTIGT OM IMPORTORDNING:
Denna ordning (Blueprint -> Repository -> Routes) är nödvändig för att undvika cirkulära importfel.
"""
# Importera Blueprint-klassen från Flask
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
maklare_bp = Blueprint(
    'maklare_bp',                       # Internt namn/identifierare. Används för url_for().
    __name__,                         # Python-modulens namn. Säger var Flask ska leta efter resurser.
    template_folder='templates'       # Säger till Flask var HTML-mallarna för detta blueprint ligger.
)


# ============================================================
# 2. IMPORTERA REPOSITORY (Databaslagret)
# ============================================================
# Importerar den enda instansen av maklare_repository. 
# Detta ger routarna tillgång till mäklardata i databasen.
from dbrepositories.maklare_repository import maklare_repo


# ============================================================
# 3. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
# Denna import MÅSTE vara sist!
# Filen 'maklare_routes.py' använder variablerna 'maklare_bp' och 'maklare_repo'
# som definierades i steg 1 och 2.
from . import maklare_routes