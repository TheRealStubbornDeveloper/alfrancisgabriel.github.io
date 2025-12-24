    /*!
     * Start Bootstrap - Grayscale v6.0.2 (https://startbootstrap.com/themes/grayscale)
     * Copyright 2013-2020 Start Bootstrap
     * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
     */
    (function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using vanilla JS
    document.querySelectorAll('a[href*="#"]:not([href="#"])').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Closes responsive menu when a scroll trigger link is clicked
    document.querySelectorAll('.js-scroll-trigger').forEach(function(anchor) {
        anchor.addEventListener('click', function() {
            const mobileMenu = document.getElementById('mobileMenu');
            if (mobileMenu) {
                mobileMenu.style.display = 'none';
            }
        });
    });

    // Navbar shrink on scroll
    window.addEventListener('scroll', function() {
        const nav = document.getElementById('mainNav');
        if (window.pageYOffset > 50) {
            nav.classList.add('bg-gray-900');
        } else {
            nav.classList.remove('bg-gray-900');
        }
    });



    // Fade in sections on scroll
    $(window).on('scroll', function() {
        $('.fade-in').each(function() {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            if (elementBottom > viewportTop && elementTop < viewportBottom) {
                $(this).addClass('visible');
            }
        });
    });



    // Mobile menu toggle
    window.toggleMenu = function() {
        const menu = document.getElementById('mobileMenu');
        const button = document.querySelector('button[onclick="toggleMenu()"]');
        const isOpen = menu.style.display === 'block';
        menu.style.display = isOpen ? 'none' : 'block';
        button.setAttribute('aria-expanded', !isOpen);
    };

    // Typing animation
    if (document.getElementById('typed-text')) {
        const typed = new Typed('#typed-text', {
            strings: ['Learn more about StubbornDeveloper', 'Interested in data engineering? Reach out', 'Explore my Python and AWS skills', 'Check out my projects on GitHub', 'Contact me via LinkedIn or email'],
            typeSpeed: 50,
            backSpeed: 30,
            backDelay: 2000,
            loop: true
        });
    }

    // Back to top button
    const backToTopBtn = document.getElementById('backToTop');
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
            backToTopBtn.style.opacity = '1';
        } else {
            backToTopBtn.style.opacity = '0';
            setTimeout(() => backToTopBtn.style.display = 'none', 300);
        }
    });
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
})(jQuery); // End of use strict
