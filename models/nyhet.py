# models/nyhet.py
"""
NYHET-MODELL - Beskriver hur en nyhet ser ut i databasen.
"""
from database import db
from datetime import datetime,timedelta
from models.kommentar import Kommentar

class Nyhet(db.Model):
    """
    Nyhet-modellen representerar EN nyhetsartikel i databasen.
    """
    __tablename__ = 'nyheter'

    # Definiera kolumner (fält) i tabellen
    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(200), nullable=False)
    innehall = db.Column(db.Text, nullable=False)
    datum = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # Valfritt: Koppling till Mäklare (vem som publicerade nyheten)
    # foreign key till maklare.id
    maklare_id = db.Column(db.Integer, db.ForeignKey('maklare.id'))
    
    # Relationsfält (ger åtkomst till relaterade objekt)
    # Tillåter oss att hämta Nyhet.maklare eller Nyhet.kommentarer
    maklare = db.relationship('Maklare', backref='nyheter')
    kommentarer = db.relationship('Kommentar', backref='nyhet')


    def __repr__(self):
        """Hur objektet visas när vi printar det (för debugging)"""
        return f'<Nyhet {self.id}: {self.titel}>'

# (Startdata och funktion för att skapa startnyheter kan läggas till här)
# ============================================================
# STARTDATA FÖR NYHETER
# ============================================================

# Lägg till 3 nyheter: 1 från maklar_id 1  och 2 för maklare_id 2.
STARTDATA_NYHETER = [
    {
        'titel': 'Marknaden i Dalarna: En het höst',
        'innehall': 'Vi ser en stark efterfrågan på fritidshus. Priserna har ökat med 5% under Q3.',
        'maklare_id': 1, # Anna Ståhl
        'datum': datetime.now() - timedelta(days=5) # Äldre
    },
    {
        'titel': 'Tips: Förbered din bostad inför visning',
        'innehall': 'Bosse delar med sig av sina bästa tips för homestyling inför försäljning. Ljus och ordning är A och O!',
        'maklare_id': 2, # Bosse Andersson
        'datum': datetime.now() - timedelta(days=2)
    },
    {
        'titel': 'Nytt lagförslag om energideklarationer',
        'innehall': 'Riksdagen diskuterar nya regler som kan påverka försäljningsprocessen. Håll utkik för uppdateringar.',
        'maklare_id': 2, # Bosse Andersson
        'datum': datetime.now()
    }
]

# ============================================================
# STARTDATA FÖR KOMMENTARER
# ============================================================

# Kommentarer till Nyhet 1 och Nyhet 2
STARTDATA_KOMMENTARER = [
    # Kommentarer till Nyhet 1 (ID 1)
    {'nyhet_id': 1, 'namn': 'Kalle Anka', 'innehall': 'Intressant läsning! Vad tror ni om prisläget i Borlänge?', 'datum': datetime.utcnow() - timedelta(days=4)},
    {'nyhet_id': 1, 'namn': 'Stina Persson', 'innehall': 'Tack för tipsen, Anna!', 'datum': datetime.utcnow() - timedelta(days=3)},
    
    # Kommentar till Nyhet 2 (ID 2)
    {'nyhet_id': 2, 'namn': 'Hemmastylisten', 'innehall': 'Håller med Bosse, en ren entré är nyckeln.', 'datum': datetime.utcnow() - timedelta(days=1)}
]


def skapa_start_nyheter_och_kommentarer():
    """
    Lägger till startdata för nyheter och kommentarer i databasen OM tabellen är tom.
    """
     

    # 2. Kolla om tabellen redan har data
    antal_nyheter = Nyhet.query.count()

    if antal_nyheter == 0:
        print("📰 Lägger till startdata för nyheter och kommentarer...")
        
        nya_objekt = []

        # --- A. Skapa Nyheter ---
        for data in STARTDATA_NYHETER:
            nya_objekt.append(Nyhet(
                titel=data['titel'],
                innehall=data['innehall'],
                maklare_id=data['maklare_id'],
                datum=data['datum']
            ))
        
        # Lägg till nyheterna och committa FÖRST
        # Detta behövs för att Nyhet-objekten ska få sina ID (1, 2, 3...)
        db.session.add_all(nya_objekt)
        db.session.commit() 
        
        # --- B. Skapa Kommentarer ---
        # Vi kan nu lägga till kommentarer eftersom Nyhet-ID:na finns
        for data in STARTDATA_KOMMENTARER:
            nya_objekt.append(Kommentar(
                nyhet_id=data['nyhet_id'],
                namn=data['namn'],
                innehall=data['innehall'],
                datum=data['datum']
            ))

        # Lägg till kommentarer
        db.session.add_all(nya_objekt)
        db.session.commit()
        print("✅ Nyheter och kommentarer har lagts till.")