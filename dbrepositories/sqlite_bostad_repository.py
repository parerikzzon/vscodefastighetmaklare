"""
🏠 BOSTAD REPOSITORY - SQLite med punktnotation via SimpleNamespace

Denna version konverterar alla rader från databasen till objekt med attributåtkomst (bostad.adress).
Perfekt för nybörjare som vill ha renare kod i templates och rutter.
"""

import sqlite3
from flask import g, abort
from types import SimpleNamespace

DATABASE = 'instance/blgeestates.db'  # Lokal SQLite-databas

def get_db():
    """
    Hämtar en databasanslutning från Flask's 'g'-objekt.
    Skapar anslutningen om den inte redan finns.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Gör att vi kan använda kolumnnamn
    return g.db

def row_to_obj(row):
    """
    Konverterar en sqlite3.Row till ett objekt med punktnotation.
    """
    return SimpleNamespace(**dict(row)) if row else None

def rows_to_objs(rows):
    """
    Konverterar en lista med sqlite3.Row till objekt med punktnotation.
    Så att man kan använda dot operatorn . för attributåtkomst  (bostad.adress).
    """
    return [row_to_obj(r) for r in rows]

class BostadRepository:
    """
    Repository-klass för Bostad.
    Hanterar all databaslogik via rå SQL och returnerar objekt med attributåtkomst.
    """

    def hamta_alla(self):
        db = get_db()
        rows = db.execute("SELECT * FROM bostader").fetchall()
        return rows_to_objs(rows)

    def hamta_en(self, bostad_id):
        db = get_db()
        row = db.execute("SELECT * FROM bostader WHERE id = ?", (bostad_id,)).fetchone()
        return row_to_obj(row)

    def hamta_eller_404(self, bostad_id):
        bostad = self.hamta_en(bostad_id)
        if bostad is None:
            abort(404)
        return bostad

    def skapa_ny(self, data):
        db = get_db()
        cursor = db.execute("""
            INSERT INTO bostader (adress, stad, pris, rum, yta, beskrivning)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['adress'],
            data['stad'],
            data['pris'],
            data['rum'],
            data['yta'],
            data.get('beskrivning', '')
        ))
        db.commit()
        return self.hamta_en(cursor.lastrowid)

    def uppdatera(self, bostad_id, data):
        db = get_db()
        db.execute("""
            UPDATE bostader
            SET adress = ?, stad = ?, pris = ?, rum = ?, yta = ?, beskrivning = ?
            WHERE id = ?
        """, (
            data['adress'],
            data['stad'],
            data['pris'],
            data['rum'],
            data['yta'],
            data.get('beskrivning', ''),
            bostad_id
        ))
        db.commit()
        return self.hamta_en(bostad_id)

    def radera(self, bostad_id):
        db = get_db()
        cursor = db.execute("DELETE FROM bostader WHERE id = ?", (bostad_id,))
        db.commit()
        return cursor.rowcount > 0

    def sok_efter_stad(self, stad):
        db = get_db()
        rows = db.execute("SELECT * FROM bostader WHERE stad = ?", (stad,)).fetchall()
        return rows_to_objs(rows)

# Skapa en instans som kan importeras
bostad_repo = BostadRepository()
