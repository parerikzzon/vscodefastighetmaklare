# models/kontor.py
"""
KONTOR-MODELL - Beskriver hur ett kontor ser ut i databasen.
"""
from database import db


class Kontor(db.Model):
    """
    Kontor-modellen representerar ETT fastighetskontor i databasen.
    """
    __tablename__ = 'kontor'

    # Definiera kolumner (fält) i tabellen
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    adress = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.Float, nullable=False)    # Latitud
    lon = db.Column(db.Float, nullable=False)    # Longitud
    kontorschef = db.Column(db.String(100))
    bild_url = db.Column(db.String(255))         # URL till kontorsbild

    def __repr__(self):
        """Hur objektet visas när vi printar det (för debugging)"""
        return f'<Kontor {self.namn}>'

    def to_dict(self):
        """Returnerar kontoret som en dictionary, användbart för JSON/API"""
        return {
            'id': self.id,
            'namn': self.namn,
            'adress': self.adress,
            'lat': self.lat,
            'lon': self.lon,
            'kontorschef': self.kontorschef,
            'bild_url': self.bild_url
        }


# ============================================================
# STARTDATA
# ============================================================

STARTDATA_KONTOR = [
    {
        'namn': 'Kontor Falun',
        'adress': 'Stora Gatan 1, 791 71 Falun',
        'lat': 60.6050,  # Ungefärliga koordinater för Falun centrum
        'lon': 15.6176,
        'kontorschef': 'Lena Persson',
        'bild_url': 'https://images.pexels.com/photos/534219/pexels-photo-534219.jpeg'
    },
    {
        'namn': 'Kontor Borlänge',
        'adress': 'Hagvägen 10, 784 31 Borlänge',
        'lat': 60.4851,  # Ungefärliga koordinater för Borlänge centrum
        'lon': 15.4214,
        'kontorschef': 'Oskar Eriksson',
        'bild_url': 'https://images.pexels.com/photos/137618/pexels-photo-137618.jpeg'
    },
    {
        'namn': 'Kontor Ludvika',
        'adress': 'Vasagatan 5, 771 30 Ludvika',
        'lat': 60.1469,  # Ungefärliga koordinater för Ludvika centrum
        'lon': 15.1843,
        'kontorschef': 'Karin Jonsson',
        'bild_url': 'https://images.pexels.com/photos/269077/pexels-photo-269077.jpeg'
    },
]


def skapa_start_kontor():
    """
    Lägger till startdata i databasen OM tabellen är tom.
    """
    # Kolla om tabellen redan har data
    antal_kontor = Kontor.query.count()

    if antal_kontor == 0:
        print("📦 Lägger till startdata för kontor...")

        # Loopa genom startdata och skapa objekt
        for data in STARTDATA_KONTOR:
            nytt_kontor = Kontor(
                namn=data['namn'],
                adress=data['adress'],
                lat=data['lat'],
                lon=data['lon'],
                kontorschef=data['kontorschef'],
                bild_url=data['bild_url']
            )
            db.session.add(nytt_kontor)

        # Spara alla till databasen
        db.session.commit()
        print(f"✓ Lade till {len(STARTDATA_KONTOR)} kontor")
    else:
        print(f"✓ Tabellen 'kontor' har redan {antal_kontor} rader")