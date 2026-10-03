# Site source (Boarding Pass redesign)

The pages in `html/` are generated from these templates. Edit a template here, then rebuild:

    python tools/site-src/build.py index about contact projects boost ecoart

- `*.tpl.html` – one template per page (`about` → `about-us.html`, `boost` → `razemprzeciwuzaleznieniom.html`)
- `activity.tpl.html` + `activities.py` – shared template and content for the activity pages
- `partial-header.html`, `partial-footer.html` – shared header/menu and footer
- Styles: `assets/css/ais.css` · Interactions: `assets/js/ais.js`

Small text edits can also be made directly in `html/*.html`, but they will be overwritten by the next rebuild.
