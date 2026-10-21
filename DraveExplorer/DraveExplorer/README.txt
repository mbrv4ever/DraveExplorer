============================================================
 DraveExplorer  v0.1
 Een snelle, toegankelijke file explorer
 Lokaal - Offline - Donationware
============================================================

WAT IS HET
----------
DraveExplorer is een bestandsverkenner die overzichtelijk al je
stations toont (harde schijven, USB-sticks en netwerkschijven),
met een duidelijke balk voor de gebruikte en vrije opslag.
Je bladert in tabbladen, opent bestanden met een dubbelklik en
beheert je bestanden zoals je gewend bent.


STARTEN
-------
1. Pak de map uit op een plek waar je schrijfrechten hebt.
2. Dubbelklik op  run.bat
   De eerste keer wordt eenmalig een kleine omgeving opgezet
   (Python-pakketten). Dit kan een halve minuut duren.
3. Daarna start het programma. Volgende keren start het direct.

Werkt het niet meteen? Start dan  start-debug.bat
Dan blijft het venster open en zie je eventuele meldingen.
Fouten worden ook bewaard in  app-fout.txt


WAT JE KUNT DOEN
----------------
Navigeren
  - Zijbalk links: snelkoppelingen en al je stations met
    een opslagbalk. Klik om te openen.
  - Knoppen Terug / Vooruit / Omhoog / Vernieuwen.
  - Broodkruimel-balk: klik op een padonderdeel om er heen te springen.
  - Mappenboom onderin de zijbalk: klap mappen uit en klik om te openen.
  - Favorieten: zet een map vast met Ctrl+D of via de rechtermuisknop;
    ze staan bovenin de zijbalk (rechtsklik om te verwijderen).
  - Adresbalk: typ een pad en druk op Enter.
  - Dubbelklik op een map opent die map.
  - Dubbelklik op een bestand opent het met het juiste programma.
  - Middelste muisknop op een map opent die in een nieuwe tab.
  - Rechtermuisknop geeft "Openen in nieuwe tab".
  - Geopende tabbladen komen terug na het opnieuw starten.

Zoeken
  - Typ in het filterveld om de huidige map te filteren.
  - Klik op het vergrootglas om ook submappen te doorzoeken.
  - Met de keuzelijst naast het filterveld toon je alleen een bepaald
    type (afbeeldingen, documenten, muziek, video, archieven). Mappen
    blijven zichtbaar.
  - Voorbeeldvenster (Ctrl+P of de voorbeeldknop): toont rechts een
    voorbeeld van het geselecteerde bestand - afbeeldingen, tekst, PDF,
    en een speler voor video en muziek. Zip/exe: geen voorbeeld.

Weergave
  - Wissel met de knop in de werkbalk (of Ctrl+1 / Ctrl+2) tussen lijst
    en grote iconen. In de iconenweergave zie je miniaturen van je foto's.

Bestanden beheren
  - Kopieren  Ctrl+C     Knippen  Ctrl+X     Plakken  Ctrl+V
  - Hernoemen F2          Verwijderen Delete (naar prullenbak)
  - Permanent verwijderen Shift+Delete
  - Nieuwe map Ctrl+Shift+N
  - Eigenschappen Alt+Enter
  - Alles selecteren Ctrl+A

Toegankelijkheid
  - Tekst groter / kleiner: Ctrl++  en  Ctrl+-
  - Beeld > Instellingen: taal (Nederlands / Engels / automatisch),
    lettergrootte, icoongrootte en extra hoog contrast.
  - Verborgen bestanden tonen: Ctrl+H


EIGEN LOGO (optioneel)
----------------------
Wil je je eigen logo gebruiken? Zet een bestand "logo.png"
in deze map en draai eenmalig  maak_icoon.py  (of bouw-exe.bat).
Anders gebruikt het programma een standaard map-icoon.


EEN LOSSE .EXE MAKEN (optioneel)
--------------------------------
Dubbelklik op  bouw-exe.bat
De .exe komt dan in de map "dist" te staan.


PROBLEMEN OPLOSSEN
------------------
- Werkt iets niet meer? Voer  herstel.bat  uit. Dat verwijdert
  de omgeving en installeert alles opnieuw.
- Geen Python? Installeer Python 3.10 t/m 3.13 via
  https://www.python.org/downloads/  en vink
  "Add Python to PATH" aan.


DONATIE
-------
DraveExplorer is gratis (donationware). Vind je het nuttig?
Steun de ontwikkeling via de knop met het hartje rechtsonder,
of via  https://paypal.me/roger076

Contact en feedback:  service@dravenlock.nl

Veel plezier!
