// BAS SWU -- shared interactions
(function(){
  "use strict";

  document.addEventListener("DOMContentLoaded", function(){
    initMarqueeClone();
    initScrollReveal();
    initFilters();
    initStaffToggle();
    initProgramsFinder();
    initProgramDetail();
    initFacultyDirectory();
    initProfile();
    initNewsDetail();
    initGlobalMap();
    initHomeNews();
    initHomeMap();
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
        more.textContent = open ? (more.getAttribute("data-label-more") || "View all partners") : (more.getAttribute("data-label-less") || "Show fewer partners");
      });
    }

    function esc(v){
      return String(v).replace(/[&<>"]/g, function(c){
        return ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" })[c];
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
      buttons.forEach(function(b){ b.setAttribute("aria-pressed", String(b.getAttribute("data-cat") === cat)); });
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

    function esc(v){
      return String(v).replace(/[&<>"']/g, function(c){
        return ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" })[c];
      });
    }
    function render(n){
      var orgs = n.partners.slice(0, SHOW).map(function(p){
        return '<li><p class="hp-org-name">' + esc(p.name) + '</p><p class="hp-org-type">' + esc(p.type) + '</p></li>';
      }).join("");
      panel.innerHTML =
        '<p class="hp-country-region" lang="en">' + esc(n.region) + '</p>' +
        '<div class="hp-country-head"><h3 lang="en">' + esc(n.country) + '</h3><span class="hp-country-count">' + n.count + ' องค์กร</span></div>' +
        '<ul class="hp-country-orgs" lang="en">' + orgs + '</ul>' +
        (n.count > SHOW ? '<a class="hp-link hp-country-more th-body" href="mou.html#directory">ดูทั้งหมด ' + n.count +
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
    function esc(v){
      return String(v == null ? "" : v).replace(/[&<>"']/g, function(c){
        return { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c];
      });
    }
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
        ? 'href="' + esc(p.external_url) + '" target="_blank" rel="noopener" aria-label="' + esc(p.abbr + " " + p.name_th) + ' (เว็บไซต์ภายนอก เปิดในแท็บใหม่)"'
        : 'href="program-detail.html?p=' + p.slug + '"';
      return '<a class="pg-card" ' + attrs + '>' +
        '<div class="pg-card-media"><img src="assets/media/program-' + p.slug + '.jpg" alt="" loading="lazy" decoding="async"><span class="pg-card-level">' + esc(p.level_label) + '</span></div>' +
        '<div class="pg-card-body">' +
          '<h3 class="pg-card-abbr" lang="en">' + esc(p.abbr) + '</h3>' +
          '<p class="pg-card-th">' + esc(p.name_th) + '</p>' +
          '<p class="pg-card-desc">' + esc(p.summary) + '</p>' +
          '<div class="pg-card-careers"><p>เส้นทางอาชีพ</p><div class="pg-tags">' +
            p.careers.map(function(c){ return '<span>' + esc(c) + '</span>'; }).join("") +
          '</div></div>' +
          '<div class="pg-card-foot">' +
            '<span class="pg-card-cue">' + (ext ? 'ไปเว็บไซต์หลักสูตร <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>' : 'ดูรายละเอียดหลักสูตร <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>') + '</span>' +
            '<span class="pg-card-lang"><i class="fa-solid fa-language" aria-hidden="true"></i>' + esc(p.language) + '</span>' +
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
    var program = BAS_PROGRAMS.find(function(p){ return p.slug === slug; }) || BAS_PROGRAMS[0];
    function esc(v){
      return String(v == null ? "" : v).replace(/[&<>"']/g, function(c){
        return { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c];
      });
    }
    function imgFor(p){ return "assets/media/program-" + p.slug + ".jpg"; }

    document.title = program.abbr + " — BAS SWU";
    setText("[data-p-abbr]", program.abbr);
    setText("[data-p-level]", program.level_label);
    setText("[data-p-name-en]", program.name_en.replace(" -- ", " — "));
    setText("[data-p-name-th]", program.name_th);
    setText("[data-p-summary]", program.summary);
    setText("[data-p-summary-en]", program.summary_en);
    var heroImg = root.querySelector("[data-p-img]");
    if(heroImg) heroImg.src = imgFor(program);

    var facts = root.querySelector("[data-p-facts]");
    if(facts){
      facts.innerHTML = [
        ["Level", "fa-graduation-cap", program.level_label],
        ["Language", "fa-language", program.language],
        ["Curriculum", "fa-book-open", program.curriculum_label]
      ].map(function(f){
        return '<div><dt><i class="fa-solid ' + f[1] + '" aria-hidden="true"></i>' + f[0] + '</dt><dd>' + esc(f[2]) + '</dd></div>';
      }).join("");
    }

    var careerList = root.querySelector("[data-p-careers]");
    if(careerList){
      careerList.innerHTML = program.careers.map(function(c){
        return '<li><span class="pd-career-ico"><i class="fa-solid fa-briefcase" aria-hidden="true"></i></span>' + esc(c) + '</li>';
      }).join("");
    }

    // related: same level first, then the rest, excluding current
    var rest = BAS_PROGRAMS.filter(function(p){ return p.slug !== program.slug; });
    var related = rest.filter(function(p){ return p.level === program.level; })
      .concat(rest.filter(function(p){ return p.level !== program.level; }))
      .slice(0, 3);
    var relatedWrap = root.querySelector("[data-p-related]");
    if(relatedWrap){
      relatedWrap.innerHTML = related.map(function(p){
        var href = p.external_url
          ? esc(p.external_url) + '" target="_blank" rel="noopener'
          : 'program-detail.html?p=' + p.slug;
        return '<a class="pd-card" href="' + href + '">' +
          '<div class="pd-card-media"><img src="' + imgFor(p) + '" alt="" loading="lazy" decoding="async"></div>' +
          '<div class="pd-card-body"><span class="pd-card-level">' + esc(p.level_label) + '</span>' +
          '<h3 class="pd-card-abbr">' + esc(p.abbr) + (p.external_url ? ' <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i>' : '') + '</h3>' +
          '<p class="pd-card-th">' + esc(p.name_th) + '</p></div></a>';
      }).join("");
    }
  }

  function escHtml(v){
    return String(v == null ? "" : v).replace(/[&<>"']/g, function(c){
      return { "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c];
    });
  }

  // faculty.html — ค้นหาชื่อ + กรองภาควิชา/ความเชี่ยวชาญ, การ์ดทุกใบลิงก์ไป profile.html?p=<id>
  function initFacultyDirectory(){
    var root = document.querySelector("[data-fd-root]");
    if(!root || typeof BAS_DIRECTORY === "undefined") return;
    var esc = escHtml;
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
    function chip(attr, key, label, count, on){
      return '<button type="button" class="pg-chip fd-chip" ' + attr + '="' + esc(key) + '" aria-pressed="' + on + '">' +
        esc(label) + '<span class="pg-count">' + count + '</span></button>';
    }
    function card(p){
      var contact = p.mail
        ? '<a class="fd-contact" href="mailto:' + esc(p.mail) + '"><i class="fa-solid fa-envelope" aria-hidden="true"></i>' + esc(p.mail) + '</a>'
        : (p.tel ? '<span class="fd-contact"><i class="fa-solid fa-phone" aria-hidden="true"></i>' + esc(p.tel) + '</span>' : '');
      return '<article class="fd-card">' +
        '<div class="fd-card-photo"><img src="' + esc(p.img) + '" alt="' + esc(p.th) + '" loading="lazy" decoding="async"><span class="fd-card-role">' + esc(p.role) + '</span></div>' +
        '<div class="fd-card-body">' +
          '<h4 lang="en"><a class="fd-card-link" href="profile.html?p=' + encodeURIComponent(p.id) + '">' + esc(p.en) + '</a></h4>' +
          '<p>' + esc(p.th) + '</p>' + contact +
        '</div></article>';
    }
    function render(){
      var byQ = byQuery();
      var inDept = byQ.filter(function(p){ return state.dept === "all" || p.d === state.dept; });
      var shown = inDept.filter(function(p){ return state.grp === "all" || p.ge === state.grp; });

      deptBox.innerHTML = [{ key:"all", short:"ทุกภาควิชา" }].concat(BAS_DEPTS).map(function(d){
        return chip("data-fd-dept", d.key, d.short, byQ.filter(function(p){ return d.key === "all" || p.d === d.key; }).length, state.dept === d.key);
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
          '<div class="fd-dept-head"><div><h2 lang="en">' + esc(d.en) + '</h2><p>' + esc(d.th) + '</p></div><span>' + ps.length + ' คน</span></div>' +
          groups.map(function(g){
            return '<div class="fd-group"><h3><span lang="en">' + esc(g.en) + '</span><span class="fd-group-th">' + esc(g.th) + '</span></h3>' +
              '<div class="fd-grid">' + g.people.map(card).join("") + '</div></div>';
          }).join("") + '</div>';
      }).join("");

      var filtered = !!state.q.trim() || state.dept !== "all" || state.grp !== "all";
      empty.hidden = !!shown.length;
      clearTop.hidden = !filtered;
      setText("[data-fd-result]", "แสดง " + shown.length + " จาก " + BAS_DIRECTORY.length + " รายชื่อ");
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
    var esc = escHtml;
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
          (m[2] ? '<a href="' + esc(m[2]) + '">' + esc(m[1]) + '</a>' : '<span>' + esc(m[1]) + '</span>') + '</li>';
      }).join("");
    var icons = { "การรับรองวิชาชีพ":"fa-solid fa-award", "ความเชี่ยวชาญ":"fa-solid fa-lightbulb", "ประวัติย่อ":"fa-solid fa-file-lines" };
    var facts = [["การรับรองวิชาชีพ","Certification"], ["ความเชี่ยวชาญ","Expertise"], ["ประวัติย่อ","CV"]].map(function(k){
      var f = P.facts.filter(function(x){ return x.k === k[0]; })[0];
      if(!f || !(f.v || f.href)) return "";
      var v = f.href
        ? '<a class="pf-cv" href="' + esc(f.href) + '" target="_blank" rel="noopener" aria-label="ดาวน์โหลด CV ของ' + esc(P.th) + ' (ไฟล์ PDF เปิดในแท็บใหม่)"><i class="fa-solid fa-file-pdf" aria-hidden="true"></i>ดาวน์โหลด CV<i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a>'
        : '<p>' + esc(f.v) + '</p>';
      return '<div class="pf-fact"><div class="pf-fact-k"><span class="pf-ico" aria-hidden="true"><i class="' + icons[k[0]] + '"></i></span>' +
        '<h3><span>' + k[0] + '</span><span class="pf-fact-en" lang="en">' + k[1] + '</span></h3></div><div class="pf-fact-v">' + v + '</div></div>';
    }).join("");
    var edu = P.edu.length
      ? P.edu.map(function(e){ return '<li><span class="pf-edu-dot" aria-hidden="true"></span><span><span class="pf-edu-deg">' + esc(e[0]) + '</span><span class="pf-edu-inst">' + esc(e[1]) + '</span></span></li>'; }).join("")
      : '<li class="pf-edu-pending"><span class="pf-edu-dot" aria-hidden="true"></span><span>ข้อมูลอยู่ระหว่างปรับปรุง</span></li>';

    body.innerHTML =
      '<div class="pf-card">' +
        '<span class="pf-ring" aria-hidden="true"></span><span class="pf-blob" aria-hidden="true"></span>' +
        '<div class="pf-photo"><img src="' + esc(P.img) + '" alt="' + esc(P.th) + '" decoding="async"></div>' +
        '<div class="pf-copy">' +
          '<p class="pf-role"><span class="pf-role-bar" aria-hidden="true"></span>' + esc(P.roleTh) + (P.roleEn ? '<span lang="en">' + esc(P.roleEn) + '</span>' : '') + '</p>' +
          '<h1 lang="en">' + esc(P.en) + '</h1>' +
          '<p class="pf-th">' + esc(P.th) + '</p>' +
          '<ul class="pf-meta">' + meta + '</ul>' +
        '</div>' +
      '</div>' +
      '<div class="pf-edu"><h2>ประวัติการศึกษา</h2><p class="pf-h2-en" lang="en">Academic background</p><ul>' + edu + '</ul></div>' +
      (facts ? '<div class="pf-facts">' + facts + '</div>' : '') +
      backLink;
  }

  function initNewsDetail(){
    var root = document.querySelector("[data-news-detail]");
    if(!root || typeof BAS_NEWS === "undefined") return;
    var slug = qs("n");
    var item = BAS_NEWS.find(function(n){ return n.slug === slug; }) || BAS_NEWS[0];

    document.title = (item.title_en || item.title) + " — BAS SWU News";
    setText("[data-n-title]", item.title_en || item.title);
    setText("[data-n-title-th]", item.title_en ? item.title : "");
    setText("[data-n-date]", item.date_en || item.date);
    setText("[data-n-category]", item.category_en || item.category);
    setText("[data-n-summary]", item.summary);
    var breadcrumbCur = document.querySelector("[data-n-breadcrumb]");
    if(breadcrumbCur) breadcrumbCur.textContent = item.title_en || item.title;

    var related = BAS_NEWS.filter(function(n){ return n.slug !== item.slug; }).slice(0,3);
    var relatedWrap = document.querySelector("[data-n-related]");
    if(relatedWrap){
      relatedWrap.innerHTML = related.map(function(n){
        return '<a class="card" href="news-detail.html?n='+n.slug+'">'+
          '<div class="card-media"><span class="ph-label">ภาพข่าว (ตัวอย่าง)</span></div>'+
          '<div class="card-body"><span class="card-tag'+(n.category_en==="News"?"":" crimson")+'">'+(n.category_en||n.category)+'</span>'+
          ((n.date_en||n.date)?'<span class="card-meta">'+(n.date_en||n.date)+'</span>':'')+
          '<h3 class="card-title bi-heading"><span class="bi-en">'+(n.title_en||n.title)+'</span><span class="bi-th th-body">'+n.title+'</span></h3></div></a>';
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
