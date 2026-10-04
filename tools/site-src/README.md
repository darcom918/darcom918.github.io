# Site source (Boarding Pass redesign)

The pages in `html/` (Romanian) and `html/en/` (English) are generated from these templates. Edit a template here, then rebuild:

    pip install pillow
    python tools/site-src/build.py              # all pages
    python tools/site-src/build.py index about  # only some pages

- `*.tpl.html` – one template per page (`about` → `about-us.html`, `boost` → `boost-your-future-skills.html`, `privacy` → `privacy-policy.html`)
- `activity.tpl.html` + `activities.py` – shared template and content for the activity pages
- `partial-header.html`, `partial-footer.html` – shared header/menu and footer
- Styles: `assets/css/ais.css` · Interactions: `assets/js/ais.js`

## Languages

Romanian is the default language and the templates are written in Romanian.
Every build also writes the English version of each page to `html/en/`, using
`translations_en.py` (`translate.py` does the work). The RO | EN button in the
header links each page to its other-language version.

- To change an English text, edit `translations_en.py` and rebuild.
- If you add or change Romanian text, add its English translation to
  `translations_en.py`. The build stops and lists any text that has no
  translation, so a page can never go out half in Romanian.

Small text edits can also be made directly in `html/*.html`, but they will be overwritten by the next rebuild.
