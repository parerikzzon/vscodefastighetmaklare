# blueprints/kontor/kontor_routes.py
"""
🏢 KONTOR ROUTES - Hanterar URL:er för att VISA kontor (Karta och API).
"""
from flask import render_template, jsonify
from . import kontor_bp, kontor_repo

# ============================================================
# 1. WEBBVY: KARTA
# ============================================================

@kontor_bp.route('/')
def visa_karta():
    """
    Visar en HTML-sida med en Leaflet-karta som visar alla kontor.
    
    URL: /kontor/ (eftersom url_prefix='/kontor' i __init__.py)
    """
    # Hämtar alla kontor, men skickar dem inte direkt till mallen
    # utan använder API:et istället för att Leaflet ska ladda datan.
    return render_template(
        'kontor_karta.html',
        titel='Våra Kontor på Karta'
    )


# ============================================================
# 2. API-ÄNDPUNKT: KONTORSDATA (JSON)
# ============================================================

@kontor_bp.route('/api/data')
def api_kontor_data():
    """
    Returnerar ALL kontorsdata i JSON-format. Används av Leaflet-kartan.
    
    URL: /kontor/api/data
    """
    alla_kontor = kontor_repo.hamta_alla()
    # Använder Kontor.to_dict() för att konvertera objekt till dictionary
    kontor_data = [kontor.to_dict() for kontor in alla_kontor]
    
    return jsonify(kontor_data)