import re, os
from PIL import Image

SP = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(SP))  # the repository folder
import sys
# Template name -> page file name (without .html)
NAMES = {'about': 'about-us', 'boost': 'boost-your-future-skills', 'privacy': 'privacy-policy'}
ALL_PAGES = ['index', 'about', 'contact', 'projects', 'blog', 'privacy', 'boost',
             'youth-in-business', 'youth-on-the-labour-market', 'youthpreneurs', 'employability', 'ready4work', 'create-your-own-path', 'projects-detail', '404', 'apeluri-deschise']
PAGES = sys.argv[1:] or ALL_PAGES

ICONS = {
 'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
 'right': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 'left': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
 'up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
 'close': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 'plus': '<svg class="pillar__chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>',
 'plane': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg>',
 'copy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4.5A1.5 1.5 0 0 1 3 13.5v-9A1.5 1.5 0 0 1 4.5 3h9A1.5 1.5 0 0 1 15 4.5V5"/></svg>',
 'check': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>',
 'fb': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21z"/></svg>',
 'tt': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 3c.4 2.1 1.7 3.5 3.9 3.7v3c-1.5.1-2.9-.4-3.9-1.1v6.2c0 3.5-3.4 5.8-6.6 4.8-2.6-.8-4.1-3.6-3.2-6.2.8-2.2 3.1-3.5 5.4-3.1v3.1c-1-.3-2.2.2-2.6 1.2-.4 1.1.2 2.3 1.3 2.6 1.2.4 2.5-.5 2.6-1.8V3z"/></svg>',
 'ext': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>',
 'star': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2.8 2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></svg>',
 'starline': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" aria-hidden="true"><path d="m12 2.8 2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></svg>',
}


def img(path, alt, sizes, mode, cls=''):
    ext = next(e for e in ('.webp', '.jpg', '.png') if os.path.exists(os.path.join(ROOT, 'assets/images', path + e)))
    w, h = Image.open(os.path.join(ROOT, 'assets/images', path + ext)).size
    stem = os.path.basename(path)
    src = f'../assets/images/{path}{ext}'
    srcset = [f'../assets/images/opt/{stem}-{ow}.webp {ow}w' for ow in (480, 800)
              if os.path.exists(os.path.join(ROOT, 'assets/images/opt', f'{stem}-{ow}.webp'))]
    attrs = [f'src="{src}"']
    if srcset:
        srcset.append(f'{src} {w}w')
        attrs += [f'srcset="{", ".join(srcset)}"', f'sizes="{sizes}"']
    attrs += [f'alt="{alt}"', f'width="{w}" height="{h}"']
    if mode == 'lazy':
        attrs.append('loading="lazy"')
    if mode == 'high':
        attrs.append('fetchpriority="high"')
    attrs.append('decoding="async"')
    if cls:
        attrs.insert(0, f'class="{cls}"')
    return '<img ' + ' '.join(attrs) + '/>'


def flap(word):
    return '<span class="flap-word">' + ''.join(f'<span class="flap" data-char="{c}">{c}</span>' for c in word) + '</span>'


def digits(n):
    return ''.join(f'<span class="flap" data-digit="{c}" aria-hidden="true">{c}</span>' for c in n)


def pas(m):
    i, code, path, href, title, t1, t2, alt = m.split('|')
    return f'''      <div class="deck__slot" data-slot>
        <a class="pass" href="{href}" draggable="false">
          <span class="pass__photo">{img(path, alt, '(min-width: 62rem) 25rem, 92vw', 'eager' if i == '1' else 'lazy')}<span class="pass__code mono">{code}</span></span>
          <span class="pass__tear" aria-hidden="true"></span>
          <span class="pass__body">
            <span class="pass__row mono"><span>Erasmus+</span><span>RO → EU</span></span>
            <span class="pass__title">{title}</span>
            <span class="pass__foot"><span class="tags"><span class="tag">{t1}</span><span class="tag">{t2}</span></span><span class="pass__go" aria-hidden="true">{ICONS['arrow']}</span></span>
          </span>
        </a>
      </div>'''


def pillar(m):
    i, num, title, text = m.split('|')
    act = i == '0'
    return f'''<li class="pillar{' is-active' if act else ''}" data-reveal style="--d:{int(i) * 0.06:.2f}s">
            <h3><button type="button" aria-expanded="{'true' if act else 'false'}" aria-controls="pilon-{i}" data-index="{i}"><span class="mono">{num}</span>{title}{ICONS['plus']}</button></h3>
            <div class="pillar__panel" id="pilon-{i}" role="region"><div><p>{text}</p></div></div>
          </li>'''


