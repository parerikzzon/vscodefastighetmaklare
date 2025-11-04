# shl/shl_routes.py
#komihå att installera
#pip install requests beautifulsoup4
#py -m pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
from flask import render_template, request
from . import shl_bp # Importera Blueprint-objektet
import re
from datetime import datetime, timedelta

# URL för SHL-tabellen
SHL_URL = "https://www.shl.se/game-stats/standings/standings?count=25"
#SHL_URL = "https://www.flashscore.se/shl/tabellstallning/#/CMVpiF7T/tabell/oversikt/"


# ============================================================
# WEBSKRAPNINGSLOGIK (Inkluderad lokalt)
# ============================================================

def skrapa_shl_tabell(url: str): 
    
    
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table =soup.find('div', class_='ui-table')

        if not table:
            return None, ["Kunde inte hitta tabell"]
        else:
            return "Fann tabellen"
        


# ============================================================
# FLASK ROUTES (URL Mapping)
# ============================================================

# Rutt 1: Huvudvy för tabellen och sökformuläret
# url_prefix: /shl/tabell
@shl_bp.route('/', methods=['GET'])
def visa_shl_tabell():
    """
    Visar SHL-tabellen och hanterar sökningen efter ett specifikt lag.
    """
    # Hämta data (använder caching)
    standings_data = skrapa_shl_tabell(SHL_URL)
    
    return render_template(
        'shl_tabell.html',
        titel="SHL tabellen",        
        standings=standings_data,
        
    )


# Rutt 2: Hjälpfunktion för att söka plats i datan
def sok_lagets_plats(standings_data, team_name: str):
    """
    Söker efter ett lag i ställningen och returnerar dess plats (används av Rutt 1).
    """
    if not standings_data:
        return "Sökningen misslyckades eftersom ingen tabellinformation kunde hämtas."

    search_name = team_name.strip().lower()

    for team in standings_data:
        # Använder det reella lagnamnet (Team-kolumnen)
        data_team_name = team.get('Lag', '').strip().lower()
        
        # Använd 'in' för att matcha delar av lagnamnet
        if search_name in data_team_name:
            plats = team.get('Plats')
            fullt_namn = team.get('Lag')
            if plats and plats.isdigit():
                return f"Laget **'{fullt_namn}'** är rankat på plats **{plats}** i SHL-tabellen."
            
    return f"Kunde inte hitta laget **'{team_name}'** i SHL-tabellen."