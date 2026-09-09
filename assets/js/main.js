(function () {
  "use strict";

  /**
   * Highlight the current page link in the navigation menu
   */
  function highlightCurrentPage() {
    const currentPage = window.location.pathname.split("/").pop().replace(/\/$/, "") || "index.html";

    const navLinks = document.querySelectorAll("#navmenu a");
    navLinks.forEach((link) => {
      const href = link.getAttribute("href");
      if (!href || href === "#") return;
      const linkHref = href.replace(/\/$/, "");
      if (linkHref === currentPage) {
        link.classList.add("active");
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
      // pick the right header file based on page
      const headerFile = document.body.dataset.site === 'inner' || document.body.classList.contains('anime-page')
        ? 'headerme.html'
        : 'header.html';
      const response = await fetch(headerFile, { cache: 'no-cache' });
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
    if (typeof imagesLoaded !== 'function' || typeof Isotope === 'undefined') return;
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
    // Highlight the current page link
    highlightCurrentPage();

    /**
     * Apply .scrolled class to the body as the page is scrolled down
     */
    function toggleScrolled() {
      const selectBody = document.querySelector("body");
      const selectHeader = document.querySelector("#header");
      if (!selectHeader) return; // <- 关键：header 异步加载前别报错

      if (
        !selectHeader.classList.contains("scroll-up-sticky") &&
        !selectHeader.classList.contains("sticky-top") &&
        !selectHeader.classList.contains("fixed-top")
      ) return;

      window.scrollY > 100
        ? selectBody.classList.add("scrolled")
        : selectBody.classList.remove("scrolled");
    }

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
    document.querySelectorAll("#navmenu a").forEach((link) => {
      link.addEventListener("click", (e) => {
        const parentLi = link.closest("li");

        // Is it the top-level dropdown item? (Notes)
        // Check two things:
        //  1) It's in an <li class="dropdown">
        //  2) Its href is "#" (dummy link)
        if (
          parentLi &&
          parentLi.classList.contains("dropdown") &&
          link.getAttribute("href") === "#"
        ) {
          // Prevent navigation and toggle
          e.preventDefault();
          parentLi.classList.toggle("active");

          // Show/hide the nested <ul>
          const subMenu = parentLi.querySelector("ul");
          if (subMenu) subMenu.classList.toggle("dropdown-active");

        } else {
          // Otherwise, it's either a normal top-level link 
          // or a sub-item link within the dropdown
          // => let it navigate, but close mobile nav if open
          if (document.querySelector(".mobile-nav-active")) {
            // close mobile nav
            document.querySelector("body").classList.remove("mobile-nav-active");
            const mobileNavToggleBtn = document.querySelector(".mobile-nav-toggle");
            if (mobileNavToggleBtn) {
              mobileNavToggleBtn.classList.add("bi-list");
              mobileNavToggleBtn.classList.remove("bi-x");
            }
          }
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
    });

    window.addEventListener("load", toggleScrollTop);
    document.addEventListener("scroll", toggleScrollTop);
  }

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    if (typeof AOS === "undefined") return;
    AOS.init({
      duration: 600,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
  }
  window.addEventListener("load", aosInit);

  /**
   * Init typed.js
   */
  const selectTyped = document.querySelector(".typed");
  if (selectTyped) {
    let typedStrings = selectTyped.getAttribute("data-typed-items");
    typedStrings = typedStrings.split(",");
    if (typeof Typed !== "undefined") new Typed(".typed", {
      strings: typedStrings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000,
    });
  }

  /**
   * Initiate Pure Counter
   */
  if (typeof PureCounter !== "undefined") new PureCounter();

  /**
   * Animate the skills items on reveal
   */
  let skillsAnimation = document.querySelectorAll(".skills-animation");
  skillsAnimation.forEach((item) => {
    if (typeof Waypoint === "undefined") return;
    new Waypoint({
      element: item,
      offset: "80%",
      handler: function () {
        let progress = item.querySelectorAll(".progress .progress-bar");
        progress.forEach((el) => {
          el.style.width = el.getAttribute("aria-valuenow") + "%";
        });
      },
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    if (typeof Swiper === "undefined") return;
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }
  window.addEventListener("load", initSwiper);

  /**
   * Initiate GLightbox
   */
  if (typeof GLightbox === "function") {
    GLightbox({ selector: ".glightbox" });
  }

  /**
   * Example: custom pagination for tabbed swipers
   */
  function initSwiperWithCustomPagination(swiperElement, config) {
    // Example logic if your "tabbed" swipers need custom pagination or triggers
    new Swiper(swiperElement, config);
  }

})();
