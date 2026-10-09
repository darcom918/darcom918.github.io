"""Where the "Apeluri deschise" page reads its open calls from (see GHID-APELURI.md).

CSV_URL   Google Sheet → Fișier → Partajare → Publică pe web → foaia „Apeluri” → Valori separate prin virgulă (.csv)
FORM_URL  the Google Form used when a row has no "Link formular" of its own
Leave a value empty ('') and the page shows "Momentan nu avem apeluri deschise".
"""
CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTjw6oS-xFtt1A9YtbaLrJXDEQ-j0Mg47T3pcz1_pZ-4tmr9cZHZqV4quH0YQZkYGvLRZVOS6RuWNhQ/pub?output=csv'
FORM_URL = ''
