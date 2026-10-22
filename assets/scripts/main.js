/*
 * secure-software-development-portfolio
 * Simple, dependency-free navigation behaviour.
 *
 * - Mobile nav toggle (opens/closes the off-canvas sidebar).
 * - Active nav item highlighting, resolved from each link's resolved URL
 *   rather than a hard-coded repository path, so the site works at a domain
 *   root, under a GitHub Pages project path, or opened via file://.
 */
(function () {
  "use strict";

  var navWrap = document.querySelector(".nav-wrap");
  var menuToggle = document.querySelector(".menu-toggle");

  if (!navWrap) return;

  /* ---------- Mobile nav toggle ---------- */
  if (menuToggle) {
    menuToggle.addEventListener("click", function () {
      var open = navWrap.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    // Close the mobile nav when a link is clicked or Escape is pressed.
    navWrap.addEventListener("click", function (event) {
      if (event.target.closest("a") && window.matchMedia("(max-width: 900px)").matches) {
        navWrap.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && navWrap.classList.contains("open")) {
        navWrap.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
        menuToggle.focus();
      }
    });
  }

  /* ---------- Active nav item highlighting ---------- */
  var navLinks = navWrap.querySelectorAll(".nav-list a");
  var currentPath = window.location.pathname.replace(/\/+$/, "") || "/";

  function normalise(path) {
    // Treat "/" and "/index.html" as the same page.
    if (path === "/" || path === "/index.html") return "/";
    return path;
  }

  // Clear any hard-coded active state so the resolved match is authoritative.
  navLinks.forEach(function (link) {
    link.classList.remove("active");
    link.removeAttribute("aria-current");
  });

  navLinks.forEach(function (link) {
    var href = link.getAttribute("href");
    if (!href) return;

    // Skip external links and pure fragments.
    if (/^(https?:|mailto:|tel:|#)/i.test(href)) return;

    // Resolve the link relative to this document so it works at any base path.
    var url;
    try {
      url = new URL(href, window.location.href);
    } catch (err) {
      return;
    }
    if (url.origin !== window.location.origin) return;

    var targetPath = normalise(url.pathname.replace(/\/+$/, "") || "/");
    if (targetPath === normalise(currentPath)) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
  });
})();

