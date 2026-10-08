"""
Bakes the dot-matrix Europe map: map-svg.txt (home page, routes start in the centre of Romania)
and map-svg-vd.txt (About page, routes start in Vatra Dornei). The contact page reuses the land
and country dots of map-svg.txt for its Romania map.

Partner countries = every country from AIS projects (archive hosted + sending projects, plus
Hungary from the accreditation activities). Edit PARTNERS to change them.

Needs Natural Earth 1:110m countries (bundled in the geopandas 0.14 wheel) and pyshp + shapely:
    pip download geopandas==0.14.4 --no-deps -d /tmp/geo   # then unzip geopandas/datasets/naturalearth_lowres/
    pip install pyshp shapely
    python map_make.py /tmp/geo/geopandas/datasets/naturalearth_lowres/naturalearth_lowres.shp
"""
import math, os, sys
import shapefile
from shapely.geometry import shape, Point
from shapely.prepared import prep

HERE = os.path.dirname(os.path.abspath(__file__))

# Mercator, fitted to the original map so existing viewBoxes keep framing the same area
SX, X0, SY, Y0 = 16.006, 189.41, 13.64, 1268.92
ROW0, ROW_STEP, ROWS, COL_STEP = 111.0, 11.08, 63, 12.8


def xy(lon, lat):
    v = math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
    return X0 + SX * lon, Y0 - SY * v


def lonlat(x, y):
    v = (Y0 - y) / SY
    return (x - X0) / SX, math.degrees(2 * math.atan(math.exp(math.radians(v))) - math.pi / 2)


# code: (Natural Earth name, pin lon, pin lat)
PARTNERS = {
    'ro': ('Romania', 24.97, 45.9),
    'pt': ('Portugal', -8.1, 39.7),
    'es': ('Spain', -3.7, 40.2),
    'no': ('Norway', 9.5, 61.0),
    'de': ('Germany', 10.4, 51.1),
    'it': ('Italy', 12.6, 42.8),
    'hr': ('Croatia', 16.0, 45.6),
    'pl': ('Poland', 19.4, 52.1),
    'sk': ('Slovakia', 19.6, 48.8),
    'hu': ('Hungary', 19.2, 47.2),
    'mk': ('North Macedonia', 21.7, 41.6),
    'el': ('Greece', 22.0, 39.4),
    'lt': ('Lithuania', 23.9, 55.3),
    'lv': ('Latvia', 25.0, 56.9),
    'bg': ('Bulgaria', 25.2, 42.7),
    'cy': ('Cyprus', 33.1, 35.0),
    'tr': ('Turkey', 34.5, 39.2),
}
ORIGINS = {'map-svg.txt': ((24.97, 45.9), 'RO'), 'map-svg-vd.txt': ((25.35, 47.35), 'VATRA DORNEI')}


def main(shp):
    r = shapefile.Reader(shp)
    geo = {rec['name']: shape(s.__geo_interface__) for s, rec in zip(r.shapes(), r.records())}
    land = [prep(g) for g in geo.values()]
    countries = {c: prep(geo[n]) for c, (n, _, _) in PARTNERS.items()}
    dots_land, dots = [], {c: [] for c in PARTNERS}
    for i in range(ROWS):
        y = round(ROW0 + i * ROW_STEP)
        k = 0
        while True:
            x = round(i % 2 * COL_STEP / 2 + k * COL_STEP)
            k += 1
            if x > 960:
                break
            lon, lat = lonlat(x, y)
            p = Point(lon, lat)
            owner = next((c for c, g in countries.items() if g.contains(p)), None)
            if owner:
                dots[owner].append((x, y))
            elif any(g.contains(p) for g in land):
                dots_land.append((x, y))
    # a country too small to catch a grid point still gets one dot at its pin
    for c, (_, lon, lat) in PARTNERS.items():
        if not dots[c]:
            x, y = xy(lon, lat)
            dots[c].append((round(x), round(y)))

    def path(ps):
        return ''.join(f'M{x} {y}h0' for x, y in ps)

    for fname, ((olon, olat), olabel) in ORIGINS.items():
        ox, oy = (round(v) for v in xy(olon, olat))
        out = [f'<path class="map-land" d="{path(dots_land)}"/>']
        out += [f'<path class="map-country map-country--{c}" data-country="{c}" d="{path(ps)}"/>' for c, ps in dots.items()]
        pins = {c: tuple(round(v) for v in xy(lon, lat)) for c, (_, lon, lat) in PARTNERS.items()}
        # routes, nearest first, each bowed to one side
        for c in sorted((c for c in PARTNERS if c != 'ro'), key=lambda c: math.dist(pins[c], (ox, oy))):
            tx, ty = pins[c]
            mx, my = (ox + tx) / 2, (oy + ty) / 2
            dx, dy = tx - ox, ty - oy
            bend = 0.18
            cx, cy = round(mx - dy * bend), round(my + dx * bend)
            out.append(f'<path class="map-route" data-country="{c}" pathLength="1" d="M{ox} {oy}Q{cx} {cy} {tx} {ty}"/>')
        out.append(f'<circle class="map-pulse" cx="{ox}" cy="{oy}" r="10"/>')
        out.append(f'<g class="map-pin map-pin--ro" data-country="ro" transform="translate({ox} {oy})"><circle class="map-pin-hit" r="34"/><circle class="map-pin-dot" r="7"/><text class="map-pin-label" y="-16">{olabel}</text></g>')
        for c in PARTNERS:
            if c == 'ro':
                continue
            x, y = pins[c]
            out.append(f'<g class="map-pin map-pin--{c}" data-country="{c}" transform="translate({x} {y})"><circle class="map-pin-hit" r="22"/><circle class="map-pin-dot" r="6"/><text class="map-pin-label" y="-13">{c.upper()}</text></g>')
        open(os.path.join(HERE, fname), 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
        print('ok', fname, {c: len(v) for c, v in dots.items()})


if __name__ == '__main__':
    main(sys.argv[1])
