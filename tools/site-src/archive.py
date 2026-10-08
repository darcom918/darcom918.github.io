"""Content for "Unde a început totul": projects from before the Erasmus+ accreditation.

Text was crawled from the old site (initiative-sociale.ro) and is kept word for word.
Photos come from each project's blog (assets/images/archive/<slug>/).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(HERE, 'archive')

HOSTED_RAW = json.load(open(os.path.join(DATA, 'hosted.json'), encoding='utf-8'))
SENDING = json.load(open(os.path.join(DATA, 'sending.json'), encoding='utf-8'))

COUNTRY = {
    'RO': 'România', 'PL': 'Polonia', 'TR': 'Turcia', 'ES': 'Spania', 'CY': 'Cipru', 'LT': 'Lituania',
    'HR': 'Croația', 'SK': 'Slovacia', 'PT': 'Portugalia', 'IT': 'Italia', 'NO': 'Norvegia', 'EL': 'Grecia',
    'DE': 'Germania', 'LV': 'Letonia', 'MK': 'Macedonia', 'BG': 'Bulgaria',
}
CODE_BY_NAME = {'Polonia': 'PL', 'Spania': 'ES', 'Letonia': 'LV', 'Germania': 'DE', 'Macedonia': 'MK', 'Cipru': 'CY',
                'Turcia': 'TR', 'Grecia': 'EL', 'Italia': 'IT'}

# Hosted projects, in chronological order. Page file: arhiva-<slug>.html
HOSTED = [
    dict(slug='antreprenoriat-social-2013', raw='h9', year=2013, program='Tineret în Acțiune',
         title='Incurajarea tinerilor pentru participarea la dezvoltarea initiativelor in antreprenoriatul social',
         short='Antreprenoriat social', place='Paulesti, Prahova', countries=[],
         links=[('Albumul de poze', 'https://www.facebook.com/media/set/?set=a.504032919673498.1073741834.478466965563427&type=3'),
                ('Feedback video', 'https://www.youtube.com/watch?v=Lgz5Wz3nEZs')],
         photos_link='https://www.facebook.com/media/set/?set=a.504032919673498.1073741834.478466965563427&type=3'),
    dict(slug='paper-handicraft-business', raw='h10', year=2013, program='Tineret în Acțiune',
         title='Paper Handicraft Bussiness – Winter Edition', short='Paper Handicraft Bussiness', place='Horezu, Valcea',
         countries=[],
         links=[('Blogul proiectului', 'http://paperhandicraftsbusiness.blogspot.com/'),
                ('Brosura', 'http://paperhandicraftsbusiness.blogspot.com/2014/02/brochure.html')],
         photos_link='https://www.facebook.com/media/set/?set=a.556355621107894.1073741844.478466965563427&type=3'),
    dict(slug='many-ideas-one-word', raw='h1', year=2014, program='Erasmus+',
         title='Many ideas, one word: entrepreneurship!', short='Many ideas, one word', place='Eforie Nord, Constanta',
         countries=['IT', 'TR', 'ES', 'LT', 'RO'],
         links=[('Blogul proiectului', 'http://ourmanyideas.blogspot.com/'),
                ('Feedback video', 'https://www.youtube.com/watch?v=zsD2cLxP7NE')],
         photos_link='https://www.facebook.com/media/set/?set=a.723307264412728.1073741860.478466965563427&type=3'),
    dict(slug='young-enterprises', raw='h2', year=2014, program='Erasmus+',
         title='Young Enterprises', short='Young Enterprises', place='Eforie Nord, Constanta', countries=[],
         links=[('Filmuletele de prezentare', 'https://www.youtube.com/watch?v=ogqUOuCWbr0&list=PLLKhi7mhuJJ66ySBT14IiCTclrtrawRJb&index=3')],
         photos_link='http://young-enterprises.blogspot.com/'),
    dict(slug='entrepreneurial-ideas', raw='h3', year=2015, program='Erasmus+',
         title='Entrepreneurial Ideas', short='Entrepreneurial Ideas', place='Eforie Nord, Constanta',
         countries=['EL', 'IT', 'PL', 'ES', 'TR', 'RO'], links=[],
         photos_link='http://entrepreneurial-ideas-project.blogspot.com/'),
    dict(slug='start-up-machine', raw='h4', year=2016, program='Erasmus+',
         title='Start-up Machine', short='Start-up Machine', place='Eforie Nord, Constanta',
         countries=['BG', 'IT', 'PL', 'ES', 'TR', 'RO'], links=[],
         photos_link='http://startup-machine.blogspot.com/'),
    dict(slug='getting-to-know-each-other', raw='h5', year=2018, program='Erasmus+',
         title='Getting to know each other!', short='Getting to know each other!', place='Horezu, Valcea',
         countries=['IT', 'EL', 'PL', 'ES', 'TR', 'RO'], links=[],
         photos_link='https://origami-youth-exchange.blogspot.com/'),
    dict(slug='grow-your-ideas', raw='h6', year=2019, program='Erasmus+',
         title='Grow Your Ideas!', short='Grow Your Ideas!', place='Horezu, Valcea',
         countries=['EL', 'IT', 'PT', 'ES', 'TR', 'RO'],
         links=[('Blogul proiectului', 'https://grow-your-ideas.blogspot.com/'),
                ('Pagina de Facebook a proiectului', 'https://www.facebook.com/Grow-Your-Ideas-YE-116002293120421/')],
         photos_link='https://www.facebook.com/pg/InitiativeSocialeAssociation/photos/?tab=album&album_id=2658349704241798'),
    dict(slug='lets-get-a-job', raw='h7', year=2019, program='Erasmus+',
         title='Let’s get a job!', short='Let’s get a job!', place='Horezu, Valcea',
         countries=['BG', 'IT', 'PL', 'ES', 'TR', 'RO'],
         links=[('Pagina de Facebook a proiectului', 'https://www.facebook.com/Lets-get-a-job-YE-105456444218711/')],
         photos_link='https://let-get-a-job-ye.blogspot.com/'),
    dict(slug='career-explorers', raw='h8', year=2019, program='Erasmus+',
         title='Career Explorers', short='Career Explorers', place='Horezu, Valcea',
         countries=['BG', 'IT', 'PL', 'ES', 'TR', 'RO'],
         links=[('Pagina de Facebook a proiectului', 'https://www.facebook.com/Career-Explorers-YE-100149881491496/')],
         photos_link='https://career-explorers.blogspot.com/'),
]
# Blogs used for the "Blogul proiectului" button when not already in links
BLOG = {
    'young-enterprises': 'http://young-enterprises.blogspot.com/',
    'entrepreneurial-ideas': 'http://entrepreneurial-ideas-project.blogspot.com/',
    'start-up-machine': 'http://startup-machine.blogspot.com/',
    'getting-to-know-each-other': 'https://origami-youth-exchange.blogspot.com/',
    'lets-get-a-job': 'https://let-get-a-job-ye.blogspot.com/',
    'career-explorers': 'https://career-explorers.blogspot.com/',
}

SKIP_EXACT = {'COMUNICAT', 'COMUNICAT DE PRESA', 'privind', 'Comunicat de presa'}
SKIP_START = ('Acest proiect a fost finantat cu sprijinul', 'This project is funded', 'Pentru mai multe detalii',
              'Pentru informatii suplimentare', 'Informatii suplimentare se pot obtine', 'Feedback-ul primit')
FACT = re.compile(r'^(Durata proiectului|Durata schimbului de tineret|Durata schimbului|Locatia desfasurarii schimbului de tineret):\s*(.+)$')
LISTY = re.compile(r'^(–|-|SO\s?\d|OS\d)')


def structure(raw):
    """Turn the crawled blocks into facts + a body of paragraphs and lists (wording unchanged)."""
    blocks = HOSTED_RAW[raw]['blocks']
    facts, body = [], []
    for tag, text in blocks:
        if tag in ('h1', 'div') or text in SKIP_EXACT or text.startswith(SKIP_START):
            continue
        if re.match(r'^(www\.|https?://)', text):
            continue
        if tag in ('h2', 'h3') or (re.match(r'^(Finalizarea|Incheierea) proiectului', text) and len(text) < 90):
            continue
        m = FACT.match(text)
        if m:
            facts.append((m.group(1), m.group(2).strip()))
            continue
        is_item = tag == 'li' or bool(LISTY.match(text))
        item = re.sub(r'^[–-]\s*', '', text) if is_item else text
        # a word split across two blocks on the old site ("condu" / "ce la ...")
        if body and body[-1][0] == 'ul' and is_item is False and text[:1].islower() and body[-1][1][-1][-1:].isalpha():
            body[-1][1][-1] += text
            continue
        if is_item:
            if body and body[-1][0] == 'ul':
                body[-1][1].append(item)
            else:
                body.append(('ul', [item]))
        else:
            body.append(('p', text))
    return facts, body


def photos(slug):
    d = os.path.join(ROOT, 'assets', 'images', 'archive', slug)
    if not os.path.isdir(d):
        return []
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith('.webp') and not f.endswith('-480.webp'))


def sending_rows():
    rows = []
    for e in SENDING:
        code = e.get('country_code') or CODE_BY_NAME.get(e.get('country', ''), '')
        if code == 'EL':
            pass
        group = str(e['year']) if e.get('year') else ('Tineret în Acțiune' if e['program'] != 'Erasmus+' else 'Erasmus+')
        rows.append(dict(name=e['name'], city=e.get('city', ''), country=COUNTRY.get(code, e.get('country', '')), code=code,
                         year=e.get('year'), group=group, photos=e.get('photos', ''), card=e.get('card', ''),
                         program=e['program']))
    return rows


STRATEGIC = dict(
    title='„SOCIAL – Inițiativa Multiregională pentru Dezvoltarea Economiei Sociale și ocuparea persoanelor vulnerabile”',
    paras=[
        'Direcţia Generală de Asistență Socială și Protecția Copilului Olt (lider de parteneriat) în parteneriat cu Asociația „Tineret pentru Dezvoltare Durabilă” din Tîrgu-Jiu, Asociația „Centrul pentru Dezvoltarea Instrumentelor Structurale” din Slatina și Asociația “Inițiative Sociale” din Constanța derulează începând cu luna octombrie 2014 proiectul POSDRU/168/6.1/S/144367 ”SOCIAL – Inițiativa Multiregională pentru Dezvoltarea Economiei Sociale și ocuparea persoanelor vulnerabile” cofinanţat din Fondul Social European prin Programul Operaţional Sectorial pentru Dezvoltarea Resurselor Umane 2007- 2013.',
        'Proiectul se înscrie în axa prioritară 6 „Promovarea incluziunii sociale”, domeniul major de intervenţie 6.1 „Dezvoltarea economiei sociale”.',
        'Activităţile prevăzute în cadrul proiectului se întind pe o perioadă de 12 luni şi vizează, ca obiectiv general, facilitarea accesului pe piaţa muncii şi promovarea incluziunii sociale pentru 580 de persoane vulnerabile (tineri care părăsesc sistemul de protecţie, persoane cu dizabilităţi, persoane de etnie romă, persoane care au părăsit timpuriu şcoala, persoane care trăiesc din venit minim garantat şi copii în situaţii de risc) şi formarea profesionala a 60 angajaţi din sistemul de asistenţă socială din Olt, Gorj şi Constanţa, prin accesul acestora la întreprinderile de economie socială ce vor fi înfiinţate şi prin implementarea de servicii inovative de formare profesională, mentorat şi consiliere de specialitate.',
    ],
    partners=[('Direcţia Generală de Asistență Socială și Protecția Copilului Olt', 'http://www.dgaspc-olt.ro/dgaspc/servlet/portal'),
              ('Asociația „Tineret pentru Dezvoltare Durabilă”', 'http://atdd.ro/'),
              ('Asociația „Centrul pentru Dezvoltarea Instrumentelor Structurale”', 'http://cpdis.ro/')],
    site=('www.stopexcluziunii.ro', 'http://www.stopexcluziunii.ro'),
)

OTHER = [
    ('„Youth and Work” – „Europe for Citizens”: 11-13 August 2013',
     'https://www.facebook.com/media/set/?set=a.517518054991651.1073741836.478466965563427&type=3', ''),
    ('Ziua Educației Non-formale: 12 Octombrie 2013',
     'https://www.facebook.com/media/set/?set=a.545377675539022.1073741842.478466965563427&type=3',
     'https://www.youtube.com/watch?v=a3uXqHyDSus'),
    ('Christmas Campaign: 12 Decembrie 2013',
     'https://www.facebook.com/media/set/?set=a.605685386174917.1073741846.478466965563427&type=3', ''),
    ('Promovare, diseminare și exploatare rezultate proiecte finanțate prin “Tineret în Acțiune”',
     'https://www.facebook.com/media/set/?set=a.626308594112596.1073741849.478466965563427&type=3',
     'https://www.youtube.com/watch?v=N-hvoPu7QsQ'),
    ('Promovare, diseminare și exploatare rezultate proiecte finanțate prin “Erasmus +”',
     'https://www.facebook.com/media/set/?set=a.750448591698595.1073741861.478466965563427&type=3',
     'https://www.youtube.com/watch?v=lD0rof8DKFk'),
]

INTRO_ERASMUS = ('Proiecte finantate din fonduri acordate de catre Uniunea Europeana prin programul „Erasmus+”, Actiunea Cheie 1: '
                 'Mobilitatea persoanelor in scop educational – Proiect de mobilitate pentru tineri si pentru lucratorii de tineret:')
INTRO_TIA = 'Proiecte finantate din fonduri acordate de catre Uniunea Europeana prin programul „Tineret in Actiune„:'