def stop(m):
    label, title, href, path, alt, kind = m.split('|')
    media_cls = 'stop__media stop__media--logo' if kind == 'logo' else 'stop__media'
    return f'''<li class="stop">
        <span class="stop__dot" aria-hidden="true"></span>
        <div class="stop__text" data-reveal>
          <p class="stop__label mono">{label}</p>
          <h3 class="stop__title">{title}</h3>
        </div>
        <a class="{media_cls}" href="{href}" aria-label="{title}" data-reveal style="--d:.1s">{img(path, alt, '(min-width: 62rem) 40vw, 80vw', 'lazy')}<span class="stop__go" aria-hidden="true">{ICONS['arrow']}</span></a>
      </li>'''


def faq(m):
    i, q, a = m.split('|')
    return f'''<div class="faq-item" data-reveal>
        <h3><button type="button" aria-expanded="false" aria-controls="raspuns-{i}">{q}<span class="faq-icon" aria-hidden="true"></span></button></h3>
        <div class="faq-panel" id="raspuns-{i}" role="region"><div><p>{a}</p></div></div>
      </div>'''


def header(page):
    h = open(os.path.join(SP, 'partial-header.html'), encoding='utf-8').read()
    h = h.replace(' aria-current="page"', '')
    h = re.sub(r'(<a href="%s\.html")' % re.escape(page), lambda m: m.group(1) + ' aria-current="page"', h)
    if page != 'index':
        h = h.replace('href="#implica"', 'href="index.html#implica"')
    return h


# The EU emblem and disclaimer appear only on the project pages
EU_PAGES = {'projects', 'projects-detail', 'boost', 'youth-in-business', 'youth-on-the-labour-market', 'youthpreneurs', 'employability', 'ready4work', 'create-your-own-path'}


def footer(page):
    f = open(os.path.join(SP, 'partial-footer.html'), encoding='utf-8').read()
    if page not in EU_PAGES and not (page.startswith('arhiva-') or page == 'unde-a-inceput-totul'):
        f = re.sub(r'\n[ \t]*<div class="eu">.*?</p>\n[ \t]*</div>(?=\n)', '', f, count=1, flags=re.S)
    return f


def gate(m):
    num, title, text, d = m.split('|')
    return (f'<li class="gate" data-reveal style="--d:{d}s"><span class="gate__head"><span class="gate__num">{num}</span>'
            f'<span class="barcode" style="width:3.5rem" aria-hidden="true"></span></span>'
            f'<span><strong class="gate__title">{title}</strong> {text}</span></li>')


def member(d):
    return (f'<li class="member" data-reveal data-placeholder style="--d:{d}s">'
            f'<span class="member__photo"><span class="member__ph mono">Fotografie</span></span>'
            f'<span class="member__body"><span class="member__name">Nume</span>'
            f'<span class="member__role mono">Rol</span>'
            f'<span class="member__quote">„Frază personală”</span></span></li>')


def story(m):
    key, name, handle, href, photo, i = m.split('|')
    at = '' if key == 'fb' else '@'
    return f'''<a class="story story--{key}" href="{href}" rel="noopener noreferrer" target="_blank" aria-label="{name}: {at}{handle}" data-reveal style="--i:{i}; --d:{int(i) * 0.1:.1f}s">
        <span class="story__media">{img(photo, '', '(min-width: 62rem) 18rem, 72vw', 'lazy')}</span>
        <span class="story__bars" aria-hidden="true"><i></i><i></i><i></i></span>
        <span class="story__top" aria-hidden="true"><span class="story__avatar"><img src="../assets/images/logos/favicon.svg" alt="" width="64" height="64"/></span><span class="story__handle">{handle}</span><span class="story__icon">{ICONS[key]}</span></span>
        <span class="story__bottom"><span class="story__name">{name}</span><span class="story__at mono" aria-hidden="true">{at}{handle}</span><span class="story__cta">Urmărește-ne {ICONS['arrow']}</span></span>
      </a>'''


