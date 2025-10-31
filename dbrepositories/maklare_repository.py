# dbrepositories/maklare_repository.py
"""
👔 MÄKLARE REPOSITORY - Ansvarar för ALL databasåtkomst för mäklare.

DETTA ÄR ETT DESIGNMÖNSTER (Repository Pattern):
Syftet är att hålla all databaslogik på ett ställe. Resten av applikationen
(som visar upp webbsidor) vet bara att den frågar en 'MaklareRepository' om data.

SINGLE RESPONSIBILITY (Enkelt ansvar): Denna fil har ENDAST ansvar för:
- Hämta data från databasen (READ)
- Lägga till ny data (CREATE)
- Uppdatera befintlig data (UPDATE)
- Ta bort data (DELETE)

Denna fil ska ALDRIG hantera webb- eller användarinteraktionslogik.
"""

# Importera Maklare-modellen (klassen som representerar 'maklare' tabellen)
from models.maklare import Maklare
# Importera databasobjektet (session-hanteraren)
from database import db


class MaklareRepository:
    """
    Repository-klass för Mäklare.
    Innehåller alla standardiserade databasoperationer (CRUD).
    """

    def hamta_alla(self):
        """
        Hämtar ALLA mäklare från databasen (SELECT * FROM maklare).

        Returns:
            list: En lista med alla Maklare-objekt.
        """
        # Maklare.query är startpunkten för att bygga databasfrågan.
        # .all() exekverar frågan och returnerar en lista.
        return Maklare.query.all()

    def hamta_en(self, maklare_id):
        """
        Hämtar EN specifik mäklare baserat på ID (Primärnyckel).

        Args:
            maklare_id (int): ID (heltal) för mäklaren att hitta.

        Returns:
            Maklare: Mäklare-objektet om det hittas, annars Python-värdet None.
        """
        # .get(id) är det snabbaste sättet att slå upp en rad i databasen via Primärnyckeln.
        return Maklare.query.get(maklare_id)

    def hamta_eller_404(self, maklare_id):
        """
        Hämtar EN mäklare eller utlöser ett 404-fel (om du använder en webbramverk t.ex. Flask).
        Detta sparar dig från att behöva skriva if/else-logik för att kontrollera om objektet finns.

        Args:
            maklare_id (int): ID för mäklaren.

        Returns:
            Maklare: Det hittade Maklare-objektet.

        Raises:
            404: Om ID:t inte finns i databasen.
        """
        # Funktionen sköter både sökning och felhantering.
        return Maklare.query.get_or_404(maklare_id)

    def skapa_ny(self, data):
        """
        Skapar en NY mäklare i databasen (INSERT-operation).

        Args:
            data (dict): Dictionary som innehåller obligatoriska och valfria fält.

        Returns:
            Maklare: Den nya Maklare-instansen som nu är sparad i databasen.
        """
        # Skapa en ny Python-instans av modellen.
        ny_maklare = Maklare(
            namn=data['namn'],
            epost=data['epost'],
            # Använder .get() med tom sträng som standard för valfria fält.
            telefon=data.get('telefon', ''),
            titel=data.get('titel', ''),
            beskrivning=data.get('beskrivning', '')
        )

        # 1. Lägg till i session: Förbereder SQL INSERT-frågan.
        db.session.add(ny_maklare)
        # 2. Commit: Exekverar frågan och sparar permanent i databasen.
        db.session.commit()

        return ny_maklare

    def uppdatera(self, maklare_id, data):
        """
        Uppdaterar en BEFINTLIG mäklare baserat på ID (UPDATE-operation).

        Args:
            maklare_id (int): ID för mäklaren att uppdatera.
            data (dict): Ny data som ska ersätta den gamla.

        Returns:
            Maklare: Den uppdaterade mäklaren, eller None om den inte hittades.
        """
        # Steg 1: Hämta det befintliga objektet.
        maklare = Maklare.query.get(maklare_id)

        if maklare:
            # Steg 2: Uppdatera fälten på Python-objektet.
            maklare.namn = data['namn']
            maklare.epost = data['epost']
            maklare.telefon = data.get('telefon', '')
            maklare.titel = data.get('titel', '')
            maklare.beskrivning = data.get('beskrivning', '')

            # Steg 3: Commit: Skickar ändringarna (UPDATE-frågan) till databasen.
            db.session.commit()

        return maklare

    def radera(self, maklare_id):
        """
        Raderar en mäklare från databasen (DELETE-operation).

        Args:
            maklare_id (int): ID för mäklaren att radera.

        Returns:
            bool: True om raderingen lyckades, False om mäklaren inte fanns.
        """
        # Steg 1: Hämta objektet för att kontrollera att det finns.
        maklare = Maklare.query.get(maklare_id)

        if maklare:
            # Steg 2: Markera objektet för radering.
            db.session.delete(maklare)
            # Steg 3: Commit: Utför den faktiska DELETE-frågan.
            db.session.commit()
            return True

        return False


# Skapa EN instans av repository
# Detta är den enda instansen som applikationen behöver för att prata med Maklare-databasen.
maklare_repo = MaklareRepository()