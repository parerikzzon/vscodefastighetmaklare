# VSCode Fastighetmäklare - Undervisningskod (GIK376)

Detta repository innehåller undervisningskod för kursen Applikationsutveckling för webben (GIK376). Syftet är att ge en praktisk förståelse för hur olika delar av en webbapplikation samverkar enligt MVC-arkitekturen (Model–View–Controller) i Flask.

Innan du dyker in i koden, ta dig tid att förstå projektstrukturen. Här är en översikt i punktform:

- Övergripande mål
  - Ge praktisk förståelse för MVC i Flask.
  - Visa hur modeller, vyer och kontroller samverkar.

- Projektstruktur (kort)
  - model / dbrepositories (Modeller)
    - Hanterar datalogik (CRUD).
    - Sätter upp tabeller i databasen.
  - Blueprints med routes (Kontrollers) och Templates(Vyer)
    - Routes definierar applikationens flöde och logik mellan vy-> kontroller-> modell.
    - De kopplar ihop vyer (templates) så att de kan få data från modeller.
      - templates (Vyer)
        - Applikationens GUI.
        - Visar innehåll och hur användaren interagerar (knappar, länkar etc.).
          - Knappen, länken har url:er mappning till kontrollern

- Tips för att komma igång
  - Läs först mappstrukturen.
  - Titta på modellerna/repositores för att förstå databasens uppbyggnad och crud funktionalitet.
  - Öppna blueprints för att förstå hur routes(Kontroller) är uppbyggda för att hämta data från repositories(Modell) för att sen skicka datat till tempaltes(Vy)
  - Öppna Templates för att se hur data presenteras i vyerna och hur vyer anropa via url:er kontrollerna/routes

- Rekommendation
  - Följ flödet: vy(templates) -> kontroller(routes) -> modell(repositores) för att förstå hur en request bearbetas från det användaren trycker på en länk/knapp till den ser resulatet av den tryckningen.
