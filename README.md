
Detta repository innehåller undervisningskod för kursen Applikationsutveckling för webben (GIK376). 
Syftet är att ge dig en praktisk förståelse för hur olika delar av en webbapplikation samverkar enligt MVC-arkitekturen (Model–View–Controller) i Flask.
Börja med att förstå strukturen innan du dyker in i koden, ta dig tid att förstå hur projektets olika komponenter hänger ihop:
Kolla först mapp strukturen
-model, dbrepositories(Modeller) – Hanterar data logik(crud), sätter upp tabeller i databasen.
-Blueprints med routes (Kontroller) – Definierar applikationens flöde och logik mellan vy->kontoller->modell.
--Templates (Vyer) – Vår apps GUI som visar innehåll, hur användare interagera med appen via knappar, länkar etc.
