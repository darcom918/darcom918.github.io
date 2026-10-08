# AIS website redesign — project brief for Claude

Website of **Asociația Inițiative Sociale (AIS)**, a youth NGO in Romania (Erasmus+ accredited, activities in Vatra Dornei, registered office in Constanța). Site language: **Romanian**. The owner also uses this site as a portfolio piece, so the bar is "wow".

## Design: "Boarding Pass" concept
- Travel/airport metaphor: departure-board split-flap tiles, boarding-pass cards with perforations, flight routes, stamps of years/codes.
- Colors: ink navy `#0E1530`, cream `#F6F1E7`, brand red `#ED1C24` (use `#D7141C` for text on red / buttons), sun yellow `#FFC93C` (small doses).
- Fonts: **Archivo** (variable width, headings) + **JetBrains Mono** (labels). Both support ș ț ă â î.
- Apple-style motion: interruptible springs, momentum, frosted-glass header, reduced-motion fallbacks. Use the `apple-design` skill (copied into `.claude/skills/apple-design`).
- No framework. One stylesheet `assets/css/ais.css`, one script `assets/js/ais.js` (custom Spring class, flap boards, deck, lightbox, map, filters…).

## STRICT RULES from the owner
1. Keep the owner's text **word for word**. Never rewrite/translate/delete wording without asking. New microcopy must be listed for approval.
2. Never recolor, crop or distort the **EU "Co-funded by the European Union" emblem** (`assets/images/co-funded-black.png`); it lives in the footer on a white plate with the disclaimer.
3. Keep all images, pages and links working. `backup-original/` = pristine original site — never modify it.
4. Mobile-first; respect reduced motion; good contrast; alt text on every image.
5. Activity photos must never be mixed between projects.

## How pages are built (IMPORTANT)
Pages in `html/` are **generated** — edit the sources in `tools/site-src/`, then rebuild:
```
cd tools/site-src
python build.py index about contact projects boost ecoart fashionforward followyourdrums aiart2-blog eye2025 firstaid-blog
python build.py archive
```
- `*.tpl.html` — one template per page (`about`→`about-us.html`, `boost`→`razemprzeciwuzaleznieniom.html`)
- `partial-header.html` / `partial-footer.html` — shared header + hamburger menu / footer
- `activity.tpl.html` + `activities.py` — the 6 accreditation activity pages (A1–A7)
- `archive.py` + `archive_build.py` + `archive/*.json` — "Unde a început totul" + 10 old hosted-project pages
- `map-svg*.txt` — baked dot-matrix Europe map
- Requires Python 3 + Pillow. Preview: `python -m http.server 8766` in the project root → http://localhost:8766/html/index.html
- Image copies for phones: `python tools/optimize-images.py`

## Status (done)
- Home (`index.html`), About (`about-us.html`, owner's new text), Contact (email boarding pass, story cards for FB/IG/TikTok, registered office with Romania map), Projects (`projects.html`: departures board + sticky flight route + programme chapters), BOOST coming-soon page, 6 activity pages (Impact + story sections are lorem ipsum placeholders on purpose), "Unde a început totul" (`unde-a-inceput-totul.html`) + 10 `arhiva-*.html` pages (text crawled from old site initiative-sociale.ro, kept verbatim without diacritics; photos from project blogs in `assets/images/archive/`).
- Footer title: "Descoperă Erasmus+". Hamburger menu includes "Unde a început totul".

## Still to do / open questions
- Not redesigned yet: `blog.html` (Noutăți), `projects-detail.html`, `privacy-policy.html`, `404.html`.
- A5 "Rural Youth in Action" has no page and no photos.
- Team section on About has placeholders (needs photos, names, roles, quotes).
- Partner-country map only shows RO/PL/HU/BG; photos suggest more (IT, ES, TR, GR, RS…) — ask owner.
- Owner may want diacritics added to the old archive text (ask first).
- No git repo yet; owner wants GitHub + a pull request (main = original from `backup-original/`, branch = redesign).
- Lorem ipsum placeholders on activity pages to be replaced with real text.
