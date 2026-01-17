// BalansAI.uz - Premium Minimalist Design
// 3 Colors: Blue, Black, White

// ============================================
// FULLSCREEN MENU
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const fullscreenMenu = document.getElementById('fullscreen-menu');
    const menuIconOpen = menuBtn?.querySelector('.menu-icon-open');
    const menuIconClose = menuBtn?.querySelector('.menu-icon-close');
    const body = document.body;

    if (menuBtn && fullscreenMenu) {
        menuBtn.addEventListener('click', function() {
            const isActive = fullscreenMenu.classList.contains('active');
            
            if (isActive) {
                // Close menu
                fullscreenMenu.classList.remove('active');
                menuIconOpen.style.display = 'block';
                menuIconClose.style.display = 'none';
                body.style.overflow = '';
            } else {
                // Open menu
                fullscreenMenu.classList.add('active');
                menuIconOpen.style.display = 'none';
                menuIconClose.style.display = 'block';
                body.style.overflow = 'hidden';
            }
        });

        // Close menu when clicking on links
        const menuLinks = fullscreenMenu.querySelectorAll('.menu-link');
        menuLinks.forEach(link => {
            link.addEventListener('click', function() {
                fullscreenMenu.classList.remove('active');
                menuIconOpen.style.display = 'block';
                menuIconClose.style.display = 'none';
                body.style.overflow = '';
            });
        });
    }
});

// ============================================
// NAVBAR BACKGROUND CHANGE ON SCROLL
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.getElementById('main-navbar');
    const sections = document.querySelectorAll('.snap-section');
    
    if (navbar && sections.length > 0) {
        const observerOptions = {
            threshold: 0.5,
            rootMargin: '-80px 0px 0px 0px'
        };
        
        const sectionObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const section = entry.target;
                    
                    // Remove all classes
                    navbar.classList.remove('on-white', 'on-blue', 'on-black');
                    
                    // Add appropriate class
                    if (section.classList.contains('bg-white')) {
                        navbar.classList.add('on-white');
                    } else if (section.classList.contains('bg-blue')) {
                        navbar.classList.add('on-blue');
                    } else {
                        navbar.classList.add('on-black');
                    }
                }
            });
        }, observerOptions);
        
        sections.forEach(section => {
            sectionObserver.observe(section);
        });
    }
});

// ============================================
// SCROLL ANIMATIONS - Elements appear on scroll
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    const animatableElements = document.querySelectorAll(
        '.stat-item, .feature-card, .how-step, .pricing-card, .faq-item'
    );
    
    animatableElements.forEach(el => {
        observer.observe(el);
    });
});

// ============================================
// FAQ ACCORDION
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        if (question) {
            question.addEventListener('click', function() {
                const isActive = item.classList.contains('active');
                
                // Close all other items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                    }
                });
                
                // Toggle current item
                item.classList.toggle('active');
            });
        }
    });
});

// ============================================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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

// ============================================
// TESTIMONIALS PAUSE ON HOVER
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.testimonials-track');
    
    if (track) {
        track.addEventListener('mouseenter', function() {
            this.style.animationPlayState = 'paused';
        });
        
        track.addEventListener('mouseleave', function() {
            this.style.animationPlayState = 'running';
        });
    }
});

// ============================================
// SCROLL INDICATOR HIDE ON SCROLL
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    
    if (scrollIndicator) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                scrollIndicator.style.opacity = '0';
                scrollIndicator.style.pointerEvents = 'none';
            } else {
                scrollIndicator.style.opacity = '1';
                scrollIndicator.style.pointerEvents = 'auto';
            }
        }, { passive: true });
    }
});

// ============================================
// AUTO-HIDE ALERTS
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
});

// ============================================
// FORM VALIDATION
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    this.style.borderColor = '#dc2626';
                } else {
                    this.style.borderColor = '';
                }
            });
            
            input.addEventListener('input', function() {
                if (this.value.trim() !== '') {
                    this.style.borderColor = '';
                }
            });
        });
    });
});

// ============================================
// LANGUAGE SWITCHER (Placeholder)
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const langBtn = document.getElementById('lang-btn');
    
    if (langBtn) {
        langBtn.addEventListener('click', function() {
            // Placeholder - implement language switching logic
            alert('Til o\'zgartirish tez orada qo\'shiladi!');
        });
    }
});

// ============================================
// PARALLAX EFFECT ON HERO
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const heroSection = document.querySelector('.hero-section');
    
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.scrollY;
            const heroContent = heroSection.querySelector('.hero-content');
            
            if (heroContent && scrolled < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroContent.style.opacity = 1 - (scrolled / window.innerHeight);
            }
        }, { passive: true });
    }
});
