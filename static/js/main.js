// BalansAI.uz - Professional JavaScript

// Floating Navbar scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.floating-navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const body = document.body;

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const isActive = mobileMenuBtn.classList.contains('active');
            
            if (isActive) {
                mobileMenuBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
                setTimeout(() => {
                    mobileMenu.classList.add('hidden');
                }, 300);
                body.style.overflow = '';
            } else {
                mobileMenuBtn.classList.add('active');
                mobileMenu.classList.remove('hidden');
                setTimeout(() => {
                    mobileMenu.classList.add('active');
                }, 10);
                body.style.overflow = 'hidden';
            }
        });

        // Close menu when clicking on links
        const mobileLinks = mobileMenu.querySelectorAll('.mobile-nav-link, .mobile-nav-cta');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenuBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
                setTimeout(() => {
                    mobileMenu.classList.add('hidden');
                }, 300);
                body.style.overflow = '';
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                if (mobileMenuBtn.classList.contains('active')) {
                    mobileMenuBtn.classList.remove('active');
                    mobileMenu.classList.remove('active');
                    setTimeout(() => {
                        mobileMenu.classList.add('hidden');
                    }, 300);
                    body.style.overflow = '';
                }
            }
        });
    }
});

// Animated Counter
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = formatNumber(target);
            clearInterval(timer);
        } else {
            element.textContent = formatNumber(Math.floor(current));
        }
    }, 16);
}

function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K+';
    }
    return num.toString();
}

// Initialize counters when they come into view
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
            const target = parseInt(entry.target.getAttribute('data-target') || entry.target.textContent);
            entry.target.classList.add('counted');
            animateCounter(entry.target, target);
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.counter-number');
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
});

// Scroll animations
const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.addEventListener('DOMContentLoaded', function() {
    const fadeElements = document.querySelectorAll('.fade-on-scroll');
    fadeElements.forEach(el => {
        fadeObserver.observe(el);
    });
});

// Smooth scroll for anchor links
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href !== '') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.classList.add('error');
                } else {
                    this.classList.remove('error');
                }
            });
            
            input.addEventListener('input', function() {
                if (this.value.trim() !== '') {
                    this.classList.remove('error');
                }
            });
        });
    });
});

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

// Dashboard card sticky/fixed behavior
document.addEventListener('DOMContentLoaded', function() {
    const dashboardCard = document.querySelector('.dashboard-overlay-section .card');
    const dashboardSection = document.querySelector('.dashboard-overlay-section');
    
    if (dashboardCard && dashboardSection) {
        let cardOffsetTop = 0;
        let cardHeight = 0;
        let isFixed = false;
        
        // Calculate initial positions
        function updatePositions() {
            cardOffsetTop = dashboardSection.offsetTop;
            cardHeight = dashboardCard.offsetHeight;
        }
        
        updatePositions();
        
        // Recalculate on resize
        window.addEventListener('resize', function() {
            updatePositions();
        });
        
        window.addEventListener('scroll', function() {
            const scrollY = window.scrollY || window.pageYOffset;
            
            // Calculate when card should become fixed (when section reaches top)
            const shouldBeFixed = scrollY >= cardOffsetTop - 100;
            
            if (shouldBeFixed && !isFixed) {
                isFixed = true;
                dashboardCard.classList.add('dashboard-fixed');
                // Add padding to section to prevent content jump
                dashboardSection.style.paddingBottom = cardHeight + 'px';
            } else if (!shouldBeFixed && isFixed) {
                isFixed = false;
                dashboardCard.classList.remove('dashboard-fixed');
                dashboardSection.style.paddingBottom = '';
            }
        }, { passive: true });
    }
});
