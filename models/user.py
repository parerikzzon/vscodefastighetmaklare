# models/user.py
"""
👤 ANVÄNDARE-MODELL - Beskriver hur en användare ser ut i databasen.

FOKUS:
1. Definiera tabellstrukturen för användare.
2. Integrera med Flask-Login genom att ärva från UserMixin.
3. Hantera fälten 'username' (unikt) och 'password' (med SÄKERHETSVARNING).
"""
# Importera UserMixin från Flask-Login för att ge User-klassen autentiseringsfunktionalitet
from flask_login import UserMixin
# Importera 'db' (SQLAlchemy-instansen)
from database import db
# Glöm inte att installera: py -m pip install flask-login 

class User(db.Model, UserMixin):
    """
    User-modellen representerar EN användare i databasen.
    Ärver från db.Model (SQLAlchemy) och UserMixin (Flask-Login).
    """
    # Berättar för SQLAlchemy vilket tabellnamn vi vill ha
    __tablename__ = 'users'

    # -----------------------------------------------------------------
    # KOLUMNER (Fält)
    # -----------------------------------------------------------------
    # id: Primärnyckel, Flask-Login använder detta för att hantera sessioner
    id = db.Column(db.Integer, primary_key=True)
    
    # username: Användarnamnet måste vara unikt och får inte vara tomt
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # password: Lösenordet. Ska vara lagrat som en hashad sträng (inte i klartext!).
    # db.String(100) ger plats för en hashad version (som bcrypt).
    password = db.Column(db.String(100), nullable=False) 
    
    # role: Används för behörighetskontroll (t.ex. 'admin', 'user')
    role = db.Column(db.String(20), nullable=False)

    # -----------------------------------------------------------------
    # FLASK-LOGIN FUNKTIONALITET
    # -----------------------------------------------------------------
    def get_id(self):
        """
        Denna metod KRÄVS av Flask-Login. 
        Den returnerar användarens ID som en sträng för att hantera sessionen.
        """
        return str(self.id)
    
    def __repr__(self):
        """Hur objektet visas när vi printar det (för debugging)"""
        return f'<User {self.username} ({self.role})>'


# ============================================================
# STARTDATA FÖR ANVÄNDARE (Seeding Data)
# ============================================================

STARTDATA_USERS = [
    {
        'username': 'pei',
        # SÄKERHETSVARNING: Dessa lösenord är i KLARTEXT. 
        # I ett produktionssystem MÅSTE lösenorden hash-as INNAN de sparas.
        'password': '1234', 
        'role': 'admin',
        
    },
    {
        'username': 'pdo',
        'password': '123',
        'role': 'user',
        
    },
]


def skapa_start_users():
    """
    Lägger till startdata för användare i databasen ENDAST OM tabellen är tom.
    """
    # 1. Kolla om tabellen redan har data
    antal_users = User.query.count()

    if antal_users == 0:
        print("📦 Lägger till startdata för users...")

        # 2. Loopa genom startdata och skapa User-objekt
        for data in STARTDATA_USERS:
            # Skapa objekt med data (inklusive klartextlösenordet i detta exempel)
            ny_user = User(
                username=data['username'],
                password=data['password'],
                role=data['role']
            )
            db.session.add(ny_user)

        # 3. Spara alla till databasen
        db.session.commit()
        print(f"✓ Lade till {len(STARTDATA_USERS)} users")
    else:
        print(f"✓ Tabellen 'users' har redan {antal_users} rader. Ingen startdata lades till.")