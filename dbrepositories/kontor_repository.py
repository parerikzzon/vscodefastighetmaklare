# dbrepositories/kontor_repository.py
"""
🏢 KONTOR REPOSITORY - Ansvarar för ALL databasåtkomst för kontor.
"""

from models.kontor import Kontor
from database import db


class KontorRepository:
    """
    Repository-klass för Kontor. Innehåller databasoperationer (CRUD).
    """

    def hamta_alla(self):
        """
        Hämtar ALLA kontor från databasen (SELECT * FROM kontor).
        """
        return Kontor.query.all()

    def hamta_en(self, kontor_id):
        """
        Hämtar ETT specifikt kontor baserat på ID (Primärnyckel).
        """
        return Kontor.query.get(kontor_id)

    # Lägg till andra CRUD-metoder (skapa_ny, uppdatera, radera) vid behov.
    # För detta exempel räcker det med hämta_alla och hamta_en.


# Skapa EN instans av repository
kontor_repo = KontorRepository()