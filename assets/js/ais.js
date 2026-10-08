/* =====================================================================
   AIS · "Boarding Pass" interactions
   No dependencies. Motion follows Apple's fluid-interface principles:
   springs that start from the current value, inherit gesture velocity,
   project momentum, and can be grabbed at any moment.
   ===================================================================== */
(() => {
  'use strict';
  window.AIS_READY = true;

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const motionQuery = matchMedia('(prefers-reduced-motion: reduce)');
  const reduced = () => motionQuery.matches;
  const desktop = matchMedia('(min-width: 62rem)');

  /* Interface text: Romanian by default, English on the pages in html/en/ */
  const T = document.documentElement.lang === 'en'
    ? { copied: 'Copied!', close: 'Close', prev: 'Previous', next: 'Next',
        countries: { ro: 'Romania', pl: 'Poland', hu: 'Hungary', bg: 'Bulgaria' } }
    : { copied: 'Copiat!', close: 'Închide', prev: 'Înapoi', next: 'Înainte',
        countries: { ro: 'România', pl: 'Polonia', hu: 'Ungaria', bg: 'Bulgaria' } };

  /* ---------- Spring ----------
     Designer parameters, as in UIKit/SwiftUI:
     response = time to (roughly) reach the target, in seconds
     damping  = 1 → no overshoot, < 1 → bounce                       */
  class Spring {
    constructor(value = 0, { response = 0.4, damping = 1, precision = 0.25 } = {}) {
      this.value = value;
      this.target = value;
      this.velocity = 0;
      this.precision = precision;
      this.raf = 0;
      this.onUpdate = null;
      this.onRest = null;
      this.config(response, damping);
    }
    config(response, damping = 1) {
      this.k = (2 * Math.PI / response) ** 2;
      this.c = (4 * Math.PI * damping) / response;
      return this;
    }
    to(target, { velocity, response, damping } = {}) {
      if (response) this.config(response, damping ?? 1);
      if (velocity !== undefined) this.velocity = velocity;
      this.target = target;
      if (reduced()) return this.jump(target);
      this.run();
      return this;
    }
    jump(v) {
      cancelAnimationFrame(this.raf);
      this.raf = 0;
      this.value = this.target = v;
      this.velocity = 0;
      this.onUpdate && this.onUpdate(v);
      this.onRest && this.onRest();
      return this;
    }
    stop() { cancelAnimationFrame(this.raf); this.raf = 0; }
    run() {
      if (this.raf) return;
      let last = performance.now();
      const step = (now) => {
        const dt = Math.min(0.064, (now - last) / 1000);
        last = now;
        const n = Math.max(1, Math.ceil(dt / 0.004));
        const h = dt / n;
        for (let i = 0; i < n; i++) {
          const f = -this.k * (this.value - this.target) - this.c * this.velocity;
          this.velocity += f * h;
          this.value += this.velocity * h;
        }
        this.onUpdate && this.onUpdate(this.value);
        if (Math.abs(this.velocity) < this.precision * 10 && Math.abs(this.value - this.target) < this.precision) {
          this.value = this.target;
          this.velocity = 0;
          this.raf = 0;
          this.onUpdate && this.onUpdate(this.value);
          this.onRest && this.onRest();
          return;
        }
        this.raf = requestAnimationFrame(step);
      };
      this.raf = requestAnimationFrame(step);
    }
  }

  /* Progressive resistance past an edge: the further you pull, the less it follows */
  const rubber = (over, dim = 300, c = 0.55) => (over * dim * c) / (dim + c * over);

  /* Apple's momentum projection: where would a flick come to rest? */
  const project = (velocity, rate = 0.99) => (velocity / 1000) * rate / (1 - rate);

  /* Velocity tracker over the last ~100 ms of pointer samples */
  const tracker = () => {
    let samples = [];
    return {
      add(v) { const t = performance.now(); samples.push([t, v]); samples = samples.filter((s) => t - s[0] < 100); },
      velocity() {
        if (samples.length < 2) return 0;
        const a = samples[0], b = samples[samples.length - 1];
        const dt = (b[0] - a[0]) / 1000;
        return dt > 0 ? (b[1] - a[1]) / dt : 0;
      },
      reset() { samples = []; },
    };
  };

  /* ---------- Header: glass that adapts to what's underneath ---------- */
  const header = $('.site-header');
  const themed = $$('[data-header]');
  const updateHeader = () => {
    const probe = 36;
    let hit = null; // innermost section under the header wins
    for (const el of themed) {
      const r = el.getBoundingClientRect();
      if (r.top <= probe && r.bottom > probe) hit = el;
    }
    if (hit) header.classList.toggle('is-dark', hit.dataset.header === 'dark');
  };

  /* ---------- Mobile menu ---------- */
  const menuBtn = $('.menu-btn');
  const sheet = $('#meniu');
  let lastFocus = null;
  const setMenu = (open) => {
    sheet.classList.toggle('is-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    document.documentElement.style.overflow = open ? 'hidden' : '';
    if (open) {
      lastFocus = document.activeElement;
      setTimeout(() => $('a', sheet).focus({ preventScroll: true }), 50);
    } else if (lastFocus) {
      lastFocus.focus({ preventScroll: true });
    }
  };
  menuBtn && menuBtn.addEventListener('click', () => setMenu(true));
  $('.menu-sheet__close', sheet).addEventListener('click', () => setMenu(false));
  $$('a', sheet).forEach((a) => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sheet.classList.contains('is-open')) setMenu(false);
  });
  sheet.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;
    const f = $$('a, button', sheet);
    if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
    else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
  });

  /* ---------- Split-flap ---------- */
  const POOL = 'ABCDEFGHIJKLMNOPRSTUVZĂÂÎȘȚ';
  const flip = (tile, ch) => {
    tile.textContent = ch;
    tile.classList.remove('is-flipping');
    void tile.offsetWidth; // restart the flap animation
    tile.classList.add('is-flipping');
  };
  const runBoard = (tiles, pick, { stagger = 34, tick = 62, minFlips = 5 } = {}) => {
    if (reduced()) return;
    const start = performance.now();
    const plan = tiles.map((t, i) => ({ t, final: t.textContent, at: i * stagger, flips: minFlips + (i % 4), done: 0 }));
    plan.forEach((p) => { p.t.textContent = ' '; });
    // Time-based, so a slow device skips frames instead of running long
    const loop = (now) => {
      const el = now - start;
      let busy = false;
      for (const p of plan) {
        if (p.done > p.flips) continue;
        busy = true;
        if (el < p.at) continue;
        const due = Math.min(p.flips + 1, Math.floor((el - p.at) / tick) + 1);
        if (due <= p.done) continue;
        p.done = due;
        flip(p.t, p.done > p.flips ? p.final : pick(p, p.done));
      }
      if (busy) requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  };

  // Boards in the hero flip on load; the rest flip when they scroll into view
  const flipBoard = (b) => runBoard($$('.flap', b), () => POOL[(Math.random() * POOL.length) | 0]);
  const boardIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      flipBoard(e.target);
      boardIO.unobserve(e.target);
    });
  }, { threshold: 0.6 });
  $$('[data-flap-board]').forEach((b) => (b.closest('.hero') ? flipBoard(b) : boardIO.observe(b)));

  const rollDigits = (wrap) => {
    const tiles = $$('.flap[data-digit]', wrap);
    runBoard(tiles, (p, n) => String((Number(p.final) + n) % 10), { stagger: 90, tick: 70, minFlips: 9 });
  };

  /* ---------- Split text into word spans (for kinetic and scroll-lit text) ---------- */
  const splitWords = (root) => {
    let i = 0;
    const words = [];
    const walk = (node) => {
      Array.from(node.childNodes).forEach((n) => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement('span');
            w.className = 'w';
            w.style.setProperty('--i', i++);
            w.textContent = part;
            words.push(w);
            frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && !n.classList.contains('visually-hidden')) {
          walk(n);
        }
      });
    };
    walk(root);
    return words;
  };

  /* ---------- Hero headline: words rise in ---------- */
  const split = $('[data-split]');
  if (split && !reduced()) splitWords(split);
  requestAnimationFrame(() => {
    split && split.classList.add('is-in');
    const fan = $('[data-fan]');
    fan && fan.classList.add('is-in');
  });

  /* ---------- Scroll-lit text: each word brightens as reading reaches it ---------- */
  const scrubs = $$('[data-scrub]').map((el) => ({ el, words: reduced() ? [] : splitWords(el) }));
  const paintScrub = () => {
    scrubs.forEach(({ el, words }) => {
      if (!words.length) return;
      const r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > innerHeight + 200) return;
      const p = clamp((innerHeight * 0.82 - r.top) / (r.height + innerHeight * 0.3), 0, 1);
      const lit = Math.round(p * words.length);
      words.forEach((w, i) => w.classList.toggle('is-lit', i < lit));
    });
  };

  /* ---------- Values: the one crossing the middle of the screen lights up ---------- */
  const valueIO = new IntersectionObserver((entries) => {
    entries.forEach((e) => e.target.classList.toggle('is-active', e.isIntersecting));
  }, { rootMargin: '-42% 0px -42% 0px' });
  $$('[data-values] .value').forEach((v) => valueIO.observe(v));

  /* ---------- Reveal on scroll ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('is-in');
      if ($('.flap[data-digit]', e.target)) rollDigits(e.target);
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  $$('[data-reveal]').forEach((el) => io.observe(el));

  /* ---------- Hero fan: depth that follows the pointer ---------- */
  const fan = $('[data-fan]');
  const fanX = new Spring(0, { response: 0.6, damping: 1, precision: 0.01 });
  const fanY = new Spring(0, { response: 0.6, damping: 1, precision: 0.01 });
  let fanScroll = 0;
  const paintFan = () => {
    if (!fan) return;
    fan.style.transform = `translate3d(0, ${fanScroll}px, 0) rotateX(${fanY.value}deg) rotateY(${fanX.value}deg)`;
  };
  fanX.onUpdate = fanY.onUpdate = paintFan;
  if (fan && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const hero = fan.closest('.hero');
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      fanX.to(((e.clientX - r.left) / r.width - 0.5) * 10);
      fanY.to(-((e.clientY - r.top) / r.height - 0.5) * 8);
    });
    hero.addEventListener('pointerleave', () => { fanX.to(0); fanY.to(0); });
  }

  /* ---------- Europe map ---------- */
  const mapSection = $('[data-map]');
  if (mapSection) {
    const svg = $('.map-svg', mapSection);
    const frame = $('.map__frame', mapSection);
    const pass = $('[data-country-pass]', mapSection);
    const plane = $('.map-plane', svg);
    const names = T.countries;
    let current = null;

    const setViewBox = () => svg.setAttribute('viewBox', desktop.matches ? '250 300 580 456' : '330 330 440 390');
    setViewBox();
    desktop.addEventListener('change', setViewBox);

    $$('.map-route', svg).forEach((r, i) => r.style.setProperty('--i', i));
    new IntersectionObserver((entries, obs) => {
      if (entries[0].isIntersecting) { mapSection.classList.add('is-in'); obs.disconnect(); }
    }, { threshold: 0.3 }).observe(frame);

    // Plane flies once along the chosen route
    let flight = 0;
    const fly = (code) => {
      cancelAnimationFrame(flight);
      const route = $(`.map-route[data-country="${code}"]`, svg);
      if (!route || reduced()) { plane.style.opacity = 0; return; }
      const len = route.getTotalLength();
      const t0 = performance.now();
      const dur = 900;
      const ease = (t) => 1 - Math.pow(1 - t, 3);
      const frameFn = (now) => {
        const t = clamp((now - t0) / dur, 0, 1);
        const d = ease(t) * len;
        const p = route.getPointAtLength(d);
        const q = route.getPointAtLength(Math.min(len, d + 1));
        const a = Math.atan2(q.y - p.y, q.x - p.x) * 180 / Math.PI + 90;
        plane.setAttribute('transform', `translate(${p.x} ${p.y}) rotate(${a}) scale(1.4)`);
        plane.style.opacity = t < 0.9 ? 1 : (1 - t) * 10;
        if (t < 1) flight = requestAnimationFrame(frameFn);
      };
      flight = requestAnimationFrame(frameFn);
    };

    // The pass slides up from the bottom of the map, and leaves the same way
    const passY = new Spring(0, { response: 0.42, damping: 1 });
    const hiddenY = () => pass.offsetHeight + 24;
    passY.onUpdate = (y) => { pass.style.transform = `translate3d(0, ${y}px, 0)`; };
    passY.onRest = () => { if (!current) pass.classList.remove('is-open'); };
    passY.jump(400);

    const select = (code) => {
      current = code;
      svg.classList.toggle('has-focus', !!code);
      $$('[data-country]', mapSection).forEach((el) => {
        const on = el.dataset.country === code;
        el.classList.toggle('is-focus', on);
        if (el.tagName === 'BUTTON') el.setAttribute('aria-pressed', String(on));
      });
      if (!code) { passY.to(hiddenY(), { response: 0.38, damping: 1 }); return; }
      $('[data-pass-name]', pass).textContent = names[code];
      $('[data-pass-code]', pass).textContent = code.toUpperCase();
      $('[data-pass-code-to]', pass).textContent = code.toUpperCase();
      $('.country-pass__route', pass).style.visibility = code === 'ro' ? 'hidden' : '';
      const wasOpen = pass.classList.contains('is-open');
      pass.classList.add('is-open');
      if (!wasOpen) passY.jump(hiddenY());
      passY.to(0, { response: 0.5, damping: 0.86 });
      if (code !== 'ro') fly(code);
    };

    $$('.legend button', mapSection).forEach((b) => b.addEventListener('click', () => {
      select(current === b.dataset.country ? null : b.dataset.country);
    }));
    $$('.map-pin', svg).forEach((g) => g.addEventListener('click', () => select(g.dataset.country)));
    $('.country-pass__close', pass).addEventListener('click', () => select(null));
    // A sheet shouldn't linger once the map has scrolled away
    new IntersectionObserver((entries) => {
      if (!entries[0].isIntersecting && current) select(null);
    }).observe(frame);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && current) select(null); });

    // Swipe the pass down to dismiss: 1:1 tracking, rubber-band upward, velocity hand-off
    const vt = tracker();
    let dragging = false, startY = 0, startVal = 0;
    pass.addEventListener('pointerdown', (e) => {
      if (e.target.closest('button')) return;
      dragging = true;
      startY = e.clientY;
      startVal = passY.value;
      passY.stop();
      vt.reset();
      try { pass.setPointerCapture(e.pointerId); } catch (_) {}
    });
    pass.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      let y = startVal + (e.clientY - startY);
      if (y < 0) y = -(1 - 1 / (-y * 0.02 + 1)) * 40; // resist past the top
      passY.value = y;
      passY.onUpdate(y);
      vt.add(e.clientY);
    });
    const release = () => {
      if (!dragging) return;
      dragging = false;
      const v = vt.velocity();
      if (passY.value + project(v) > pass.offsetHeight * 0.5) {
        current = null;
        select(null);
        passY.to(hiddenY(), { velocity: v, response: 0.38, damping: 1 });
      } else {
        passY.to(0, { velocity: v, response: 0.45, damping: 0.8 });
      }
    };
    pass.addEventListener('pointerup', release);
    pass.addEventListener('pointercancel', release);
  }

  /* ---------- Boarding-pass deck ---------- */
  const deck = $('[data-deck]');
  if (deck) {
    const slots = $$('[data-slot]', deck);
    const passes = slots.map((s) => $('.pass', s));
    const total = slots.length;
    const TILT = [0, 2.6, -2.2, 1.6, 0, 0, 0, 0];
    let order = slots.map((_, i) => i);
    const indexEl = $('[data-deck-index]');

    const springs = passes.map((p) => {
      const s = new Spring(0, { response: 0.45, damping: 0.85 });
      s.onUpdate = (x) => {
        p.style.transform = `translate3d(${x}px, ${-Math.abs(x) * 0.04}px, 0) rotate(${x * 0.045}deg)`;
      };
      return s;
    });

    const layout = () => {
      order.forEach((idx, depth) => {
        const slot = slots[idx];
        slot.style.setProperty('--depth', depth);
        slot.style.setProperty('--tilt', TILT[depth] || 0);
        slot.dataset.depth = depth;
        const top = depth === 0;
        slot.setAttribute('aria-hidden', String(!top));
        passes[idx].tabIndex = top ? 0 : -1;
      });
      indexEl.textContent = String(order[0] + 1).padStart(2, '0');
    };
    layout();

    const width = () => deck.offsetWidth;

    // Throw the top card off-screen; once it clears the stack it tucks in behind
    const next = (dir = -1, velocity) => {
      const idx = order[0];
      const s = springs[idx];
      if (reduced()) { order.push(order.shift()); layout(); return; }
      const out = dir * width() * 1.15;
      let swapped = false;
      s.onRest = null;
      const prevUpdate = s.onUpdate;
      s.onUpdate = (x) => {
        prevUpdate(x);
        if (!swapped && Math.abs(x) > width() * 0.85) {
          swapped = true;
          order = order.filter((i) => i !== idx).concat(idx);
          layout();
          s.onUpdate = prevUpdate;
          s.to(0, { response: 0.6, damping: 0.9 });
        }
      };
      s.to(out, { velocity: velocity ?? dir * 1800, response: 0.4, damping: 1 });
    };

    const prev = () => {
      const idx = order[order.length - 1];
      order = [idx].concat(order.slice(0, -1));
      layout();
      const s = springs[idx];
      if (reduced()) return;
      s.jump(-width() * 1.1);
      s.to(0, { response: 0.55, damping: 0.85 });
    };

    $('[data-deck-next]').addEventListener('click', () => next(-1));
    $('[data-deck-prev]').addEventListener('click', prev);
    deck.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); next(-1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); prev(); }
    });

    // Drag: 1:1 with the grab point, intent decided after ~8px, momentum on release
    const vt = tracker();
    let active = null, sx = 0, sy = 0, base = 0, axis = null, moved = false;
    deck.addEventListener('pointerdown', (e) => {
      const p = e.target.closest('.pass');
      if (!p || passes.indexOf(p) !== order[0] || e.button > 0) return;
      active = p;
      sx = e.clientX; sy = e.clientY;
      const s = springs[order[0]];
      s.stop();
      base = s.value; // grab mid-flight from the current value
      axis = null; moved = false;
      vt.reset();
    });
    deck.addEventListener('pointermove', (e) => {
      if (!active) return;
      const dx = e.clientX - sx, dy = e.clientY - sy;
      if (!axis) {
        if (Math.hypot(dx, dy) < 8) return;
        axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
        if (axis === 'y') { active = null; return; }
        try { active.setPointerCapture(e.pointerId); } catch (_) {}
      }
      moved = true;
      const s = springs[order[0]];
      s.value = base + dx;
      s.onUpdate(s.value);
      vt.add(e.clientX);
    });
    const end = () => {
      if (!active) return;
      active = null;
      if (!moved) return;
      const s = springs[order[0]];
      const v = vt.velocity();
      const landing = s.value + project(v);
      if (Math.abs(landing) > width() * 0.45) next(Math.sign(landing), v);
      else s.to(0, { velocity: v, response: 0.45, damping: 0.72 });
    };
    deck.addEventListener('pointerup', end);
    deck.addEventListener('pointercancel', end);
    deck.addEventListener('click', (e) => { if (moved) { e.preventDefault(); moved = false; } }, true);
  }

  /* ---------- Pillars ---------- */
  const pillars = $('[data-pillars]');
  if (pillars) {
    const items = $$('.pillar', pillars);
    const imgs = $$('.pillars__media img', pillars);
    items.forEach((li, i) => $('button', li).addEventListener('click', () => {
      items.forEach((o, j) => {
        o.classList.toggle('is-active', i === j);
        $('button', o).setAttribute('aria-expanded', String(i === j));
      });
      imgs.forEach((im, j) => im.classList.toggle('is-active', i === j));
    }));
  }

  /* ---------- Journey: a flight path drawn by scrolling ---------- */
  const track = $('[data-journey]');
  let paintJourney = () => {};
  if (track) {
    const svgJ = $('.journey__svg', track);
    const base = $('.journey__base', svgJ);
    const line = $('.journey__line', svgJ);
    const planeJ = $('.journey__plane', svgJ);
    const stops = $$('.stop', track);
    let len = 0, pts = [];

    const build = () => {
      const tr = track.getBoundingClientRect();
      pts = stops.map((s) => {
        const r = $('.stop__dot', s).getBoundingClientRect();
        return [r.left + r.width / 2 - tr.left, r.top + r.height / 2 - tr.top];
      });
      const amp = desktop.matches ? 34 : 14;
      let d = `M${pts[0][0]} ${pts[0][1]}`;
      for (let i = 1; i < pts.length; i++) {
        const [x1, y1] = pts[i - 1], [x2, y2] = pts[i];
        const a = (i % 2 ? 1 : -1) * amp, dy = y2 - y1;
        d += ` C${x1 + a} ${y1 + dy * 0.4} ${x2 + a} ${y2 - dy * 0.4} ${x2} ${y2}`;
      }
      base.setAttribute('d', d);
      line.setAttribute('d', d);
      len = line.getTotalLength();
      line.style.strokeDasharray = `${len} ${len}`;
      paintJourney();
    };

    paintJourney = () => {
      if (!len) return;
      const tr = track.getBoundingClientRect();
      const first = pts[0][1], last = pts[pts.length - 1][1];
      const p = clamp((innerHeight * 0.62 - (tr.top + first)) / (last - first), 0, 1);
      line.style.strokeDashoffset = String(len * (1 - p));
      const at = Math.max(0.5, len * p);
      const pt = line.getPointAtLength(at);
      const ah = line.getPointAtLength(Math.min(len, at + 1));
      const ang = Math.atan2(ah.y - pt.y, ah.x - pt.x) * 180 / Math.PI + 90;
      planeJ.setAttribute('transform', `translate(${pt.x} ${pt.y}) rotate(${ang})`);
      stops.forEach((s, i) => s.classList.toggle('is-passed', p >= (pts[i][1] - first) / (last - first) - 0.002));
    };

    new ResizeObserver(build).observe(track);
    desktop.addEventListener('change', build);
  }

  /* ---------- Photo that grows to full-bleed as it scrolls in ---------- */
  const grows = $$('[data-grow]');
  const paintGrow = () => {
    grows.forEach((g) => {
      const r = g.getBoundingClientRect();
      const p = reduced() ? 1 : clamp(1 - (r.top - innerHeight * 0.1) / (innerHeight * 0.8), 0, 1);
      g.style.setProperty('--p', p.toFixed(4));
    });
  };

  /* ---------- Contact: send & copy feedback ---------- */
  $$('[data-send]').forEach((a) => a.addEventListener('click', () => {
    a.classList.remove('is-sent');
    void a.offsetWidth;
    a.classList.add('is-sent');
    setTimeout(() => a.classList.remove('is-sent'), 1200);
  }));
  $$('[data-copy]').forEach((b) => {
    const status = $('[data-copy-status]');
    let t = 0;
    const done = () => {
      b.classList.add('is-copied');
      if (status) status.textContent = T.copied;
      clearTimeout(t);
      t = setTimeout(() => { b.classList.remove('is-copied'); if (status) status.textContent = ''; }, 2200);
    };
    const fallback = () => {
      const ta = document.createElement('textarea');
      ta.value = b.dataset.copy;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (_) {}
      ta.remove();
    };
    b.addEventListener('click', () => {
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(b.dataset.copy).then(done, fallback);
      else fallback();
    });
  });

  /* ---------- Stories: 3D tilt that follows the pointer (springs, no overshoot) ---------- */
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    $$('.story').forEach((card) => {
      const rx = new Spring(0, { response: 0.45, damping: 1, precision: 0.01 });
      const ry = new Spring(0, { response: 0.45, damping: 1, precision: 0.01 });
      rx.onUpdate = (v) => card.style.setProperty('--rx', `${v}deg`);
      ry.onUpdate = (v) => card.style.setProperty('--ry', `${v}deg`);
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        ry.to(((e.clientX - r.left) / r.width - 0.5) * 14);
        rx.to(-((e.clientY - r.top) / r.height - 0.5) * 10);
      });
      // The springs already smooth the tilt, so the CSS transition only handles the lift
      card.addEventListener('pointerenter', () => { card.style.transition = 'transform 0.35s var(--ease), box-shadow 0.4s'; });
      card.addEventListener('pointerleave', () => { card.style.transition = ''; rx.to(0); ry.to(0); });
    });
  }

  /* ---------- Departures board: names scramble into place like an airport display ---------- */
  const SCRAMBLE = 'ABCDEFGHIJKLMNOPRSTUVZĂÂÎȘȚ0123456789';
  const scramble = (el, dur = 650) => {
    if (reduced() || el.dataset.busy) return;
    const final = el.dataset.final || (el.dataset.final = el.textContent);
    el.dataset.busy = '1';
    const t0 = performance.now();
    const step = (now) => {
      const t = clamp((now - t0) / dur, 0, 1);
      const settled = Math.floor(t * final.length);
      let out = final.slice(0, settled);
      for (let i = settled; i < final.length; i++) {
        out += final[i] === ' ' ? ' ' : SCRAMBLE[(Math.random() * SCRAMBLE.length) | 0];
      }
      el.textContent = out;
      if (t < 1) requestAnimationFrame(step);
      else { el.textContent = final; delete el.dataset.busy; }
    };
    requestAnimationFrame(step);
  };
  $$('[data-deps]').forEach((list) => {
    const names = $$('[data-scramble]', list);
    new IntersectionObserver((entries, obs) => {
      if (!entries[0].isIntersecting) return;
      names.forEach((n, i) => setTimeout(() => scramble(n, 700), 250 + i * 110));
      obs.disconnect();
    }, { threshold: 0.3 }).observe(list);
    $$('.dep', list).forEach((row) => {
      const n = $('[data-scramble]', row);
      row.addEventListener('pointerenter', () => scramble(n, 450));
      row.addEventListener('focus', () => scramble(n, 450));
    });
  });

  /* ---------- Pinned horizontal gallery: scrolling down moves the passes sideways ---------- */
  const hs = $('[data-hscroll]');
  let paintHscroll = () => {};
  if (hs) {
    const track = $('[data-hscroll-track]', hs);
    const fill = $('.hscroll__rail', hs);
    const idx = $('[data-hscroll-index]', hs);
    const items = $$('.bpass-item', hs);
    let dist = 0;
    const setup = () => {
      const pin = desktop.matches && !reduced();
      hs.classList.toggle('is-pinned', pin);
      if (!pin) { hs.style.height = ''; track.style.transform = ''; dist = 0; return; }
      dist = Math.max(0, track.scrollWidth - document.documentElement.clientWidth);
      hs.style.height = `${dist + innerHeight}px`;
      paintHscroll();
    };
    paintHscroll = () => {
      if (!dist) return;
      const r = hs.getBoundingClientRect();
      const p = clamp(-r.top / (r.height - innerHeight), 0, 1);
      track.style.transform = `translate3d(${(-p * dist).toFixed(1)}px, 0, 0)`;
      fill.style.setProperty('--p', p.toFixed(4));
      idx.textContent = String(Math.round(p * (items.length - 1)) + 1).padStart(2, '0');
    };
    setup();
    addEventListener('resize', setup);
    desktop.addEventListener('change', setup);
    motionQuery.addEventListener && motionQuery.addEventListener('change', setup);
  }

  /* ---------- Chapters: sticky route with a plane between programmes ---------- */
  const route = $('[data-route]');
  let paintRoute = () => {};
  if (route) {
    const chapters = $$('[data-chapter]');
    const links = $$('[data-route-link]', route);
    const line = $('.route__line', route);
    paintRoute = () => {
      const edge = route.getBoundingClientRect().bottom + 40;
      let cur = 0;
      chapters.forEach((c, i) => { if (c.getBoundingClientRect().top <= edge) cur = i; });
      const r = chapters[cur].getBoundingClientRect();
      const within = cur < chapters.length - 1 ? clamp((edge - r.top) / r.height, 0, 1) : 0;
      const p = clamp((cur + within) / (chapters.length - 1), 0, 1);
      line.style.setProperty('--p', p.toFixed(4));
      links.forEach((a, i) => {
        a.classList.toggle('is-passed', i <= cur);
        a.classList.toggle('is-current', i === cur);
        if (i === cur) a.setAttribute('aria-current', 'step'); else a.removeAttribute('aria-current');
      });
    };
  }
  // In-page links glide (or jump, with reduced motion)
  $$('a[href^="#"]').forEach((a) => {
    const id = a.getAttribute('href');
    if (id.length < 2 || a.matches('.skip-link, .to-top')) return;
    a.addEventListener('click', (e) => {
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth', block: 'start' });
      history.replaceState(null, '', id);
    });
  });

  /* ---------- BOOST skills orbit: turns with the scroll ---------- */
  const orbit = $('[data-spin]');
  const paintOrbit = () => {
    if (!orbit || reduced()) return;
    const r = orbit.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    orbit.style.setProperty('--spin', `${(scrollY * 0.12).toFixed(2)}deg`);
  };

  /* ---------- Gallery lightbox: swipe with momentum, swipe down to close ---------- */
  const gallery = $('[data-gallery]');
  if (gallery) {
    const thumbs = $$('[data-gal]', gallery);
    const SVG = {
      close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
      prev: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
      next: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    };
    const lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.hidden = true;
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', gallery.dataset.label || '');
    lb.innerHTML = `<div class="lightbox__scrim"></div>
      <div class="lightbox__stage"><div class="lightbox__track">${thumbs.map((t) => `<figure class="lightbox__slide"><img alt="" data-src="${t.dataset.full}" draggable="false"/></figure>`).join('')}</div></div>
      <button class="lightbox__btn lightbox__close" type="button" aria-label="${T.close}">${SVG.close}</button>
      <p class="lightbox__caption" aria-live="polite"></p>
      <div class="lightbox__bar"><button class="lightbox__btn" type="button" data-lb-prev aria-label="${T.prev}">${SVG.prev}</button><span class="lightbox__count mono"></span><button class="lightbox__btn" type="button" data-lb-next aria-label="${T.next}">${SVG.next}</button></div>`;
    document.body.appendChild(lb);
    const stage = $('.lightbox__stage', lb);
    const track = $('.lightbox__track', lb);
    const scrim = $('.lightbox__scrim', lb);
    const imgs = $$('img', track);
    const count = $('.lightbox__count', lb);
    const caption = $('.lightbox__caption', lb);
    const n = thumbs.length;
    let index = 0, opener = null;
    const W = () => stage.clientWidth;

    const x = new Spring(0, { response: 0.45, damping: 0.92 });
    const y = new Spring(0, { response: 0.4, damping: 1 });
    x.onUpdate = (v) => { track.style.transform = `translate3d(${v}px, 0, 0)`; };
    y.onUpdate = (v) => {
      stage.style.transform = `translate3d(0, ${v}px, 0) scale(${1 - Math.min(Math.abs(v) / 2400, 0.15)})`;
      scrim.style.opacity = String(1 - Math.min(Math.abs(v) / 500, 0.8));
    };

    const load = (i) => [i - 1, i, i + 1].forEach((k) => {
      const im = imgs[k];
      if (im && !im.src) { im.src = im.dataset.src; im.alt = $('img', thumbs[k]).alt; }
    });
    const label = () => {
      count.textContent = `${String(index + 1).padStart(2, '0')} / ${String(n).padStart(2, '0')}`;
      caption.textContent = $('img', thumbs[index]).alt;
    };
    const go = (i, velocity) => {
      index = clamp(i, 0, n - 1);
      load(index);
      label();
      x.to(-index * W(), { velocity, response: 0.45, damping: 0.92 });
    };
    const onKey = (e) => {
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') go(index + 1);
      else if (e.key === 'ArrowLeft') go(index - 1);
      else if (e.key === 'Tab') {
        const f = $$('button', lb);
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    };
    const open = (i, from) => {
      opener = from;
      lb.hidden = false;
      document.documentElement.style.overflow = 'hidden';
      index = i;
      load(i);
      label();
      x.jump(-i * W());
      y.jump(0);
      requestAnimationFrame(() => lb.classList.add('is-open'));
      $('.lightbox__close', lb).focus({ preventScroll: true });
      document.addEventListener('keydown', onKey);
    };
    const close = () => {
      lb.classList.remove('is-open');
      document.removeEventListener('keydown', onKey);
      document.documentElement.style.overflow = '';
      setTimeout(() => { lb.hidden = true; y.jump(0); }, reduced() ? 0 : 300);
      opener && opener.focus({ preventScroll: true });
    };
    thumbs.forEach((t, i) => t.addEventListener('click', () => open(i, t)));
    $('.lightbox__close', lb).addEventListener('click', close);
    $('[data-lb-prev]', lb).addEventListener('click', () => go(index - 1));
    $('[data-lb-next]', lb).addEventListener('click', () => go(index + 1));
    addEventListener('resize', () => { if (!lb.hidden) x.jump(-index * W()); });

    // Drag: decide the axis after ~8px, track 1:1, then hand the velocity to a spring
    const vx = tracker(), vy = tracker();
    let down = false, sx = 0, sy = 0, axis = null, moved = false, baseX = 0;
    stage.addEventListener('pointerdown', (e) => {
      if (e.button > 0) return;
      down = true; moved = false; axis = null;
      sx = e.clientX; sy = e.clientY;
      x.stop(); y.stop();
      baseX = x.value;
      vx.reset(); vy.reset();
      try { stage.setPointerCapture(e.pointerId); } catch (_) {}
    });
    stage.addEventListener('pointermove', (e) => {
      if (!down) return;
      const dx = e.clientX - sx, dy = e.clientY - sy;
      if (!axis) {
        if (Math.hypot(dx, dy) < 8) return;
        axis = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
      }
      moved = true;
      if (axis === 'x') {
        let v = baseX + dx;
        const min = -(n - 1) * W();
        if (v > 0) v = rubber(v);
        if (v < min) v = min - rubber(min - v);
        x.value = v; x.onUpdate(v); vx.add(e.clientX);
      } else {
        const v = dy < 0 ? -rubber(-dy) : dy;
        y.value = v; y.onUpdate(v); vy.add(e.clientY);
      }
    });
    const up = (e) => {
      if (!down) return;
      down = false;
      if (!moved) {
        if (e && e.target && e.target.tagName !== 'IMG') close();
        return;
      }
      if (axis === 'x') {
        const v = vx.velocity();
        const shift = x.value - (-index * W()) + project(v);
        if (shift < -W() * 0.3) go(index + 1, v);
        else if (shift > W() * 0.3) go(index - 1, v);
        else go(index, v);
      } else {
        const v = vy.velocity();
        if (y.value + project(v) > 160) close();
        else y.to(0, { velocity: v, response: 0.4, damping: 0.85 });
      }
    };
    stage.addEventListener('pointerup', up);
    stage.addEventListener('pointercancel', () => up(null));
  }

  /* ---------- Sending board: filter by year, show the first rows until asked for more ---------- */
  $$('[data-sendboard]').forEach((board) => {
    const rows = $$('.sb-row', board);
    const more = $('[data-sb-more]', board);
    const buttons = $$('[data-filter]', board.closest('section'));
    const LIMIT = 10;
    let expanded = false, current = 'all';
    const apply = () => {
      let shown = 0;
      rows.forEach((r) => {
        const match = current === 'all' || r.dataset.group === current;
        const visible = match && (current !== 'all' || expanded || shown < LIMIT);
        r.hidden = !visible;
        if (match) shown++;
      });
      more.hidden = current !== 'all' || expanded;
    };
    buttons.forEach((b) => b.addEventListener('click', () => {
      current = b.dataset.filter;
      buttons.forEach((o) => { o.classList.toggle('is-active', o === b); o.setAttribute('aria-pressed', String(o === b)); });
      apply();
    }));
    more.addEventListener('click', () => { expanded = true; apply(); rows[LIMIT] && rows[LIMIT].querySelector('a, .sb-row__name'); });
    apply();
  });

  /* ---------- FAQ ---------- */
  $$('[data-faq] .faq-item').forEach((item) => {
    const b = $('button', item);
    b.addEventListener('click', () => {
      const open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      b.setAttribute('aria-expanded', String(open));
    });
  });

  /* ---------- Back to top ---------- */
  const toTop = $('.to-top');
  toTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: reduced() ? 'auto' : 'smooth' });
    $('#top a').focus({ preventScroll: true });
  });

  /* ---------- One scroll loop for everything scroll-linked ---------- */
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      updateHeader();
      paintJourney();
      paintGrow();
      paintScrub();
      paintHscroll();
      paintRoute();
      paintOrbit();
      toTop.classList.toggle('is-visible', scrollY > innerHeight * 1.2);
      if (fan && !reduced()) {
        fanScroll = Math.min(scrollY, innerHeight) * -0.12;
        paintFan();
      }
    });
  };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll, { passive: true });
  onScroll();
})();
