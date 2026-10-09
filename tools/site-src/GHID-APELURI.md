# Ghid: apelurile deschise pe site

Pagina **Apeluri deschise** (`html/apeluri-deschise.html`) își ia apelurile dintr-un **Google Sheet**.
Președintele scrie apelurile în tabel, iar site-ul se actualizează singur. Nu e nevoie de cod.

---

## A. Pregătirea (o singură dată, ~15 minute)

### 1. Tabelul cu apeluri (Google Sheets)
1. Deschide [sheets.new](https://sheets.new) și numește fișierul **AIS – Apeluri deschise**.
2. **Fișier → Importă → Încarcă** fișierul `assets/data/apeluri-exemplu.csv` din site
   (alege „Înlocuiește foaia curentă”). Așa ai deja toate coloanele și 3 exemple.
3. Redenumește foaia (jos, în stânga) în **Apeluri**.
4. **Fișier → Setări → Setări regionale: România**, ca datele să fie de forma `14.10.2026`.
5. Șterge cele 3 rânduri de exemplu (lasă rândul 1, cu titlurile coloanelor, neatins).

### 2. Formularul de înscriere (Google Forms)
1. Deschide [forms.new](https://forms.new) și numește-l **Aplică la un proiect AIS**.
2. Întrebări recomandate:
   - La ce proiect aplici? (răspuns scurt)
   - Nume și prenume · Data nașterii · Oraș · E-mail · Telefon
   - De ce vrei să participi? (paragraf)
   - Ai mai participat la un proiect Erasmus+? (Da / Nu)
   - Ai nevoi speciale (alimentație, sănătate, acces)? (paragraf, opțional)
   - Bifă obligatorie: „Sunt de acord ca Asociația Inițiative Sociale să folosească datele mele doar pentru selecția participanților la acest proiect.”
3. **Răspunsuri → Link către Sheets**: răspunsurile ajung într-un tabel.
4. **Răspunsuri → ⋮ → Primește notificări prin e-mail pentru răspunsuri noi**.
5. **Trimite → 🔗 Link**: copiază linkul formularului.

### 3. Legarea de site (o singură dată)
1. În tabelul cu apeluri: **Fișier → Partajare → Publică pe web**.
2. Alege foaia **Apeluri** și formatul **Valori separate prin virgulă (.csv)** → **Publică**.
3. Trimite cele două linkuri (tabelul publicat .csv + formularul) celui care se ocupă de site.
   El le pune în `tools/site-src/apeluri_config.py` (`CSV_URL` și `FORM_URL`) și reconstruiește site-ul.

---

## B. Folosirea zilnică

### Adaugi un apel nou
Scrie un rând nou în foaia **Apeluri**:

| Coloana | Ce scrii | Exemplu |
|---|---|---|
| Activ | `DA` ca să apară pe site, `NU` ca să-l ascunzi | DA |
| Titlu | numele proiectului | Green Skills Lab |
| Tip | Schimb de tineri / Curs de formare / Seminar | Schimb de tineri |
| Țară | numele țării în română | Italia |
| Oraș | orașul | Padova |
| Început / Sfârșit | datele mobilității | 02.11.2026 / 10.11.2026 |
| Termen limită | ultima zi în care se poate aplica | 14.10.2026 |
| Locuri | câți participanți trimite AIS | 5 |
| Vârstă | vârsta cerută | 18–25 |
| Ce acoperim | ce costuri sunt acoperite | Transport până la 275 €, cazare, masă |
| Descriere | 1–3 propoziții despre proiect | … |
| Link formular | *opțional* – alt formular doar pentru acest apel | |
| Link detalii | *opțional* – infopack, postare Facebook | |
| Titlu (EN) / Descriere (EN) | *opțional* – pentru versiunea în engleză a site-ului | |

Apelul apare pe site în **aproximativ 5 minute** (cât îi ia lui Google să actualizeze tabelul publicat).

### Închizi un apel
Nu trebuie să faci nimic: **după termenul limită apelul dispare singur**.
Ca să-l scoți mai devreme, scrie `NU` în coloana **Activ**.

### Vezi cine a aplicat
Deschide tabelul cu **răspunsurile formularului** (sau e-mailurile de notificare).
Coloana „La ce proiect aplici?” arată proiectul.

---

## C. Bine de știut
- Pe site, apelurile sunt ordonate după termenul limită (cel mai apropiat primul).
  Când mai sunt 7 zile sau mai puțin, apare eticheta roșie „Mai sunt N zile”.
- Dacă nu e niciun apel deschis, pagina arată „Momentan nu avem apeluri deschise.” și linkuri spre Facebook, Instagram și TikTok.
- Ca să vezi cum arată pagina cu apeluri de test, deschide `apeluri-deschise.html#demo`.
- Nu scrie în tabel date personale: tabelul publicat poate fi văzut de oricine are linkul.