def dep(m):
    code, name, prog, href = m.split('|')
    inner = (f'<span class="dep__code mono">{code}</span>'
             f'<span class="dep__name" data-scramble>{name}</span>'
             f'<span class="dep__prog mono">{prog}</span>')
    if not href:
        return f'<li><div class="dep dep--static">{inner}<span class="dep__go" aria-hidden="true"></span></div></li>'
    return (f'<li><a class="dep" href="{href}" aria-label="{code} {name}">{inner}'
            f'<span class="dep__go" aria-hidden="true">{ICONS["arrow"]}</span></a></li>')


def card(m):
    i, code, title, t1, t2, meta, photo, alt, href = m.split('|')
    logo = ' bpass__photo--logo' if 'logo' in photo else ''
    body = f'''<span class="bpass__photo{logo}">{img(photo, alt, '(min-width: 62rem) 26rem, 92vw', 'lazy')}<span class="pass__code mono">{code}</span></span>
          <span class="pass__tear" aria-hidden="true"></span>
          <span class="bpass__body">
            <span class="pass__row mono"><span>{meta}</span><span>RO → EU</span></span>
            <span class="bpass__title">{title}</span>
            <span class="tags"><span class="tag">{t1}</span><span class="tag">{t2}</span></span>
            <span class="bpass__foot"><span class="barcode" aria-hidden="true"></span>{'<span class="pass__go" aria-hidden="true">' + ICONS['arrow'] + '</span>' if href else ''}</span>
          </span>'''
    if href:
        return f'<li class="bpass-item"><a class="bpass" href="{href}" style="--i:{i}">{body}</a></li>'
    return f'<li class="bpass-item"><div class="bpass bpass--static" style="--i:{i}">{body}</div></li>'


def act(m):
    code, en, ro, kws, desc, photo, alt, href, d = m.split('|')
    chips = ''.join(f'<span class="tag">{k.strip()}</span>' for k in kws.split('·'))
    logo = ' act__photo--logo' if 'logo' in photo else ''
    inner = f'''<span class="act__photo{logo}">{img(photo, alt, '(min-width: 62rem) 16rem, 92vw', 'lazy')}<span class="pass__code mono">{code}</span></span>
          <span class="act__tear" aria-hidden="true"></span>
          <span class="act__body">
            <span class="act__ro mono">{ro}</span>
            <span class="act__title">{en}</span>
            <span class="tags">{chips}</span>
            <span class="act__desc">{desc}</span>
          </span>'''
    if href:
        inner += f'<span class="pass__go act__go" aria-hidden="true">{ICONS["arrow"]}</span>'
        return f'<li data-reveal style="--d:{d}s"><a class="act" href="{href}">{inner}</a></li>'
    return f'<li data-reveal style="--d:{d}s"><div class="act act--static">{inner}</div></li>'


from html import escape as _esc
from activities import ACTIVITIES, P_STATS
from translate import to_english


def lang_switch(name, lang):
    """RO | EN switch in the header. Romanian pages live in html/, English ones in html/en/."""
    if lang == 'ro':
        href, target, label = f'en/{name}.html', 'en', 'English version'
    else:
        href, target, label = f'../{name}.html', 'ro', 'Versiunea în limba română'
    ro = '<span class="lang-switch__opt' + (' is-current' if lang == 'ro' else '') + '">RO</span>'
    en = '<span class="lang-switch__opt' + (' is-current' if lang == 'en' else '') + '">EN</span>'
    return (f'<a class="lang-switch" href="{href}" hreflang="{target}" lang="{target}" aria-label="{label}">'
            f'{ro}{en}</a>')


def photo_path(ph):
    return ph if '/' in ph else 'ais/projects/' + ph


