---
name: ais-redesign-project
description: "AIS youth-NGO site redesign (\"Boarding Pass\" concept) — rules, approvals, status, and where things live"
metadata:
  node_type: memory
  type: project
  originSessionId: 7b4055f8-d294-4ada-8090-2a21308f26cc
  modified: 2026-10-08T15:01:55.251Z
---

Redesign of the Asociația Inițiative Sociale (Romania, Erasmus+ youth) static site. The user also uses it as a portfolio piece to sell web work to other NGOs, so "wow" factor matters.

- Chosen concept (2026-10-04): **A "Boarding Pass"** — ink navy #0E1530, cream #F6F1E7, red #ED1C24 (#D7141C for text-on-red), sun #FFC93C; Archivo (variable wdth) + JetBrains Mono; no framework, custom spring JS. Files: html/index.html, assets/css/ais.css, assets/js/ais.js, tools/optimize-images.py (writes assets/images/opt/).
- Homepage approved 2026-10-04 ("I like it"). about-us.html rebuilt around the user's NEW about text (2026-10-04, "Aici ideile prind curaj." …): scroll-lit text, values that light up, Vatra Dornei map origin, team grid with placeholders awaiting real profiles; kept stat tickets + grow photo. AIS is based in Vatra Dornei (Bucovina), active 10+ years. contact.html done 2026-10-04 (email as hero boarding pass with send/copy micro-interactions; FB/IG/TikTok as story cards — user rejected the passport-stamp idea; copy button is icon-only). projects.html rebuilt 2026-10-04 around user's new text: programmes InnoVenture (A1 You(th) in Business, A2 You(th) on the Labour Market), NextGEN (A3 YouthPreneurs, A4 EmployAbility), LevelUP (A5 Rural Youth in Action — no detail page, A6 Ready4Work, A7 Create Your Own Path), BOOST: Your Future Skills (în curând); each has a blogspot blog. Departures-board hero + sticky route bar + chapters. BOOST page (razemprzeciwuzaleznieniom.html) redesigned 2026-10-04 as "coming soon + take part now" — title must stay in English "BOOST: Your Future Skills"; the 15 placeholder logos and past-tense copy-paste paragraphs were removed. Activity pages use tools/site-src/activity.tpl.html + activities.py (ecoart.html/A1 done 2026-10-04: hero, status board, bento gallery + swipe lightbox, impact stats, prev/next; user then removed the number tiles, added lorem-ipsum story section + "See All Results and Photos" Drive button). Later (same day) all activity pages were done the same way: fashionforward A2, followyourdrums A3, aiart2-blog A4 (+ais/A4, ais/A4_2 since only 1 photo), eye2025 A6, firstaid-blog A7 — each uses ONLY its own original photos (verified); Impact = lorem ipsum; results button = page's own Drive link (A4, A6 have none). A5 Rural Youth in Action has no page/photos. Build: `python tools/site-src/build.py <pages>` — templates live in tools/site-src/, html/ is generated. Photos show flags of PL, IT, ES, TR, GR — partner list on the map (RO/PL/HU/BG) may be incomplete. Archive (2026-10-08): "Unde a început totul" = html/unde-a-inceput-totul.html + 10 hosted-project pages html/arhiva-<slug>.html, built by tools/site-src/archive.py + archive_build.py (`build.py archive`); text crawled verbatim from old site initiative-sociale.ro (diacritics added 2026-10-08 with owner approval; wording and old typos unchanged), photos from project blogs in assets/images/archive/; 62 sending projects as filterable board. Footer title changed by user to "Descoperă Erasmus+" on all pages. Remaining pages (about, projects, blog, contact, 7 activity pages) still on the old Bootstrap template — to be redesigned after homepage approval. User wants separate project pages later; file names stay as they are.
- `backup-original/` holds the pristine original (made 2026-10-03). Don't overwrite it.
- Partner countries for the map: Romania (home), Poland, Hungary, Bulgaria — no per-activity country mapping given.
- Approved new copy: "Cum te poți implica" join section (4 steps), EU disclaimer mentioning ANPCDEFP, email is initiative.sociale@gmail.com (owner, 2026-10-08), 404 "Ups! Pagina nu a fost găsită".

2026-10-08 (later): projects-detail.html + 404 redesigned (templates in tools/site-src; root /404.html for GitHub Pages); archive got diacritics (owner said yes) and English versions (html/en/arhiva-*.html, unde-a-inceput-totul.html). Work branch: redesign-boarding-pass.

Workflow (owner, 2026-10-09): "push" = git push to redesign-boarding-pass only. Never create or merge PRs unless the owner specifically asks for a merge in that message (2026-10-09: "stop merging unless I specifically ask").

**Why:** user's rule — keep all existing text verbatim; ask before changing wording; keep images/pages/links working; EU emblem untouched.
**How to apply:** never rewrite their text; list any new microcopy for approval; reuse ais.css/ais.js when converting the remaining pages.
