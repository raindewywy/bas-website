// BAS SWU -- โหลด nav/footer ที่ใช้ร่วมกันทุกหน้า โดยไม่มี build step
// แก้ nav/footer แก้ที่ partials/nav.html · partials/footer.html แล้วเห็นผลทุกหน้าทันที
//
// ต้องเปิดผ่าน http(s) (Live Server / GitHub Pages / `python -m http.server`) —
// เปิดไฟล์ตรง ๆ แบบ file:// เบราว์เซอร์จะบล็อก fetch() ของไฟล์ local (CORS)
(function () {
  "use strict";

  function inject(el, html) {
    el.outerHTML = html;
  }

  function markCurrentNav() {
    var key = document.body.getAttribute("data-nav");
    if (!key) return;
    var item = document.querySelector('.nav-item[data-key="' + key + '"]');
    if (item) item.classList.add("current");
  }

  var nodes = Array.prototype.slice.call(document.querySelectorAll("[data-include]"));
  var pending = nodes.length;
  if (!pending) return;

  nodes.forEach(function (el) {
    var url = el.getAttribute("data-include");
    fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error(url + " -> " + res.status);
        return res.text();
      })
      .then(function (html) {
        inject(el, html);
      })
      .catch(function (err) {
        console.error("include.js:", err);
      })
      .finally(function () {
        pending -= 1;
        if (pending === 0) {
          markCurrentNav();
          // script.js โหลดก่อนหน้านี้แล้ว (ดู <script> ท้ายไฟล์) — ตอนนี้ nav/footer
          // อยู่ใน DOM ครบแล้ว จึงเรียก initNav() ที่ผูก event ของ header/drawer/search/admin ได้
          if (window.BASSite && typeof window.BASSite.initNav === "function") {
            window.BASSite.initNav();
          }
        }
      });
  });
})();