def activity_source(page):
    d = ACTIVITIES[page]
    out = open(os.path.join(SP, 'activity.tpl.html'), encoding='utf-8').read()
    photos = d['photos']
    v = dict(d, count=str(len(photos)))
    out = re.sub(r'\{\{V:(\w+)\}\}', lambda m: _esc(str(v[m.group(1)]), quote=True), out)
    drive_btn = ''
    if d.get('drive') and d.get('drive') != d.get('results'):
        drive_btn = f'<a class="btn btn--ghost" href="{d["drive"]}" target="_blank" rel="noopener noreferrer">Vezi resursele și fotografiile</a>'
    out = out.replace('{{DRIVEBTN}}', drive_btn)
    out = re.sub(r'\s*<div class="status-row"><dt class="mono">[^<]+</dt><dd></dd></div>', '', out)
    out = out.replace('{{KWS}}', ''.join(f'<span class="tag">{_esc(k)}</span>' for k in d['kws']))
    fan = []
    for cls, ph in zip(('l', 'r', 'c'), d['fan']):
        alt = dict(photos).get(ph, '')
        fan.append(f'<figure class="fan__card fan__card--{cls}">{{{{IMG:{photo_path(ph)}|{alt}|(min-width: 62rem) 24vw, 56vw|eager}}}}</figure>')
    out = out.replace('{{FAN}}', ''.join(fan))
    desc = [f'<p class="scrub" data-scrub>{_esc(d["desc"][0])}</p>'] + [f'<p class="lead" data-reveal>{_esc(p)}</p>' for p in d['desc'][1:]]
    out = out.replace('{{DESC}}', '\n      '.join(desc))
    gal = []
    for i, (ph, alt) in enumerate(photos):
        path = photo_path(ph)
        ext = next(e for e in ('.jpg', '.webp', '.png') if os.path.exists(os.path.join(ROOT, 'assets/images', path + e)))
        gal.append(f'<li data-reveal style="--d:{(i % 6) * 0.05:.2f}s"><button class="gal__item" type="button" data-gal="{i}" '
                   f'data-full="../assets/images/{path}{ext}" aria-label="{_esc(alt, quote=True)}">'
                   f'{{{{IMG:{path}|{alt}|(min-width: 62rem) 22vw, 46vw|lazy}}}}</button></li>')
    out = out.replace('{{GALLERY}}', '\n      '.join(gal))
    impact = ''
    if d.get('stats') or d.get('extra'):
        stats = ''
        if d.get('stats'):
            stats = '''<ul class="act-stats">
        <li data-reveal><p class="stat__value" aria-label="49">{{DIGITS:49}}</p><p class="mono">evenimente și sesiuni de informare</p></li>
        <li data-reveal style="--d:.08s"><p class="stat__value" aria-label="952">{{DIGITS:952}}</p><p class="mono">participanți</p></li>
        <li data-reveal style="--d:.16s"><p class="stat__value" aria-label="150+">{{DIGITS:150}}<span class="stat__plus" aria-hidden="true">+</span></p><p class="mono">tineri informați suplimentar</p></li>
      </ul>
      <p class="lead act-impact__lead" data-reveal>''' + _esc(P_STATS) + '</p>'
        extra = ''.join(f'<p data-reveal>{_esc(p)}</p>' for p in d.get('extra', []))
        impact = f'''<!-- ============ Impact ============ -->
<section class="section section--ink act-impact" data-header="dark" aria-labelledby="impact-title">
  <div class="container">
    <p class="eyebrow mono" data-reveal><span class="eyebrow__num">AIS</span>Acreditarea Erasmus+</p>
    <h2 class="h2" id="impact-title" data-reveal>Impact</h2>
    {stats}
    <div class="act-impact__cols">{extra}</div>
  </div>
</section>'''
    out = out.replace('{{IMPACT}}', impact)
    results = ''
    if d.get('results'):
        results = (f'<p class="gallery-cta" data-reveal><a class="btn btn--ink gallery-cta__btn" href="{d["results"]}" target="_blank" rel="noopener noreferrer">'
                   'See All Results and Photos {{ICON:ext}}</a></p>')
    out = out.replace('{{RESULTS}}', results)
    out = out.replace('{{LOREM}}', LOREM if d.get('lorem') else '')
    nav = []
    if d.get('prev'):
        href, code, name, ph = d['prev']
        nav.append(f'<a class="next-card" href="{href}" data-reveal><span class="next-card__photo">{{{{IMG:{ph}||(min-width: 48rem) 46vw, 92vw|lazy}}}}</span>'
                   f'<span class="next-card__foot"><span><span class="next-card__kicker mono">← {code}</span><span class="next-card__label">{_esc(name)}</span></span><span class="pass__go pass__go--back" aria-hidden="true">{{{{ICON:left}}}}</span></span></a>')
    else:
        nav.append('<a class="next-card" href="projects.html" data-reveal><span class="next-card__photo">{{IMG:banners-user/projects-canva||(min-width: 48rem) 46vw, 92vw|lazy}}</span>'
                   '<span class="next-card__foot"><span><span class="next-card__kicker mono">← Proiecte</span><span class="next-card__label">Înapoi</span></span><span class="pass__go pass__go--back" aria-hidden="true">{{ICON:left}}</span></span></a>')
    if d.get('next'):
        href, code, name, ph = d['next']
        nav.append(f'<a class="next-card next-card--red" href="{href}" data-reveal style="--d:.08s"><span class="next-card__photo">{{{{IMG:{ph}||(min-width: 48rem) 46vw, 92vw|lazy}}}}</span>'
                   f'<span class="next-card__foot"><span><span class="next-card__kicker mono">{code} →</span><span class="next-card__label">{_esc(name)}</span></span><span class="pass__go" aria-hidden="true">{{{{ICON:arrow}}}}</span></span></a>')
    out = out.replace('{{NAV}}', '\n    '.join(nav))
    return out


