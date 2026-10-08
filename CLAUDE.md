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
Pages in `html/` (Romanian) and `html/en/` (English) are **generated** — edit the sources in `tools/site-src/`, then rebuild:
```
pip install pillow
python tools/site-src/build.py            # all pages (RO + EN, plus the archive pages)
python tools/site-src/build.py contact    # only some pages
python tools/site-src/build.py archive    # only "Unde a început totul" + arhiva-*.html
```
- `*.tpl.html` — one template per page (`about`→`about-us.html`, `boost`→`boost-your-future-skills.html`, `privacy`→`privacy-policy.html`, `blog`→`blog.html`)
- `partial-header.html` / `partial-footer.html` — shared header + hamburger menu (with RO | EN switch) / footer
- `activity.tpl.html` + `activities.py` — activity pages: youth-in-business, youth-on-the-labour-market, youthpreneurs, employability, ready4work, create-your-own-path (old file names like ecoart.html are redirect pages)
- `translations_en.py` + `translate.py` — English version. **Any new Romanian text needs an English entry in `translations_en.py`, or the build stops and lists it.**
- `archive.py` + `archive_build.py` + `archive/*.json` — "Unde a început totul" + 10 old hosted-project pages (Romanian only; text crawled verbatim from old site initiative-sociale.ro, photos in `assets/images/archive/`)
- `map-svg*.txt` — baked dot-matrix Europe map
- Preview: `python -m http.server 8766` in the repo root → http://localhost:8766/html/index.html
- This repo is GitHub Pages (`darcom918.github.io`): **whatever is on `main` is the live site** — work on a branch and open a pull request.

## Status (done)
- Home, About (owner's new text), Contact (email boarding pass, story cards for FB/IG/TikTok, registered office "Sediul social" with Romania map), Projects (departures board + sticky flight route + programme chapters + "2013 → Unde a început totul" teaser), Noutăți, privacy policy, BOOST coming-soon page, 6 activity pages (Impact + story sections are lorem ipsum placeholders on purpose), English version of all of these, "Unde a început totul" + 10 `arhiva-*.html` pages.
- Footer title: "Descoperă Erasmus+". Hamburger menu includes "Unde a început totul". EU emblem + disclaimer only on project pages.

## Still to do / open questions
- Not redesigned yet: `projects-detail.html`, `404.html`. Archive pages have no English version yet.
- A5 "Rural Youth in Action" has no page and no photos.
- Team section on About has placeholders (needs photos, names, roles, quotes).
- Partner-country map only shows RO/PL/HU/BG; photos suggest more (IT, ES, TR, GR, RS…) — ask owner.
- Archive text: diacritics added (2026-10-08, owner approved); wording unchanged, old typos kept.
- Lorem ipsum placeholders on activity pages to be replaced with real text.
