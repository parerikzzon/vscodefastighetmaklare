"""
MAKLARE-FORMULÄR – Flask-WTF-formulär för att skapa/redigera mäklare.

SINGLE RESPONSIBILITY: Denna fil har ENDAST ansvar för:
1. Definiera ett formulär som matchar Maklare-modellen
2. Hantera validering och fälttyper

Ingen affärslogik eller databasoperationer här!
"""

# Flask-WTF är ett tillägg som gör det enkelt att skapa formulär i Flask
# Installera med: pip install flask-wtf
# För e-postvalidering behövs också: pip install email_validator

from flask_wtf import FlaskForm  # Basformulärklass från Flask-WTF
from wtforms import StringField, TextAreaField, SubmitField  # Fälttyper vi använder
from wtforms.validators import DataRequired, Email, Length  # Valideringsregler

# Vi skapar en klass som ärver från FlaskForm
class MaklareForm(FlaskForm):
    """
    Formulär för att skapa eller redigera en mäklare.
    Matchar fälten i Maklare-modellen.
    """

    # Namn-fältet: måste fyllas i och får max vara 50 tecken
    namn = StringField(
        'Namn',  # Etikett som visas i HTML
        validators=[
            DataRequired(message="Du måste ange ett namn."),  # Fältet får inte vara tomt
            Length(max=50, message="Namnet får max vara 50 tecken.")  # Maxlängd
        ]
    )

    # E-post-fältet: måste fyllas i, måste vara giltig e-post, max 120 tecken
    epost = StringField(
        'E-post',
        validators=[
            DataRequired(message="Du måste ange en e-postadress."),  # Obligatoriskt
            Email(message="Ange en giltig e-postadress."),  # Kontrollera format
            Length(max=50, message="E-postadressen får max vara 50 tecken.")  # Maxlängd
        ]
    )

    # Telefon-fältet: valfritt, men max 20 tecken
    telefon = StringField(
        'Telefon',
        validators=[
            Length(max=15, message="Telefonnumret får max vara 15 tecken.")  # Maxlängd
        ]
    )

    # Titel-fältet: valfritt, max 50 tecken
    titel = StringField(
        'Titel',
        validators=[
            Length(max=50, message="Titeln får max vara 50 tecken.")  # Maxlängd
        ]
    )

    # Beskrivning: fritextfält utan validering (valfritt)
    beskrivning = TextAreaField('Beskrivning')

    # Skicka-knapp: visas som "Lägg till mäklare"
    submit = SubmitField('Lägg till mäklare')
