// BAS SWU -- shared interactions
(function(){
  "use strict";

  document.addEventListener("DOMContentLoaded", function(){
    initMarqueeClone();
    initPartnerMarquee();
    initClubs();
    initScrollReveal();
    initStaffToggle();
    initProgramsFinder();
    initProgramDetail();
    initFacultyDirectory();
    initProfile();
    initNewsList();
    initNewsDetail();
    initGlobalMap();
    initHomeNews();
    initHomeMap();
    initFaq();
    initChipFilter();
    initStaffDirectory();
    initForms();
    initHistoryBack();
    initAdminLogin();
  });

  // header/drawer/search/admin ต้องรอ nav+footer ถูก inject โดย assets/include.js ก่อน
  // (nav/footer มาจาก fetch() แบบ async — มาไม่ทันตอน DOMContentLoaded ยิง)
  // include.js เรียก window.BASSite.initNav() เองหลัง inject เสร็จ
  window.BASSite = window.BASSite || {};
  window.BASSite.initNav = function(){
    initHeaderScroll();
    initMegaMenuKeyboard();
    initMobileDrawer();
    initSearchPanel();
    initAdmin();
    if(window.BASSite.initDeanFab) window.BASSite.initDeanFab();
  };



  /* ---- ชิปเลือกได้ทีละอัน: sync aria-pressed ให้ตรงกับค่าที่เลือก ------------ */
  function pressChips(chips, val, attr){
    attr = attr || "data-value";
    Array.prototype.forEach.call(chips, function(c){
      c.setAttribute("aria-pressed", String(c.getAttribute(attr) === val));
    });
  }

  /* ---- ชิปกรองหมวด (data-chips): ซ่อน/แสดง [data-cat] ในเป้าหมาย ---------- */
  function initChipFilter(){
    document.querySelectorAll("[data-chips]").forEach(function(group){
      var target = document.querySelector(group.getAttribute("data-chips-target"));
      if(!target) return;
      var chips = group.querySelectorAll("[data-value]");
      Array.prototype.forEach.call(chips, function(chip){
        chip.addEventListener("click", function(){
          var val = chip.getAttribute("data-value");
          pressChips(chips, val);
          target.querySelectorAll("[data-cat]").forEach(function(item){
            item.hidden = !(val === "all" || item.getAttribute("data-cat") === val);
          });
        });
      });
    });
  }

  // forms.html — ค้นหาแบบฟอร์ม (ชื่อ/รหัส/ประเภทไฟล์ ใน data-q) + ชิปหมวด, ซ่อนหมวดที่ไม่มีผลลัพธ์
  function initForms(){
    var root = document.querySelector("[data-fm-root]");
    if(!root) return;
    var input = root.querySelector("[data-fm-q]");
    var chips = root.querySelectorAll("[data-fm-chips] [data-value]");
    var groups = root.querySelectorAll(".fm-group");
    var count = root.querySelector("[data-fm-count]");
    var empty = root.querySelector("[data-fm-empty]");
    var state = { q: "", cat: "all" };

    function apply(){
      var q = state.q.trim().toLowerCase(), shown = 0;
      Array.prototype.forEach.call(groups, function(g){
        var n = 0;
        var inCat = state.cat === "all" || g.getAttribute("data-cat") === state.cat;
        g.querySelectorAll(".fm-item").forEach(function(it){
          var hit = inCat && (!q || it.getAttribute("data-q").indexOf(q) !== -1);
          it.hidden = !hit;
          if(hit) n++;
        });
        g.querySelectorAll(".fm-list").forEach(function(ul){
          var any = ul.querySelector(".fm-item:not([hidden])");
          ul.hidden = !any;
          var sub = ul.previousElementSibling;
          if(sub && sub.classList.contains("fm-sub")) sub.hidden = !any;
        });
        g.hidden = n === 0;
        shown += n;
      });
      if(count) count.textContent = "แสดง " + shown + " รายการ";
      if(empty) empty.hidden = shown !== 0;
    }

    Array.prototype.forEach.call(chips, function(chip){
      chip.addEventListener("click", function(){
        state.cat = chip.getAttribute("data-value");
        pressChips(chips, state.cat);
        apply();
      });
    });
    if(input) input.addEventListener("input", function(){ state.q = input.value; apply(); });
  }

  // staff-deans-office.html — หน้าตาเดียวกับ faculty.html: ค้นหาชื่อ/หน้าที่ + ชิปงาน, การ์ดแบ่งตามงาน (data: BAS_STAFF)
  function initStaffDirectory(){
    var root = document.querySelector("[data-so-root]");
    if(!root || typeof BAS_STAFF === "undefined") return;
    var input = root.querySelector("[data-so-q]");
    var unitBox = root.querySelector("[data-so-units]");
    var list = root.querySelector("[data-so-list]");
    var empty = root.querySelector("[data-so-empty]");
    var clearTop = root.querySelector(".fd-clear");
    var state = { q: "", unit: "all" };

    function byQuery(){
      var q = state.q.trim().toLowerCase();
      return BAS_STAFF.filter(function(p){ return !q || (p.th + " " + p.en + " " + p.role + " " + (p.pos || "")).toLowerCase().indexOf(q) !== -1; });
    }
    function card(p){
      return '<article class="fd-card">' +
        '<div class="fd-card-photo"><img src="' + escHtml(p.img) + '" alt="' + escHtml(p.th) + '" loading="lazy" decoding="async"><span class="fd-card-role">' + escHtml(p.role) + '</span></div>' +
        '<div class="fd-card-body">' +
          '<h4 lang="en">' + escHtml(p.en) + '</h4>' +
          '<p>' + escHtml(p.th) + '</p>' +
          (p.pos ? '<p class="fd-card-pos">' + escHtml(p.pos) + '</p>' : '') +
          '<span class="fd-contact fd-contact--tel"><i class="fa-solid fa-phone" aria-hidden="true"></i>' + escHtml(p.tel) + '</span>' +
          '<a class="fd-contact fd-contact--sub" href="mailto:' + escHtml(p.mail) + '"><i class="fa-solid fa-envelope" aria-hidden="true"></i>' + escHtml(p.mail) + '</a>' +
        '</div></article>';
    }
    function render(){
      var byQ = byQuery();
      var shown = byQ.filter(function(p){ return state.unit === "all" || p.u === state.unit; });

      unitBox.innerHTML = [{ key:"all", short:"ทั้งหมด" }].concat(BAS_STAFF_UNITS).map(function(u){
        var n = byQ.filter(function(p){ return u.key === "all" || p.u === u.key; }).length;
        return '<button type="button" class="pg-chip fd-chip" data-so-unit="' + escHtml(u.key) + '" aria-pressed="' + (state.unit === u.key) + '">' +
          escHtml(u.short) + '<span class="pg-count">' + n + '</span></button>';
      }).join("");

      list.innerHTML = BAS_STAFF_UNITS.map(function(u){
        var ps = shown.filter(function(p){ return p.u === u.key; });
        if(!ps.length) return "";
        return '<div class="fd-dept">' +
          '<div class="fd-dept-head"><div><h2 lang="en">' + escHtml(u.en) + '</h2><p>' + escHtml(u.th) + '</p></div><span>' + ps.length + ' คน</span></div>' +
          '<div class="fd-grid">' + ps.map(card).join("") + '</div></div>';
      }).join("");

      var filtered = !!state.q.trim() || state.unit !== "all";
      empty.hidden = !!shown.length;
      clearTop.hidden = !filtered;
      setText("[data-so-result]", "แสดง " + shown.length + " จาก " + BAS_STAFF.length + " รายชื่อ");
    }
    root.addEventListener("click", function(e){
      var b = e.target.closest("[data-so-unit],[data-so-clear]");
      if(!b) return;
      if(b.hasAttribute("data-so-unit")){ state.unit = b.getAttribute("data-so-unit"); }
      else { state.q = ""; state.unit = "all"; input.value = ""; input.focus(); }
      render();
    });
    input.addEventListener("input", function(){ state.q = input.value; render(); });
    render();
  }

  /* ---- ปุ่มย้อนกลับ (404) ------------------------------------------------- */
  function initHistoryBack(){
    document.querySelectorAll("[data-history-back]").forEach(function(b){
      b.addEventListener("click", function(){
        if(window.history.length > 1) window.history.back(); else window.location.href = "index.html";
      });
    });
  }

  /* ---- FAQ accordion: เปิดได้ทีละข้อ ------------------------------------- */
  function initFaq(){
    function panelOf(btn){ return document.getElementById(btn.getAttribute("aria-controls") || ""); }
    document.querySelectorAll("[data-faq]").forEach(function(list){
      var btns = Array.prototype.slice.call(list.querySelectorAll(".ip-faq-btn"));
      btns.forEach(function(btn){
        btn.addEventListener("click", function(){
          var open = btn.getAttribute("aria-expanded") === "true";
          btns.forEach(function(b){
            b.setAttribute("aria-expanded", "false");
            var p = panelOf(b);
            if(p) p.hidden = true;
          });
          var panel = panelOf(btn);
          if(!open && panel){
            btn.setAttribute("aria-expanded", "true");
            panel.hidden = false;
          }
        });
      });
    });
  }

  /* ---- Global Partnerships: world map + partner list ---------------------- */
  function initGlobalMap(){
    var map = document.getElementById("gp-map");
    var detail = document.getElementById("gp-detail");
    var data = window.BAS_PARTNERS;
    if (map && detail && data){
      var pins = Array.prototype.slice.call(map.querySelectorAll(".gp-pin"));
      var byId = {};
      data.nodes.forEach(function(n){ byId[n.id] = n; });

      function render(node){
        var items = node.partners.map(function(p){
          return '<li>' + escHtml(p.name) + '<span class="gp-detail-type">' + escHtml(p.type) + '</span></li>';
        }).join("");
        detail.innerHTML =
          '<p class="gp-detail-country">' + escHtml(node.country) + '</p>' +
          '<p class="gp-detail-meta"><span>' + escHtml(node.region) + '</span><span aria-hidden="true">&middot;</span><span>' +
          node.count + (node.count === 1 ? ' partner' : ' partners') + '</span></p>' +
          '<ul class="gp-detail-list">' + items + '</ul>';
      }

      function select(id){
        var node = byId[id];
        if (!node) return;
        pins.forEach(function(b){
          var on = b.getAttribute("data-id") === id;
          b.classList.toggle("is-active", on);
          b.setAttribute("aria-pressed", String(on));
        });
        render(node);
      }

      pins.forEach(function(b){
        var id = b.getAttribute("data-id");
        b.setAttribute("aria-pressed", "false");
        b.addEventListener("click", function(){ select(id); });
        b.addEventListener("mouseenter", function(){ var n = byId[id]; if (n) render(n); });
        b.addEventListener("focus", function(){ select(id); });
      });
      map.addEventListener("mouseleave", function(){
        var active = map.querySelector(".gp-pin.is-active");
        var n = active ? byId[active.getAttribute("data-id")] : null;
        if (n) render(n);
      });

      // largest partner base first, so the panel is never empty on load
      var first = data.nodes.slice().sort(function(a,b){ return b.count - a.count; })[0];
      if (first){
        select(first.id);
        // on narrow screens the map scrolls inside its own box — start on the busiest region
        var col = map.closest(".gp-map-scroll") || map.parentElement;
        var pin = map.querySelector('.gp-pin[data-id="' + first.id + '"]');
        if (col && pin && col.scrollWidth > col.clientWidth){
          col.scrollLeft = pin.offsetLeft - col.clientWidth / 2;
        }
      }
    }

    var more = document.getElementById("gp-plist-more");
    var list = document.getElementById("gp-plist");
    if (more && list){
      more.addEventListener("click", function(){
        var open = more.getAttribute("aria-expanded") === "true";
        Array.prototype.forEach.call(list.children, function(li, i){
          if (i >= 6) li.hidden = open;
        });
        more.setAttribute("aria-expanded", String(!open));
        more.textContent = open ? (more.getAttribute("data-label-more") || "View all partners") : (more.getAttribute("data-label-less") || "Show fewer partners");
      });
    }

  }

  /* ---- Home: news category filter --------------------------------------------
     Markup ships the "all" state. Filtering hides cards that don't match and
     moves the first match into the feature slot, the rest into the row list. */
  function initHomeNews(){
    var chips = document.querySelector("[data-news-chips]");
    var grid = document.querySelector("[data-news]");
    if(!chips || !grid) return;
    var featureSlot = grid.querySelector("[data-news-feature]");
    var rowsSlot = grid.querySelector("[data-news-rows]");
    var empty = document.querySelector("[data-news-empty]");
    var status = document.querySelector("[data-news-status]");
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".hp-ncard[data-cat]"));
    var buttons = Array.prototype.slice.call(chips.querySelectorAll("[data-cat]"));

    function select(cat){
      pressChips(buttons, cat, "data-cat");
      var shown = cards.filter(function(c){ return cat === "all" || c.getAttribute("data-cat") === cat; });
      cards.forEach(function(c){ c.hidden = shown.indexOf(c) === -1; });
      shown.forEach(function(c, i){
        c.classList.toggle("is-feature", i === 0);
        (i === 0 ? featureSlot : rowsSlot).appendChild(c);
      });
      grid.hidden = !shown.length;
      if(empty) empty.hidden = !!shown.length;
      if(status) status.textContent = shown.length ? "แสดง " + shown.length + " ข่าว" : "ยังไม่มีข่าวในหมวดนี้";
    }
    buttons.forEach(function(b){
      b.addEventListener("click", function(){ select(b.getAttribute("data-cat")); });
    });
  }

  /* ---- Home: partner map pins -> country panel (data: BAS_PARTNERS) -------- */
  function initHomeMap(){
    var map = document.querySelector("[data-hp-map]");
    var panel = document.querySelector("[data-hp-country]");
    var data = window.BAS_PARTNERS;
    if(!map || !panel || !data) return;
    var byId = {};
    data.nodes.forEach(function(n){ byId[n.id] = n; });
    var pins = Array.prototype.slice.call(map.querySelectorAll(".hp-pin"));
    var SHOW = 4;

    function render(n){
      var orgs = n.partners.slice(0, SHOW).map(function(p){
        return '<li><p class="hp-org-name">' + escHtml(p.name) + '</p><p class="hp-org-type">' + escHtml(p.type) + '</p></li>';
      }).join("");
      panel.innerHTML =
        '<p class="hp-country-region" lang="en">' + escHtml(n.region) + '</p>' +
        '<div class="hp-country-head"><h3 lang="en">' + escHtml(n.country) + '</h3><span class="hp-country-count">' + n.count + ' องค์กร</span></div>' +
        '<ul class="hp-country-orgs" lang="en">' + orgs + '</ul>' +
        (n.count > SHOW ? '<a class="hp-link hp-country-more th-body" href="international.html#directory">ดูทั้งหมด ' + n.count +
          ' องค์กรใน Partner Directory <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>' : '');
    }
    pins.forEach(function(pin){
      pin.addEventListener("click", function(){
        var n = byId[pin.getAttribute("data-id")];
        if(!n) return;
        pins.forEach(function(p){
          var on = p === pin;
          p.classList.toggle("is-active", on);
          p.setAttribute("aria-pressed", String(on));
        });
        render(n);
      });
    });
  }

  function initHeaderScroll(){
    var header = document.querySelector(".site-header");
    if(!header) return;
    function onScroll(){
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    }
    onScroll();
    window.addEventListener("scroll", onScroll, {passive:true});
  }

  /* ---- Header mega menu: hover or click opens, Esc / mouse-leave closes ----- */
  function initMegaMenuKeyboard(){
    var header = document.querySelector(".site-header");
    var items = Array.prototype.slice.call(document.querySelectorAll(".nav-item"))
      .filter(function(item){ return item.querySelector(".hd-mega"); });
    if(!header || !items.length) return;

    function setOpen(item, open){
      item.classList.toggle("open", open);
      item.querySelector(".nav-link").setAttribute("aria-expanded", open ? "true" : "false");
    }
    function closeAll(except){
      items.forEach(function(o){ if(o !== except && o.classList.contains("open")) setOpen(o, false); });
    }
    window.BASSite.closeMega = function(){ closeAll(null); };

    items.forEach(function(item){
      var btn = item.querySelector(".nav-link");
      btn.addEventListener("mouseenter", function(){
        if(window.BASSite.closeSearch) window.BASSite.closeSearch();
        closeAll(item);
        setOpen(item, true);
      });
      btn.addEventListener("click", function(){
        var isOpen = item.classList.contains("open");
        if(window.BASSite.closeSearch) window.BASSite.closeSearch();
        closeAll(item);
        setOpen(item, !isOpen);
      });
      item.addEventListener("focusout", function(){
        window.setTimeout(function(){
          if(!item.contains(document.activeElement)) setOpen(item, false);
        }, 0);
      });
    });
    // hovering a plain link (News & Events) closes any open panel
    document.querySelectorAll(".nav-item > a.nav-link").forEach(function(a){
      a.addEventListener("mouseenter", function(){ closeAll(null); });
    });

    header.addEventListener("mouseleave", function(){ closeAll(null); });
    document.addEventListener("click", function(e){
      if(!e.target.closest(".nav-item")) closeAll(null);
    });
    document.addEventListener("keydown", function(e){
      if(e.key !== "Escape") return;
      var open = document.querySelector(".nav-item.open");
      if(!open) return;
      closeAll(null);
      if(open.contains(document.activeElement)) open.querySelector(".nav-link").focus();
    });
  }

  /* ---- Mobile drawer: modal dialog with focus trap + accordion ------------- */
  function initMobileDrawer(){
    var toggle = document.querySelector(".menu-toggle");
    var drawer = document.querySelector(".mobile-drawer");
    if(!toggle || !drawer) return;
    var panel = drawer.querySelector("[role='dialog']");
    var closeBtn = drawer.querySelector(".drawer-close");
    var scrim = drawer.querySelector(".drawer-scrim");
    var lastFocus = null;

    function focusables(){
      return Array.prototype.slice.call(panel.querySelectorAll("a[href], button:not([disabled]), input, [tabindex]:not([tabindex='-1'])"))
        .filter(function(el){ return el.offsetParent !== null; });
    }
    function isOpen(){ return !drawer.hidden; }
    function open(){
      lastFocus = document.activeElement;
      drawer.hidden = false;
      drawer.classList.add("open");
      toggle.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
      var first = panel.querySelector("button");
      if(first) first.focus();
    }
    function close(){
      if(!isOpen()) return;
      drawer.hidden = true;
      drawer.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      if(lastFocus && lastFocus.focus) lastFocus.focus();
      lastFocus = null;
    }
    toggle.addEventListener("click", open);
    if(closeBtn) closeBtn.addEventListener("click", close);
    if(scrim) scrim.addEventListener("click", close);

    document.addEventListener("keydown", function(e){
      if(!isOpen()) return;
      if(e.key === "Escape"){ close(); return; }
      if(e.key !== "Tab") return;
      var f = focusables();
      if(!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if(!panel.contains(document.activeElement)){ e.preventDefault(); first.focus(); }
      else if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    });

    // the drawer only exists below the desktop breakpoint — close it if the window grows
    var mqDesk = window.matchMedia("(min-width: 1200px)");
    function onDesk(){ if(mqDesk.matches) close(); }
    if(mqDesk.addEventListener) mqDesk.addEventListener("change", onDesk);

    var toggles = Array.prototype.slice.call(drawer.querySelectorAll("button.dr-toggle"));
    function setItem(btn, open){
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      var sub = document.getElementById(btn.getAttribute("aria-controls"));
      if(sub) sub.hidden = !open;
      var ico = btn.querySelector("i");
      if(ico){ ico.classList.toggle("fa-plus", !open); ico.classList.toggle("fa-minus", open); }
    }
    toggles.forEach(function(btn){
      btn.addEventListener("click", function(){
        var wasOpen = btn.getAttribute("aria-expanded") === "true";
        toggles.forEach(function(b){ setItem(b, false); });
        setItem(btn, !wasOpen);
      });
    });
  }

  function initSearchPanel(){
    var btn = document.querySelector(".search-toggle");
    var panel = document.querySelector(".search-panel");
    if(!btn || !panel) return;
    var form = panel.querySelector("form");
    var input = panel.querySelector("input");
    function setOpen(open){
      panel.hidden = !open;
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    window.BASSite.closeSearch = function(){ setOpen(false); };
    btn.addEventListener("click", function(){
      var open = panel.hidden;
      if(open && window.BASSite.closeMega) window.BASSite.closeMega();
      setOpen(open);
      if(open && input){ input.focus(); }
    });
    document.addEventListener("keydown", function(e){
      if(e.key === "Escape" && !panel.hidden){
        var inside = panel.contains(document.activeElement);
        setOpen(false);
        if(inside) btn.focus();
      }
    });
    if(form){
      form.addEventListener("submit", function(e){
        e.preventDefault();
        var q = input ? input.value.trim() : "";
        if(q){ window.location.href = "programs.html?search=" + encodeURIComponent(q); }
      });
    }
  }

  function initMarqueeClone(){
    document.querySelectorAll(".marquee-track").forEach(function(track){
      if(track.dataset.cloned) return;
      // ชุดที่ 2 ไว้ให้เลื่อนวนต่อเนื่อง — ซ่อนจาก screen reader และซ่อนเมื่อผู้ใช้ลดการเคลื่อนไหว (ดู CSS)
      Array.prototype.slice.call(track.children).forEach(function(item){
        var copy = item.cloneNode(true);
        copy.setAttribute("aria-hidden", "true");
        copy.querySelectorAll("a, button").forEach(function(el){ el.tabIndex = -1; });
        track.appendChild(copy);
      });
      track.dataset.cloned = "true";
    });
  }

  // R2 · International: แบ่งโลโก้พันธมิตรเป็น 2 แถว (ซ้าย ~40px/s, ขวา ~32px/s) แต่ละแถวมีชุดซ้ำ aria-hidden
  // ใช้ margin-right ต่อการ์ดแทน gap → ครึ่งหนึ่งของ scrollWidth = 1 รอบพอดี จึงวนต่อได้ไม่สะดุด
  function initPartnerMarquee(){
    var box = document.querySelector("[data-partner-marquee]");
    if(!box) return;
    var list = box.querySelector(".it-mq-list");
    if(!list || (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches)) return;

    var items = Array.prototype.slice.call(list.children);
    var cut = Math.ceil(items.length / 2);
    var rows = [items.slice(0, cut), items.slice(cut)].map(function(group, i){
      var ul = document.createElement("ul");
      ul.className = "it-mq-row";
      group.forEach(function(li){ ul.appendChild(li); });
      group.forEach(function(li){
        var copy = li.cloneNode(true);
        copy.setAttribute("aria-hidden", "true");
        copy.querySelectorAll("a, button").forEach(function(el){ el.tabIndex = -1; });
        ul.appendChild(copy);
      });
      return { el: ul, dir: i === 0 ? -1 : 1, speed: i === 0 ? 40 : 32, x: 0, half: 0 };
    });
    list.replaceWith(rows[0].el, rows[1].el);
    box.classList.add("is-moving");

    function measure(){
      rows.forEach(function(r){ r.half = r.el.scrollWidth / 2; });
      if(!rows[1].x) rows[1].x = -rows[1].half; // แถว 2 เริ่มที่ -half แล้วเลื่อนไปทางขวา
    }
    measure();
    window.addEventListener("resize", measure);
    window.addEventListener("load", measure);

    var last = 0, raf = 0;
    function frame(t){
      var dt = last ? Math.min(t - last, 64) / 1000 : 0;
      last = t;
      rows.forEach(function(r){
        if(!r.half) return;
        r.x += r.dir * r.speed * dt;
        // แถว 1: 0 → -half · แถว 2: -half → 0 แล้ววนกลับ
        if(r.x <= -r.half) r.x += r.half;
        if(r.x > 0) r.x -= r.half;
        r.el.style.transform = "translate3d(" + r.x + "px,0,0)";
      });
      raf = requestAnimationFrame(frame);
    }
    raf = requestAnimationFrame(frame);
    window.addEventListener("pagehide", function(){ cancelAnimationFrame(raf); });
  }

  // R4 · Student Life: การ์ดองค์กรและชมรมนิสิตจาก BAS_CLUBS (data.js)
  // เมื่อคณะส่งข้อมูล: desc แทนบรรทัดรอข้อมูล · href ทำให้ทั้งการ์ดเป็นลิงก์ · img แสดงด้านบน 16:9
  function initClubs(){
    var grid = document.querySelector("[data-clubs]");
    if(!grid || !window.BAS_CLUBS) return;
    grid.innerHTML = window.BAS_CLUBS.map(function(c, i){
      var ext = c.href && /^https?:/.test(c.href);
      var name = c.href
        ? '<a href="' + escHtml(c.href) + '"' + (ext ? ' target="_blank" rel="noopener"' : '') + '>' + escHtml(c.en) + (ext ? '<span class="sr-only"> (เปิดในแท็บใหม่)</span>' : '') + '</a>'
        : escHtml(c.en);
      var foot = c.desc
        ? '<p class="sl-orgc-foot">' + escHtml(c.desc) + '</p>'
        : '<p class="sl-orgc-foot"><i class="fa-regular fa-clock" aria-hidden="true"></i>รายละเอียด รูป และลิงก์ รอข้อมูลจากคณะ</p>';
      return '<li class="sl-orgc">' +
        (c.img ? '<img class="sl-orgc-img" src="' + escHtml(c.img) + '" alt="" loading="lazy" decoding="async">' : '') +
        '<div class="sl-orgc-top"><span class="sl-orgc-ico"><i class="fa-solid ' + escHtml(c.icon) + '" aria-hidden="true"></i></span>' +
        '<span class="sl-orgc-no" aria-hidden="true">' + String(i + 1).padStart(2, "0") + '</span></div>' +
        '<div><h3 class="sl-orgc-name" lang="en">' + name + '</h3>' +
        (c.th ? '<p class="sl-orgc-th">' + escHtml(c.th) + '</p>' : '') + '</div>' +
        foot + '</li>';
    }).join("");
  }

  function initScrollReveal(){
    var items = document.querySelectorAll(".reveal");
    if(!items.length) return;
    if(!("IntersectionObserver" in window)){
      items.forEach(function(el){ el.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting){
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, {threshold:.14, rootMargin:"0px 0px -40px 0px"});
    items.forEach(function(el){ io.observe(el); });
  }

  function initStaffToggle(){
    var toggle = document.querySelector(".staff-toggle");
    if(!toggle) return;
    var buttons = toggle.querySelectorAll("button");
    buttons.forEach(function(btn){
      btn.addEventListener("click", function(){
        buttons.forEach(function(b){ b.setAttribute("aria-pressed","false"); });
        btn.setAttribute("aria-pressed","true");
        var variant = btn.getAttribute("data-variant");
        document.querySelectorAll(".staff-card").forEach(function(card){
          card.classList.toggle("staff-name-a", variant === "a");
          card.classList.toggle("staff-name-b", variant === "b");
        });
      });
    });
  }

  // หา object แรกใน list ที่ field ตรงกับค่า (list อาจไม่มี เช่น data.js ไม่ได้โหลด)
  function findBy(list, key, val){
    return (list || []).filter(function(x){ return x && x[key] === val; })[0];
  }

  function qs(name){
    var params = new URLSearchParams(window.location.search);
    return params.get(name);
  }

  function initProgramsFinder(){
    var root = document.querySelector("[data-pg-finder]");
    if(!root || typeof BAS_PROGRAMS === "undefined") return;
    var grid = root.querySelector("[data-pg-grid]");
    var input = root.querySelector("[data-pg-q]");
    var chips = root.querySelectorAll("[data-pg-level]");
    var empty = root.querySelector("[data-pg-empty]");
    var state = {
      level: qs("level") === "graduate" || qs("level") === "undergraduate" ? qs("level") : "all",
      q: qs("search") || ""
    };
    input.value = state.q;
    function matches(p, q){
      if(!q) return true;
      return [p.abbr, p.name_th, p.name_en, p.summary, p.summary_en, p.level_label, p.language]
        .concat(p.careers).join(" ").toLowerCase().indexOf(q) !== -1;
    }
    function filtered(level){
      var q = state.q.trim().toLowerCase();
      return BAS_PROGRAMS.filter(function(p){ return (level === "all" || p.level === level) && matches(p, q); });
    }
    function card(p){
      var ext = !!p.external_url;
      var attrs = ext
        ? 'href="' + escHtml(p.external_url) + '" target="_blank" rel="noopener" aria-label="' + escHtml(p.abbr + " " + p.name_th) + ' (เว็บไซต์ภายนอก เปิดในแท็บใหม่)"'
        : 'href="program-detail.html?p=' + p.slug + '"';
      return '<a class="pg-card" ' + attrs + '>' +
        '<div class="pg-card-media"><img src="assets/media/program-' + p.slug + '.jpg" alt="" loading="lazy" decoding="async"><span class="pg-card-level">' + escHtml(p.level_label) + '</span></div>' +
        '<div class="pg-card-body">' +
          '<h3 class="pg-card-abbr" lang="en">' + escHtml(p.abbr) + '</h3>' +
          '<p class="pg-card-th">' + escHtml(p.name_th) + '</p>' +
          '<p class="pg-card-desc">' + escHtml(p.summary) + '</p>' +
          '<div class="pg-card-foot">' +
            '<span class="pg-card-cue">' + (ext ? 'ไปเว็บไซต์หลักสูตร <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>' : 'ดูรายละเอียดหลักสูตร <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>') + '</span>' +
            '<span class="pg-card-lang"><i class="fa-solid fa-language" aria-hidden="true"></i>' + escHtml(p.language) + '</span>' +
          '</div>' +
        '</div></a>';
    }
    function render(){
      var list = filtered(state.level);
      chips.forEach(function(chip){
        var lv = chip.getAttribute("data-pg-level");
        chip.setAttribute("aria-pressed", lv === state.level ? "true" : "false");
        chip.querySelector("[data-pg-count]").textContent = filtered(lv).length;
      });
      grid.innerHTML = list.map(card).join("");
      grid.hidden = !list.length;
      empty.hidden = !!list.length;
      setText("[data-pg-empty-q]", state.q);
      setText("[data-pg-result]", "แสดง " + list.length + " จาก " + BAS_PROGRAMS.length + " หลักสูตร");
    }
    chips.forEach(function(chip){
      chip.addEventListener("click", function(){ state.level = chip.getAttribute("data-pg-level"); render(); });
    });
    input.addEventListener("input", function(){ state.q = input.value; render(); });
    root.querySelector("[data-pg-clear]").addEventListener("click", function(){
      state.q = ""; state.level = "all"; input.value = ""; render(); input.focus();
    });
    var showGrad = document.querySelector("[data-pg-show-grad]");
    if(showGrad){
      showGrad.addEventListener("click", function(){
        state.level = "graduate"; state.q = ""; input.value = ""; render();
        window.scrollTo({ top: root.getBoundingClientRect().top + window.scrollY - 80, behavior: "smooth" });
      });
    }
    render();
  }

  function initProgramDetail(){
    var root = document.querySelector("[data-program-detail]");
    if(!root || typeof BAS_PROGRAMS === "undefined") return;
    var slug = qs("p");
    if(slug === "phd"){ window.location.replace("https://mba.swu.ac.th/phd"); return; }
    if(slug === "bba-tourism-hotel") slug = "bba-tourism"; // ลิงก์เก่าก่อนแยกท่องเที่ยว/โรงแรม
    var program = BAS_PROGRAMS.find(function(p){ return p.slug === slug; }) || BAS_PROGRAMS[0];
    function imgFor(p){ return "assets/media/program-" + p.slug + ".jpg"; }
    function deptKeyOf(p){ return window.BAS_PROGRAM_DEPT && BAS_PROGRAM_DEPT[p.slug]; }
    function deptOf(p){ var k = deptKeyOf(p); return k ? findBy(window.BAS_DEPTS, "key", k) : null; }

    document.title = program.abbr + " — BAS SWU";
    setText("[data-p-abbr]", program.abbr);
    setText("[data-p-level]", program.level_label);
    setText("[data-p-name-en]", program.name_en.replace(" -- ", " — "));
    setText("[data-p-name-th]", program.name_th);
    setText("[data-p-summary]", program.summary);
    setText("[data-p-summary-en]", program.summary_en);
    var heroImg = root.querySelector("[data-p-img]");
    if(heroImg) heroImg.src = imgFor(program);

    // ปุ่มสมัครใหญ่ใต้ hero — แสดงเฉพาะหลักสูตรที่มี apply_url (ตอนนี้: GBM)
    var applyBox = root.querySelector("[data-p-apply]");
    if(applyBox && program.apply_url){
      root.querySelector("[data-p-apply-link]").href = program.apply_url;
      setText("[data-p-apply-name]", program.abbr);
      applyBox.hidden = false;
    }

    var facts = root.querySelector("[data-p-facts]");
    if(facts){
      facts.innerHTML = [
        ["Level", "fa-graduation-cap", program.level_label],
        ["Language", "fa-language", program.language],
        ["Department", "fa-building-columns", deptOf(program) ? deptOf(program).th : ""],
        ["Curriculum", "fa-book-open", program.curriculum_label]
      ].filter(function(f){ return f[2]; })
      .map(function(f){
        return '<div><dt><i class="fa-solid ' + f[1] + '" aria-hidden="true"></i>' + f[0] + '</dt><dd>' + escHtml(f[2]) + '</dd></div>';
      }).join("");
    }

    // เอกสารหลักสูตร (PDF บน bas2.swu.ac.th) — ไม่มีเอกสาร → คงป้าย "อยู่ระหว่างปรับปรุง"
    var docsBox = root.querySelector("[data-p-docs]");
    if(docsBox && program.docs && program.docs.length){
      root.querySelector("[data-p-docs-list]").innerHTML = program.docs.map(function(d){
        return '<li><a class="pd-doc" href="' + escHtml(d.href) + '" target="_blank" rel="noopener">' +
          '<i class="fa-regular fa-file-pdf" aria-hidden="true"></i><span><span class="pd-doc-t">' + escHtml(d.t) + '</span>' +
          '<span class="pd-doc-en" lang="en">' + escHtml(d.en) + '</span></span>' +
          '<i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i><span class="sr-only"> (PDF เปิดในแท็บใหม่)</span></a></li>';
      }).join("");
      docsBox.hidden = false;
      var docsNote = root.querySelector("[data-p-docs-note]");
      if(docsNote) docsNote.hidden = true;
    }

    var careerList = root.querySelector("[data-p-careers]");
    if(careerList){
      careerList.innerHTML = program.careers.map(function(c){
        return '<li><span class="pd-career-ico"><i class="fa-solid fa-briefcase" aria-hidden="true"></i></span>' + escHtml(c) + '</li>';
      }).join("");
    }

    // ค่าเล่าเรียน — program.fee { amount, unit, note, src } · ป.ตรีเก็บรายภาค (8 ภาค), บัณฑิตศึกษาเหมาจ่ายตลอดหลักสูตร
    var feeSec = root.querySelector("#tuition");
    if(feeSec){
      var fee = program.fee || {};
      var feeNum = fee.amount ? Number(String(fee.amount).replace(/,/g, "")) : null;
      var perTerm = !fee.unit || /ภาค/.test(fee.unit);
      var feeTerms = perTerm && program.level === "undergraduate" ? 8 : null;
      var feeYear = (String(fee.src || "").match(/25\d\d/) || [])[0];
      var baht = function(n){ return n == null || isNaN(n) ? "—" : "฿" + n.toLocaleString("en-US"); };
      setText("[data-f-label]", perTerm ? "ต่อภาคการศึกษา · เหมาจ่าย" : "ตลอดหลักสูตร · เหมาจ่าย");
      setText("[data-f-amount]", feeNum ? feeNum.toLocaleString("en-US") : "—");
      setText("[data-f-unit]", perTerm ? "บาท / ภาคการศึกษา" : "บาท / ตลอดหลักสูตร");
      setText("[data-f-intro]", (perTerm ? "อัตราค่าเล่าเรียนแบบเหมาจ่ายรายภาคการศึกษา" : "อัตราค่าเล่าเรียนแบบเหมาจ่ายตลอดหลักสูตร") +
        (feeYear ? " สำหรับนิสิตที่เข้าศึกษาปีการศึกษา " + feeYear : ""));
      if(fee.src) setText("[data-f-src]", "อ้างอิง" + fee.src + " — อัตราอาจเปลี่ยนแปลงตามประกาศของมหาวิทยาลัย");
      var feeNote = feeSec.querySelector("[data-f-note]");
      if(feeNote && fee.note){ feeNote.textContent = fee.note; feeNote.hidden = false; }
      var feePending = feeSec.querySelector("[data-f-pending]");
      if(feePending){
        feePending.hidden = !!feeNum;
        setText("[data-f-pending-t]", "อยู่ระหว่างยืนยันอัตรา" + (feeYear ? "ปีการศึกษา " + feeYear : "ค่าเล่าเรียน"));
      }
      var feeRows = feeSec.querySelector("[data-f-rows]");
      if(feeRows){
        feeRows.innerHTML = [
          ["จำนวนภาคการศึกษา", feeTerms ? feeTerms + " ภาค" : "—"],
          ["ตลอดหลักสูตร (ประมาณ)", baht(feeNum && (feeTerms ? feeNum * feeTerms : (perTerm ? null : feeNum)))],
          fee.entry != null && ["ค่าธรรมเนียมแรกเข้า", baht(fee.entry)],
          fee.summer != null && ["ภาคฤดูร้อน", baht(fee.summer)]
        ].filter(Boolean).map(function(r){
          return '<div><dt>' + r[0] + '</dt><dd>' + escHtml(r[1]) + '</dd></div>';
        }).join("");
      }
    }

    // department contact — BAS_DEPT_HEADS เก็บแค่ pid + focus, ที่เหลือดึงจากข้อมูลบุคลากร/ภาควิชา
    var deptSec = root.querySelector("[data-p-dept]");
    var deptKey = window.BAS_PROGRAM_DEPT && BAS_PROGRAM_DEPT[program.slug];
    var deptInfo = deptKey && window.BAS_DEPT_HEADS && BAS_DEPT_HEADS[deptKey];
    var dept = deptInfo && findBy(window.BAS_DEPTS, "key", deptKey);
    var head = deptInfo && findBy(window.BAS_PEOPLE, "id", deptInfo.pid);
    if(deptSec && dept && head){
      var leader = findBy(window.BAS_LEADERSHIP, "email", head.mail);
      var img = deptSec.querySelector("[data-d-img]");
      var profile = deptSec.querySelector("[data-d-profile]");
      var mailto = deptSec.querySelector("[data-d-mailto]");
      setText("[data-d-en]", dept.en);
      setText("[data-d-th]", dept.th);
      setText("[data-d-focus]", deptInfo.focus);
      setText("[data-d-head]", leader ? leader.name : head.th);
      setText("[data-d-mail]", head.mail);
      if(img) img.src = head.img;
      if(profile) profile.href = "profile.html?p=" + encodeURIComponent(head.id);
      if(mailto) mailto.href = "mailto:" + head.mail;
      deptSec.hidden = false;
    }

    // related: same department first, then other departments at the same level (max 3)
    var rest = BAS_PROGRAMS.filter(function(p){ return p.slug !== program.slug; });
    var myDept = deptKeyOf(program);
    var related = rest.filter(function(p){ return myDept && deptKeyOf(p) === myDept; })
      .concat(rest.filter(function(p){ return deptKeyOf(p) !== myDept && p.level === program.level; }))
      .slice(0, 3);
    var relatedWrap = root.querySelector("[data-p-related]");
    if(relatedWrap){
      relatedWrap.innerHTML = related.map(function(p){
        var href = p.external_url
          ? escHtml(p.external_url) + '" target="_blank" rel="noopener'
          : 'program-detail.html?p=' + p.slug;
        return '<a class="pd-card" href="' + href + '">' +
          '<div class="pd-card-media"><img src="' + imgFor(p) + '" alt="" loading="lazy" decoding="async"></div>' +
          '<div class="pd-card-body"><span class="pd-card-level">' + escHtml(p.level_label) + '</span>' +
          '<h3 class="pd-card-abbr">' + escHtml(p.abbr) + (p.external_url ? ' <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>' : '') + '</h3>' +
          '<p class="pd-card-th">' + escHtml(p.name_th) + '</p></div></a>';
      }).join("");
    }
  }

  function escHtml(v){
    return String(v == null ? "" : v).replace(/[&<>"']/g, function(c){
      return { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c];
    });
  }

  // faculty.html — ค้นหาชื่อ + กรองภาควิชา/ความเชี่ยวชาญ, การ์ดลิงก์ไป profile.html?p=<id> (ยกเว้นผู้ประสานงาน: hover ได้แต่กดไม่ได้)
  function initFacultyDirectory(){
    var root = document.querySelector("[data-fd-root]");
    if(!root || typeof BAS_DIRECTORY === "undefined") return;
    var input = root.querySelector("[data-fd-q]");
    var deptBox = root.querySelector("[data-fd-depts]");
    var groupBox = root.querySelector("[data-fd-groups]");
    var list = root.querySelector("[data-fd-list]");
    var empty = root.querySelector("[data-fd-empty]");
    var clearTop = root.querySelector(".fd-clear");
    var state = { q: qs("q") || "", dept: "all", grp: "all" };
    if(BAS_DEPTS.some(function(d){ return d.key === qs("dept"); })) state.dept = qs("dept");
    input.value = state.q;

    function byQuery(){
      var q = state.q.trim().toLowerCase();
      return BAS_DIRECTORY.filter(function(p){ return !q || (p.en + " " + p.th).toLowerCase().indexOf(q) !== -1; });
    }
    // คนเดียวอาจอยู่หลายภาควิชา (เช่นผู้ประสานงาน) → นับจำนวนคนตาม id ไม่ใช่จำนวนรายการ
    function uniqCount(ps){
      var seen = {};
      return ps.filter(function(p){ return seen[p.id] ? false : (seen[p.id] = true); }).length;
    }
    function chip(attr, key, label, count, on){
      return '<button type="button" class="pg-chip fd-chip" ' + attr + '="' + escHtml(key) + '" aria-pressed="' + on + '">' +
        escHtml(label) + '<span class="pg-count">' + count + '</span></button>';
    }
    function card(p){
      var contact = p.mail
        ? '<a class="fd-contact" href="mailto:' + escHtml(p.mail) + '"><i class="fa-solid fa-envelope" aria-hidden="true"></i>' + escHtml(p.mail) + '</a>'
        : (p.tel ? '<span class="fd-contact"><i class="fa-solid fa-phone" aria-hidden="true"></i>' + escHtml(p.tel) + '</span>' : '');
      return '<article class="fd-card">' +
        '<div class="fd-card-photo"><img src="' + escHtml(p.img) + '" alt="' + escHtml(p.th) + '" loading="lazy" decoding="async"><span class="fd-card-role">' + escHtml(p.role) + '</span></div>' +
        '<div class="fd-card-body">' +
          '<h4 lang="en">' + (p.ge === "Coordinators" ? escHtml(p.en)
            : '<a class="fd-card-link" href="profile.html?p=' + encodeURIComponent(p.id) + '">' + escHtml(p.en) + '</a>') + '</h4>' +
          '<p>' + escHtml(p.th) + '</p>' + contact +
        '</div></article>';
    }
    function render(){
      var byQ = byQuery();
      var inDept = byQ.filter(function(p){ return state.dept === "all" || p.d === state.dept; });
      var shown = inDept.filter(function(p){ return state.grp === "all" || p.ge === state.grp; });

      deptBox.innerHTML = [{ key:"all", short:"ทุกภาควิชา" }].concat(BAS_DEPTS).map(function(d){
        return chip("data-fd-dept", d.key, d.short, uniqCount(byQ.filter(function(p){ return d.key === "all" || p.d === d.key; })), state.dept === d.key);
      }).join("");

      groupBox.hidden = state.dept === "all";
      if(!groupBox.hidden){
        var names = [];
        BAS_DIRECTORY.forEach(function(p){ if(p.d === state.dept && names.indexOf(p.ge) === -1) names.push(p.ge); });
        groupBox.innerHTML = '<span class="fd-chips-label">ความเชี่ยวชาญ</span>' + ["all"].concat(names).map(function(g){
          var label = g === "all" ? "ทั้งหมด" : (g === "Coordinators" ? "ผู้ประสานงาน" : g);
          return chip("data-fd-grp", g, label, inDept.filter(function(p){ return g === "all" || p.ge === g; }).length, state.grp === g);
        }).join("");
      }

      list.innerHTML = BAS_DEPTS.map(function(d){
        var ps = shown.filter(function(p){ return p.d === d.key; });
        if(!ps.length) return "";
        var groups = [];
        ps.forEach(function(p){
          var g = groups.filter(function(x){ return x.en === p.ge; })[0];
          if(!g){ g = { en:p.ge, th:p.gt, people:[] }; groups.push(g); }
          g.people.push(p);
        });
        return '<div class="fd-dept">' +
          '<div class="fd-dept-head"><div><h2 lang="en">' + escHtml(d.en) + '</h2><p>' + escHtml(d.th) + '</p></div><span>' + ps.length + ' คน</span></div>' +
          groups.map(function(g){
            return '<div class="fd-group"><h3><span lang="en">' + escHtml(g.en) + '</span><span class="fd-group-th">' + escHtml(g.th) + '</span></h3>' +
              '<div class="fd-grid">' + g.people.map(card).join("") + '</div></div>';
          }).join("") + '</div>';
      }).join("");

      var filtered = !!state.q.trim() || state.dept !== "all" || state.grp !== "all";
      empty.hidden = !!shown.length;
      clearTop.hidden = !filtered;
      setText("[data-fd-result]", "แสดง " + uniqCount(shown) + " จาก " + uniqCount(BAS_DIRECTORY) + " รายชื่อ");
    }
    root.addEventListener("click", function(e){
      var b = e.target.closest("[data-fd-dept],[data-fd-grp],[data-fd-clear]");
      if(!b) return;
      if(b.hasAttribute("data-fd-dept")){ state.dept = b.getAttribute("data-fd-dept"); state.grp = "all"; }
      else if(b.hasAttribute("data-fd-grp")){ state.grp = b.getAttribute("data-fd-grp"); }
      else { state.q = ""; state.dept = "all"; state.grp = "all"; input.value = ""; input.focus(); }
      render();
    });
    input.addEventListener("input", function(){ state.q = input.value; render(); });
    render();
  }

  // profile.html?p=<id> — ส่วนที่ยังไม่มีข้อมูลจะไม่แสดง (ประวัติการศึกษาแสดง "ข้อมูลอยู่ระหว่างปรับปรุง")
  function initProfile(){
    var root = document.querySelector("[data-profile]");
    if(!root || typeof BAS_PEOPLE === "undefined") return;
    var body = root.querySelector("[data-pf-body]");
    var id = qs("p");
    var P = BAS_PEOPLE.filter(function(x){ return x.id === id; })[0];
    var back = P && P.leader
      ? { href:"leadership.html", label:"Leadership", text:"กลับไปหน้าผู้บริหารทั้งหมด" }
      : { href:"faculty.html", label:"Faculty & Staff", text:"กลับไปหน้าคณาจารย์และบุคลากร" };
    var crumbBack = root.querySelector("[data-pf-back-crumb]");
    crumbBack.href = back.href; crumbBack.textContent = back.label;
    var backLink = '<a class="pf-back" href="' + back.href + '"><i class="fa-solid fa-arrow-left" aria-hidden="true"></i>' + back.text + '</a>';

    if(!P){
      setText("[data-pf-crumb]", "ไม่พบข้อมูล");
      document.title = "ไม่พบข้อมูลบุคลากร — BAS SWU";
      body.innerHTML = '<div class="pg-empty pf-missing"><p>ไม่พบข้อมูลบุคลากรที่ต้องการ</p>' +
        '<p class="pf-missing-sub">ลิงก์อาจไม่ถูกต้องหรือข้อมูลถูกย้าย ลองค้นหาจากรายชื่อคณาจารย์ทั้งหมด</p></div>' + backLink;
      return;
    }

    setText("[data-pf-crumb]", P.en);
    document.title = P.th + " — " + (P.leader ? "ผู้บริหาร" : "คณาจารย์") + " BAS SWU";
    var meta = [["fa-solid fa-building-columns", P.dept], ["fa-solid fa-envelope", P.mail, P.mail && "mailto:" + P.mail], ["fa-solid fa-building", P.office]]
      .filter(function(m){ return m[1]; })
      .map(function(m){
        return '<li><span class="pf-ico" aria-hidden="true"><i class="' + m[0] + '"></i></span>' +
          (m[2] ? '<a href="' + escHtml(m[2]) + '">' + escHtml(m[1]) + '</a>' : '<span>' + escHtml(m[1]) + '</span>') + '</li>';
      }).join("");
    var icons = { "การรับรองวิชาชีพ":"fa-solid fa-award", "ความเชี่ยวชาญ":"fa-solid fa-lightbulb", "ประวัติย่อ":"fa-solid fa-file-lines" };
    var facts = [["การรับรองวิชาชีพ","Certification"], ["ความเชี่ยวชาญ","Expertise"], ["ประวัติย่อ","CV"]].map(function(k){
      var f = P.facts.filter(function(x){ return x.k === k[0]; })[0];
      if(!f || !(f.v || f.href)) return "";
      var v = f.href
        ? '<a class="pf-cv" href="' + escHtml(f.href) + '" target="_blank" rel="noopener" aria-label="ดาวน์โหลด CV ของ' + escHtml(P.th) + ' (ไฟล์ PDF เปิดในแท็บใหม่)"><i class="fa-solid fa-file-pdf" aria-hidden="true"></i>ดาวน์โหลด CV<i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>'
        : '<p>' + escHtml(f.v) + '</p>';
      return '<div class="pf-fact"><div class="pf-fact-k"><span class="pf-ico" aria-hidden="true"><i class="' + icons[k[0]] + '"></i></span>' +
        '<h3><span>' + k[0] + '</span><span class="pf-fact-en" lang="en">' + k[1] + '</span></h3></div><div class="pf-fact-v">' + v + '</div></div>';
    }).join("");
    var edu = P.edu.length
      ? P.edu.map(function(e){ return '<li><span class="pf-edu-dot" aria-hidden="true"></span><span><span class="pf-edu-deg">' + escHtml(e[0]) + '</span><span class="pf-edu-inst">' + escHtml(e[1]) + '</span></span></li>'; }).join("")
      : '<li class="pf-edu-pending"><span class="pf-edu-dot" aria-hidden="true"></span><span>ข้อมูลอยู่ระหว่างปรับปรุง</span></li>';

    body.innerHTML =
      '<div class="pf-card">' +
        '<span class="pf-ring" aria-hidden="true"></span><span class="pf-blob" aria-hidden="true"></span>' +
        '<div class="pf-photo"><img src="' + escHtml(P.img) + '" alt="' + escHtml(P.th) + '" decoding="async"></div>' +
        '<div class="pf-copy">' +
          '<p class="pf-role"><span class="pf-role-bar" aria-hidden="true"></span>' + escHtml(P.roleTh) + (P.roleEn ? '<span lang="en">' + escHtml(P.roleEn) + '</span>' : '') + '</p>' +
          '<h1 lang="en">' + escHtml(P.en) + '</h1>' +
          '<p class="pf-th">' + escHtml(P.th) + '</p>' +
          '<ul class="pf-meta">' + meta + '</ul>' +
        '</div>' +
      '</div>' +
      '<div class="pf-edu"><h2>ประวัติการศึกษา</h2><p class="pf-h2-en" lang="en">Academic background</p><ul>' + edu + '</ul></div>' +
      (facts ? '<div class="pf-facts">' + facts + '</div>' : '') +
      backLink;
  }

  function newsCard(n){
    return '<a class="nw-card" href="news-detail.html?n=' + encodeURIComponent(n.slug) + '">' +
      '<div class="nw-card-media"><img src="' + escHtml(n.img) + '" alt="" loading="lazy" decoding="async"></div>' +
      '<div class="nw-card-body"><div class="nw-card-meta"><span>' + escHtml(n.tag) + '</span><time>' + escHtml(n.date) + '</time></div>' +
      '<h3>' + escHtml(n.title) + '</h3></div></a>';
  }

  /* ---- News list: ข่าวเด่น + ชิปหมวด + ค้นหา ------------------------------ */
  function initNewsList(){
    var root = document.querySelector("[data-news-list]");
    var news = window.BAS_NEWS;
    if(!root || !news || !news.length) return;
    var featWrap = root.querySelector("[data-nw-feature]");
    var catWrap = root.querySelector("[data-nw-cats]");
    var input = root.querySelector("[data-nw-q]");
    var grid = root.querySelector("[data-nw-grid]");
    var count = root.querySelector("[data-nw-count]");
    var empty = root.querySelector("[data-nw-empty]");
    var clear = root.querySelector("[data-nw-clear]");
    if(!grid) return;
    // แสดงเฉพาะหมวดที่มีข่าวจริง — ไม่มีชิปที่กดแล้วว่างเปล่า
    var cats = (window.BAS_NEWS_CATS || [["all", "ทั้งหมด"]]).filter(function(c){
      return c[0] === "all" || news.some(function(n){ return n.cat === c[0]; });
    });
    var requested = qs("cat");
    var state = { cat: "all", q: "" };
    if(requested){
      if(cats.some(function(c){ return c[0] === requested; })) state.cat = requested;
      else dropParam("cat"); // ?cat= ไม่รู้จัก/ยังไม่มีข่าว → แสดงทั้งหมด และไม่ค้าง param ผิดใน URL
    }

    if(catWrap){
      catWrap.innerHTML = cats.map(function(c){
        return '<button type="button" class="pg-chip" data-value="' + escHtml(c[0]) + '" aria-pressed="false">' + escHtml(c[1]) + '</button>';
      }).join("");
      catWrap.addEventListener("click", function(e){
        var b = e.target.closest("[data-value]");
        if(!b) return;
        state.cat = b.getAttribute("data-value");
        render();
      });
    }
    var f = news[0];
    if(featWrap){
      featWrap.innerHTML = '<a class="nw-feat" href="news-detail.html?n=' + encodeURIComponent(f.slug) + '">' +
        '<div class="nw-feat-media"><img src="' + escHtml(f.img) + '" alt=""></div>' +
        '<div class="nw-feat-body"><div class="nw-feat-meta"><span class="nw-feat-new">ล่าสุด</span><span class="nw-feat-tag">' + escHtml(f.tag) + '</span><time>' + escHtml(f.date) + '</time></div>' +
        '<h2>' + escHtml(f.title) + '</h2>' + (f.desc ? '<p class="nw-feat-desc">' + escHtml(f.desc) + '</p>' : '') +
        '<span class="nw-feat-cue">อ่านต่อ <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span></div></a>';
    }

    function render(){
      var q = state.q.trim().toLowerCase();
      var list = news.filter(function(n){
        return (state.cat === "all" || n.cat === state.cat) &&
          (!q || [n.title, n.desc, n.tag].join(" ").toLowerCase().indexOf(q) !== -1);
      });
      var showFeat = !!featWrap && state.cat === "all" && !q;
      if(featWrap) featWrap.hidden = !showFeat;
      var cards = showFeat ? list.slice(1) : list;
      grid.innerHTML = cards.map(newsCard).join("");
      grid.hidden = !cards.length;
      if(empty) empty.hidden = list.length > 0;
      if(count) count.textContent = "พบ " + list.length + " ข่าว";
      if(catWrap) pressChips(catWrap.querySelectorAll("[data-value]"), state.cat);
    }
    if(input) input.addEventListener("input", function(){ state.q = input.value; render(); });
    if(clear) clear.addEventListener("click", function(){
      state.cat = "all"; state.q = "";
      if(input) input.value = "";
      render();
    });
    render();
  }

  // ลบ query param ออกจาก URL โดยไม่โหลดหน้าใหม่
  function dropParam(name){
    try {
      var url = new URL(window.location.href);
      url.searchParams.delete(name);
      window.history.replaceState(null, "", url.pathname + url.search + url.hash);
    } catch(err){}
  }

  /* ---- News detail: ?n=<slug> ------------------------------------------- */
  function initNewsDetail(){
    var root = document.querySelector("[data-news-detail]");
    var news = window.BAS_NEWS;
    if(!root || !news) return;
    var a = findBy(news, "slug", qs("n"));
    var article = root.querySelector("[data-n-article]");
    var missing = root.querySelector("[data-n-missing]");
    var wrap = root.querySelector("[data-n-related]");

    if(!a){
      // slug ไม่รู้จัก (เช่นลิงก์เก่าก่อนเปลี่ยนชุดข่าว) หรือไม่มี ?n= → แจ้งว่าไม่พบ แทนที่จะแสดงข่าวอื่นแบบเงียบ ๆ
      document.title = "ไม่พบข่าว — BAS SWU";
      setText("[data-n-short]", "ไม่พบข่าว");
      if(article) article.hidden = true;
      if(missing) missing.hidden = false;
      var robots = document.createElement("meta");
      robots.name = "robots"; robots.content = "noindex";
      document.head.appendChild(robots);
      if(wrap) wrap.innerHTML = news.slice(0, 3).map(newsCard).join("");
      return;
    }

    document.title = a.title + " — BAS SWU";
    setText("[data-n-short]", a.title.length > 48 ? a.title.slice(0, 46) + "…" : a.title);
    setText("[data-n-tag]", a.tag);
    setText("[data-n-date]", a.date);
    setText("[data-n-title]", a.title);
    var img = root.querySelector("[data-n-img]");
    if(img){ img.src = a.img; img.alt = a.title; }
    var src = root.querySelector("[data-n-url]");
    if(src && a.url){ src.href = a.url; src.hidden = false; }
    var rest = news.filter(function(n){ return n !== a; });
    var related = rest.filter(function(n){ return n.cat === a.cat; })
      .concat(rest.filter(function(n){ return n.cat !== a.cat; })).slice(0, 3);
    if(wrap) wrap.innerHTML = related.map(newsCard).join("");
  }


  function setText(sel, val){
    document.querySelectorAll(sel).forEach(function(el){ el.textContent = val; });
  }

  var toastTimer = null;
  function showToast(message){
    var toast = document.querySelector(".toast");
    if(!toast){
      toast = document.createElement("div");
      toast.className = "toast";
      toast.setAttribute("role","status");
      toast.setAttribute("aria-live","polite");
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(function(){ toast.classList.remove("show"); }, 2600);
  }

  // ------------------------------------------------------------- admin mode (demo only, no real auth)
  // ล็อกอินที่ admin.html → ตั้ง flag ใน localStorage แล้วทุกหน้าอ่าน flag นี้เพื่อแสดง admin-bar
  var ADMIN_KEY = "bas-admin";
  function getAdminFlag(){
    try { return window.localStorage.getItem(ADMIN_KEY) === "1"; } catch(e){ return false; }
  }
  function setAdminFlag(active){
    try {
      if(active) window.localStorage.setItem(ADMIN_KEY, "1");
      else window.localStorage.removeItem(ADMIN_KEY);
    } catch(e){}
  }
  // ------------------------------------------------------------- admin.html login form (demo only, no real auth)
  function initAdminLogin(){
    var form = document.getElementById("adm-form");
    if(!form) return;
    var view = document.getElementById("adm-login");
    var done = document.getElementById("adm-done");
    var user = form.elements.username;
    var pw = form.elements.password;
    var err = document.getElementById("adm-error");
    var errText = document.getElementById("adm-error-text");
    var toggle = document.getElementById("adm-pw-toggle");
    var tried = false;

    function markInvalid(){
      [user, pw].forEach(function(f){
        var bad = tried && !f.value.trim();
        f.classList.toggle("is-invalid", bad);
        f.setAttribute("aria-invalid", bad ? "true" : "false");
      });
    }
    function showError(msg){
      errText.textContent = msg;
      err.hidden = !msg;
    }
    function showDone(active){
      view.hidden = active;
      done.hidden = !active;
      (active ? done.querySelector("h1") : user).focus();
    }

    [user, pw].forEach(function(f){
      f.addEventListener("input", function(){ showError(""); markInvalid(); });
    });

    toggle.addEventListener("click", function(){
      var show = pw.type === "password";
      pw.type = show ? "text" : "password";
      toggle.setAttribute("aria-label", show ? "ซ่อนรหัสผ่าน" : "แสดงรหัสผ่าน");
      toggle.querySelector("i").className = show ? "fa-solid fa-eye-slash" : "fa-solid fa-eye";
    });

    form.addEventListener("submit", function(e){
      e.preventDefault();
      tried = true;
      markInvalid();
      if(!user.value.trim() || !pw.value.trim()){
        showError("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน");
        (user.value.trim() ? pw : user).focus();
        return;
      }
      showError("");
      setAdminFlag(true);
      showDone(true);
    });

    document.getElementById("adm-logout").addEventListener("click", function(){
      setAdminFlag(false);
      form.reset();
      tried = false;
      markInvalid();
      showDone(false);
    });

    if(getAdminFlag()){ view.hidden = true; done.hidden = false; }
  }

  function initAdmin(){
    var adminLink = document.getElementById("admin-open");
    var bar = document.getElementById("admin-bar");
    var logoutBtn = document.getElementById("admin-logout");

    function setAdminActive(active){
      document.body.classList.toggle("is-admin", active);
      if(adminLink) adminLink.classList.toggle("is-active", active);
      if(bar) bar.hidden = !active;
    }
    setAdminActive(getAdminFlag());

    if(logoutBtn){
      logoutBtn.addEventListener("click", function(){
        setAdminFlag(false);
        setAdminActive(false);
        showToast("ออกจากโหมดผู้ดูแลระบบแล้ว");
      });
    }
  }
})();

/* ==========================================================================
   HERO เต็มแบนเนอร์ — เลือกไฟล์วิดีโอ/โปสเตอร์ตามขนาดจอ + ปุ่มหยุด (WCAG 2.2.2)
   ========================================================================== */
(function(){
  var v = document.getElementById("hero-video");
  if(!v) return;
  var mqMobile = window.matchMedia("(max-width: 767px)");
  var mqReduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  function pick(){
    var mobile = mqMobile.matches;
    v.poster = mobile ? v.dataset.posterMobile : v.dataset.posterDesktop;
    var src = mobile ? v.dataset.srcMobile : v.dataset.srcDesktop;
    // ยังไม่มีไฟล์วิดีโอจริง -> คงไว้ที่ภาพนิ่ง (poster) ไม่ยิง request ที่จะ 404
    if(!src){ v.removeAttribute("src"); v.innerHTML = ""; return; }
    if(v.getAttribute("data-current") === src) return;
    v.setAttribute("data-current", src);
    v.innerHTML = "";
    var sEl = document.createElement("source");
    sEl.src = src; sEl.type = "video/mp4";
    v.appendChild(sEl);
    // โหลดเฉพาะเมื่อไม่ได้ตั้งค่าลดการเคลื่อนไหว — ไม่งั้นคงไว้ที่ภาพนิ่ง
    if(!mqReduce.matches){ v.load(); }
  }
  pick();
  if(mqMobile.addEventListener) mqMobile.addEventListener("change", pick);

  var btn = document.getElementById("hero-toggle");
  if(!btn) return;
  // ไม่มีไฟล์วิดีโอ -> ซ่อนปุ่มควบคุม ไม่ให้มีปุ่มที่กดแล้วไม่เกิดอะไร
  if(!v.dataset.srcDesktop && !v.dataset.srcMobile){ btn.hidden = true; return; }
  function setPaused(paused){
    btn.setAttribute("aria-pressed", paused ? "true" : "false");
    btn.setAttribute("aria-label", paused ? "เล่นวิดีโอพื้นหลัง" : "หยุดวิดีโอพื้นหลัง");
  }
  if(mqReduce.matches){ try{ v.pause(); }catch(e){} setPaused(true); }
  btn.addEventListener("click", function(){
    if(v.paused){ v.play().catch(function(){}); setPaused(false); }
    else { v.pause(); setPaused(true); }
  });
})();

/* ==========================================================================
   ตัวเลขวิ่ง — ตัวเลขจริงอยู่ใน DOM ตั้งแต่แรก (screen reader / JS พังก็ยังอ่านได้)
   ========================================================================== */
(function(){
  var tiles = document.querySelectorAll("[data-count-to]");
  if(!tiles.length) return;
  if(window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if(!("IntersectionObserver" in window)) return;

  function run(el){
    var target = el.getAttribute("data-count-to");
    var n = parseInt(target.replace(/[^0-9]/g, ""), 10);
    if(!n || n > 100000) return;
    var dur = 900, t0 = null;
    function step(ts){
      if(!t0) t0 = ts;
      var p = Math.min((ts - t0) / dur, 1);
      var val = Math.floor(n * (1 - Math.pow(1 - p, 3)));
      el.textContent = val.toLocaleString("en-US");
      if(p < 1) requestAnimationFrame(step); else el.textContent = target;
    }
    requestAnimationFrame(step);
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){ run(en.target); io.unobserve(en.target); }
    });
  }, {threshold: .4});
  tiles.forEach(function(t){ io.observe(t); });
})();

