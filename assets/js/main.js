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
      const response = await fetch('header.html');
      if (!response.ok) throw new Error(`Failed to load header: ${response.statusText}`);
      const headerHTML = await response.text();
      document.querySelector('#header').outerHTML = headerHTML;

      // Initialize header-related features
      initializeHeaderFeatures();

      // Initialize Isotope after the header is loaded
      initIsotopeLayout();
    } catch (error) {
      console.error('Error loading header:', error);
    }
  }

  // Call Isotope initialization separately
  function initIsotopeLayout() {
    document.querySelectorAll('.isotope-layout').forEach(function (isotopeItem) {
      let layout = isotopeItem.getAttribute('data-layout') ?? 'masonry';
      let filter = isotopeItem.getAttribute('data-default-filter') ?? '*';
      let sort = isotopeItem.getAttribute('data-sort') ?? 'original-order';

      let initIsotope;
      imagesLoaded(isotopeItem.querySelector('.isotope-container'), function () {
        initIsotope = new Isotope(isotopeItem.querySelector('.isotope-container'), {
          itemSelector: '.isotope-item',
          layoutMode: layout,
          filter: filter,
          sortBy: sort,
        });
      });

      isotopeItem.querySelectorAll('.isotope-filters li').forEach(function (filters) {
        filters.addEventListener('click', function () {
          isotopeItem.querySelector('.isotope-filters .filter-active').classList.remove('filter-active');
          this.classList.add('filter-active');
          initIsotope.arrange({
            filter: this.getAttribute('data-filter'),
          });
          if (typeof AOS !== 'undefined' && typeof AOS.init === 'function') {
            AOS.init(); // Reinitialize animations on filtering
          }
        });
      });
    });
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
     * Mobile nav toggle (applies to all headers)
     */
    document.querySelectorAll('.mobile-nav-toggle').forEach(btn => {
      btn.addEventListener('click', () => {
        document.body.classList.toggle('mobile-nav-active');
        btn.classList.toggle('bi-list');
        btn.classList.toggle('bi-x');
      });
    });

    // Hide mobile nav on link click & handle dropdowns
    document.querySelectorAll('nav.navmenu a').forEach(link => {
      link.addEventListener('click', e => {
        const dropdownLi = link.closest('li.dropdown');
        if (dropdownLi && link.getAttribute('href') === '#') {
          e.preventDefault();
          dropdownLi.classList.toggle('active');
          dropdownLi.querySelector('ul')
            .classList.toggle('dropdown-active');
        } else if (document.body.classList.contains('mobile-nav-active')) {
          document.body.classList.remove('mobile-nav-active');
          document.querySelectorAll('.mobile-nav-toggle').forEach(btn => {
            btn.classList.add('bi-list');
            btn.classList.remove('bi-x');
          });
        }
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
