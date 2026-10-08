"""HTML for "Unde a început totul" (overview) and one page per hosted project."""
import os
from html import escape as esc
from PIL import Image
from archive import (HOSTED, BLOG, COUNTRY, structure, photos, sending_rows, STRATEGIC, OTHER,
                     INTRO_ERASMUS, INTRO_TIA, ROOT)

OVERVIEW = 'unde-a-inceput-totul'
HEAD = '''<!DOCTYPE html>
<html lang="ro" class="no-js">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>{title} | Asociația Inițiative Sociale</title>
<meta name="description" content="{desc}"/>
<meta name="theme-color" content="#0E1530"/>
<meta property="og:type" content="website"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{desc}"/>
<link href="../assets/images/logos/favicon.svg" rel="icon" type="image/svg+xml"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin=""/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&amp;family=JetBrains+Mono:wght@500;700&amp;display=swap"/>
<link rel="stylesheet" href="../assets/css/ais.css"/>
<script>document.documentElement.classList.replace('no-js','js');setTimeout(function(){{if(!window.AIS_READY)document.documentElement.classList.remove('js')}},2500)</script>
</head>
<body>
{{{{HEADER:projects}}}}<main id="continut">
'''
TAIL = '''
</main>

{{FOOTER}}
</body>
</html>
'''


def aimg(base, alt, sizes, mode='lazy', cls=''):
    """<img> for an archive photo (base = 'archive/<slug>/<name>') with its 480px thumbnail."""
    full = os.path.join(ROOT, 'assets', 'images', base + '.webp')
    w, h = Image.open(full).size
    a = [f'src="../assets/images/{base}.webp"',
         f'srcset="../assets/images/{base}-480.webp 480w, ../assets/images/{base}.webp {w}w"',
         f'sizes="{sizes}"', f'alt="{esc(alt, quote=True)}"', f'width="{w}" height="{h}"', 'decoding="async"']
    if mode == 'lazy':
        a.append('loading="lazy"')
    if cls:
        a.insert(0, f'class="{cls}"')
    return '<img ' + ' '.join(a) + '/>'


def ext_link(label, href, cls='btn btn--ghost'):
    return f'<a class="{cls}" href="{esc(href, quote=True)}" target="_blank" rel="noopener noreferrer">{esc(label)} {{{{ICON:ext}}}}</a>'


def chips(codes):
    return ''.join(f'<span class="tag"><b class="mono">{c}</b> {COUNTRY[c]}</span>' for c in codes)


