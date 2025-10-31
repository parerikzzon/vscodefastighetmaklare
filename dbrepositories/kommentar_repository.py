# dbrepositories/kommentar_repository.py
"""
💬 KOMMENTAR REPOSITORY - Hanterar ALL databasåtkomst för kommentarer.

SYFTE: Att isolera all logik som rör sparande, hämtning och hantering av
kommentarobjekt i databasen. Den fungerar som datalagret för alla kommentarer.

FOKUS: CRUD-operationer (hittills endast READ och CREATE) för objektet Kommentar,
med särskilt fokus på relationen till en Nyhet.
"""

# Importera Kommentar-modellen (klassen som representerar 'kommentar' tabellen i databasen)
from models.kommentar import Kommentar
# Importera databasobjektet (SQLAlchemy-sessionen)
from database import db


class KommentarRepository:
    """
    Repository-klass för Kommentar.
    Innehåller alla databasoperationer (CRUD).
    """

    def hamta_alla_for_nyhet(self, nyhet_id):
        """
        Hämtar ALLA kommentarer som är kopplade till en specifik nyhetsartikel.

        Detta är en sökfråga baserad på en RELATION (nyhet_id är en främmande nyckel).

        Args:
            nyhet_id (int): ID för nyhetsartikeln vars kommentarer ska hämtas.

        Returns:
            list: En sorterad lista med Kommentar-objekt.
        """
        # 1. Kommentar.query: Startar databasfrågan (SELECT * FROM kommentar).
        # 2. .filter_by(nyhet_id=nyhet_id): Lägger till villkoret (WHERE nyhet_id = X).
        # 3. .order_by(Kommentar.datum.asc()): Sorterar resultatet.
        #    - Kommentar.datum: Fältet i tabellen som ska sorteras.
        #    - .asc(): Sorterar i stigande ordning (Ascending), t.ex. äldsta först.
        # 4. .all(): Exekverar frågan och returnerar resultaten som en lista.
        return Kommentar.query.filter_by(nyhet_id=nyhet_id).order_by(Kommentar.datum.asc()).all()

    def skapa_ny(self, nyhet_id, data):
        """
        Skapar en NY kommentar i databasen och kopplar den till en nyhetsartikel (INSERT-operation).
        Kommentaren får automatiskt ett datum (om modellen är konfigurerad för det).

        Args:
            nyhet_id (int): ID för nyhetsartikeln som kommentaren tillhör (Främmande Nyckel).
            data (dict): Dictionary med kommentar-information (t.ex. 'namn' och 'innehall').

        Returns:
            Kommentar: Den nya Kommentar-instansen som skapades.
        """
        # Skapa en ny instans av Kommentar-modellen.
        ny_kommentar = Kommentar(
            namn=data['namn'],
            innehall=data['innehall'],
            # VIKTIGT: Sätter Främmande Nyckel (FK) för att länka kommentaren till rätt nyhet.
            nyhet_id=nyhet_id
        )

        # 1. Lägg till i session: Förbereder objektet för att sparas.
        db.session.add(ny_kommentar)
        # 2. Spara/Committa: Utför den faktiska INSERT-frågan till databasen.
        db.session.commit()

        return ny_kommentar


# Skapa EN instans av repository som kan användas överallt
# Denna instans ska importeras av andra moduler (t.ex. views/controllers)
# för att hantera kommentarer utan att behöva skapa en ny instans varje gång.
kommentar_repo = KommentarRepository()