# Placeholder long-form text (to be replaced with the real story of the activity)
LOREM = '''<!-- ============ Story (placeholder text: replace the lorem ipsum with the real story) ============ -->
<section class="section story-text" data-header="light" aria-labelledby="poveste-title">
  <div class="container story-text__wrap">
    <p class="eyebrow mono" data-reveal><span class="eyebrow__num">Lorem</span>Ipsum</p>
    <h2 class="h2" id="poveste-title" data-reveal>Lorem ipsum dolor sit amet</h2>
    <div class="story-text__body">
      <p class="story-text__intro" data-reveal>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer posuere erat a ante venenatis dapibus, posuere velit aliquet. Curabitur blandit tempus porttitor, sed posuere consectetur est at lobortis.</p>
      <p data-reveal>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt.</p>
      <p data-reveal>Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur.</p>
      <h3 class="story-text__sub" data-reveal>Donec sed odio dui</h3>
      <p data-reveal>Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur. At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident.</p>
      <blockquote class="story-text__quote" data-reveal><p>„Maecenas faucibus mollis interdum. Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor.”</p><cite class="mono">Lorem Ipsum</cite></blockquote>
      <p data-reveal>Similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.</p>
      <h3 class="story-text__sub" data-reveal>Cras mattis consectetur purus</h3>
      <p data-reveal>Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.</p>
      <p data-reveal>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean lacinia bibendum nulla sed consectetur. Vestibulum id ligula porta felis euismod semper, etiam porta sem malesuada magna mollis euismod.</p>
    </div>
  </div>
</section>'''


