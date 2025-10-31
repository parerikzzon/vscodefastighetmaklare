# dbrepositories/nyhet_repository.py
"""
📰 NYHET REPOSITORY - Ansvarar för ALL databasåtkomst för nyheter.

FOKUS: CRUD-operationer och, VIKTIGT, optimering av hämtning av relaterade data
(som Mäklare och Kommentarer) för att hålla webbplatsen snabb.

SINGLE RESPONSIBILITY: Precis som de andra repositorierna, hanterar denna fil
ENDAST databasinteraktioner och är helt oberoende av webbrouting.
"""

# Importera Nyhet-modellen
from models.nyhet import Nyhet
# Importera databasobjektet (session-hanteraren)
from database import db
# VIKTIGT: Importera SQLAlchemy-verktyg för Eager Loading (laddning av relationer)
from sqlalchemy.orm import joinedload, selectinload


class NyhetRepository:
    """
    Repository-klass för Nyhet.
    Innehåller alla databasoperationer (CRUD).
    """

    def hamta_alla(self):
        """
        Hämtar ALLA nyheter från databasen.
        Denna metod används när vi bara behöver nyhetsdatan självt (titel, innehåll).

        Sortering: Nyast först (.desc() = Descending, fallande).

        Returns:
            list: Lista med alla Nyhet-objekt, sorterade efter datum.
        """
        # Sorterar baserat på 'datum'-fältet i fallande ordning.
        return Nyhet.query.order_by(Nyhet.datum.desc()).all()

    def hamta_alla_med_relationer(self):
        """
        Hämtar ALLA nyheter OCH deras relaterade data (Mäklare och Kommentarer)
        i ett optimerat antal databasfrågor.

        OPTIMERING (Eager Loading för att undvika N+1-problem):
        - joinedload(Nyhet.maklare): Utför en SQL JOIN. Laddar Mäklarens data
          i SAMMA fråga som nyheten hämtas. Effektivt för One-to-One eller Many-to-One relationer.
        - selectinload(Nyhet.kommentarer): Utför en SEPARAT, men OPTIMERAD, fråga.
          Den hämtar alla kommentarer för alla nyheter som hittades i EN fråga.
          Effektivt för One-to-Many relationer (som Nyhet -> Kommentarer).

        Returns:
            list: Lista med Nyhet-objekt där varje Nyhet-objekt redan har sin Mäklare
                  och sina Kommentarer inlästa.
        """
        return Nyhet.query \
            .options(
                # Ladda den enskilda Mäklaren som är kopplad till nyheten
                joinedload(Nyhet.maklare),
                # Ladda alla kommentarer som är kopplade till nyheten
                selectinload(Nyhet.kommentarer)
            ) \
            .order_by(Nyhet.datum.desc()).all()

    def hamta_en(self, nyhet_id):
        """
        Hämtar EN specifik nyhet baserat på ID (utan att ladda relationer).

        Args:
            nyhet_id (int): ID för nyheten.

        Returns:
            Nyhet: Nyhet-objektet, eller None.
        """
        return Nyhet.query.get(nyhet_id)

    def hamta_eller_404(self, nyhet_id):
        """
        Hämtar EN nyhet eller utlöser 404-fel. Används ofta i detaljvyer.

        Args:
            nyhet_id (int): ID för nyheten.

        Returns:
            Nyhet: Nyhet-objektet (garanterat att existera).
        """
        return Nyhet.query.get_or_404(nyhet_id)

    def skapa_ny(self, data):
        """
        Skapar en NY nyhet i databasen (INSERT).

        Args:
            data (dict): Dictionary med titel, innehåll och maklare_id.

        Returns:
            Nyhet: Den nya Nyhet-instansen.
        """
        ny_nyhet = Nyhet(
            titel=data['titel'],
            innehall=data['innehall'],
            # Ställer in Främmande Nyckel (FK) för relationen till Mäklaren.
            maklare_id=data.get('maklare_id')
        )

        # 1. Lägg till i session.
        db.session.add(ny_nyhet)
        # 2. Commit: Spara permanent.
        db.session.commit()
        return ny_nyhet

    def radera(self, nyhet_id):
        """
        Raderar en nyhet från databasen (DELETE).

        Args:
            nyhet_id (int): ID för nyheten att radera.

        Returns:
            bool: True om radering lyckades, False om nyheten inte fanns.
        """
        nyhet = Nyhet.query.get(nyhet_id)
        if nyhet:
            db.session.delete(nyhet)
            # VIKTIGT: Detta kan också radera relaterade kommentarer
            # om din Nyhet-modell har 'cascade="all, delete-orphan"' inställt.
            db.session.commit()
            return True
        return False

    # Du kan enkelt lägga till en uppdatera-metod (se t.ex. MaklareRepository) här vid behov.
    def uppdatera(self, nyhet_id, data):
        """
        Uppdaterar en BEFINTLIG nyhet (UPDATE).
        """
        nyhet = Nyhet.query.get(nyhet_id)
        if nyhet:
            nyhet.titel = data['titel']
            nyhet.innehall = data['innehall']
            nyhet.maklare_id = data.get('maklare_id') # Uppdatera även mäklaren vid behov
            db.session.commit()
            return nyhet
        return None


# Skapa EN instans av repository som kan användas överallt
nyhet_repo = NyhetRepository()