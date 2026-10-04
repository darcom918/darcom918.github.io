"""
Turns a built Romanian page into its English version (html/en/<page>.html).

Every piece of visible text, every image description (alt), every screen-reader
label (aria-label, title), the page description and the e-mail subjects are
looked up in translations_en.py. If anything Romanian has no translation the
build stops and lists it, so no page can go out half-translated.

To change an English text: edit translations_en.py and rebuild.
To add a new Romanian text: add its translation to translations_en.py too.
"""
import re
from html import escape, unescape
from urllib.parse import quote, unquote

from translations_en import T, FLAPS, KEEP

TOKEN = re.compile(r'<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>|[^<]+', re.S)
ATTR = re.compile(r'(\s)(alt|aria-label|title|placeholder|data-label|content|href)="([^"]*)"')
BOARD = re.compile(r'(?:<span class="flap-word">(?:<span class="flap" data-char="[^"]+">[^<]+</span>)+</span>)+')
FLAP_WORD = re.compile(r'<span class="flap-word">((?:<span class="flap" data-char="[^"]+">[^<]+</span>)+)</span>')
LETTERS = re.compile(r'[A-Za-zĂÂÎȘȚăâîșțŞşŢţ]')
# Placeholder story text on the activity pages (to be replaced with real text in both languages)
LOREM = re.compile(r'\b(lorem|ipsum|dolor|amet|consectetur|voluptat\w*|nullam|temporibus|similique|maecenas|cras|donec|neque|quis)\b', re.I)
# Activity codes and route labels read the same in both languages ("A2 →", "A1 · RO → EU")
CODE_TOKENS = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'BOOST', 'AIS', 'Erasmus+', 'RO', 'EU', '→', '←', '·'}
# Romanian decimal comma -> English decimal point (4,81 -> 4.81)
DECIMAL = re.compile(r'(?<![\d,])(\d+),(\d{1,2})(?![\d,])')
TRANSLATABLE_META = ('name="description"', 'property="og:title"', 'property="og:description"')


class Missing(Exception):
    pass


def _lookup(text, missing):
    if not LETTERS.search(text):
        return DECIMAL.sub(r'\1.\2', text)
    if len(text) == 1 or text in KEEP or LOREM.search(text) or set(text.split()) <= CODE_TOKENS:
        return text
    if text in T:
        return T[text]
    missing.append(text)
    return text


def _text(raw, missing):
    stripped = raw.strip()
    if not stripped:
        return raw
    value = unescape(stripped)
    out = _lookup(value, missing)
    if out == value:
        return raw
    lead = raw[:len(raw) - len(raw.lstrip())]
    trail = raw[len(raw.rstrip()):]
    return lead + escape(out, quote=False) + trail


def _mailto(href, missing):
    # mailto:address?subject=...&body=...  -> translate subject and body
    if not href.startswith('mailto:') or '?' not in href:
        return href
    addr, query = href.split('?', 1)
    parts = []
    for pair in query.split('&'):
        key, _, val = pair.partition('=')
        text = unquote(val)
        parts.append(f'{key}={quote(_lookup(text, missing), safe="")}')
    return addr + '?' + '&'.join(parts)


def _tag(tag, missing):
    is_meta = tag.startswith('<meta')

    def repl(m):
        space, name, raw = m.groups()
        if name == 'content' and not (is_meta and any(k in tag for k in TRANSLATABLE_META)):
            return m.group(0)
        value = unescape(raw)
        if name == 'href':
            new = _mailto(value, missing)
        else:
            new = _lookup(value.strip(), missing) if value.strip() else value
        if new == value:
            return m.group(0)
        return f'{space}{name}="{escape(new, quote=True)}"'
    return ATTR.sub(repl, tag)


def _flaps(out, missing):
    def repl(m):
        words = [''.join(re.findall(r'data-char="([^"]+)"', w)) for w in FLAP_WORD.findall(m.group(0))]
        key = ' '.join(words)
        if key in KEEP or re.fullmatch(r'A\d', key):
            return m.group(0)
        if key not in FLAPS:
            missing.append('FLAP: ' + key)
            return m.group(0)
        return ''.join('<span class="flap-word">' + ''.join(
            f'<span class="flap" data-char="{c}">{c}</span>' for c in word) + '</span>'
            for word in FLAPS[key].split(' '))
    return BOARD.sub(repl, out)


def to_english(page, switch_ro, switch_en):
    missing = []
    assert page.count(switch_ro) == 1
    page = page.replace(switch_ro, '<!--LANG-SWITCH-->')
    page = _flaps(page, missing)
    parts = []
    for tok in TOKEN.findall(page):
        if tok.startswith('<!--') or tok.startswith('<script') or tok.startswith('<style'):
            parts.append(tok)
        elif tok.startswith('<'):
            parts.append(_tag(tok, missing))
        else:
            parts.append(_text(tok, missing))
    en = ''.join(parts)
    if missing:
        seen = list(dict.fromkeys(missing))
        raise Missing('No English translation for:\n  ' + '\n  '.join(seen))
    en = en.replace('<!--LANG-SWITCH-->', switch_en)
    en = en.replace('<html lang="ro"', '<html lang="en"', 1)
    en = en.replace('../assets/', '../../assets/')
    return en
