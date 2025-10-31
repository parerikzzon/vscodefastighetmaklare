# myblueprints/auth/__init__.py
"""
🔑 AUTH BLUEPRINT - Initialiseringsfil (Instruktioner för att starta autentiseringsmodulen)

SYFTE: Att definiera en isolerad del av applikationen som hanterar all autentisering
och användarhantering (login, logout, registrering).

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera auth-blueprintet.
2. Importera nödvändigt repository (user_repo).
3. Importera routes (URL-hanterarna) som tillhör autentiseringen.
"""
# Importera Blueprint-klassen från Flask
from flask import Blueprint

# ============================================================
# 1. SKAPA BLUEPRINTET
# ============================================================
auth_bp = Blueprint(
    'auth_bp',                       # Internt namn/identifierare. Används för url_for('auth_bp.login').
    __name__,                         # Python-modulens namn. Säger var Flask ska leta efter resurser.
    template_folder='templates',      # Säger till Flask var HTML-mallarna för detta blueprint ligger (t.ex. myblueprints/auth/templates).
    # url_prefix='/auth' är valfritt, ofta lämnas login/logout utan prefix i huvudnivån.
)


# ============================================================
# 2. IMPORTERA REPOSITORY (Databaslagret)
# ============================================================
# Importerar den enda instansen av user_repository. 
# Detta är nödvändigt för att kunna slå upp användare vid inloggning.
from dbrepositories.user_repository import user_repo


# ============================================================
# 3. IMPORTERA ROUTES (URL:er och logik)
# ============================================================
# Denna import MÅSTE vara sist!
# Anledningen: Filen 'auth_routes.py' använder variabeln 'auth_bp'
# som just definierades OVANFÖR.
from . import auth_routes