# ---------------------------------------------------------------- project page
def project(slug):
    i = next(k for k, h in enumerate(HOSTED) if h['slug'] == slug)
    h = HOSTED[i]
    facts, body = structure(h['raw'])
    ph = photos(slug)
    title = h['title']
    lead = next((t for k, t in body if k == 'p'), '')
    out = [HEAD.format(title=esc(h['short']), desc=esc(lead[:150], quote=True))]

    # hero
    hero_btns = []
    blog = BLOG.get(slug)
    if blog and not any(l[0] == 'Blogul proiectului' for l in h['links']) and blog != h['photos_link']:
        hero_btns.append(ext_link('Blogul proiectului', blog, 'btn'))
    for k, (label, href) in enumerate(h['links']):
        hero_btns.append(ext_link(label, href, 'btn' if not hero_btns else 'btn btn--ghost'))
    if not hero_btns:
        hero_btns.append(ext_link('See All Results and Photos', h['photos_link'], 'btn'))
    fan = ''
    if len(ph) >= 3:
        pick = [ph[min(2, len(ph) - 1)], ph[0], ph[len(ph) // 2]]
        fan = '<div class="fan act-fan" data-fan>' + ''.join(
            f'<figure class="fan__card fan__card--{c}">{aimg(f"archive/{slug}/{p}", f"Fotografie din proiectul {title}", "(min-width: 62rem) 24vw, 56vw", "eager")}</figure>'
            for c, p in zip(('l', 'r', 'c'), pick)) + '</div>'
    kicker = f'{h["program"]} · Organizație gazdă · {h["place"]}'
    out.append(f'''
<section class="hero act-hero section--ink{' act-hero--solo' if not fan else ''}" data-header="dark" aria-labelledby="page-title">
  <div class="container act-hero__grid">
    <div class="act-hero__copy">
      <nav class="crumbs mono" aria-label="Breadcrumb">
        <a href="index.html">Acasă</a><span aria-hidden="true">/</span><a href="projects.html">Proiecte</a><span aria-hidden="true">/</span><a href="{OVERVIEW}.html">Unde a început totul</a><span aria-hidden="true">/</span><span aria-current="page">{h["year"]}</span>
      </nav>
      <div class="act-hero__code" aria-hidden="true"><span class="flap-board" data-flap-board>{{{{FLAP:{h["year"]}}}}}</span></div>
      <p class="act-hero__kicker mono">{esc(kicker)}</p>
      <h1 class="act-hero__title arch-title" id="page-title">{esc(title)}</h1>
      {('<div class="tags act-hero__tags">' + chips(h['countries']) + '</div>') if h['countries'] else ''}
      <div class="hero__actions">{''.join(hero_btns)}</div>
    </div>
    {fan}
  </div>
</section>
''')

    # body: original text + status board
    rows = [('Program', h['program']), ('An', str(h['year'])), ('Rol', 'Organizație gazdă')]
    rows += facts
    if h['countries']:
        rows.append(('Țări', ', '.join(COUNTRY[c] for c in h['countries'])))
    parts = []
    for k, (kind, val) in enumerate(body):
        if kind == 'p':
            cls = ' class="arch-article__lead"' if k == 0 else ''
            parts.append(f'<p{cls}>{esc(val)}</p>')
        else:
            parts.append('<ul class="arch-list">' + ''.join(f'<li>{esc(x)}</li>' for x in val) + '</ul>')
    board = '\n'.join(f'<div class="status-row"><dt class="mono">{esc(a)}</dt><dd>{esc(b)}</dd></div>' for a, b in rows)
    out.append(f'''
<section class="section arch-body-section" data-header="light" aria-labelledby="descriere-title">
  <div class="container arch-body">
    <article class="arch-article">
      <p class="eyebrow mono" data-reveal><span class="eyebrow__num">{h["year"]}</span>{esc(h["program"])}</p>
      <h2 class="h2" id="descriere-title" data-reveal>Descriere</h2>
      <div class="arch-article__text" data-reveal>
        {''.join(parts)}
      </div>
    </article>
    <aside class="arch-aside">
      <div class="departures status-board" data-reveal>
        <div class="departures__head mono"><span>{{{{ICON:plane}}}}</span><span>{h["year"]} · RO</span></div>
        <dl class="status-rows">{board}</dl>
      </div>
    </aside>
  </div>
</section>
''')

    # gallery
    cta = f'<p class="gallery-cta" data-reveal>{ext_link("See All Results and Photos", h["photos_link"], "btn btn--ink gallery-cta__btn")}</p>'
    if ph:
        items = []
        for n, p in enumerate(ph):
            alt = f'Fotografie din proiectul {title} ({n + 1} din {len(ph)})'
            items.append(f'<li data-reveal style="--d:{(n % 6) * 0.05:.2f}s"><button class="gal__item" type="button" data-gal="{n}" '
                         f'data-full="../assets/images/archive/{slug}/{p}.webp" aria-label="{esc(alt, quote=True)}">'
                         f'{aimg(f"archive/{slug}/{p}", alt, "(min-width: 62rem) 22vw, 46vw")}</button></li>')
        out.append(f'''
<section class="section section--paper2 gallery-section" data-header="light" aria-labelledby="galerie-title">
  <div class="container">
    <div class="gallery-head">
      <p class="eyebrow mono" data-reveal><span class="eyebrow__num">{len(ph)}</span>Fotografii</p>
      <h2 class="visually-hidden" id="galerie-title">Fotografii · {esc(title)}</h2>
    </div>
    <ul class="gallery" data-gallery data-label="{esc(title, quote=True)}">
      {''.join(items)}
    </ul>
    {cta}
  </div>
</section>
''')
    else:
        out.append(f'''
<section class="section section--paper2 section--tight" data-header="light" aria-label="Fotografii">
  <div class="container">{cta}</div>
</section>
''')

    # previous / next
    nav = []
    prev = HOSTED[i - 1] if i > 0 else None
    nxt = HOSTED[i + 1] if i < len(HOSTED) - 1 else None
    def card(p, label, red=False, back=False):
        pp = photos(p['slug'])
        photo = aimg(f"archive/{p['slug']}/{pp[0]}", '', '(min-width: 48rem) 46vw, 92vw') if pp else '<span class="arch-card__ph" aria-hidden="true">{{ICON:plane}}</span>'
        arrow = '{{ICON:left}}' if back else '{{ICON:arrow}}'
        return (f'<a class="next-card{" next-card--red" if red else ""}" href="arhiva-{p["slug"]}.html" data-reveal>'
                f'<span class="next-card__photo">{photo}</span><span class="next-card__foot"><span>'
                f'<span class="next-card__kicker mono">{label}</span><span class="next-card__label">{esc(p["short"])}</span></span>'
                f'<span class="pass__go{" pass__go--back" if back else ""}" aria-hidden="true">{arrow}</span></span></a>')
    nav.append(card(prev, f'← {prev["year"]}', back=True) if prev else
               f'<a class="next-card" href="{OVERVIEW}.html" data-reveal><span class="next-card__photo">{aimg("archive/paper-handicraft-business/" + photos("paper-handicraft-business")[3], "", "(min-width: 48rem) 46vw, 92vw")}</span>'
               '<span class="next-card__foot"><span><span class="next-card__kicker mono">← 2013</span><span class="next-card__label">Unde a început totul</span></span><span class="pass__go pass__go--back" aria-hidden="true">{{ICON:left}}</span></span></a>')
    nav.append(card(nxt, f'{nxt["year"]} →', red=True) if nxt else
               '<a class="next-card next-card--red" href="projects.html#innoventure" data-reveal><span class="next-card__photo">{{IMG:ais/A1|Tineri participanți la o activitate Erasmus+, în fața unui castel|(min-width: 48rem) 46vw, 92vw|lazy}}</span>'
               '<span class="next-card__foot"><span><span class="next-card__kicker mono">2023 →</span><span class="next-card__label">InnoVenture</span></span><span class="pass__go" aria-hidden="true">{{ICON:arrow}}</span></span></a>')
    out.append(f'''
<section class="section act-nav" data-header="light" aria-label="Unde a început totul">
  <div class="container next__grid">
    {''.join(nav)}
  </div>
</section>
''')
    out.append(TAIL)
    return ''.join(out)


# ---------------------------------------------------------------- overview page
def overview():
    rows = sending_rows()
    countries = {c for r in rows for c in [r['code']] if c} | {c for h in HOSTED for c in h['countries']} | {'RO'}
    out = [HEAD.format(title='Unde a început totul',
                       desc='De peste un deceniu, deschidem uși pentru tineri: către competențe noi, oameni noi și locuri noi.')]
    fan_pics = [('paper-handicraft-business', 3), ('many-ideas-one-word', 14), ('getting-to-know-each-other', 0)]
    fan = '<div class="fan act-fan" data-fan>' + ''.join(
        f'<figure class="fan__card fan__card--{c}">{aimg(f"archive/{s}/{photos(s)[n]}", "Fotografie din primele proiecte AIS", "(min-width: 62rem) 24vw, 56vw", "eager")}</figure>'
        for c, (s, n) in zip(('l', 'r', 'c'), fan_pics)) + '</div>'
    out.append(f'''
<section class="hero act-hero arch-hero section--ink" data-header="dark" aria-labelledby="page-title">
  <div class="container act-hero__grid">
    <div class="act-hero__copy">
      <nav class="crumbs mono" aria-label="Breadcrumb">
        <a href="index.html">Acasă</a><span aria-hidden="true">/</span><a href="projects.html">Proiecte</a><span aria-hidden="true">/</span><span aria-current="page">Unde a început totul</span>
      </nav>
      <div class="act-hero__code" aria-hidden="true"><span class="flap-board" data-flap-board>{{{{FLAP:2013}}}}</span></div>
      <h1 class="act-hero__title arch-hero__title" id="page-title">Unde a început totul</h1>
      <p class="lead act-hero__lead">De peste un deceniu, deschidem uși pentru tineri: către competențe noi, oameni noi și locuri noi.</p>
      <ul class="arch-stats">
        <li><p class="stat__value" aria-label="{len(HOSTED)}">{{{{DIGITS:{len(HOSTED)}}}}}</p><p class="mono">Proiecte ca organizație gazdă</p></li>
        <li><p class="stat__value" aria-label="{len(rows)}">{{{{DIGITS:{len(rows)}}}}}</p><p class="mono">Proiecte ca organizație de trimitere</p></li>
        <li><p class="stat__value" aria-label="{len(countries)}">{{{{DIGITS:{len(countries)}}}}}</p><p class="mono">Țări</p></li>
      </ul>
    </div>
    {fan}
  </div>
</section>
''')

    # hosted projects as boarding passes, grouped by programme
    def hcard(h, n):
        pp = photos(h['slug'])
        photo = aimg(f"archive/{h['slug']}/{pp[0]}", f"Fotografie din proiectul {h['title']}", '(min-width: 62rem) 24vw, (min-width: 48rem) 46vw, 92vw') if pp else '<span class="arch-card__ph" aria-hidden="true">{{ICON:plane}}</span>'
        codes = ''.join(f'<span class="tag">{c}</span>' for c in h['countries'])
        codes = f'<span class="tags">{codes}</span>' if codes else ''
        return (f'<li data-reveal style="--d:{(n % 3) * 0.06:.2f}s"><a class="bpass arch-card" href="arhiva-{h["slug"]}.html">'
                f'<span class="bpass__photo">{photo}<span class="pass__code mono">{h["year"]}</span></span>'
                f'<span class="pass__tear" aria-hidden="true"></span>'
                f'<span class="bpass__body"><span class="pass__row mono"><span>{esc(h["program"])}</span><span>{esc(h["place"].split(",")[0])}</span></span>'
                f'<span class="bpass__title">{esc(h["title"])}</span>'
                f'{codes}'
                f'<span class="bpass__foot"><span class="barcode" aria-hidden="true"></span><span class="pass__go" aria-hidden="true">{{{{ICON:arrow}}}}</span></span></span></a></li>')
    tia = [h for h in HOSTED if h['program'] != 'Erasmus+']
    era = [h for h in HOSTED if h['program'] == 'Erasmus+']
    out.append(f'''
<section class="section arch-hosted" data-header="light" aria-labelledby="gazda-title">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow mono" data-reveal><span class="eyebrow__num">{len(HOSTED)}</span>Mobilități de tineret</p>
      <h2 class="h2" id="gazda-title" data-reveal>Organizație gazdă</h2>
    </div>
    <p class="arch-group__intro mono" data-reveal>{esc(INTRO_TIA)}</p>
    <ul class="arch-cards">{''.join(hcard(h, n) for n, h in enumerate(tia))}</ul>
    <p class="arch-group__intro mono" data-reveal>{esc(INTRO_ERASMUS)}</p>
    <ul class="arch-cards">{''.join(hcard(h, n) for n, h in enumerate(era))}</ul>
  </div>
</section>
''')

    # sending projects: a filterable departures board
    order = ['Tineret în Acțiune', '2014', '2015', '2016', '2017', '2018', '2019', 'Erasmus+']
    groups = [g for g in order if any(r['group'] == g for r in rows)]
    filt = '<button type="button" class="is-active" data-filter="all" aria-pressed="true">Toate <span class="mono">' + str(len(rows)) + '</span></button>' + ''.join(
        f'<button type="button" data-filter="{esc(g)}" aria-pressed="false">{esc(g)} <span class="mono">{sum(r["group"] == g for r in rows)}</span></button>'
        for g in groups)
    lis = []
    for g in groups:
        for r in [r for r in rows if r['group'] == g]:
            place = ', '.join(x for x in (r['city'], r['country']) if x)
            meta = ' · '.join(x for x in (place, str(r['year']) if r['year'] else '', r['program'] if not r['year'] else '') if x)
            acts = ''
            if r['photos']:
                acts += f'<a class="sb-link" href="{esc(r["photos"], quote=True)}" target="_blank" rel="noopener noreferrer">Fotografii</a>'
            if r['card']:
                acts += f'<a class="sb-link sb-link--ghost" href="{esc(r["card"], quote=True)}" target="_blank" rel="noopener noreferrer">Project card</a>'
            lis.append(f'<li class="sb-row" data-group="{esc(g)}"><span class="dep__code mono">{r["code"] or "EU"}</span>'
                       f'<span class="sb-row__main"><span class="sb-row__name">{esc(r["name"])}</span><span class="sb-row__meta mono">{esc(meta)}</span></span>'
                       f'<span class="sb-row__acts">{acts}</span></li>')
    out.append(f'''
<section class="section section--ink arch-sending" data-header="dark" aria-labelledby="trimitere-title">
  <div class="container">
    <div class="section-head section-head--split">
      <div>
        <p class="eyebrow mono" data-reveal><span class="eyebrow__num">{len(rows)}</span>Mobilități de tineret</p>
        <h2 class="h2" id="trimitere-title" data-reveal>Organizație de trimitere</h2>
      </div>
      <div class="sb-filters" role="group" aria-label="Filtru" data-reveal>{filt}</div>
    </div>
    <div class="departures departures--big sendboard" data-sendboard>
      <div class="departures__head mono"><span>{{{{ICON:plane}}}}</span><span>RO → EU</span></div>
      <ul class="sb-rows">{''.join(lis)}</ul>
      <button class="btn btn--paper sb-more" type="button" data-sb-more>Vezi toate <span class="mono">{len(rows)}</span></button>
    </div>
  </div>
</section>
''')

    # strategic project
    partners = ''.join(f'<a class="tag arch-partner" href="{esc(u, quote=True)}" target="_blank" rel="noopener noreferrer">{esc(n)}</a>' for n, u in STRATEGIC['partners'])
    paras = ''.join(f'<p data-reveal>{esc(p)}</p>' for p in STRATEGIC['paras'])
    out.append(f'''
<section class="section section--paper2 arch-strategic" data-header="light" aria-labelledby="strategice-title">
  <div class="container arch-strategic__grid">
    <div>
      <p class="eyebrow mono" data-reveal><span class="eyebrow__num">2014</span>Strategice</p>
      <h2 class="h3 arch-strategic__title" id="strategice-title" data-reveal>Titlul proiectului: {esc(STRATEGIC["title"])}.</h2>
      <div class="tags arch-strategic__partners" data-reveal>{partners}</div>
      <p class="hero__actions" data-reveal>{ext_link(STRATEGIC["site"][0], STRATEGIC["site"][1], "btn btn--ink")}</p>
    </div>
    <div class="arch-strategic__text">{paras}</div>
  </div>
</section>
''')

    # other activities
    items = []
    for n, (t, album, video) in enumerate(OTHER):
        links = f'<a class="sb-link" href="{esc(album, quote=True)}" target="_blank" rel="noopener noreferrer">Albumul de poze</a>'
        if video:
            links += f'<a class="sb-link sb-link--ghost" href="{esc(video, quote=True)}" target="_blank" rel="noopener noreferrer">video</a>'
        items.append(f'<li class="other-ticket" data-reveal style="--d:{n * 0.05:.2f}s"><span class="other-ticket__num mono">{n + 1:02d}</span>'
                     f'<span class="other-ticket__title">{esc(t)}</span><span class="other-ticket__links">{links}</span></li>')
    out.append(f'''
<section class="section arch-other" data-header="light" aria-labelledby="alte-title">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow mono" data-reveal><span class="eyebrow__num">2013</span>AIS</p>
      <h2 class="h2" id="alte-title" data-reveal>Alte activități</h2>
    </div>
    <ul class="other-list">{''.join(items)}</ul>
  </div>
</section>
''')

    # where the story continues
    out.append('''
<section class="section section--tight-top act-nav" data-header="light" aria-label="Proiecte">
  <div class="container next__grid">
    <a class="next-card" href="projects.html" data-reveal><span class="next-card__photo">{{IMG:banners-user/projects-canva||(min-width: 48rem) 46vw, 92vw|lazy}}</span>
      <span class="next-card__foot"><span><span class="next-card__kicker mono">← Proiecte</span><span class="next-card__label">Înapoi</span></span><span class="pass__go pass__go--back" aria-hidden="true">{{ICON:left}}</span></span></a>
    <a class="next-card next-card--red" href="projects.html#innoventure" data-reveal style="--d:.08s"><span class="next-card__photo">{{IMG:ais/A1|Tineri participanți la o activitate Erasmus+, în fața unui castel|(min-width: 48rem) 46vw, 92vw|lazy}}</span>
      <span class="next-card__foot"><span><span class="next-card__kicker mono">2023 →</span><span class="next-card__label">InnoVenture</span></span><span class="pass__go" aria-hidden="true">{{ICON:arrow}}</span></span></a>
  </div>
</section>
''')
    out.append(TAIL)
    return ''.join(out)


PAGES = {OVERVIEW: overview, **{f'arhiva-{h["slug"]}': (lambda s=h['slug']: project(s)) for h in HOSTED}}
