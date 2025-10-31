# blueprints/maklare/maklare_routes.py
"""
🤵 MÄKLARE ROUTES - Hanterar URL:er för att VISA mäklare (både HTML och JSON API).

SINGLE RESPONSIBILITY: Fungerar som "Controller"-lagret för mäklardata.
- Hanterar URL:er för listor, detaljer och API-svar.
- Använder maklare_repo för all dataåtkomst.
"""
# Importera jsonify för att returnera JSON-svar i API-rutten
from flask import jsonify, render_template
# Importera blueprint-objektet och maklare_repo från __init__.py
from . import maklare_bp, maklare_repo


# ============================================================
# 1. WEBBVY: LISTA
# ============================================================

@maklare_bp.route('/')
def lista_maklare():
    """
    Visar ALLA mäklare på en HTML-sida.
    
    URL: /maklare/ (om prefixet är satt till /maklare i app.py)
    """
    # 1. Hämta alla Mäklare-objekt från databasen (via repository)
    alla_maklare = maklare_repo.hamta_alla()

    # 2. Skicka datan till HTML-mallen (Webbvy)
    return render_template(
        'maklare_lista.html',
        maklare_lista=alla_maklare,
        titel='Våra Mäklare'
    )


# ============================================================
# 2. WEBBVY: DETALJ
# ============================================================

@maklare_bp.route('/<int:maklare_id>')
def maklare_detalj(maklare_id):
    """
    Visar DETALJER för EN specifik mäklare på en HTML-sida.

    URL: /maklare/1

    Args:
        maklare_id (int): ID för mäklaren (från URL-parametern)
    """
    # 1. Hämta den specifika mäklaren via Repository.
    # hamta_eller_404: Om objektet inte hittas, skickar den automatiskt 404.
    maklare = maklare_repo.hamta_eller_404(maklare_id)

    # 2. Skicka mäklaren till HTML-mallen (Webbvy)
    return render_template(
        'maklare_detalj.html',
        maklare=maklare,
        titel=maklare.namn
    )

# ============================================================
# 3. API-ÄNDPUNKT: DETALJ (JSON)
# ============================================================

# Denna rutt returnerar JSON-data istället för HTML
@maklare_bp.route('/api/v1/maklare/<int:maklare_id>')
def api_maklare(maklare_id):
    """
    Returnerar mäklardata i JSON-format för externa system.
    
    URL: /maklare/api/v1/maklare/1
    """
    # 1. Hämta den specifika mäklaren (hamta_en returnerar None om den inte hittas)
    maklare = maklare_repo.hamta_en(maklare_id)

    if maklare:
        # 2. jsonify: Konverterar Python-dictionaryn till ett JSON-svar
        return jsonify({
            'namn': maklare.namn,
            'titel': maklare.titel,
            'epost': maklare.epost,
            'telefon': maklare.telefon,
            'beskrivning': maklare.beskrivning
        })
    else:
        # 3. Om den inte hittas, returnera ett felmeddelande och HTTP-status 404
        return jsonify({'error': 'Mäklare hittades inte'}), 404