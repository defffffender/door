document.addEventListener('DOMContentLoaded', function() {

    // ================================================================
    // MOBILE MENU
    // ================================================================
    const burger = document.getElementById('burgerBtn');
    const nav = document.getElementById('mainNav');
    let overlay = document.createElement('div');
    overlay.className = 'nav-overlay';
    // Insert overlay inside header to share stacking context with nav
    const header = document.querySelector('.header');
    if (header) {
        header.appendChild(overlay);
    } else {
        document.body.appendChild(overlay);
    }

    function closeMenu() {
        burger.classList.remove('active');
        nav.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (burger && nav) {
        burger.addEventListener('click', function() {
            burger.classList.toggle('active');
            nav.classList.toggle('active');
            overlay.classList.toggle('active');
            document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
        });
        overlay.addEventListener('click', closeMenu);
        // Close on nav link click (mobile)
        nav.querySelectorAll('.nav__link').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    }

    // ================================================================
    // HERO SLIDER (auto-play with pause on hover)
    // ================================================================
    const slider = document.getElementById('heroSlider');
    if (slider) {
        const track = slider.querySelector('.slider__track');
        const slides = slider.querySelectorAll('.slider__slide');
        const prevBtn = document.getElementById('sliderPrev');
        const nextBtn = document.getElementById('sliderNext');
        const dotsContainer = document.getElementById('sliderDots');
        let current = 0;
        const total = slides.length;

        if (total > 1) {
            for (let i = 0; i < total; i++) {
                const dot = document.createElement('button');
                dot.className = 'slider__dot' + (i === 0 ? ' active' : '');
                dot.addEventListener('click', () => goTo(i));
                dotsContainer.appendChild(dot);
            }
            const dots = dotsContainer.querySelectorAll('.slider__dot');

            function goTo(index) {
                current = (index + total) % total;
                track.style.transform = 'translateX(-' + (current * 100) + '%)';
                dots.forEach((d, i) => d.classList.toggle('active', i === current));
            }

            if (prevBtn) prevBtn.addEventListener('click', () => goTo(current - 1));
            if (nextBtn) nextBtn.addEventListener('click', () => goTo(current + 1));

            // Auto-play: 5s interval, pause on hover
            let autoPlay = setInterval(() => goTo(current + 1), 5000);
            slider.addEventListener('mouseenter', () => clearInterval(autoPlay));
            slider.addEventListener('mouseleave', () => {
                autoPlay = setInterval(() => goTo(current + 1), 5000);
            });

            // Swipe support for mobile
            let touchStartX = 0;
            slider.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
            slider.addEventListener('touchend', e => {
                const diff = touchStartX - e.changedTouches[0].clientX;
                if (Math.abs(diff) > 50) {
                    diff > 0 ? goTo(current + 1) : goTo(current - 1);
                }
            }, { passive: true });
        }
    }

    // ================================================================
    // SCROLL ANIMATIONS (fade-in / slide-up)
    // ================================================================
    const animatedElements = document.querySelectorAll(
        '.section__title, .section__subtitle, .section__divider, ' +
        '.product-card, .category-card, .advantage-card, .pillar-card, ' +
        '.stat-item, .partner-logo, .portfolio-card, .news-card, ' +
        '.about-home__text, .about-home__image, .contact-home, ' +
        '.contacts-info, .contacts-form, .slider__buttons'
    );

    animatedElements.forEach(el => el.classList.add('animate-on-scroll'));

    const scrollObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                scrollObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    animatedElements.forEach(el => scrollObserver.observe(el));

    // ================================================================
    // COUNTER ANIMATION (statistics numbers)
    // ================================================================
    const statNumbers = document.querySelectorAll('.stat-item__number');

    function animateCounter(el) {
        const text = el.textContent.trim();
        // Extract number and surrounding text (e.g., "48 000+" -> number=48000, suffix="+", prefix="")
        const match = text.match(/^([^\d]*)(\d[\d\s]*)(.*)$/);
        if (!match) return;

        const prefix = match[1];
        const numStr = match[2].replace(/\s/g, '');
        const suffix = match[3];
        const target = parseInt(numStr);
        if (isNaN(target)) return;

        const duration = 2000;
        const startTime = performance.now();

        function formatNum(n) {
            return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        }

        function step(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(target * eased);
            el.textContent = prefix + formatNum(current) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    }

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    statNumbers.forEach(el => counterObserver.observe(el));

    // ================================================================
    // PRODUCT GALLERY (thumbnail switch + lightbox)
    // ================================================================
    const thumbs = document.querySelectorAll('.product-gallery__thumb');
    const mainImage = document.querySelector('.product-gallery__main img');

    if (thumbs.length && mainImage) {
        thumbs.forEach(thumb => {
            thumb.addEventListener('click', function() {
                thumbs.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
                mainImage.src = this.querySelector('img').src;
            });
        });

        // Lightbox
        mainImage.style.cursor = 'zoom-in';
        mainImage.addEventListener('click', function() {
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = '<div class="lightbox__backdrop"></div>' +
                '<div class="lightbox__content">' +
                '<img src="' + this.src + '" alt="">' +
                '<button class="lightbox__close">&times;</button>' +
                '</div>';
            document.body.appendChild(lightbox);
            document.body.style.overflow = 'hidden';
            requestAnimationFrame(() => lightbox.classList.add('active'));

            function closeLightbox() {
                lightbox.classList.remove('active');
                setTimeout(() => {
                    lightbox.remove();
                    document.body.style.overflow = '';
                }, 300);
            }

            lightbox.querySelector('.lightbox__backdrop').addEventListener('click', closeLightbox);
            lightbox.querySelector('.lightbox__close').addEventListener('click', closeLightbox);
            document.addEventListener('keydown', function handler(e) {
                if (e.key === 'Escape') { closeLightbox(); document.removeEventListener('keydown', handler); }
            });
        });
    }

    // ================================================================
    // BACK TO TOP + FLOATING BUTTONS
    // ================================================================
    const floatingBtns = document.querySelector('.floating-buttons');
    const backToTop = document.getElementById('backToTop');

    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                floatingBtns.classList.add('visible');
            } else {
                floatingBtns.classList.remove('visible');
            }
        }, { passive: true });

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ================================================================
    // IMAGE SKELETON LOADING
    // ================================================================
    document.querySelectorAll('.product-card__image img, .category-card__image img, .portfolio-card__image img, .news-card__image img').forEach(img => {
        img.parentElement.classList.add('skeleton-loading');
        if (img.complete) {
            img.parentElement.classList.remove('skeleton-loading');
        } else {
            img.addEventListener('load', function() {
                this.parentElement.classList.remove('skeleton-loading');
            });
            img.addEventListener('error', function() {
                this.parentElement.classList.remove('skeleton-loading');
            });
        }
    });

    // ================================================================
    // CATALOG SEARCH (live filter on category page)
    // ================================================================
    const searchInput = document.getElementById('catalogSearch');
    if (searchInput) {
        const cards = document.querySelectorAll('.product-card');
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            cards.forEach(card => {
                const name = card.querySelector('.product-card__name');
                const text = name ? name.textContent.toLowerCase() : '';
                card.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // ================================================================
    // CATALOG SORT/FILTER
    // ================================================================
    const sortSelect = document.getElementById('catalogSort');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const url = new URL(window.location);
            if (this.value) {
                url.searchParams.set('sort', this.value);
            } else {
                url.searchParams.delete('sort');
            }
            window.location = url;
        });
    }

    // ================================================================
    // AUTO-DISMISS MESSAGES
    // ================================================================
    document.querySelectorAll('.message').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(30px)';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });

});
