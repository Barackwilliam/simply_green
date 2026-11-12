/* Progressive enhancement only. Every page works with this file absent:
   the menu links all resolve on their own, and revealed sections are visible
   by default unless this script takes over. */
(function () {
  "use strict";

  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

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

  /* ---------------------------------------------------------- slideshow */

  document.querySelectorAll("[data-slider]").forEach(function (root) {
    var slides = root.querySelectorAll(".hero__slide");
    if (slides.length < 2) return;

    var dots = root.querySelectorAll("[data-dot]");
    var counter = root.querySelector("[data-slide-now]");
    var prev = root.querySelector("[data-prev]");
    var next = root.querySelector("[data-next]");
    // Three seconds per slide, as the client asked.
    var DELAY = 3000;
    var index = 0;
    var timer = null;
    var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    // Autoplay must not restart underneath someone who is still reading,
    // which is what happened when an arrow was clicked with the pointer
    // resting on the slideshow.
    var held = false;

    root.style.setProperty("--hero-delay", DELAY + "ms");

    // A slide that is not showing is transparent, not off screen, so the
    // browser counts it as in the viewport and downloads it immediately —
    // loading="lazy" buys nothing. Three hero photographs came to 1.7MB
    // before the page had painted. Only the first carries a src in the
    // markup; the rest are fetched here, one slide ahead of being needed.
    // With JavaScript off there is no way to reach them, so nothing is lost.
    function load(i) {
      var slide = slides[(i + slides.length) % slides.length];
      // The <source> first: setting the img's src while the source list is
      // still empty makes the browser commit to the JPEG fallback, and the
      // WebP arriving a moment later is a second download, not a cheaper
      // first one.
      var source = slide.querySelector("source[data-srcset]");
      if (source) {
        source.srcset = source.dataset.srcset;
        source.removeAttribute("data-srcset");
      }
      var img = slide.querySelector("img[data-src]");
      if (!img) return;
      img.src = img.dataset.src;
      img.removeAttribute("data-src");
    }

    function show(to) {
      index = (to + slides.length) % slides.length;
      load(index);
      load(index + 1);
      slides.forEach(function (slide, i) {
        var on = i === index;
        slide.classList.toggle("is-active", on);
        slide.setAttribute("aria-hidden", String(!on));
      });
      if (counter) counter.textContent = String(index + 1);
      dots.forEach(function (dot, i) {
        dot.setAttribute("aria-selected", String(i === index));
        // Restart the timer bar rather than letting it continue from
        // wherever the previous slide left it.
        var fill = dot.querySelector(".hero__dot-fill");
        if (fill) {
          fill.style.animation = "none";
          void fill.offsetWidth;
          fill.style.animation = "";
        }
      });
    }

    function play() {
      if (still || held) return;
      stop();
      timer = window.setInterval(function () { show(index + 1); }, DELAY);
      root.classList.remove("is-paused");
    }

    function stop() {
      if (timer) { window.clearInterval(timer); timer = null; }
      root.classList.add("is-paused");
    }

    function go(to) { show(to); if (held) stop(); else play(); }

    if (prev) prev.addEventListener("click", function () { go(index - 1); });
    if (next) next.addEventListener("click", function () { go(index + 1); });
    dots.forEach(function (dot, i) {
      dot.addEventListener("click", function () { go(i); });
    });

    // Reading the slide should not have it snatched away.
    root.addEventListener("mouseenter", function () { held = true; stop(); });
    root.addEventListener("mouseleave", function () { held = false; play(); });
    root.addEventListener("focusin", function () { held = true; stop(); });
    root.addEventListener("focusout", function (e) {
      if (!root.contains(e.relatedTarget)) { held = false; play(); }
    });

    // Nothing moves while the tab is in the background.
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop(); else play();
    });

    // Swipe.
    var startX = null;
    root.addEventListener("touchstart", function (e) {
      startX = e.changedTouches[0].clientX; stop();
    }, { passive: true });

    root.addEventListener("touchend", function (e) {
      if (startX === null) return;
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 45) go(dx < 0 ? index + 1 : index - 1); else play();
      startX = null;
    }, { passive: true });

    // Arrow keys when the slideshow has focus.
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") { e.preventDefault(); go(index - 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); go(index + 1); }
    });

    // show(0) would fetch slide two straight away, which is the competition
    // for bandwidth this was meant to remove. Mark slide one active without
    // touching the others, and wait for the page to settle first.
    slides[0].classList.add("is-active");
    var warm = function () { load(1); };
    if (window.requestIdleCallback) {
      window.addEventListener("load", function () { window.requestIdleCallback(warm); });
    } else {
      window.addEventListener("load", function () { window.setTimeout(warm, 400); });
    }
    play();
  });

  /* ----------------------------------------------------------- carousels */

  document.querySelectorAll("[data-carousel]").forEach(function (root) {
    var view = root.querySelector(".carousel__viewport");
    var prev = root.parentElement.querySelector("[data-cprev]")
            || document.querySelector("[data-cprev]");
    var next = root.parentElement.querySelector("[data-cnext]")
            || document.querySelector("[data-cnext]");
    var section = root.closest("section") || document;
    prev = section.querySelector("[data-cprev]");
    next = section.querySelector("[data-cnext]");
    if (!view) return;

    function step() {
      var item = view.querySelector(".carousel__item");
      if (!item) return view.clientWidth;
      var gap = parseFloat(getComputedStyle(view).columnGap || "0") || 0;
      return item.getBoundingClientRect().width + gap;
    }

    function sync() {
      if (!prev || !next) return;
      var max = view.scrollWidth - view.clientWidth - 2;
      prev.disabled = view.scrollLeft <= 2;
      next.disabled = view.scrollLeft >= max;
      // One screenful of cards means nothing to scroll to.
      var idle = view.scrollWidth <= view.clientWidth + 2;
      prev.hidden = next.hidden = idle;
    }

    if (prev) prev.addEventListener("click", function () {
      view.scrollBy({ left: -step(), behavior: "smooth" });
    });
    if (next) next.addEventListener("click", function () {
      view.scrollBy({ left: step(), behavior: "smooth" });
    });

    view.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  });

  /* ------------------------------------------------------------ counters */

  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var countObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        countObs.unobserve(el);
        var target = parseFloat(el.getAttribute("data-count"));
        if (isNaN(target)) return;
        // Preserve how the editor wrote it: 12,400 stays 12,400.
        var grouped = /,/.test(el.textContent);
        var decimals = (String(target).split(".")[1] || "").length;
        var started = null;
        var DURATION = 1400;
        var tick = function (now) {
          if (started === null) started = now;
          var t = Math.min((now - started) / DURATION, 1);
          var eased = 1 - Math.pow(1 - t, 3);
          var value = target * eased;
          el.textContent = grouped
            ? value.toLocaleString("en-GB", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
            : value.toFixed(decimals);
          if (t < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { countObs.observe(el); });
  }

  /* --------------------------------------------------------- back to top */

  var toTop = document.querySelector("[data-totop]");
  if (toTop) {
    var showTop = function () { toTop.hidden = window.scrollY < 700; };
    window.addEventListener("scroll", showTop, { passive: true });
    showTop();
    toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  }

  /* ------------------------------------------------------- card tilt */

  // A slight tilt toward the pointer and a light that follows it. Only for
  // a mouse or trackpad (a finger has no hover), and never when the
  // reader has asked for less motion.
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (fine && !still) {
    document.querySelectorAll(
      ".card, .pillar, .fcard, .vcard, .photogrid__item > a, .fieldreel__item"
    ).forEach(function (el) {
      el.classList.add("tilt");
      if (getComputedStyle(el).position === "static") el.style.position = "relative";
      var glow = document.createElement("span");
      glow.className = "tilt__glow";
      glow.setAttribute("aria-hidden", "true");
      el.appendChild(glow);
      var frame = 0;
      el.addEventListener("pointermove", function (e) {
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(function () {
          var r = el.getBoundingClientRect();
          var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
          el.style.setProperty("--mx", x * 100 + "%");
          el.style.setProperty("--my", y * 100 + "%");
          el.style.setProperty("--rx", (x - 0.5) * 7 + "deg");
          el.style.setProperty("--ry", (0.5 - y) * 7 + "deg");
          el.classList.add("is-tilting");
        });
      });
      el.addEventListener("pointerleave", function () {
        cancelAnimationFrame(frame);
        el.classList.remove("is-tilting");
      });
    });
  }

  /* -------------------------------------------------------- reveal on scroll */

  // [data-reveal] is one element. [data-reveal-group] is a grid or a row
  // whose children should arrive one after another — which is most of
  // what is on this site, and tagging every card by hand across twenty
  // templates would have been twenty chances to forget.
  var revealables = document.querySelectorAll("[data-reveal], [data-reveal-group]");
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
