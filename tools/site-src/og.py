"""Link previews (WhatsApp, Facebook, LinkedIn, X): one 1200x630 boarding-pass card per page and language,
saved to assets/images/og/, plus the Open Graph / Twitter tags that point to it."""
import os, re, random
from html import escape, unescape
from PIL import Image, ImageDraw, ImageFont, ImageOps

SP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(SP))
SITE = 'https://initiative-sociale.ro'
OUT = os.path.join(ROOT, 'assets', 'images', 'og')
W, H = 1200, 630
INK, INK3, CREAM, CARD = '#0E1530', '#222C61', '#F6F1E7', '#FFFDF8'
RED, REDINK, SUN, TEXT2, LINE = '#ED1C24', '#D7141C', '#FFC93C', '#4A5068', '#D9D1C1'


def _font(name, size, **axes):
    f = ImageFont.truetype(os.path.join(SP, 'fonts', name), size)
    names = [a['name'] for a in f.get_variation_axes()]
    f.set_variation_by_axes([axes.get(n.decode().lower()[:4], a['default']) for n, a in zip(names, f.get_variation_axes())])
    return f


def archivo(size, wght=800, wdth=110):
    return _font('Archivo.ttf', size, weig=wght, widt=wdth)


def mono(size, wght=700):
    return _font('JetBrainsMono.ttf', size, weig=wght)


def _wrap(draw, text, font, width):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) <= width or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur] if cur else lines


def _cover(path, w, h):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w) // 2, (im.height - h) // 3  # keep faces: crop a bit higher than centre
    return im.crop((l, t, l + w, t + h))


