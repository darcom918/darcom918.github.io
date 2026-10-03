$(function () {

    // Header Scroll
    $(window).scroll(function () {
        if ($(window).scrollTop() >= 60) {
            $("header").addClass("fixed-header");
        } else {
            $("header").removeClass("fixed-header");
        }
    });


    // Featured Owl Carousel
    $('.featured-projects-slider .owl-carousel').owlCarousel({
        center: true,
        loop: true,
        margin: 30,
        nav: false,
        dots: false,
        autoplay: true,
        autoplayTimeout: 5000,
        autoplayHoverPause: false,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            }
        }
    })


    // Count - uses a numeric data-target and preserves any suffix (e.g. +).
    $('.count').each(function () {
        const $el = $(this);
        const original = $el.text().trim();
        const target = Number($el.data('target')) || parseInt(original.replace(/[^0-9.-]/g, ''), 10) || 0;
        const suffix = original.replace(/[0-9.,\s-]/g, '');
        $({ Counter: 0 }).animate({ Counter: target }, {
            duration: 1000,
            easing: 'swing',
            step: function (now) { $el.text(Math.ceil(now) + (suffix ? ' ' + suffix : '')); },
            complete: function () { $el.text(target + (suffix ? ' ' + suffix : '')); }
        });
    });


    // ScrollToTop
    function scrollToTop() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }

    const btn = document.getElementById("scrollToTopBtn");
    if (btn) btn.addEventListener("click", scrollToTop);

    window.onscroll = function () {
        const btn = document.getElementById("scrollToTopBtn");
        if (document.documentElement.scrollTop > 100 || document.body.scrollTop > 100) {
            if (btn) btn.style.display = "flex";
        } else {
            if (btn) btn.style.display = "none";
        }
    };


    // Aos
	AOS.init({
		once: true,
	});

});

