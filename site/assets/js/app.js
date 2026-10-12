/* Le Père Lucien & Mère Martine : interactions du site (vanilla, sans dépendance). */
(() => {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const FREE_SHIP = 80;
  const KEY = "pl-cart-v1";
  const euro = (v) => v.toFixed(2).replace(".", ",") + " €";
  /* Racine du site, déduite du chemin de ce script : fonctionne en http:// comme en file://. */
  const BASE = ((document.currentScript && document.currentScript.src) || "").replace(/assets\/js\/app\.js.*$/, "") || "/";
  const FILE = location.protocol === "file:";
  const abs = (p) => {
    if (!p || !p.startsWith("/")) return p;
    let u = BASE + p.slice(1);
    if (FILE && u.endsWith("/")) u += "index.html";
    return u;
  };
  const loadScript = (src) => new Promise((ok, ko) => { const s = document.createElement("script"); s.src = BASE + src; s.onload = ok; s.onerror = ko; document.head.appendChild(s); });
  if (FILE) {
    const fl = document.createElement("link");
    fl.rel = "stylesheet"; fl.href = BASE + "assets/css/fonts-embedded.css";
    document.head.appendChild(fl);
  }
  if (FILE) {
    // En ouverture directe, un lien vers un dossier doit viser son index.html.
    document.querySelectorAll("a[href]").forEach((a) => {
      const h = a.getAttribute("href");
      if (/^[a-z]+:/i.test(h) || h.startsWith("#")) return;
      if (h.endsWith("/")) a.setAttribute("href", h + "index.html");
      else if (h === "." || h === "./" || h === "..") a.setAttribute("href", h.replace(/\/?$/, "/") + "index.html");
    });
  }
  const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  /* ---------- Stockage du panier (tolérant aux navigateurs privés) ---------- */
  const store = {
    get() { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } },
    set(v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* panier en mémoire seulement */ } memory = v; },
  };
  let memory = store.get();
  const cart = () => memory;

  let catalogue = null;
  const loadCatalogue = () => catalogue || (catalogue = loadScript("assets/catalogue.js").then(() => window.PL_CATALOGUE || {}).catch(() => ({})));

  /* ---------- Toast ---------- */
  const toastEl = $("[data-toast]");
  let toastT;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("is-on");
    clearTimeout(toastT);
    toastT = setTimeout(() => toastEl.classList.remove("is-on"), 2400);
  }

  /* ---------- Rendu du panier ---------- */
  function renderCart() {
    const items = cart();
    const count = items.reduce((n, i) => n + i.q, 0);
    const total = items.reduce((n, i) => n + i.q * i.p, 0);
    $$("[data-cart-count]").forEach((el) => { el.textContent = count; el.hidden = count === 0; });
    $$("[data-cart-total]").forEach((el) => (el.textContent = euro(total)));
    $$("[data-cart-empty]").forEach((el) => (el.hidden = count > 0));
    $$("[data-cart-ft]").forEach((el) => (el.hidden = count === 0));
    $$("[data-ship-cost]").forEach((el) => (el.textContent = total >= FREE_SHIP ? "Offerte" : "Dès 4,95 €"));
    $$("[data-ship]").forEach((el) => {
      if (!count) { el.innerHTML = ""; return; }
      const left = FREE_SHIP - total;
      const pct = Math.min(100, (total / FREE_SHIP) * 100);
      el.innerHTML = (left > 0 ? `Plus que <strong>${euro(left)}</strong> pour la livraison offerte.` : "La livraison est offerte.") +
        `<div class="ship-bar"><span style="width:${pct}%"></span></div>`;
    });
    $$("[data-cart-list]").forEach((ul) => {
      ul.innerHTML = items.map((i, idx) => `
        <li class="cart-line">
          ${i.img ? `<img src="${abs(i.img)}" alt="" width="76" height="76" loading="lazy">` : `<span></span>`}
          <div><a class="cl-name" href="${abs(i.u)}">${escapeHtml(i.n)}</a>${i.v ? `<span class="cl-var">${escapeHtml(i.v)}</span>` : ""}
            <div class="cl-ctrl"><button type="button" data-q="${idx}" data-d="-1" aria-label="Retirer un exemplaire">−</button><span>${i.q}</span><button type="button" data-q="${idx}" data-d="1" aria-label="Ajouter un exemplaire">+</button></div></div>
          <div class="cl-price">${euro(i.p * i.q)}<button class="cl-rm" type="button" data-rm="${idx}">Retirer</button></div>
        </li>`).join("");
    });
  }

  function addToCart(item) {
    const items = cart().slice();
    const found = items.find((i) => i.id === item.id && (i.v || "") === (item.v || ""));
    if (found) found.q = Math.min(20, found.q + item.q);
    else items.push(item);
    store.set(items);
    renderCart();
    $$("[data-cart-count]").forEach((el) => { el.classList.remove("bump"); void el.offsetWidth; el.classList.add("bump"); });
  }

  document.addEventListener("click", async (e) => {
    const add = e.target.closest("[data-add]");
    if (add) {
      e.preventDefault();
      const id = add.dataset.id;
      const cat = await loadCatalogue();
      const c = cat[id];
      if (!c) return;
      let q = 1, v = "";
      if (add.hasAttribute("data-with-options")) {
        const qi = $(".qty input");
        q = Math.max(1, Math.min(20, parseInt(qi && qi.value, 10) || 1));
        const chk = $(".variants input:checked");
        v = chk ? chk.value : "";
      }
      addToCart({ id, n: c.n, p: c.p, img: c.i, u: c.u, q, v });
      if (add.classList.contains("btn-buy")) {
        add.classList.add("is-done");
        add.textContent = "Ajouté au panier";
        setTimeout(() => { add.classList.remove("is-done"); add.textContent = "Ajouter au panier"; }, 1800);
        openCart();
      } else {
        toast(`${c.n} ajouté au panier`);
      }
      return;
    }
    const qb = e.target.closest("[data-q]");
    if (qb) {
      const items = cart().slice();
      const it = items[+qb.dataset.q];
      it.q += +qb.dataset.d;
      if (it.q < 1) items.splice(+qb.dataset.q, 1);
      store.set(items); renderCart(); return;
    }
    const rm = e.target.closest("[data-rm]");
    if (rm) { const items = cart().slice(); items.splice(+rm.dataset.rm, 1); store.set(items); renderCart(); return; }
    if (e.target.closest("[data-open-cart]")) { openCart(); return; }
    if (e.target.closest("[data-open-search]")) { openSearch(); return; }
    const copy = e.target.closest("[data-copy]");
    if (copy) {
      try { await navigator.clipboard.writeText(copy.dataset.copy); toast("Lien copié"); } catch { toast(copy.dataset.copy); }
      return;
    }
    const step = e.target.closest("[data-step]");
    if (step) {
      const input = step.parentElement.querySelector("input");
      input.value = Math.max(1, Math.min(20, (parseInt(input.value, 10) || 1) + +step.dataset.step));
      return;
    }
    const thumb = e.target.closest("[data-thumb]");
    if (thumb) {
      const main = $("[data-main]");
      if (main) { main.style.opacity = 0; setTimeout(() => { main.src = thumb.dataset.thumb; main.style.opacity = 1; }, 150); }
      $$("[data-thumb]").forEach((t) => t.classList.toggle("is-on", t === thumb));
      return;
    }
    if (e.target.closest("[data-scroll-buy]")) {
      const b = $(".btn-buy");
      if (b) { b.scrollIntoView({ behavior: "smooth", block: "center" }); setTimeout(() => b.click(), 450); }
      return;
    }
    if (e.target.closest("[data-checkout-btn]")) {
      store.set([]); renderCart();
      toast("Démonstration : commande simulée, merci !");
    }
  });

  /* ---------- Fenêtres (panier, recherche) : focus piégé et Échap ---------- */
  let lastFocus = null;
  function openLayer(el, focusSel) {
    if (!el) return;
    lastFocus = document.activeElement;
    el.hidden = false;
    document.body.style.overflow = "hidden";
    const f = focusSel ? $(focusSel, el) : $("button, a, input", el);
    if (f) setTimeout(() => f.focus(), 30);
  }
  function closeLayer(el) {
    if (!el || el.hidden) return;
    el.hidden = true;
    document.body.style.overflow = "";
    if (lastFocus) lastFocus.focus();
  }
  const cartEl = $("#cart");
  const searchEl = $("#search");
  function openCart() { openLayer(cartEl, ".drawer-hd button"); }
  function openSearch() { openLayer(searchEl, "#q"); loadSearch(); }
  [cartEl, searchEl].forEach((layer) => layer && layer.addEventListener("click", (e) => { if (e.target.closest("[data-close]")) closeLayer(layer); }));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeLayer(cartEl); closeLayer(searchEl); }
    if (e.key === "Tab") {
      const layer = [cartEl, searchEl].find((l) => l && !l.hidden);
      if (!layer) return;
      const f = $$("a[href], button:not([disabled]), input, select", layer).filter((x) => x.offsetParent !== null);
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* ---------- Recherche ---------- */
  let index = null;
  function loadSearch() {
    if (index) return;
    index = [];
    loadScript("assets/search.js").then(() => { index = window.PL_SEARCH || []; runSearch(); }).catch(() => {});
  }
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
  function runSearch() {
    const input = $("#q");
    const res = $("[data-search-res]");
    const hint = $("[data-search-hint]");
    if (!input || !res || !index) return;
    const q = norm(input.value.trim());
    if (q.length < 2) { res.innerHTML = ""; hint.hidden = false; return; }
    const terms = q.split(/\s+/);
    const hits = index.map((it) => {
      const hay = norm(it.n + " " + it.k + " " + it.b);
      let s = 0;
      for (const t of terms) { if (!hay.includes(t)) return null; s += norm(it.n).includes(t) ? 3 : 1; }
      return [s, it];
    }).filter(Boolean).sort((a, b) => b[0] - a[0]).slice(0, 12);
    hint.hidden = hits.length > 0;
    if (!hits.length) hint.textContent = "Aucun résultat. Essayez un autre mot, par exemple « savon » ou « brosse ».";
    res.innerHTML = hits.map(([, it]) => `<li><a href="${abs(it.u)}">${it.i ? `<img src="${abs(it.i)}" alt="" loading="lazy">` : "<span></span>"}<span><span class="sr-n">${escapeHtml(it.n)}</span><span class="sr-b">${escapeHtml(it.b)}</span></span><span class="sr-p">${escapeHtml(it.p)}</span></a></li>`).join("");
  }
  const qInput = $("#q");
  if (qInput) qInput.addEventListener("input", runSearch);
  const urlQ = new URLSearchParams(location.search).get("q");
  if (urlQ && qInput) { qInput.value = urlQ; openSearch(); }

  /* ---------- Menu mobile ---------- */
  const burger = $(".burger");
  const mnav = $("#m-nav");
  if (burger && mnav) {
    burger.addEventListener("click", () => {
      const open = mnav.hidden;
      mnav.hidden = !open;
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      document.body.style.overflow = open ? "hidden" : "";
    });
  }

  /* ---------- Listes produits : filtres par type, tri et « afficher plus » ---------- */
  $$("[data-listing]").forEach((listing) => {
    const grid = $("[data-grid]", listing);
    const more = $("[data-more]", listing);
    const sort = $("[data-sort]", listing);
    const count = $("[data-count]", listing);
    const cards = $$(".card", grid);
    const original = cards.slice();
    const PAGE = 24;
    let shown = PAGE;
    let facet = "";
    const match = (c) => !facet || (c.dataset.types || "").split("|").includes(facet);
    function apply() {
      let n = 0;
      $$(".card", grid).forEach((c) => {
        const ok = match(c);
        c.hidden = !ok || n >= shown;
        if (ok) n++;
      });
      if (count) count.textContent = n;
      if (more) more.hidden = shown >= n;
    }
    $$(".facet", listing).forEach((btn) => btn.addEventListener("click", () => {
      facet = btn.dataset.facet;
      $$(".facet", listing).forEach((b) => { b.classList.toggle("is-on", b === btn); b.setAttribute("aria-pressed", String(b === btn)); });
      shown = PAGE;
      apply();
    }));
    if (more) more.addEventListener("click", () => {
      const before = shown;
      shown += PAGE; apply();
      const next = $$(".card", grid).filter(match)[before];
      if (next) next.querySelector(".card-title a")?.focus({ preventScroll: true });
    });
    if (sort) sort.addEventListener("change", () => {
      const v = sort.value;
      const list = v ? cards.slice().sort((x, y) => {
        if (v === "name") return x.dataset.name.localeCompare(y.dataset.name, "fr");
        const d = parseFloat(x.dataset.price) - parseFloat(y.dataset.price);
        return v === "price-asc" ? d : -d;
      }) : original;
      list.forEach((c) => grid.appendChild(c));
      apply();
    });
    apply();
  });

  /* ---------- Formulaires de démonstration ---------- */
  $$("[data-fake-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const msg = $(".form-msg", form);
      const bad = $$("[required]", form).find((f) => !f.value.trim() || (f.type === "email" && !/^\S+@\S+\.\S+$/.test(f.value)));
      if (bad) {
        msg.classList.add("is-err");
        msg.textContent = bad.type === "email" ? "Vérifiez votre adresse e-mail." : "Merci de remplir ce champ.";
        bad.focus();
        return;
      }
      msg.classList.remove("is-err");
      msg.textContent = form.querySelector("textarea") ? "Message envoyé. Nous répondons sous 48 h ouvrées." : "Inscription confirmée. À bientôt dans votre boîte mail.";
      form.reset();
    });
  });

  /* ---------- Apparitions au défilement ---------- */
  const reveals = $$(".reveal");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const groups = new Map();
    reveals.forEach((el) => {
      const p = el.parentElement;
      const n = groups.get(p) || 0;
      el.style.setProperty("--i", Math.min(n, 6));
      groups.set(p, n + 1);
    });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-in"));
  }

  /* ---------- Barre d'achat collante (mobile) ---------- */
  const buyBtn = $(".btn-buy");
  const sticky = $("[data-sticky-buy]");
  if (buyBtn && sticky && "IntersectionObserver" in window) {
    new IntersectionObserver(([en]) => { sticky.hidden = en.isIntersecting; }).observe(buyBtn);
  }

  renderCart();
  window.addEventListener("storage", (e) => { if (e.key === KEY) { memory = store.get(); renderCart(); } });
})();