def card(slug, title, kicker, stamp, photo, new=False):
    """Draw the card; returns its public URL."""
    os.makedirs(OUT, exist_ok=True)
    im = Image.new('RGB', (W, H), INK)
    d = ImageDraw.Draw(im)
    for y in range(14, H, 22):  # dot-matrix night sky, like the Europe map
        for x in range(14, W, 22):
            d.ellipse((x - 1.6, y - 1.6, x + 1.6, y + 1.6), fill='#1B2350')
    # the ticket
    x0, y0, x1, y1, cut = 40, 40, 1160, 590, 800
    mask = Image.new('L', (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((x0, y0, x1, y1), 34, fill=255)
    for cy in (y0, y1):  # perforation notches
        md.ellipse((cut - 22, cy - 22, cut + 22, cy + 22), fill=0)
    ticket = Image.new('RGB', (W, H), CARD)
    td = ImageDraw.Draw(ticket)
    td.rectangle((x0, y0, x1, y0 + 12), fill=RED)
    # stub: the page's photo, or a lettered tile when there is none
    px0, py0, px1, py1 = cut + 26, y0 + 40, x1 - 30, y1 - 30
    if photo and os.path.exists(photo):
        ph = _cover(photo, px1 - px0, py1 - py0)
    else:
        ph = Image.new('RGB', (px1 - px0, py1 - py0), INK)
        pd = ImageDraw.Draw(ph)
        f = archivo(96, 800, 125)
        word = 'AIS'
        pd.text(((px1 - px0 - pd.textlength(word, font=f)) / 2, (py1 - py0) / 2 - 70), word, font=f, fill=CREAM)
        g = mono(22)
        sub = 'ERASMUS+'
        pd.text(((px1 - px0 - pd.textlength(sub, font=g)) / 2, (py1 - py0) / 2 + 40), sub, font=g, fill=SUN)
    pm = Image.new('L', ph.size, 0)
    ImageDraw.Draw(pm).rounded_rectangle((0, 0, ph.width - 1, ph.height - 1), 22, fill=255)
    ticket.paste(ph, (px0, py0), pm)
    for y in range(y0 + 34, y1 - 30, 18):  # dashed tear line
        td.line((cut, y, cut, y + 9), fill=LINE, width=3)
    im.paste(ticket, (0, 0), mask)
    d = ImageDraw.Draw(im)
    # logo + kicker
    lx, ly = 92, 92
    logo = Image.open(os.path.join(ROOT, 'assets', 'images', 'logos', 'ais-logo-dark.png')).convert('RGBA')
    logo = logo.resize((round(logo.width * 46 / logo.height), 46), Image.LANCZOS)
    im.paste(logo, (lx, ly), logo)
    d.text((lx, ly + 76), kicker.upper(), font=mono(21), fill=REDINK)
    # title: as big as it fits in three lines
    width, ty = cut - lx - 56, ly + 120
    room = (y1 - 118 - 28) - ty  # stop above the split-flap stamp
    for size in range(88, 36, -4):
        f = archivo(size, 800, 112)
        lines = _wrap(d, title, f, width)
        if len(lines) <= 3 and len(lines) * round(size * 1.04) <= room:
            break
    for ln in lines:
        d.text((lx, ty), ln, font=f, fill=INK)
        ty += round(size * 1.04)
    # split-flap stamp + barcode
    fx, fy, tw, th = lx, y1 - 118, 42, 58
    fm = mono(32, 800)
    for ch in stamp.upper():
        if ch == ' ':
            fx += 18; continue
        d.rounded_rectangle((fx, fy, fx + tw, fy + th), 7, fill=INK)
        d.line((fx + 3, fy + th / 2, fx + tw - 3, fy + th / 2), fill='#050A1E', width=2)
        d.text((fx + (tw - d.textlength(ch, font=fm)) / 2, fy + 8), ch, font=fm, fill=SUN)
        fx += tw + 5
    rnd = random.Random(slug)
    bx = max(fx + 34, cut - 250)
    while bx < cut - 44:
        bw = rnd.choice((2, 2, 3, 5))
        d.rectangle((bx, fy + 4, bx + bw, fy + th - 4), fill=INK)
        bx += bw + rnd.choice((3, 4, 6))
    d.text((lx, y1 - 46), 'initiative-sociale.ro', font=mono(19, 500), fill=TEXT2)
    if new:  # sticker on the photo
        s = Image.new('RGBA', (170, 74), (0, 0, 0, 0))
        sd = ImageDraw.Draw(s)
        sd.rounded_rectangle((4, 4, 166, 70), 12, fill=SUN)
        nf = mono(38, 800)
        sd.text(((170 - sd.textlength('NEW', font=nf)) / 2, 12), 'NEW', font=nf, fill=INK)
        s = s.rotate(6, expand=True, resample=Image.BICUBIC)
        im.paste(s, (px0 - 22, py0 - 24), s)
    path = os.path.join(OUT, slug + '.jpg')
    im.save(path, quality=84, optimize=True, progressive=True)
    return f'{SITE}/assets/images/og/{slug}.jpg'


DEFAULT_PHOTO = os.path.join(ROOT, 'assets', 'images', 'ais', 'A1_2.webp')  # the homepage hero photo
SKIP_IMG = ('logos/', 'co-funded', 'banners-simple/', 'flags/', 'favicon', 'logo-')


def first_photo(page_html, page_dir):
    main = re.search(r'<main.*?</main>', page_html, re.S)
    for src in re.findall(r'<img [^>]*src="([^"]+)"', main.group(0) if main else page_html):
        if src.startswith('http') or any(k in src for k in SKIP_IMG):
            continue
        p = os.path.normpath(os.path.join(page_dir, src))
        if os.path.exists(p):
            return p
    return None


TAGS = re.compile(r'\n?[ \t]*<meta (?:property="og:(?:image|url|site_name|locale)[^"]*"|name="twitter:[^"]*")[^>]*/?>')


def inject(page_html, name, lang, kicker, stamp, photo=None, new=False):
    """Draw the card for this page and put the full set of preview tags in <head>."""
    title = unescape(re.search(r'<title>(.*?)</title>', page_html, re.S).group(1)).strip()
    parts = [p.strip() for p in title.split('|')]
    short = parts[1] if len(parts) > 1 and 'Inițiative Sociale' in parts[0] else parts[0]  # the logo already says AIS
    m = re.search(r'<meta name="description" content="([^"]*)"', page_html)
    desc = unescape(m.group(1)) if m else ''
    page_dir = os.path.join(ROOT, 'html', 'en' if lang == 'en' else '')
    photo = photo or first_photo(page_html, page_dir) or DEFAULT_PHOTO
    url_img = card(f'{lang}-{name}', short or title, kicker, stamp, photo, new)
    url = f"{SITE}/html/{'en/' if lang == 'en' else ''}{name}.html"
    head = page_html.split('</head>', 1)
    h = TAGS.sub('', head[0])
    h = re.sub(r'(<meta property="og:title" content=")([^"]*?) · ([^"]+)"', lambda m: m.group(0) if m.group(3) not in m.group(2) else f'{m.group(1)}{m.group(2)}"', h)
    tags = []
    if 'property="og:title"' not in h:
        tags.append(f'<meta property="og:title" content="{escape(title)}"/>')
    if 'property="og:description"' not in h and desc:
        tags.append(f'<meta property="og:description" content="{escape(desc)}"/>')
    tags += [f'<meta property="og:url" content="{url}"/>',
             '<meta property="og:site_name" content="Asociația Inițiative Sociale"/>',
             f'<meta property="og:locale" content="{"en_GB" if lang == "en" else "ro_RO"}"/>',
             f'<meta property="og:image" content="{url_img}"/>',
             '<meta property="og:image:width" content="1200"/>',
             '<meta property="og:image:height" content="630"/>',
             f'<meta property="og:image:alt" content="{escape(short or title)}"/>',
             '<meta name="twitter:card" content="summary_large_image"/>']
    return h.rstrip('\n') + '\n' + '\n'.join(tags) + '\n</head>' + head[1]
