# myblueprints/admin/__init__.py
"""
⚙️ ADMIN BLUEPRINT - Initialiseringsfil (Instruktioner för att starta admin-modulen)

SYFTE: Att definiera en isolerad del av applikationen ('admin-panelen').
Blueprints hjälper till att organisera stora applikationer genom att dela upp dem i moduler.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera admin-blueprintet.
2. Importera nödvändiga resurser (t.ex. databas-repositories).
3. Importera routes (URL-hanterarna) som tillhör admin-panelen.

När blueprintet registreras i huvudapplikationen, får det url_prefix='/admin', vilket betyder att
alla URL:er som definieras här (t.ex. /users) automatiskt blir /admin/users.
"""
# Importera Blueprint-klassen från Flask
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
admin_bp = Blueprint(
    'admin_bp',                       # Internt namn/identifierare för blueprintet. Används för url_for().
    __name__,                         # Python-modulens namn. Säger var Flask ska leta efter resurser.
    template_folder='templates',      # Säger till Flask var HTML-mallarna för detta blueprint ligger (t.ex. myblueprints/admin/templates).
    url_prefix='/admin'               # (Läggs ofta till vid registrering i huvudappen, men kan definieras här också)
)


# ============================================================
# 2. IMPORTERA REPOSITORY (Databaslagret)
# ============================================================
# Importerar den enda instansen av repository-klassen. 
# Detta ger admin-routerna tillgång till databasen utan att behöva importera databasobjektet direkt.
from dbrepositories.bostad_repository import bostad_repo


# ============================================================
# 3. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
# Denna import MÅSTE vara sist!
# Anledningen: Filen 'admin_routes.py' använder variabeln 'admin_bp'
# som just definierades OVANFÖR. Om den importerades tidigare skulle det bli ett fel.
from . import admin_routes