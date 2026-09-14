// BAS SWU -- shared interactions
(function(){
  "use strict";

  document.addEventListener("DOMContentLoaded", function(){
    initHeaderScroll();
    initMegaMenuKeyboard();
    initMobileDrawer();
    initSearchPanel();
    initMarqueeClone();
    initScrollReveal();
    initFilters();
    initStaffToggle();
    initProgramDetail();
    initNewsDetail();
    initAdmin();
    initGlobalMap();
  });


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
          return '<li>' + esc(p.name) + '<span class="gp-detail-type">' + esc(p.type) + '</span></li>';
        }).join("");
        detail.innerHTML =
          '<p class="gp-detail-country">' + esc(node.country) + '</p>' +
          '<p class="gp-detail-meta"><span>' + esc(node.region) + '</span><span aria-hidden="true">&middot;</span><span>' +
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
        more.textContent = open ? "View all partners" : "Show fewer partners";
      });
    }

    function esc(v){
      return String(v).replace(/[&<>"]/g, function(c){
        return ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" })[c];
      });
    }
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

  function initMegaMenuKeyboard(){
    function closeAll(except){
      document.querySelectorAll(".nav-item.open").forEach(function(o){
        if(o === except) return;
        o.classList.remove("open");
        var l = o.querySelector(".nav-link");
        if(l) l.setAttribute("aria-expanded", "false");
      });
    }
    function setOpen(item, open){
      item.classList.toggle("open", open);
      var l = item.querySelector(".nav-link");
      if(l) l.setAttribute("aria-expanded", open ? "true" : "false");
    }

    document.querySelectorAll(".nav-item").forEach(function(item){
      var link = item.querySelector(".nav-link");
      var mega = item.querySelector(".mega");
      if(!link || !mega) return;

      link.setAttribute("aria-expanded", "false");

      link.addEventListener("click", function(e){
        if(link.getAttribute("href") === "#"){ e.preventDefault(); }
        var isOpen = item.classList.contains("open");
        closeAll(item);
        setOpen(item, !isOpen);
      });

      // เปิดเมนูย่อยเมื่อโฟกัสด้วยคีย์บอร์ด — ผู้ใช้คีย์บอร์ดจึง Tab เข้าไปในเมนูย่อยได้
      item.addEventListener("focusin", function(){
        closeAll(item);
        setOpen(item, true);
      });
      item.addEventListener("focusout", function(){
        window.setTimeout(function(){
          if(!item.contains(document.activeElement)) setOpen(item, false);
        }, 0);
      });
    });

    document.addEventListener("click", function(e){
      if(!e.target.closest(".nav-item")) closeAll(null);
    });
    document.addEventListener("keydown", function(e){
      if(e.key === "Escape"){
        var open = document.querySelector(".nav-item.open");
        closeAll(null);
        if(open){ var l = open.querySelector(".nav-link"); if(l) l.focus(); }
      }
    });
  }

  function initMobileDrawer(){
    var toggle = document.querySelector(".menu-toggle");
    var drawer = document.querySelector(".mobile-drawer");
    if(!toggle || !drawer) return;
    var closeBtn = drawer.querySelector(".drawer-close");
    var scrim = drawer.querySelector(".drawer-scrim");
    function open(){ drawer.classList.add("open"); toggle.setAttribute("aria-expanded","true"); document.body.style.overflow="hidden"; }
    function close(){ drawer.classList.remove("open"); toggle.setAttribute("aria-expanded","false"); document.body.style.overflow=""; }
    toggle.addEventListener("click", open);
    if(closeBtn) closeBtn.addEventListener("click", close);
    if(scrim) scrim.addEventListener("click", close);
    document.addEventListener("keydown", function(e){ if(e.key==="Escape") close(); });
    drawer.querySelectorAll(".drawer-item > button").forEach(function(btn){
      btn.addEventListener("click", function(){
        var item = btn.closest(".drawer-item");
        var wasOpen = item.classList.contains("open");
        drawer.querySelectorAll(".drawer-item.open").forEach(function(o){ o.classList.remove("open"); });
        item.classList.toggle("open", !wasOpen);
      });
    });
  }

  function initSearchPanel(){
    var btn = document.querySelector(".search-toggle");
    var panel = document.querySelector(".search-panel");
    if(!btn || !panel) return;
    var form = panel.querySelector("form");
    var input = panel.querySelector("input");
    btn.addEventListener("click", function(){
      panel.classList.toggle("open");
      if(panel.classList.contains("open") && input){ input.focus(); }
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
      track.innerHTML += track.innerHTML;
      track.dataset.cloned = "true";
    });
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

  function initFilters(){
    document.querySelectorAll("[data-filter-group]").forEach(function(group){
      var chips = group.querySelectorAll(".filter-chip");
      var targetSel = group.getAttribute("data-filter-target");
      var items = document.querySelectorAll(targetSel);
      chips.forEach(function(chip){
        chip.addEventListener("click", function(){
          chips.forEach(function(c){ c.setAttribute("aria-pressed","false"); });
          chip.setAttribute("aria-pressed","true");
          var val = chip.getAttribute("data-filter-value");
          items.forEach(function(item){
            var match = (val === "all") || (item.getAttribute("data-filter") === val);
            item.hidden = !match;
          });
        });
      });
    });
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

  function qs(name){
    var params = new URLSearchParams(window.location.search);
    return params.get(name);
  }

  function initProgramDetail(){
    var root = document.querySelector("[data-program-detail]");
    if(!root || typeof BAS_PROGRAMS === "undefined") return;
    var slug = qs("p");
    var program = BAS_PROGRAMS.find(function(p){ return p.slug === slug; }) || BAS_PROGRAMS[0];
    var dept = (typeof BAS_DEPARTMENTS !== "undefined") ? BAS_DEPARTMENTS.find(function(d){ return d.slug === program.dept; }) : null;

    document.title = program.name_th + " — BAS SWU";
    setText("[data-p-name-en]", program.name_en);
    setText("[data-p-name-th]", program.name_th);
    setText("[data-p-summary]", program.summary);
    setText("[data-p-curriculum]", program.curriculum);
    setText("[data-p-level]", program.level === "graduate" ? "ปริญญาโท-เอก" : "ปริญญาตรี");
    setText("[data-p-dept]", dept ? (dept.name_th) : "—");
    setText("[data-p-dept-th]", dept ? (dept.name_en) : "");

    var careerList = document.querySelector("[data-p-careers]");
    if(careerList){
      careerList.innerHTML = "";
      program.careers.forEach(function(c){
        var span = document.createElement("span");
        span.textContent = c;
        careerList.appendChild(span);
      });
    }

    var breadcrumbCur = document.querySelector("[data-p-breadcrumb]");
    if(breadcrumbCur) breadcrumbCur.textContent = program.name_th;

    // related programs (same department, excluding current)
    var related = BAS_PROGRAMS.filter(function(p){ return p.dept === program.dept && p.slug !== program.slug; }).slice(0,3);
    var relatedWrap = document.querySelector("[data-p-related]");
    if(relatedWrap){
      if(!related.length){ relatedWrap.closest("section").hidden = true; }
      relatedWrap.innerHTML = related.map(function(p){
        return '<a class="card program-card" href="program-detail.html?p='+p.slug+'">'+
          '<div class="card-media"><span class="level-badge">'+(p.level==="graduate"?"ปริญญาโท-เอก":"ปริญญาตรี")+'</span><span class="ph-label">ภาพประกอบหลักสูตร (ตัวอย่าง)</span></div>'+
          '<div class="card-body"><span class="card-tag">'+p.curriculum+'</span>'+
          '<h3 class="card-title bi-heading"><span class="bi-th">'+p.name_th+'</span><span class="bi-en">'+p.name_en+'</span></h3>'+
          '<p class="card-desc">'+p.summary+'</p></div></a>';
      }).join("");
    }
  }

  function initNewsDetail(){
    var root = document.querySelector("[data-news-detail]");
    if(!root || typeof BAS_NEWS === "undefined") return;
    var slug = qs("n");
    var item = BAS_NEWS.find(function(n){ return n.slug === slug; }) || BAS_NEWS[0];

    document.title = item.title + " — BAS SWU News";
    setText("[data-n-title]", item.title);
    setText("[data-n-date]", item.date);
    setText("[data-n-category]", item.category);
    setText("[data-n-summary]", item.summary);
    var breadcrumbCur = document.querySelector("[data-n-breadcrumb]");
    if(breadcrumbCur) breadcrumbCur.textContent = item.title;

    var related = BAS_NEWS.filter(function(n){ return n.slug !== item.slug; }).slice(0,3);
    var relatedWrap = document.querySelector("[data-n-related]");
    if(relatedWrap){
      relatedWrap.innerHTML = related.map(function(n){
        return '<a class="card" href="news-detail.html?n='+n.slug+'">'+
          '<div class="card-media"><span class="ph-label">ภาพข่าว (ตัวอย่าง)</span></div>'+
          '<div class="card-body"><span class="card-tag'+(n.category_en==="News"?"":" crimson")+'">'+n.category+'</span>'+
          '<span class="card-meta">'+n.date+'</span>'+
          '<h3 class="card-title">'+n.title+'</h3></div></a>';
      }).join("");
    }
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
  function initAdmin(){
    var openBtn = document.getElementById("admin-open");
    var modal = document.getElementById("admin-modal");
    var bar = document.getElementById("admin-bar");
    var form = document.getElementById("admin-login-form");
    var logoutBtn = document.getElementById("admin-logout");
    if(!openBtn || !modal) return;

    function openModal(){
      modal.setAttribute("aria-hidden","false");
      document.body.style.overflow = "hidden";
      var firstField = modal.querySelector("input");
      if(firstField) window.setTimeout(function(){ firstField.focus(); }, 60);
    }
    function closeModal(){
      modal.setAttribute("aria-hidden","true");
      document.body.style.overflow = "";
      openBtn.focus();
    }
    openBtn.addEventListener("click", openModal);
    modal.querySelectorAll("[data-admin-close]").forEach(function(el){
      el.addEventListener("click", closeModal);
    });
    document.addEventListener("keydown", function(e){
      if(e.key === "Escape" && modal.getAttribute("aria-hidden") === "false"){ closeModal(); }
    });

    function setAdminActive(active){
      document.body.classList.toggle("is-admin", active);
      openBtn.classList.toggle("is-active", active);
      openBtn.setAttribute("aria-pressed", active ? "true" : "false");
      if(bar) bar.hidden = !active;
    }

    if(form){
      form.addEventListener("submit", function(e){
        e.preventDefault();
        closeModal();
        setAdminActive(true);
        showToast("เข้าสู่โหมดผู้ดูแลระบบแล้ว (ต้นแบบสาธิต — ไม่มีการยืนยันตัวตนจริง)");
        form.reset();
      });
    }
    if(logoutBtn){
      logoutBtn.addEventListener("click", function(){
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
(function(){
  var el = document.getElementById("dean-direct");
  if(!el) return;
  var closeBtn = document.getElementById("dean-direct-close");
  if(closeBtn){
    closeBtn.addEventListener("click", function(e){
      e.preventDefault(); e.stopPropagation();
      el.parentNode.hidden = true;
    });
  }
})();

/* ==========================================================================
   ข่าว: deep link ?cat=<slug> จากหน้าแรก + empty state เมื่อหมวดยังไม่มีข่าว
   ========================================================================== */
document.addEventListener("DOMContentLoaded", function(){
  var bar = document.getElementById("news-cats");
  if(!bar) return;
  var empty = document.getElementById("news-empty");
  var feature = document.querySelector(".news-feature");

  function syncEmpty(){
    var val = (bar.querySelector('[aria-pressed="true"]') || {}).getAttribute
      ? bar.querySelector('[aria-pressed="true"]').getAttribute("data-filter-value") : "all";
    var cards = document.querySelectorAll("[data-filter]");
    var visible = 0;
    cards.forEach(function(c){ if(!c.hidden) visible++; });
    // ข่าวเด่นเป็นหมวด inter — ซ่อนเมื่อกรองหมวดอื่น
    if(feature){
      var show = (val === "all" || val === "inter");
      feature.hidden = !show;
      if(show) visible++;
    }
    if(empty) empty.hidden = visible > 0;
  }

  bar.addEventListener("click", function(e){
    if(e.target.closest(".filter-chip")) setTimeout(syncEmpty, 0);
  });

  var cat = new URLSearchParams(window.location.search).get("cat");
  if(cat){
    // อนุญาตตัวเลข/ยัติภังค์ด้วย — slug หมวดหมู่ในอนาคตอาจมี เช่น "study-abroad"
    var chip = bar.querySelector('[data-filter-value="' + cat.toLowerCase().replace(/[^a-z0-9-]/g, "") + '"]');
    if(chip){ chip.click(); }
  }
  syncEmpty();
});


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
