# flask_app.py
"""
HUVUDFIL FÖR FLASK-APPLIKATIONEN (Applikationens Nav)

SYFTE: Att initiera och konfigurera alla delar (databaser, inloggning, moduler)
som applikationen behöver för att fungera.

DESIGNPRINCIP: Denna fil följer "Application Factory Pattern" (skapa_app), 
vilket är bäst praxis för att skapa en skalbar och testbar Flask-applikation.

SINGLE RESPONSIBILITY: 
1. Skapa Flask-applikationen.
2. Konfigurera applikationen (inställningar).
3. Initiera databas och inloggning.
4. Registrera alla blueprints.
5. Definiera routes för huvudnivån (t.ex. startsidan).
6. Starta applikationen.
"""
from flask import Flask, render_template
# Importera init_db-funktionen som sätter upp SQLAlchemy (databasen)
from database import init_db 

# Importera Flask-Login för att hantera användarsessioner
from flask_login import LoginManager
# Importera User-modellen som Flask-Login behöver för att hämta användardata
from models.user import User 


def skapa_app():
    """
    Application Factory: Skapar och konfigurerar Flask-applikationen.
    
    Returns:
        Flask: Den färdiga Flask-applikationen-instansen.
    """
    # 1. Skapa Flask-appen
    app = Flask(__name__)

    # ============================================================
    # 2. KONFIGURATION (Applikationsinställningar)
    # ============================================================
    # SECRET_KEY: Nödvändig för att skydda session cookies (inloggning). BYT DENNA I PRODUKTION!
    app.config['SECRET_KEY'] = 'din_superhemliga_nyckel' 
    # SQLALCHEMY_DATABASE_URI: Anger vilken databas vi ska använda (en SQLite-fil).
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blgeestates.db'
    # SQLALCHEMY_TRACK_MODIFICATIONS: Stängs av för att spara resurser (bäst praxis).
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ============================================================
    # 3. INITIERA DATABASEN
    # ============================================================
    # init_db: Anropar funktionen som kopplar SQLAlchemy till appen och skapar tabellerna.
    init_db(app) 

    # ============================================================
    # 4. REGISTRERA BLUEPRINTS
    # ============================================================
    # Anropar hjälpfunktionen som kopplar alla moduler till appen.
    registrera_blueprints(app)

    # ============================================================
    # 5. REGISTRERA ROUTES (URL:er för hela appen)
    # ============================================================
    # Anropar hjälpfunktionen som definierar startsidor och huvud-rutter.
    create_routes(app)

    # ============================================================
    # 6. INITIERA FLASK-LOGIN (Autentiseringshantering)
    # ============================================================
    
    # Skapar en LoginManager-instans
    login_manager = LoginManager()
    # Kopplar LoginManager till din Flask-app
    login_manager.init_app(app)
    # login_view: Säger till Flask-Login vart användaren ska omdirigeras om de försöker 
    # nå en @login_required-rutt utan att vara inloggade.
    login_manager.login_view = 'auth_bp.login' 

    @login_manager.user_loader
    def load_user(user_id):
        """
        Denna funktion är KRITISK för Flask-Login. 
        Den laddar en användare från databasen baserat på ID:t som lagras i sessionen.
        """
        # User.query.get() är en SQLAlchemy-metod som hämtar en rad efter Primärnyckeln (ID)
        return User.query.get(int(user_id)) 

    return app


def registrera_blueprints(app):
    """
    Registrerar alla blueprints i applikationen.
    Kopplar ihop de separata modulerna (Blueprints) med huvudapplikationen.

    Args:
        app (Flask): Flask-applikationen
    """
    # Importera blueprint-objekten från deras respektive moduler
    from myblueprints.bostader import bostader_bp
    from myblueprints.admin import admin_bp
    from myblueprints.maklare import maklare_bp
    from myblueprints.auth import auth_bp
    from myblueprints.nyheter import nyheter_bp

    # app.register_blueprint: Den faktiska kopplingen sker här.
    # url_prefix: Anger det prefix som alla routes i blueprintet kommer att ha.
    app.register_blueprint(bostader_bp, url_prefix='/bostader')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(maklare_bp, url_prefix='/maklare')
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(nyheter_bp, url_prefix='/nyheter') 


def create_routes(app):
    """
    Skapar routes som hör till hela appen (globala routes).

    Args:
        app (Flask): Flask-applikationen
    """

    @app.route("/hello")
    def hello_world():
        """En enkel test-rutt."""
        return "<p>Hej Världen! Min första Flask-app!</p>"

    @app.route('/')
    def index():
        """Startsidan."""
        # render_template: Letar efter home.html i mappen 'templates' i roten
        return render_template('home.html', titel='Välkommen')

# ============================================================
# STARTPUNKT
# ============================================================
# Anropar Application Factory för att bygga hela appen
app = skapa_app()
# kommentera bort hela if när man lägger upp på pythonanywhere
if __name__ == '__main__':
    # Kör applikationen!
    # debug=True: Aktiverar debug-läget, vilket gör att koden laddas om vid ändring i vscode
    #denna komer bort när man lägger upp till pythonanywhere
    app.run(debug=True)