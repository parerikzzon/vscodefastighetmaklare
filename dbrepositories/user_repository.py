# dbrepositories/user_repository.py
"""
👤 ANVÄNDARE REPOSITORY - Ansvarar för ALL databasåtkomst för användare.

SÄKERHETSANMÄRKNING:
Detta repository hanterar lösenordsfältet ('password'). I en verklig applikation
SKULLE INTE det faktiska, okrypterade lösenordet sparas i databasen.
Lösenordet måste hashas och saltas INNAN det skickas till denna 'skapa_ny' metod.
Detta repository hanterar dock enbart databasoperationerna (CRUD).

SINGLE RESPONSIBILITY: ENDAST databasoperationer (CREATE, READ, UPDATE, DELETE).
"""

# Importera User-modellen (klassen som representerar 'user' tabellen)
from models.user import User
# Importera databasobjektet (session-hanteraren)
from database import db


class UserRepository:
    """
    Repository-klass för User.
    Innehåller alla databasoperationer (CRUD).
    """

    def hamta_alla(self):
        """
        Hämtar ALLA användare från databasen.

        Returns:
            list: Lista med alla User-objekt.
        """
        return User.query.all()

    def hamta_en(self, user_id):
        """
        Hämtar EN specifik användare baserat på ID (Primärnyckel).

        Args:
            user_id (int): ID för användaren.

        Returns:
            User: User-objektet, eller None om det inte finns.
        """
        return User.query.get(user_id)

    def hamta_eller_404(self, user_id):
        """
        Hämtar EN användare eller utlöser 404-fel. Användbar för admin-gränssnitt.

        Args:
            user_id (int): ID för användaren.

        Returns:
            User: User-objektet (garanterat att existera).
        """
        return User.query.get_or_404(user_id)

    def hamta_user_username(self, username):
        """
        Hämtar EN användare baserat på dess UNIKA användarnamn.
        Detta är den primära sökmetoden som används vid inloggning.

        Args:
            username (str): Användarnamnet att söka efter.

        Returns:
            User: User-objektet, eller None om användarnamnet inte hittas.
        """
        # 1. .filter_by(username=username): Lägger till villkoret WHERE username = '...'
        # 2. .first(): Exekverar frågan och returnerar ENDAST det första matchande resultatet.
        #    (Detta förutsätter att 'username' är unikt i databasen.)
        user = User.query.filter_by(username=username).first()

        if user:
            return user
        return None # Returnerar None explicit om ingen användare hittades.

    def skapa_ny(self, data):
        """
        Skapar en NY användare i databasen (INSERT).

        Args:
            data (dict): Dictionary med user-information (username, password, role).

        Returns:
            User: Den nya User-instansen.
        """
        # Skapa en ny instans av User-modellen.
        ny_user = User(
            username=data['username'],
            # VIKTIGT: Fältet 'password' bör vara hashat och saltat av en annan funktion
            # INNAN det når detta lager. Här sparas bara det värde som skickas in.
            password=data['password'],
            # 'role' används ofta för behörighetskontroll (t.ex. 'admin', 'standard').
            roll=data['role'],
        )

        # 1. Lägg till i session.
        db.session.add(ny_user)
        # 2. Commit: Spara permanent.
        db.session.commit()

        return ny_user

    def uppdatera(self, user_id, data):
        """
        Uppdaterar en BEFINTLIG användare (UPDATE-operation).

        Args:
            user_id (int): ID för användaren att uppdatera.
            data (dict): Ny data.

        Returns:
            User: Den uppdaterade användaren, eller None.
        """
        user = User.query.get(user_id)

        if user:
            # Uppdatera alla fält på objektet.
            user.username = data['username']
            # Uppdatera lösenord (OBS: data['password'] måste vara det nya hashede värdet)
            user.password = data['password']
            user.role = data['role']

            # Spara ändringarna
            db.session.commit()

        return user

    def radera(self, user_id):
        """
        Raderar en användare från databasen (DELETE).

        Args:
            user_id (int): ID för användaren att radera.

        Returns:
            bool: True om radering lyckades, False om användaren inte fanns.
        """
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            # Commit: Utför DELETE.
            db.session.commit()
            return True

        return False


# Skapa EN instans av repository som kan användas överallt
user_repo = UserRepository()