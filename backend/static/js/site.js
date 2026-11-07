/* Progressive enhancement only. Every page works with this file absent:
   the menu links all resolve on their own, and revealed sections are visible
   by default unless this script takes over. */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");

  /* ---------------------------------------------------------------- menu */

  var burger = document.querySelector("[data-burger]");
  var sidenav = document.getElementById("sidenav");
  var scrim = document.querySelector("[data-scrim]");
  var closeBtn = document.querySelector("[data-close]");
  var lastFocus = null;

  function setMenu(open) {
    if (!sidenav) return;
    sidenav.setAttribute("data-open", String(open));
    sidenav.setAttribute("aria-hidden", String(!open));
    if (scrim) {
      scrim.hidden = false;
      scrim.setAttribute("data-open", String(open));
    }
    if (burger) {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    document.body.style.overflow = open ? "hidden" : "";

    if (open) {
      lastFocus = document.activeElement;
      var first = sidenav.querySelector("a, button");
      if (first) first.focus();
    } else if (lastFocus) {
      lastFocus.focus();
      lastFocus = null;
    }
  }

  if (burger) burger.addEventListener("click", function () {
    setMenu(sidenav.getAttribute("data-open") !== "true");
  });
  if (closeBtn) closeBtn.addEventListener("click", function () { setMenu(false); });
  if (scrim) scrim.addEventListener("click", function () { setMenu(false); });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && sidenav && sidenav.getAttribute("data-open") === "true") {
      setMenu(false);
    }
  });

  // Keep focus inside the panel while it is open.
  if (sidenav) sidenav.addEventListener("keydown", function (e) {
    if (e.key !== "Tab" || sidenav.getAttribute("data-open") !== "true") return;
    var items = sidenav.querySelectorAll("a[href], button:not([disabled])");
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  // Submenus.
  document.querySelectorAll("[data-subtoggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var panel = button.closest("li").querySelector(".sidenav__sub");
      if (!panel) return;
      var open = panel.getAttribute("data-open") === "true";
      panel.setAttribute("data-open", String(!open));
      button.setAttribute("aria-expanded", String(!open));
    });
  });

  /* ------------------------------------------------------- sticky header */

  var header = document.querySelector(".header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("is-stuck", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* -------------------------------------------------------- reveal on scroll */

  var revealables = document.querySelectorAll("[data-reveal]");
  if (!revealables.length) return;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced || !("IntersectionObserver" in window)) {
    revealables.forEach(function (el) { el.classList.add("is-in"); });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-in");
      observer.unobserve(entry.target);
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });

  revealables.forEach(function (el) { observer.observe(el); });

  // Anything already on screen at load should not wait for a scroll.
  window.addEventListener("load", function () {
    revealables.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight) el.classList.add("is-in");
    });
  });
})();
