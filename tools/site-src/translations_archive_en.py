"""
English for "Unde a început totul" and the arhiva-*.html pages.

- T_ARCHIVE  Romanian text -> English (page labels + the old project texts).
             The old project texts are translated paragraph by paragraph in
             archive/hosted_en.txt (same order as archive/hosted.json).
- KEEP_ARCHIVE  project names, places and organisations: the same in both languages.
- PATTERNS   text that repeats with a different name or number in it
             (photo descriptions, dates, "City, Country · Programme").
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'archive')

COUNTRY_EN = {
    'România': 'Romania', 'Polonia': 'Poland', 'Turcia': 'Turkey', 'Spania': 'Spain', 'Cipru': 'Cyprus',
    'Lituania': 'Lithuania', 'Croația': 'Croatia', 'Slovacia': 'Slovakia', 'Portugalia': 'Portugal',
    'Italia': 'Italy', 'Norvegia': 'Norway', 'Grecia': 'Greece', 'Germania': 'Germany', 'Letonia': 'Latvia',
    'Macedonia': 'Macedonia', 'Bulgaria': 'Bulgaria',
}
MONTHS_EN = {
    'ianuarie': 'January', 'februarie': 'February', 'martie': 'March', 'aprilie': 'April', 'mai': 'May',
    'iunie': 'June', 'iulie': 'July', 'august': 'August', 'septembrie': 'September', 'octombrie': 'October',
    'noiembrie': 'November', 'noimebrie': 'November', 'decembrie': 'December',
}
PROGRAMME_EN = {'Tineret în Acțiune': 'Youth in Action', 'Erasmus+': 'Erasmus+'}
CITY_EN = {'Atena': 'Athens'}

# ---------- Page labels ----------
T_ARCHIVE = {
    'Unde a început totul': 'Where it all began',
    'De peste un deceniu, deschidem uși pentru tineri: către competențe noi, oameni noi și locuri noi.':
        'For more than a decade, we have been opening doors for young people: to new skills, new people and new places.',
    'Proiecte ca organizație gazdă': 'Projects as host organisation',
    'Proiecte ca organizație de trimitere': 'Projects as sending organisation',
    'Fotografie din primele proiecte AIS': 'Photo from the first AIS projects',
    'Mobilități de tineret': 'Youth mobilities',
    'Organizație gazdă': 'Host organisation',
    'Organizație de trimitere': 'Sending organisation',
    'Tineret în Acțiune': 'Youth in Action',
    'Filtru': 'Filter',
    'Toate': 'All',
    'Vezi toate': 'See all',
    'Strategice': 'Strategic',
    'Alte activități': 'Other activities',
    'Albumul de poze': 'Photo album',
    'video': 'video',
    'Feedback video': 'Video feedback',
    'Blogul proiectului': 'Project blog',
    'Broșura': 'Brochure',
    'Filmulețele de prezentare': 'Presentation videos',
    'Pagina de Facebook a proiectului': 'The project’s Facebook page',
    'An': 'Year',
    'Rol': 'Role',
    'Țări': 'Countries',
    'Program': 'Programme',
    'Durata proiectului': 'Project duration',
    'Durata schimbului de tineret': 'Youth exchange dates',
    'Durata schimbului': 'Exchange dates',
    'Locația desfășurării schimbului de tineret': 'Youth exchange venue',
    'Antreprenoriat social': 'Social entrepreneurship',
    'Proiecte finanțate din fonduri acordate de către Uniunea Europeană prin programul „Tineret în Acțiune„:':
        'Projects funded by the European Union through the “Youth in Action” programme:',
    'Proiecte finanțate din fonduri acordate de către Uniunea Europeană prin programul „Erasmus+”, Acțiunea Cheie 1: '
    'Mobilitatea persoanelor în scop educațional – Proiect de mobilitate pentru tineri și pentru lucrătorii de tineret:':
        'Projects funded by the European Union through the “Erasmus+” programme, Key Action 1: '
        'Learning mobility of individuals – Mobility project for young people and youth workers:',
    'Încurajarea tinerilor pentru participarea la dezvoltarea inițiativelor în antreprenoriatul social':
        'Encouraging young people to take part in developing social entrepreneurship initiatives',
    'Încurajarea tinerilor pentru participarea la dezvoltarea inițiativelor în antreprenoriatul social”':
        'Encouraging young people to take part in developing social entrepreneurship initiatives”',
    # Strategic partnership (2014)
    'Titlul proiectului: „SOCIAL – Inițiativa Multiregională pentru Dezvoltarea Economiei Sociale și ocuparea persoanelor vulnerabile”.':
        'Project title: “SOCIAL – Multiregional Initiative for the Development of the Social Economy and the employment of vulnerable people”.',
    '„SOCIAL – Inițiativa Multiregională pentru Dezvoltarea Economiei Sociale și ocuparea persoanelor vulnerabile”':
        '“SOCIAL – Multiregional Initiative for the Development of the Social Economy and the employment of vulnerable people”',
    'Direcţia Generală de Asistență Socială și Protecția Copilului Olt':
        'Direcţia Generală de Asistență Socială și Protecția Copilului Olt (Olt General Directorate for Social Assistance and Child Protection)',
    'Asociația „Tineret pentru Dezvoltare Durabilă”': 'Asociația „Tineret pentru Dezvoltare Durabilă” (Youth for Sustainable Development Association)',
    'Asociația „Centrul pentru Dezvoltarea Instrumentelor Structurale”':
        'Asociația „Centrul pentru Dezvoltarea Instrumentelor Structurale” (Centre for the Development of Structural Instruments Association)',
    'Direcţia Generală de Asistență Socială și Protecția Copilului Olt (lider de parteneriat) în parteneriat cu Asociația „Tineret pentru Dezvoltare Durabilă” din Tîrgu-Jiu, Asociația „Centrul pentru Dezvoltarea Instrumentelor Structurale” din Slatina și Asociația “Inițiative Sociale” din Constanța derulează începând cu luna octombrie 2014 proiectul POSDRU/168/6.1/S/144367 ”SOCIAL – Inițiativa Multiregională pentru Dezvoltarea Economiei Sociale și ocuparea persoanelor vulnerabile” cofinanţat din Fondul Social European prin Programul Operaţional Sectorial pentru Dezvoltarea Resurselor Umane 2007- 2013.':
        'The Olt General Directorate for Social Assistance and Child Protection (partnership leader), in partnership with the Youth for Sustainable Development Association from Târgu Jiu, the Centre for the Development of Structural Instruments Association from Slatina and Asociația “Inițiative Sociale” from Constanța, has been running, since October 2014, the project POSDRU/168/6.1/S/144367 “SOCIAL – Multiregional Initiative for the Development of the Social Economy and the employment of vulnerable people”, co-financed by the European Social Fund through the Sectoral Operational Programme Human Resources Development 2007–2013.',
    'Proiectul se înscrie în axa prioritară 6 „Promovarea incluziunii sociale”, domeniul major de intervenţie 6.1 „Dezvoltarea economiei sociale”.':
        'The project falls under priority axis 6 “Promoting social inclusion”, key area of intervention 6.1 “Developing the social economy”.',
    'Activităţile prevăzute în cadrul proiectului se întind pe o perioadă de 12 luni şi vizează, ca obiectiv general, facilitarea accesului pe piaţa muncii şi promovarea incluziunii sociale pentru 580 de persoane vulnerabile (tineri care părăsesc sistemul de protecţie, persoane cu dizabilităţi, persoane de etnie romă, persoane care au părăsit timpuriu şcoala, persoane care trăiesc din venit minim garantat şi copii în situaţii de risc) şi formarea profesionala a 60 angajaţi din sistemul de asistenţă socială din Olt, Gorj şi Constanţa, prin accesul acestora la întreprinderile de economie socială ce vor fi înfiinţate şi prin implementarea de servicii inovative de formare profesională, mentorat şi consiliere de specialitate.':
        'The project activities run over 12 months and have the general objective of making it easier to access the labour market and promoting social inclusion for 580 vulnerable people (young people leaving the care system, people with disabilities, Roma people, early school leavers, people living on the guaranteed minimum income and children at risk), and of training 60 employees of the social assistance system in Olt, Gorj and Constanța, through their access to the social economy enterprises to be set up and through innovative services of vocational training, mentoring and specialist counselling.',
    # Other activities (2013–2014)
    '„Youth and Work” – „Europe for Citizens”: 11-13 August 2013': '“Youth and Work” – “Europe for Citizens”: 11–13 August 2013',
    'Ziua Educației Non-formale: 12 Octombrie 2013': 'Non-formal Education Day: 12 October 2013',
    'Christmas Campaign: 12 Decembrie 2013': 'Christmas Campaign: 12 December 2013',
    'Promovare, diseminare și exploatare rezultate proiecte finanțate prin “Tineret în Acțiune”':
        'Promotion, dissemination and use of the results of projects funded through “Youth in Action”',
    'Promovare, diseminare și exploatare rezultate proiecte finanțate prin “Erasmus +”':
        'Promotion, dissemination and use of the results of projects funded through “Erasmus +”',
}

FLAPS_ARCHIVE = {str(y): str(y) for y in range(2013, 2021)}


# ---------- Old project texts: archive/hosted_en.txt, aligned with archive/hosted.json ----------
def _hosted_pairs():
    hosted = json.load(open(os.path.join(DATA, 'hosted.json'), encoding='utf-8'))
    en, key = {}, None
    path = os.path.join(DATA, 'hosted_en.txt')
    if not os.path.exists(path):
        return []
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('## '):
            key = line[3:]
            en[key] = []
        elif line and not line.startswith('#'):
            en[key].append(line.split(' | ', 1)[1])
    pairs = []
    for key, texts in en.items():
        ro = [t for tag, t in hosted[key]['blocks'] if tag != 'div']
        assert len(ro) == len(texts), (key, len(ro), len(texts))
        pairs += list(zip(ro, texts))
    return pairs


_FACT = re.compile(r'^([^:]{4,60}):\s*(.+)$')
_pairs = _hosted_pairs()
for (ro, en), (ro2, en2) in zip(_pairs, _pairs[1:]):
    # a word split across two blocks on the old site ("condu" / "ce la ...") is joined on the page
    if ro2[:1].islower() and ro[-1:].isalpha():
        T_ARCHIVE.setdefault(re.sub(r'^[–-]\s*', '', ro) + ro2, re.sub(r'^[–-]\s*', '', en) + ' ' + en2)
for ro, en in _pairs:
    T_ARCHIVE.setdefault(ro, en)
    # list items lose their leading dash on the page
    T_ARCHIVE.setdefault(re.sub(r'^[–-]\s*', '', ro), re.sub(r'^[–-]\s*', '', en))
    # the page description is the first 150 characters of the first paragraph
    T_ARCHIVE.setdefault(ro[:150].strip(), en if len(en) <= 160 else en[:150].rsplit(' ', 1)[0] + '…')
    # "Durata proiectului: ..." becomes a label + value on the page
    m, n = _FACT.match(ro), _FACT.match(en)
    if m and n and ro.startswith(('Durata', 'Locația')):
        T_ARCHIVE.setdefault(m.group(2), n.group(2))
        T_ARCHIVE.setdefault(m.group(1), n.group(1))


# ---------- Names that read the same in English ----------
KEEP_ARCHIVE = {'Horezu', 'Eforie Nord', 'Păulești', 'www.stopexcluziunii.ro', 'Project card'}
_hosted = json.load(open(os.path.join(DATA, 'hosted.json'), encoding='utf-8'))
for _e in json.load(open(os.path.join(DATA, 'sending.json'), encoding='utf-8')):
    KEEP_ARCHIVE.update(x for x in (_e.get('name'), _e.get('title'), _e.get('city')) if x)
from archive import HOSTED as _H  # noqa: E402
for _h in _H:
    KEEP_ARCHIVE.update((_h['title'], _h['short']))
KEEP_ARCHIVE = {k for k in KEEP_ARCHIVE if k not in T_ARCHIVE}


# ---------- Repeated shapes ----------
def _date(m, tr):
    def one(d, mo, y):
        return f'{int(d)} {MONTHS_EN[mo.lower()]}' + (f' {y}' if y else '')
    return f'{one(*m.group(1, 2, 3))} – {one(*m.group(4, 5, 6))}'


def _place(text):
    """'Struga, Macedonia' / 'Horezu, Vâlcea – România' / 'Polonia'"""
    return ', '.join(COUNTRY_EN.get(p, CITY_EN.get(p, p)) for p in text.split(', ')).replace('– România', '– Romania')


PATTERNS = [
    (re.compile(r'Fotografie din proiectul (.+) \((\d+) din (\d+)\)'),
     lambda m, tr: f'Photo from the project {m.group(1)} ({m.group(2)} of {m.group(3)})'),
    (re.compile(r'Fotografie din proiectul (.+)'), lambda m, tr: f'Photo from the project {m.group(1)}'),
    (re.compile(r'Fotografii · (.+)'), lambda m, tr: f'Photos · {m.group(1)}'),
    (re.compile(r'(.+) \| Asociația Inițiative Sociale'), lambda m, tr: f'{tr(m.group(1))} | Asociația Inițiative Sociale'),
    (re.compile(r'(.+) · Organizație gazdă · (.+)'),
     lambda m, tr: f'{PROGRAMME_EN[m.group(1)]} · Host organisation · {_place(m.group(2))}'),
    (re.compile(r'(?:(.+), )?([^,·]+) · (Tineret în Acțiune|Erasmus\+|\d{4})'),
     lambda m, tr: (f'{CITY_EN.get(m.group(1), m.group(1))}, ' if m.group(1) else '')
     + f'{COUNTRY_EN.get(m.group(2), m.group(2))} · {PROGRAMME_EN.get(m.group(3), m.group(3))}'),
    (re.compile(r'(\d{1,2}) (\w+)(?: (\d{4}))? – (\d{1,2}) (\w+) (\d{4})'), _date),
    (re.compile(r'\d{4} · [A-Z]{2}'), lambda m, tr: m.group(0)),
    (re.compile(r'[A-Z]{2}'), lambda m, tr: m.group(0)),
    (re.compile(r'(?:[^,·]+, )*[^,·]+'), lambda m, tr: _places(m.group(0))),
    (re.compile(r'Horezu, Vâlcea – România'), lambda m, tr: 'Horezu, Vâlcea – Romania'),
]


def _places(text):
    """A list of known places/countries, e.g. 'Italia, Turcia, România' or 'Păulești, Prahova'."""
    known = set(COUNTRY_EN) | KEEP_ARCHIVE | {'Prahova', 'Vâlcea', 'Constanța'}
    if not all(p in known for p in text.split(', ')):
        raise LookupError(text)
    return _place(text)


# a pattern that cannot translate its text falls through to "missing"
_wrapped = []
for _p, _f in PATTERNS:
    def _safe(m, tr, _f=_f):
        try:
            return _f(m, tr)
        except (LookupError, KeyError):
            return None
    _wrapped.append((_p, _safe))
PATTERNS = _wrapped
