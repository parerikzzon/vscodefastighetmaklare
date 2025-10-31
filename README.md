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
  - Blueprints med routes (Kontroller)
    - Definierar applikationens flöde och logik.
    - Kopplar ihop vyer (templates) med modeller.
  - templates (Vyer)
    - Applikationens GUI.
    - Visar innehåll och hur användaren interagerar (knappar, länkar etc.).

- Tips för att komma igång
  - Läs först mappstrukturen och öppna huvudfilerna för app-setup och routes.
  - Titta på modellerna för att förstå databasens uppbyggnad.
  - Öppna templates för att se hur data presenteras i vyerna.

- Rekommendation
  - Följ flödet: vy -> kontroller -> modell för att förstå hur en request bearbetas.
