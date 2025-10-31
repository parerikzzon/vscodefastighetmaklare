# myblueprints/nyheter/nyheter_routes.py
"""
📰 NYHETER ROUTES - Hanterar URL:er för att VISA nyheter.

SINGLE RESPONSIBILITY: Fungerar som "Controller"-lagret för nyhetslistan.
- Hanterar URL:er för listvisning.
- Anropar nyhet_repo för att hämta data från databasen.
- Skickar data till HTML-mallar för visning.
"""
from flask import render_template
# Importera blueprint-objektet och repositories från __init__.py
from . import nyheter_bp, nyhet_repo # Vi importerar endast vad som behövs för denna rutt


@nyheter_bp.route('/') # url_prefix /nyheter ger den fullständiga URL:en /nyheter/
def lista_nyheter():
    """
    Visar ALLA nyheter på en sida, optimerat för att visa relaterade objekt (Mäklare och Kommentarer).

    URL: /nyheter/
    """
    # 1. Hämta data från Repository.
    # hamta_alla_med_relationer() är en optimerad metod som hämtar nyheterna 
    # TILLSAMMANS med deras relaterade Mäklare och Kommentarer (eager loading).
    alla_nyheter = nyhet_repo.hamta_alla_med_relationer() # <--- Hämta med relationer!

    # 2. Skicka datan till HTML-mallen (View Layer)
    return render_template(
        'nyhets_lista.html',
        nyheter_lista=alla_nyheter,
        titel='Nyheter & Kommentarer'
    )