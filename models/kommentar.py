# models/kommentar.py
"""
💬 KOMMENTAR-MODELL - Beskriver hur en kommentar ser ut i databasen.

FOKUS:
1. Definiera tabellstrukturen för kommentarer.
2. Sätta upp en Främmande Nyckel (nyhet_id) för att länka till Nyhet-tabellen.
3. Hantera tidsstämpling (datum) automatiskt.

OBS! Denna fil hanterar INTE logiken för att hämta eller spara kommentarer.
Det sköts av KommentarRepository.
"""
# Importera 'db' (SQLAlchemy-instansen)
from database import db
# Importera datetime-modulen för att kunna sätta aktuellt datum automatiskt
from datetime import datetime


class Kommentar(db.Model):
    """
    Kommentar-modellen representerar EN kommentar i databasen.
    Ärver från db.Model för att hantera ORM-mappningen.
    """
    # Berättar för SQLAlchemy vilket tabellnamn vi vill ha
    __tablename__ = 'kommentarer'

    # -----------------------------------------------------------------
    # KOLUMNER (Fält)
    # -----------------------------------------------------------------
    # id: Primärnyckel
    id = db.Column(db.Integer, primary_key=True)
    
    # namn: Vem som skrev kommentaren
    namn = db.Column(db.String(100), nullable=False)
    
    # innehall: Själva kommentaren (lång text)
    innehall = db.Column(db.Text, nullable=False)
    
    # datum: Tidsstämpling.
    # db.DateTime lagrar datum och tid.
    # default=datetime.now: VIKTIGT! Sätter automatiskt in aktuell tid
    # NÄR objektet skapas (INSERT) om inget datum specificeras manuellt.
    datum = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # -----------------------------------------------------------------
    # FRÄMMANDE NYCKEL (RELATION)
    # -----------------------------------------------------------------
    # nyhet_id: Detta fält länkar kommentaren till en specifik Nyhetsartikel.
    # db.ForeignKey('nyheter.id'): Skapar länken till Primärnyckeln 'id'
    # i tabellen som heter 'nyheter'. Denna kolumn är Främmande Nyckel (FK).
    nyhet_id = db.Column(db.Integer, db.ForeignKey('nyheter.id'), nullable=False)

    # -----------------------------------------------------------------
    # RELATIONSFÄLT (Valfritt här, men definieras oftast i Nyhet-modellen)
    # -----------------------------------------------------------------
    # Här skulle vi KUNNA definiera en "backref" till Nyhet, men det är vanligare
    # att göra detta i den andra änden av relationen (i Nyhet-modellen).

    def __repr__(self):
        """Hur objektet visas när vi printar det (för debugging)"""
        return f'<Kommentar {self.id} av {self.namn} till Nyhet {self.nyhet_id}>'

# (Här skulle funktionen för att lägga till startdata ligga, om sådan behövdes.)
# Finns nu i nyheter istället 