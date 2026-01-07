// BalansAI.uz - Main JavaScript

// Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all elements with fade-on-scroll class
document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-on-scroll');
    fadeElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red-500');
        } else {
            input.classList.remove('border-red-500');
        }
    });

    return isValid;
}

// Auto-hide alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// Button hover wave effect
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(button => {
        button.addEventListener('mouseenter', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: translate(-50%, -50%);
                pointer-events: none;
                animation: ripple 0.6s ease-out;
            `;
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';

            button.style.position = 'relative';
            button.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
});

// Add ripple animation CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            width: 300px;
            height: 300px;
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Parallax effect for hero section
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const heroSection = document.querySelector('.hero-gradient');

    if (heroSection && scrolled < window.innerHeight) {
        heroSection.style.transform = `translateY(${scrolled * 0.3}px)`;
        heroSection.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;
    }
});

// Card tilt effect on hover
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', function() {
            card.style.transform = '';
        });
    });
});

// ========================================
// ADVANCED SCROLL ANIMATIONS & EFFECTS
// ========================================

// Scroll Progress Indicator
function updateScrollProgress() {
    const scrollProgress = document.querySelector('.scroll-progress');
    if (!scrollProgress) {
        const progressBar = document.createElement('div');
        progressBar.className = 'scroll-progress';
        document.body.appendChild(progressBar);
    }

    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;

    const progressBar = document.querySelector('.scroll-progress');
    if (progressBar) {
        progressBar.style.width = scrolled + '%';
    }
}

window.addEventListener('scroll', updateScrollProgress);

// Advanced Reveal on Scroll
const revealObserverOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -100px 0px'
};

const revealObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            // Keep observing for elements that might scroll out and in again
        }
    });
}, revealObserverOptions);

document.addEventListener('DOMContentLoaded', function() {
    // Observe all reveal elements
    const revealElements = document.querySelectorAll(
        '.reveal-fade, .reveal-slide-left, .reveal-slide-right, .reveal-scale, .reveal-rotate, .text-reveal, .clip-reveal'
    );

    revealElements.forEach(el => {
        revealObserver.observe(el);
    });
});

// Parallax Layers Effect
function updateParallaxLayers() {
    const scrolled = window.pageYOffset;
    const parallaxLayers = document.querySelectorAll('.parallax-layer');

    parallaxLayers.forEach((layer, index) => {
        const speed = (index + 1) * 0.15;
        const yPos = -(scrolled * speed);
        layer.style.transform = `translate3d(0, ${yPos}px, 0)`;
    });
}

window.addEventListener('scroll', function() {
    requestAnimationFrame(updateParallaxLayers);
});

// 3D Icon Mouse Tracking
document.addEventListener('DOMContentLoaded', function() {
    const icon3dElements = document.querySelectorAll('.icon-3d');

    icon3dElements.forEach(icon => {
        icon.addEventListener('mousemove', function(e) {
            const rect = icon.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            icon.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });

        icon.addEventListener('mouseleave', function() {
            icon.style.transform = 'rotateX(0) rotateY(0) scale(1)';
        });
    });
});

// Magnetic Button Effect
document.addEventListener('DOMContentLoaded', function() {
    const magneticButtons = document.querySelectorAll('.btn-magnetic');

    magneticButtons.forEach(button => {
        button.addEventListener('mousemove', function(e) {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
        });

        button.addEventListener('mouseleave', function() {
            button.style.transform = 'translate(0, 0)';
        });
    });
});

// Image Zoom on Scroll
function updateImageZoom() {
    const imageZoomContainers = document.querySelectorAll('.image-zoom-container');

    imageZoomContainers.forEach(container => {
        const rect = container.getBoundingClientRect();
        const windowHeight = window.innerHeight;

        if (rect.top < windowHeight && rect.bottom > 0) {
            const scrollPercent = 1 - (rect.top / windowHeight);
            const scale = 1 + (scrollPercent * 0.2);

            const image = container.querySelector('.image-zoom');
            if (image) {
                image.style.transform = `scale(${Math.min(scale, 1.2)})`;
            }
        }
    });
}

window.addEventListener('scroll', function() {
    requestAnimationFrame(updateImageZoom);
});

// Sticky Section with Slide-Over Effect
function updateStickySections() {
    const stickySections = document.querySelectorAll('.sticky-section');

    stickySections.forEach((section, index) => {
        const rect = section.getBoundingClientRect();
        const nextSection = section.nextElementSibling;

        if (nextSection && nextSection.classList.contains('slide-over-section')) {
            if (rect.top <= 0) {
                const opacity = Math.max(0, 1 - Math.abs(rect.top) / (window.innerHeight * 0.5));
                section.style.opacity = opacity;
            } else {
                section.style.opacity = 1;
            }
        }
    });
}

window.addEventListener('scroll', function() {
    requestAnimationFrame(updateStickySections);
});

// Horizontal Scroll Indicator
document.addEventListener('DOMContentLoaded', function() {
    const horizontalScrollWrappers = document.querySelectorAll('.horizontal-scroll-wrapper');

    horizontalScrollWrappers.forEach(wrapper => {
        wrapper.addEventListener('scroll', function() {
            const scrollLeft = wrapper.scrollLeft;
            const scrollWidth = wrapper.scrollWidth - wrapper.clientWidth;
            const scrollPercent = (scrollLeft / scrollWidth) * 100;

            // Can be used to show progress indicator
            console.log('Horizontal scroll progress:', scrollPercent + '%');
        });
    });
});

// Text Split Animation
function splitTextToSpans(element) {
    const text = element.textContent;
    const words = text.split(' ');
    element.innerHTML = '';

    words.forEach((word, index) => {
        const span = document.createElement('span');
        span.textContent = word;
        span.style.animationDelay = `${index * 0.1}s`;
        element.appendChild(span);

        if (index < words.length - 1) {
            element.appendChild(document.createTextNode(' '));
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const splitTextElements = document.querySelectorAll('.split-text');
    splitTextElements.forEach(el => {
        splitTextToSpans(el);
    });
});

// Smooth Scroll for Anchor Links (Enhanced)
document.addEventListener('DOMContentLoaded', function() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');

    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);

            if (target) {
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
                const startPosition = window.pageYOffset;
                const distance = targetPosition - startPosition;
                const duration = 1000;
                let start = null;

                function animation(currentTime) {
                    if (start === null) start = currentTime;
                    const timeElapsed = currentTime - start;
                    const run = ease(timeElapsed, startPosition, distance, duration);
                    window.scrollTo(0, run);
                    if (timeElapsed < duration) requestAnimationFrame(animation);
                }

                function ease(t, b, c, d) {
                    t /= d / 2;
                    if (t < 1) return c / 2 * t * t + b;
                    t--;
                    return -c / 2 * (t * (t - 2) - 1) + b;
                }

                requestAnimationFrame(animation);
            }
        });
    });
});

// Intersection Observer for lazy loading 3D elements
const lazyLoadObserver = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = entry.target;

            // Add loaded class for 3D icons
            if (element.classList.contains('icon-3d-container')) {
                element.classList.add('loaded');
            }

            lazyLoadObserver.unobserve(element);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '50px'
});

document.addEventListener('DOMContentLoaded', function() {
    const lazyElements = document.querySelectorAll('.icon-3d-container, .lazy-load');
    lazyElements.forEach(el => {
        lazyLoadObserver.observe(el);
    });
});

// Mouse move parallax effect for containers
document.addEventListener('DOMContentLoaded', function() {
    const parallaxContainers = document.querySelectorAll('.parallax-container');

    parallaxContainers.forEach(container => {
        container.addEventListener('mousemove', function(e) {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const percentX = (x - centerX) / centerX;
            const percentY = (y - centerY) / centerY;

            const layers = container.querySelectorAll('.parallax-layer');
            layers.forEach((layer, index) => {
                const depth = (index + 1) * 10;
                const moveX = percentX * depth;
                const moveY = percentY * depth;

                layer.style.transform = `translate(${moveX}px, ${moveY}px)`;
            });
        });

        container.addEventListener('mouseleave', function() {
            const layers = container.querySelectorAll('.parallax-layer');
            layers.forEach(layer => {
                layer.style.transform = 'translate(0, 0)';
            });
        });
    });
});

// Initialize all animations on load
document.addEventListener('DOMContentLoaded', function() {
    // Add a small delay to ensure smooth initial load
    setTimeout(function() {
        document.body.classList.add('animations-ready');
    }, 100);
});
