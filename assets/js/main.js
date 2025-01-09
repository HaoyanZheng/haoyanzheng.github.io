(function () {
  "use strict";

  /**
   * Highlight the current page link in the navigation menu
   */
  function highlightCurrentPage() {
    // Get the current page name (without trailing slash)
    const currentPage = window.location.pathname.split("/").pop().replace(/\/$/, "") || "index.html";
    console.log("Current page:", currentPage); // Debugging log

    // Select all nav links
    const navLinks = document.querySelectorAll("#navmenu a");
    navLinks.forEach((link) => {
      const linkHref = link.getAttribute("href").replace(/\/$/, "");
      if (linkHref === currentPage) {
        link.classList.add("active");
        console.log(`Active link set: ${linkHref}`); // Debugging log
      } else {
        link.classList.remove("active");
      }
    });
  }

  /**
   * Load the header from an external file (header.html)
   */
  async function loadHeader() {
    try {
      const response = await fetch("header.html");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const text = await response.text();

      // Insert header HTML into #header
      const headerContainer = document.querySelector("#header");
      headerContainer.outerHTML = text;
      console.log("Header loaded at:", new Date()); // Debugging log

      // Once header is loaded, initialize header-related features
      initializeHeaderFeatures();
    } catch (error) {
      console.error("Error loading header:", error);
    }
  }

  /**
   * Initialize all header-related features
   */
  function initializeHeaderFeatures() {
    console.log("Initializing header features..."); // Debugging log

    // Highlight the current page link
    highlightCurrentPage();

    /**
     * Apply .scrolled class to the body as the page is scrolled down
     */
    function toggleScrolled() {
      const selectBody = document.querySelector("body");
      const selectHeader = document.querySelector("#header");
      if (
        !selectHeader.classList.contains("scroll-up-sticky") &&
        !selectHeader.classList.contains("sticky-top") &&
        !selectHeader.classList.contains("fixed-top")
      ) return;
      window.scrollY > 100
        ? selectBody.classList.add("scrolled")
        : selectBody.classList.remove("scrolled");
    }
    document.addEventListener("scroll", toggleScrolled);
    window.addEventListener("load", toggleScrolled);

    /**
     * Mobile nav toggle
     */
    const mobileNavToggleBtn = document.querySelector(".mobile-nav-toggle");
    function mobileNavToggle() {
      document.querySelector("body").classList.toggle("mobile-nav-active");
      if (mobileNavToggleBtn) {
        mobileNavToggleBtn.classList.toggle("bi-list");
        mobileNavToggleBtn.classList.toggle("bi-x");
      }
    }
    if (mobileNavToggleBtn) {
      mobileNavToggleBtn.addEventListener("click", mobileNavToggle);
    }

    // Hide mobile nav on same-page/hash links
    document.querySelectorAll("#navmenu a").forEach((navmenu) => {
      navmenu.addEventListener("click", () => {
        if (document.querySelector(".mobile-nav-active")) {
          mobileNavToggle();
        }
      });
    });

    // Toggle mobile nav dropdowns
    document.querySelectorAll(".navmenu .toggle-dropdown").forEach((navmenu) => {
      navmenu.addEventListener("click", function (e) {
        e.preventDefault();
        this.parentNode.classList.toggle("active");
        this.parentNode.nextElementSibling.classList.toggle("dropdown-active");
      });
    });
  }

  /**
   * Main: load header on DOMContentLoaded
   */
  document.addEventListener("DOMContentLoaded", () => {
    loadHeader();
  });

  /**
   * Preloader
   */
  const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      preloader.remove();
      console.log("Preloader removed"); // Debugging log
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector(".scroll-top");

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100
        ? scrollTop.classList.add("active")
        : scrollTop.classList.remove("active");
    }
  }
  if (scrollTop) {
    scrollTop.addEventListener("click", (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
      console.log("Scroll to top"); // Debugging log
    });

    window.addEventListener("load", toggleScrollTop);
    document.addEventListener("scroll", toggleScrollTop);
  }

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
    console.log("AOS Initialized"); // Debugging log
  }
  window.addEventListener("load", aosInit);

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector(".typed");
  if (selectTyped) {
    let typedStrings = selectTyped.getAttribute("data-typed-items");
    typedStrings = typedStrings.split(",");
    new Typed(".typed", {
      strings: typedStrings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000,
    });
    console.log("Typed.js Initialized"); // Debugging log
  }

  /**
   * Initiate Pure Counter
   */
  new PureCounter();
  console.log("PureCounter Initialized"); // Debugging log

  /**
   * Animate the skills items on reveal
   */
  let skillsAnimation = document.querySelectorAll(".skills-animation");
  skillsAnimation.forEach((item) => {
    new Waypoint({
      element: item,
      offset: "80%",
      handler: function () {
        let progress = item.querySelectorAll(".progress .progress-bar");
        progress.forEach((el) => {
          el.style.width = el.getAttribute("aria-valuenow") + "%";
        });
        console.log("Skills Animation Triggered"); // Debugging log
      },
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
      console.log("Swiper Initialized"); // Debugging log
    });
  }
  window.addEventListener("load", initSwiper);

  /**
   * Initiate GLightbox
   */
  const glightbox = GLightbox({
    selector: ".glightbox",
  });
  console.log("GLightbox Initialized"); // Debugging log

  /**
   * Example: custom pagination for tabbed swipers
   */
  function initSwiperWithCustomPagination(swiperElement, config) {
    // Example logic if your "tabbed" swipers need custom pagination or triggers
    new Swiper(swiperElement, config);
    console.log("Swiper with custom pagination initialized");
  }

})();
