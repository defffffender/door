document.addEventListener('DOMContentLoaded', function() {

    // === Mobile Menu ===
    const burger = document.getElementById('burgerBtn');
    const nav = document.getElementById('mainNav');
    let overlay = document.createElement('div');
    overlay.className = 'nav-overlay';
    document.body.appendChild(overlay);

    if (burger && nav) {
        burger.addEventListener('click', function() {
            burger.classList.toggle('active');
            nav.classList.toggle('active');
            overlay.classList.toggle('active');
            document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
        });
        overlay.addEventListener('click', function() {
            burger.classList.remove('active');
            nav.classList.remove('active');
            overlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    // === Hero Slider ===
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
            // Create dots
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

            // Auto-play
            let autoPlay = setInterval(() => goTo(current + 1), 5000);
            slider.addEventListener('mouseenter', () => clearInterval(autoPlay));
            slider.addEventListener('mouseleave', () => {
                autoPlay = setInterval(() => goTo(current + 1), 5000);
            });
        }
    }

    // === Product Gallery Thumbnails ===
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
    }

    // === Auto-dismiss messages ===
    const messages = document.querySelectorAll('.message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(30px)';
            setTimeout(() => msg.remove(), 300);
        }, 4000);
    });

});
