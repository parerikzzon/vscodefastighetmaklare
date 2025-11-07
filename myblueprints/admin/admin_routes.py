# blueprints/admin/admin_routes.py
"""
🛠️ ADMIN ROUTES - Hanterar URL:er för att ADMINISTRERA bostäder (CRUD).

SYFTE: Fungera som "Controller"-lagret. Tar emot HTTP-förfrågningar, 
hanterar användarinteraktioner (formulär) och anropar databasoperationer via Repository.

DESIGNPRINCIP: Denna fil gör INGA direkta databasoperationer!
Den använder ENBART den importerade instansen 'bostad_repo' för all databasåtkomst.

CRUD = Create, Read, Update, Delete
"""
# Importera standard Flask-funktioner
from flask import render_template, request, redirect, url_for, abort, flash
# Importera blueprint-instansen och det nödvändiga repositoryt från __init__.py
from . import admin_bp, bostad_repo
# Importera autentiseringsfunktioner från Flask-Login
from flask_login import login_required, current_user 


# ============================================================
# 1. LISTA (READ) - Visa alla bostäder för admin
# ============================================================

# @admin_bp.route('/') skapar den fullständiga URL:en /admin/ (om prefixet är /admin)
@admin_bp.route('/')
# login_required säkerställer att ENDAST inloggade användare kan nå denna vy
@login_required 
def admin_lista_bostader():
    """
    Visar ALLA bostäder i admin-läge, som en tabell med redigerings- och raderingslänkar.

    URL: /admin/
    """
    # 1. Anropa Repository (Service Layer) för att hämta data
    alla_bostader = bostad_repo.hamta_alla()

    # 2. Returnera HTML (View Layer)
    return render_template(
        'admin_bostader_lista.html',
        bostader=alla_bostader,
        titel='Administration av Bostäder'
    )


# ============================================================
# 2. FORMULÄR (CREATE & UPDATE) - Lägg till eller redigera
# ============================================================

# Två URL:er hanteras av samma funktion: /admin/add och /admin/edit/<id>
@admin_bp.route('/add', methods=['GET', 'POST'])
@admin_bp.route('/edit/<int:bostad_id>', methods=['GET', 'POST'])
@login_required 
def admin_form(bostad_id=None):
    # Kontrollera om användaren har rollen 'admin'
    if current_user.role != 'admin':
        flash('Du har inte behörighet att lägga till eller uppdatera bostäder.', 'warning')
        return redirect(url_for('auth_bp.login'))  
    """
    Hantera logiken för att antingen visa formuläret (GET) eller spara data (POST).
    """
    bostad = None
    titel = "Lägg till ny bostad"

    # --------------------------------------------------------
    # A. Redigeringsläge? (bostad_id är angivet)
    # --------------------------------------------------------
    if bostad_id:
        # Hämta befintlig bostad via Repository
        bostad = bostad_repo.hamta_en(bostad_id)

        if bostad is None:
            # Stoppar körningen och visar 404-sida om ID:t är ogiltigt
            abort(404) 

        titel = f"Redigera: {bostad.adress}"

    # --------------------------------------------------------
    # B. Formulär inskickat (POST-metod)
    # --------------------------------------------------------
    if request.method == 'POST':
        # 1. Validera och rensa data via Hjälpfunktion
        form_data = validera_formular(request.form)

        if form_data is None:
            # 2. Validering misslyckades: Visa felmeddelande
            flash('Ogiltiga formulärdata. Kontrollera dina värden.', 'warning')
        else:
            # 3. Validering lyckades: Anropa Repository för att spara
            if bostad_id:
                # UPPDATERA
                bostad_repo.uppdatera(bostad_id, form_data)
                flash(f'Bostad "{form_data["adress"]}" har uppdaterats!', 'success')
            else:
                # SKAPA NY
                ny_bostad = bostad_repo.skapa_ny(form_data)
                flash(f'Ny bostad "{ny_bostad.adress}" har lagts till!', 'success')

            # 4. PRG-mönstret (Post/Redirect/Get): Omdirigera för att förhindra dubbel-submission
            return redirect(url_for('.admin_lista_bostader'))

    # --------------------------------------------------------
    # C. Visa formuläret (GET-metod)
    # --------------------------------------------------------
    return render_template(
        'admin_bostader_form.html',
        bostad=bostad, # Skickar antingen det befintliga objektet eller None
        titel=titel
    )


# ============================================================
# 3. RADERA (DELETE) - Ta bort en bostad
# ============================================================

@admin_bp.route('/delete/<int:bostad_id>', methods=['POST'])
@login_required 
def admin_delete(bostad_id):
    # Kontrollera om användaren har rollen 'admin'
    if current_user.role != 'admin':
        flash('Du har inte behörighet att ta bort bostäder.', 'warning')
        return redirect(url_for('auth_bp.login'))  

    """
    Raderar en bostad. Använder POST-metod för säkerhet mot CSRF/slumpmässiga klick.
    """
    
    # 1. Hämta objektet FÖRST (för att få dess namn till meddelandet)
    bostad = bostad_repo.hamta_en(bostad_id)

    if bostad:
        adress = bostad.adress
        # 2. Anropa Repository för radering
        bostad_repo.radera(bostad_id)
        flash(f'Bostad "{adress}" har tagits bort!', 'success')
    else:
        flash('Bostaden kunde inte hittas.', 'warning')

    # 3. Gå tillbaka till listan
    return redirect(url_for('.admin_lista_bostader'))


# ============================================================
# HJÄLPFUNKTIONER (Validering)
# ============================================================

def validera_formular(form_data):
    """
    Validerar, konverterar datatyper och rensar formulärdata.

    SINGLE RESPONSIBILITY: Detta är en isolerad funktion som hanterar
    all komplexitet kring formulärdata och felhantering.

    Returns:
        dict: Validerad data (med korrekta Python-typer), eller None om valideringen misslyckades.
    """
    try:
        # Hämta, rensa (strip) och konvertera till korrekta typer
        data = {
            'adress': form_data['adress'].strip(),
            'stad': form_data['stad'].strip(),
            'pris': form_data['pris'].strip(),
            # Försök konvertera till heltal: detta utlöser ValueError om det misslyckas
            'rum': int(form_data['rum']), 
            'yta': int(form_data['yta']),
            'beskrivning': form_data['beskrivning'].strip()
        }

        # Affärsvalidering (t.ex. säkerställa att värden är rimliga)
        if not data['adress'] or not data['stad']:
            return None # Saknar adress/stad
        
        if data['rum'] < 1 or data['yta'] < 1:
            return None # Rum eller yta måste vara minst 1

        return data

    except (KeyError, ValueError):
        # Fångar fel om ett fält saknas (KeyError) eller om konvertering till int misslyckas (ValueError)
        return None