/* ==========================================================================
   สายตรงคณบดี — ปิดได้ และจำไว้ในเซสชันเดียว
   ========================================================================== */
window.BASSite = window.BASSite || {};
window.BASSite.initDeanFab = function(){
  var wrap = document.querySelector(".dean-direct-wrap");
  if(!wrap) return;
  var KEY = "bas-dean-direct-hidden";
  function setHidden(hidden){
    wrap.hidden = hidden;
    // footer เผื่อที่ด้านล่างให้ปุ่มลอยบนจอแคบ (ดู .has-fab ใน styles.css)
    document.body.classList.toggle("has-fab", !hidden);
  }
  var stored = false;
  try { stored = window.sessionStorage.getItem(KEY) === "1"; } catch(e){}
  setHidden(stored);
  var closeBtn = document.getElementById("dean-fab-close");
  if(closeBtn){
    closeBtn.addEventListener("click", function(e){
      e.preventDefault(); e.stopPropagation();
      setHidden(true);
      try { window.sessionStorage.setItem(KEY, "1"); } catch(err){}
    });
  }
};

/* == v4 interactive ======================================================
   Activity rail (carousel) + B·A·S tablist
   progressive enhancement: ถ้า JS ไม่ทำงาน rail ยังเลื่อนด้วยนิ้ว/เทรกแพดได้
   และ panel แรกของ B·A·S ยังแสดงอยู่
   ====================================================================== */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Activity rail ------------------------------------------- */
  document.querySelectorAll('[data-rail]').forEach(function (rail) {
    var vp = rail.querySelector('[data-rail-viewport]');
    var prev = rail.querySelector('[data-rail-prev]');
    var next = rail.querySelector('[data-rail-next]');
    var wrap = rail.parentElement;
    var dots = Array.prototype.slice.call(wrap.querySelectorAll('[data-rail-dot]'));
    var status = wrap.querySelector('[data-rail-status]');
    var items = Array.prototype.slice.call(rail.querySelectorAll('.rail-item'));
    if (!vp || !items.length) return;

    function step() {
      var r = items[0].getBoundingClientRect();
      // getComputedStyle().columnGap can come back as the keyword "normal"
      // (not a length) when no gap is set -- parseFloat("normal") is NaN,
      // so the px fallback has to wrap the parse, not the input string.
      var gap = parseFloat(getComputedStyle(vp.firstElementChild).columnGap) || 16;
      return r.width + gap;
    }
    function perPage() {
      return Math.max(1, Math.round(vp.clientWidth / step()));
    }
    function pageCount() {
      return Math.max(1, Math.ceil(items.length / perPage()));
    }
    function currentPage() {
      return Math.round(vp.scrollLeft / (step() * perPage()));
    }
    function go(page) {
      var max = vp.scrollWidth - vp.clientWidth;
      var target = Math.min(page * step() * perPage(), max);
      vp.scrollTo({ left: target, behavior: reduce ? 'auto' : 'smooth' });
    }

    function sync() {
      var max = vp.scrollWidth - vp.clientWidth - 8;
      if (prev) prev.disabled = vp.scrollLeft <= 8;
      if (next) next.disabled = vp.scrollLeft >= max;
      var pc = pageCount();
      var cur = vp.scrollLeft >= max ? pc - 1 : Math.min(currentPage(), pc - 1);
      dots.forEach(function (d, i) {
        d.hidden = i >= pc;
        if (i < pc) d.setAttribute('aria-current', i === cur ? 'true' : 'false');
      });
      if (status) status.textContent = 'ชุดที่ ' + (cur + 1) + ' จาก ' + pc;
    }

    if (prev) prev.addEventListener('click', function () { go(Math.max(0, currentPage() - 1)); });
    if (next) next.addEventListener('click', function () { go(Math.min(pageCount() - 1, currentPage() + 1)); });
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });

    vp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); go(Math.min(pageCount() - 1, currentPage() + 1)); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(Math.max(0, currentPage() - 1)); }
      if (e.key === 'Home') { e.preventDefault(); go(0); }
      if (e.key === 'End') { e.preventDefault(); go(pageCount() - 1); }
    });

    var t;
    vp.addEventListener('scroll', function () {
      clearTimeout(t);
      t = setTimeout(sync, 90);
    }, { passive: true });
    window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(sync, 150); });
    sync();
  });

  /* ---------- B · A · S tablist --------------------------------------- */
  document.querySelectorAll('[data-identity]').forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) p.hidden = !on;
      });
      tab.focus();
    }
    tabs.forEach(function (tab, i) {
      tab.addEventListener('click', function () { select(tab); });
      tab.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === 'Home') n = tabs[0];
        if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); select(n); }
      });
    });
  });
})();
