/* Progressive enhancement only: every page works without this file. */
(function () {
  "use strict";

  var burger = document.querySelector("[data-burger]");
  var mobileNav = document.getElementById("mobile-nav");

  if (burger && mobileNav) {
    burger.addEventListener("click", function () {
      var open = mobileNav.getAttribute("data-open") === "true";
      mobileNav.setAttribute("data-open", String(!open));
      burger.setAttribute("aria-expanded", String(!open));
      burger.setAttribute("aria-label", open ? "Open menu" : "Close menu");
    });
  }

  // Submenus inside the mobile drawer.
  document.querySelectorAll("[data-subtoggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var panel = button.closest("li").querySelector(".mobile-nav__sub");
      if (!panel) return;
      var open = panel.getAttribute("data-open") === "true";
      panel.setAttribute("data-open", String(!open));
      button.setAttribute("aria-expanded", String(!open));
    });
  });
})();