def render(page):
    import archive_build
    if page in archive_build.PAGES:
        out = archive_build.PAGES[page]()
    elif page in ACTIVITIES:
        out = activity_source(page)
    else:
        out = open(os.path.join(SP, page + '.tpl.html'), encoding='utf-8').read()
    out = re.sub(r'\{\{HEADER:(\w[\w-]*)\}\}', lambda m: header(m.group(1)), out)
    out = out.replace('{{FOOTER}}', footer(page))
    if '{{CALLS_CSV}}' in out:
        import apeluri_config
        out = out.replace('{{CALLS_CSV}}', _esc(apeluri_config.CSV_URL, quote=True)).replace('{{CALLS_FORM}}', _esc(apeluri_config.FORM_URL, quote=True))
    out = re.sub(r'\{\{ICON:(\w+)\}\}', lambda m: ICONS[m.group(1)], out)
    out = re.sub(r'\{\{FLAP:([^}]+)\}\}', lambda m: flap(m.group(1)), out)
    out = re.sub(r'\{\{DIGITS:([^}]+)\}\}', lambda m: digits(m.group(1)), out)
    out = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: img(*m.group(1).split('|')), out)
    out = re.sub(r'\{\{IMGC:([^}]+)\}\}', lambda m: img(*m.group(1).split('|')), out)
    out = re.sub(r'\{\{PASS:([^}]+)\}\}', lambda m: pas(m.group(1)), out)
    out = re.sub(r'\{\{PILLAR:([^}]+)\}\}', lambda m: pillar(m.group(1)), out)
    out = re.sub(r'\{\{STOP:([^}]+)\}\}', lambda m: stop(m.group(1)), out)
    out = re.sub(r'\{\{STORY:([^}]+)\}\}', lambda m: story(m.group(1)), out)
    out = re.sub(r'\{\{DEP:([^}]+)\}\}', lambda m: dep(m.group(1)), out)
    out = re.sub(r'\{\{CARD:([^}]+)\}\}', lambda m: card(m.group(1)), out)
    out = re.sub(r'\{\{ACT:([^}]+)\}\}', lambda m: act(m.group(1)), out)
    out = re.sub(r'\{\{GATE:([^}]+)\}\}', lambda m: gate(m.group(1)), out)
    out = re.sub(r'\{\{MEMBER:([^}]+)\}\}', lambda m: member(m.group(1)), out)
    out = re.sub(r'\{\{FAQ:([^}]+)\}\}', lambda m: faq(m.group(1)), out)
    if '{{MAPRO}}' in out:
        mp = open(os.path.join(SP, 'map-svg.txt'), encoding='utf-8').read().split('\n')
        keep = [l for l in mp if l.startswith('<path class="map-land"') or l.startswith('<path class="map-country')]
        out = out.replace('{{MAPRO}}', '\n'.join('        ' + l for l in keep))
    if '{{MAPVD}}' in out:
        mp = open(os.path.join(SP, 'map-svg-vd.txt'), encoding='utf-8').read()
        out = out.replace('{{MAPVD}}', '\n'.join('        ' + l for l in mp.split('\n')))
    if '{{MAP}}' in out:
        mp = open(os.path.join(SP, 'map-svg.txt'), encoding='utf-8').read()
        out = out.replace('{{MAP}}', '\n'.join('        ' + l for l in mp.split('\n')))
    name = NAMES.get(page, page)
    out = out.replace('{{LANG}}', lang_switch(name, 'ro'))
    left = re.findall(r'\{\{[^}]*\}\}', out)
    assert not left, left[:3]
    open(os.path.join(ROOT, 'html', name + '.html'), 'w', encoding='utf-8', newline='\n').write(out)
    # English version: same page, translated with translations_en.py
    en = to_english(out, lang_switch(name, 'ro'), lang_switch(name, 'en'))
    # Pages without an English version (e.g. projects-detail.html) open in Romanian instead of a dead link
    built = {NAMES.get(p, p) for p in ALL_PAGES} | set(archive_build.PAGES)
    en = re.sub(r'href="([\w-]+)\.html', lambda m: m.group(0) if m.group(1) in built else f'href="../{m.group(1)}.html', en)
    os.makedirs(os.path.join(ROOT, 'html', 'en'), exist_ok=True)
    open(os.path.join(ROOT, 'html', 'en', name + '.html'), 'w', encoding='utf-8', newline='\n').write(en)
    print('ok', name, len(out) // 1024, 'KB', '+ en')
    if page == '404':  # GitHub Pages shows /404.html for any missing address, so it needs root-absolute links
        root = re.sub(r'(href|src)="(?!https?:|#|/|\.\./)([^"]+)"', r'\1="/html/\2"', out).replace('../assets/', '/assets/')
        open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8', newline='\n').write(root)


# Old page names (from the original website template) -> current names.
# A small page under each old name forwards visitors, so links shared before the rename keep working.
REDIRECTS = {
    'ecoart': 'youth-in-business',
    'fashionforward': 'youth-on-the-labour-market',
    'followyourdrums': 'youthpreneurs',
    'aiart2-blog': 'employability',
    'eye2025': 'ready4work',
    'firstaid-blog': 'create-your-own-path',
    'razemprzeciwuzaleznieniom': 'boost-your-future-skills',
}


def write_redirects():
    for old, new in REDIRECTS.items():
        page = (f'<!DOCTYPE html>\n<html lang="ro">\n<head>\n<meta charset="utf-8"/>\n'
                f'<title>Asociația Inițiative Sociale</title>\n<meta name="robots" content="noindex"/>\n'
                f'<link rel="canonical" href="{new}.html"/>\n<meta http-equiv="refresh" content="0; url={new}.html"/>\n'
                f'<script>location.replace("{new}.html" + location.hash)</script>\n</head>\n<body>\n'
                f'<p><a href="{new}.html">Pagina s-a mutat aici. / This page has moved here.</a></p>\n</body>\n</html>\n')
        open(os.path.join(ROOT, 'html', old + '.html'), 'w', encoding='utf-8', newline='\n').write(page)


import archive_build
if PAGES == ['archive']:
    PAGES = list(archive_build.PAGES)
elif not sys.argv[1:]:
    PAGES = ALL_PAGES + list(archive_build.PAGES)
for p in PAGES:
    render(p)
write_redirects()
