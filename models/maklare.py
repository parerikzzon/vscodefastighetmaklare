# models/maklare.py
"""
MÄKLARE-MODELL - Beskriver hur en mäklare ser ut i databasen.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera strukturen på mäklare-tabellen (kolumner, datatyper)
2. Tillhandahålla startdata för mäklare

Denna fil har INGEN affärslogik eller CRUD-operationer!
Det sköts av repository-lagret.
"""
from database import db


class Maklare(db.Model):
    """
    Mäklare-modellen representerar EN mäklare i databasen.

    Varje rad i tabellen 'maklare' blir ett Maklare-objekt.
    """
    # Tala om vilket tabellnamn vi vill ha i databasen
    __tablename__ = 'maklare'

    # Definiera kolumner (fält) i tabellen
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    epost = db.Column(db.String(120), unique=True, nullable=False)
    telefon = db.Column(db.String(20))
    titel = db.Column(db.String(100))
    beskrivning = db.Column(db.Text)

    def __repr__(self):
        """Hur objektet visas när vi printar det (för debugging)"""
        return f'<Maklare {self.namn}>'


# ============================================================
# STARTDATA
# ============================================================

STARTDATA_MAKLARE = [
    {
        'namn': 'Anna Ståhl',
        'epost': 'anna.stahl@maklare.se',
        'telefon': '070-123 45 67',
        'titel': 'Fastighetsmäklare',
        'beskrivning': 'Specialist på villor och nyproduktion i Dalarna.'
    },
    {
        'namn': 'Bosse Andersson',
        'epost': 'bosse.a@maklare.se',
        'telefon': '073-987 65 43',
        'titel': 'Mäklarassistent',
        'beskrivning': 'Är din kontaktperson för visningar och prospekt.'
    },
]


def skapa_start_maklare():
    """
    Lägger till startdata i databasen OM tabellen är tom.

    SINGLE RESPONSIBILITY: Denna funktion har ENDAST ansvar för
    att lägga till startdata - inget annat!
    """
    # Kolla om tabellen redan har data
    antal_maklare = Maklare.query.count()

    if antal_maklare == 0:
        print("📦 Lägger till startdata för mäklare...")

        # Loopa genom startdata och skapa objekt
        for data in STARTDATA_MAKLARE:
            ny_maklare = Maklare(
                namn=data['namn'],
                epost=data['epost'],
                telefon=data['telefon'],
                titel=data['titel'],
                beskrivning=data['beskrivning']
            )
            db.session.add(ny_maklare)

        # Spara alla till databasen
        db.session.commit()
        print(f"✓ Lade till {len(STARTDATA_MAKLARE)} mäklare")
    else:
        print(f"✓ Tabellen 'maklare' har redan {antal_maklare} rader")