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
    
    // Hero section hide on scroll
    const hero = document.querySelector('.hero-gradient');
    if (hero) {
        if (window.scrollY > window.innerHeight * 0.5) {
            hero.classList.add('scrolled');
        } else {
            hero.classList.remove('scrolled');
        }
    }
}, { passive: true });

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

// FAQ Accordion
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
                if (isActive) {
                    item.classList.remove('active');
                } else {
                    item.classList.add('active');
                }
            });
        }
    });
});

// Newsletter Form
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('.newsletter-input');
            const email = emailInput.value.trim();
            
            if (email) {
                // Here you would typically send the email to your backend
                alert('Rahmat! Newsletter\'ga muvaffaqiyatli qo\'shildingiz.');
                emailInput.value = '';
            }
        });
    }
});

// Dashboard Images Scroll Animation
document.addEventListener('DOMContentLoaded', function() {
    const dashboardSection = document.querySelector('.dashboard-overlay-section');
    const image1 = document.querySelector('.dashboard-image-1');
    const image2 = document.querySelector('.dashboard-image-2');
    const image3 = document.querySelector('.dashboard-image-3');
    
    if (dashboardSection && image1 && image2 && image3) {
        let currentImage = 1;
        let sectionTop = dashboardSection.offsetTop;
        let sectionHeight = dashboardSection.offsetHeight;
        
        function updateImages() {
            const scrollY = window.scrollY || window.pageYOffset;
            const viewportHeight = window.innerHeight;
            const sectionStart = sectionTop - viewportHeight;
            const scrollProgress = (scrollY - sectionStart) / (sectionHeight * 0.6);
            
            // Clamp scroll progress between 0 and 1
            const progress = Math.max(0, Math.min(1, scrollProgress));
            
            // Show image 1 initially (0-33%)
            if (progress < 0.33) {
                if (currentImage !== 1) {
                    currentImage = 1;
                    image1.style.opacity = '1';
                    image1.style.transform = 'translateX(0)';
                    image2.style.opacity = '0';
                    image2.style.transform = 'translateX(100%)';
                    image3.style.opacity = '0';
                    image3.style.transform = 'translateX(100%)';
                }
            }
            // Show image 2 when scroll reaches 33% (33-66%)
            else if (progress < 0.66) {
                if (currentImage !== 2) {
                    currentImage = 2;
                    image1.style.opacity = '0';
                    image1.style.transform = 'translateX(-100%)';
                    image2.style.opacity = '1';
                    image2.style.transform = 'translateX(0)';
                    image3.style.opacity = '0';
                    image3.style.transform = 'translateX(100%)';
                }
            }
            // Show image 3 when scroll reaches 66% (66-100%)
            else {
                if (currentImage !== 3) {
                    currentImage = 3;
                    image1.style.opacity = '0';
                    image1.style.transform = 'translateX(-100%)';
                    image2.style.opacity = '0';
                    image2.style.transform = 'translateX(-100%)';
                    image3.style.opacity = '1';
                    image3.style.transform = 'translateX(0)';
                }
            }
        }
        
        // Initial check
        updateImages();
        
        // Update on scroll
        window.addEventListener('scroll', function() {
            updateImages();
        }, { passive: true });
        
        // Recalculate on resize
        window.addEventListener('resize', function() {
            sectionTop = dashboardSection.offsetTop;
            sectionHeight = dashboardSection.offsetHeight;
        });
    }
});
