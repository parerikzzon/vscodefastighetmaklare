# blueprints/auth/auth_routes.py
"""
🔑 AUTH ROUTES - Hanterar URL:er för inloggning och utloggning.

SINGLE RESPONSIBILITY: Fungerar som "Controller"-lagret för autentisering.
- Tar emot inloggningsformulär.
- Använder user_repo för att slå upp användare i databasen.
- Använder Flask-Login för att hantera sessioner (login_user, logout_user).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
# login_user, logout_user, login_required är Flask-Logins centrala funktioner
from flask_login import login_user, logout_user, login_required 

# Importera blueprint-objektet och user_repo från __init__.py
from . import auth_bp
from . import user_repo


# ============================================================
# 1. INLOGGNING (LOGIN)
# ============================================================

# url_prefix /auth används ofta för auth-blueprints (i detta fall: /auth/login)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Visar inloggningsformuläret (GET) eller behandlar inloggningsförsöket (POST).
    """
    
    if request.method == 'POST':
        # Hämta data från formuläret
        username = request.form['username']
        password = request.form['password']

        # 1. AUTENTISERING: Hämta användaren via unikt användarnamn
        user = user_repo.hamta_user_username(username=username)
        
        # Jämför: Kontrollera om användaren finns OCH om lösenordet matchar
        # OBS! I en riktig app ska lösenordsjämförelsen ske mot det HASHADE lösenordet.
        if user and user.password == password: 
            
            # Autentisering lyckades! 
            # Flask-Login skapar en session (cookie) för användaren.
            login_user(user)
            
            # 2. AUKTORISATION: Kontrollera användarroll för omdirigering
            if user.role == 'admin':
                flash('Administratörsinloggning lyckades!', 'success')
                # Omdirigera admin till admin-panelen
                # 'admin_bp.admin_lista_bostader' är blueprintnamn.funktionsnamn
                return redirect(url_for('admin_bp.admin_lista_bostader'))
            else:
                # Omdirigera vanliga användare till startsidan
                
                # Lägg till varning om otillräcklig behörighet
                flash('Inloggning lyckades! Men din användarroll (' + user.role + ') har inte behörighet att administrera sidan. Så logga ut och logga in som admin', 'warning')
                # url_for('index') förutsätter att du har en rutt med namnet 'index' (vanligtvis startsidan)
                return redirect(url_for('index')) 
        else:
            # Autentisering misslyckades (användare hittades inte eller lösenord fel)
            flash('Felaktigt användarnamn eller lösenord.', 'error')

    # Om metoden är GET (eller om POST misslyckades), visa formuläret
    return render_template('login.html')

# ============================================================
# 2. UTLOGGNING (LOGOUT)
# ============================================================

@auth_bp.route('/logout')
@login_required # Man måste vara inloggad för att kunna logga ut
def logout():
    """
    Loggar ut den aktuella användaren och rensar sessionen.
    """
    # Flask-Login raderar användarsessionen
    logout_user() 
    flash('Du har loggats ut.', 'info')
    # Omdirigera tillbaka till inloggningssidan
    return redirect(url_for('auth_bp.login'))