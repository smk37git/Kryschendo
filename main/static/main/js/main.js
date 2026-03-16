// ===== Mobile Navigation Toggle =====
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const hamburgerIcon = document.getElementById('hamburger-icon');
const closeIcon = document.getElementById('close-icon');

if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', () => {
    const isOpen = !mobileMenu.classList.contains('hidden');
    mobileMenu.classList.toggle('hidden');
    hamburgerIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');
    mobileMenuBtn.setAttribute('aria-expanded', !isOpen);
  });
}

// ===== Scroll-Triggered Animations =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px',
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.fade-in-up, .fade-in').forEach((el) => {
  observer.observe(el);
});

// ===== Navbar Scroll Effect =====
const nav = document.getElementById('main-nav');
let lastScroll = 0;

window.addEventListener('scroll', () => {
  const currentScroll = window.scrollY;
  if (currentScroll > 50) {
    nav.classList.add('nav-scrolled');
  } else {
    nav.classList.remove('nav-scrolled');
  }
  lastScroll = currentScroll;
});

// ===== Hero Animations =====
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

(() => {
  const heroSection = document.getElementById('hero');
  if (!heroSection) return;

  // Character-by-character text reveal
  const charRevealEl = heroSection.querySelector('.hero-reveal-char');
  if (charRevealEl) {
    const text = charRevealEl.dataset.text;
    charRevealEl.innerHTML = '';
    for (let i = 0; i < text.length; i++) {
      const span = document.createElement('span');
      span.className = 'hero-char';
      span.textContent = text[i] === ' ' ? '\u00A0' : text[i];
      span.style.transitionDelay = `${400 + i * 35}ms`;
      charRevealEl.appendChild(span);
    }
  }

  // Staggered element reveals
  const heroReveals = heroSection.querySelectorAll('.hero-reveal');
  const heroChars = heroSection.querySelectorAll('.hero-char');

  if (prefersReducedMotion) {
    heroReveals.forEach((el) => el.classList.add('hero-visible'));
    heroChars.forEach((el) => el.classList.add('hero-visible'));
    return;
  }

  // Trigger reveals after a short load delay
  setTimeout(() => {
    heroReveals.forEach((el) => {
      const delay = parseInt(el.dataset.delay || '0', 10);
      setTimeout(() => el.classList.add('hero-visible'), delay);
    });
    heroChars.forEach((el) => el.classList.add('hero-visible'));
  }, 200);

  // Floating particles
  createHeroParticles();
})();

function createHeroParticles() {
  const container = document.getElementById('hero-particles');
  if (!container || prefersReducedMotion) return;

  const particleCount = 25;
  const types = ['hero-particle-gold', 'hero-particle-cream', 'hero-particle-white'];

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    const size = Math.random() * 6 + 2;
    const type = types[Math.floor(Math.random() * types.length)];
    const duration = Math.random() * 8 + 6;
    const delay = Math.random() * 10;
    const startX = Math.random() * 100;
    const startY = Math.random() * 100;
    const endX = startX + (Math.random() - 0.5) * 30;
    const endY = startY - Math.random() * 40 - 10;
    const opacity = Math.random() * 0.5 + 0.2;

    particle.className = `hero-particle ${type}`;
    particle.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      left: ${startX}%;
      top: ${startY}%;
      --px-start: 0px;
      --py-start: 0px;
      --px-end: ${(endX - startX) * 3}px;
      --py-end: ${(endY - startY) * 3}px;
      --p-opacity: ${opacity};
      animation: particleFloat ${duration}s ease-in-out ${delay}s infinite;
    `;
    container.appendChild(particle);
  }
}

// ===== Testimonial Carousel (Upgraded) =====
const track = document.getElementById('testimonial-track');
if (track) {
  const cards = track.querySelectorAll('.testimonial-card');
  const dotsContainer = document.getElementById('carousel-dots');
  const progressBar = document.getElementById('carousel-progress-bar');
  let currentIndex = 0;
  let cardsPerView = 1;
  const autoPlayDuration = 5000;
  let autoPlayTimer = null;
  let progressAnimation = null;

  const updateCardsPerView = () => {
    if (window.innerWidth >= 1024) cardsPerView = 3;
    else if (window.innerWidth >= 768) cardsPerView = 2;
    else cardsPerView = 1;
  };

  const getTotalPages = () => Math.max(1, Math.ceil(cards.length / cardsPerView));

  const getCurrentPage = () => Math.floor(currentIndex / cardsPerView);

  // Build dot indicators
  const buildDots = () => {
    if (!dotsContainer) return;
    dotsContainer.innerHTML = '';
    const totalPages = getTotalPages();
    for (let i = 0; i < totalPages; i++) {
      const dot = document.createElement('button');
      dot.className = `carousel-dot${i === getCurrentPage() ? ' active' : ''}`;
      dot.setAttribute('aria-label', `Go to slide group ${i + 1}`);
      dot.addEventListener('click', () => {
        goToPage(i);
        restartAutoPlay();
      });
      dotsContainer.appendChild(dot);
    }
  };

  const updateDots = () => {
    if (!dotsContainer) return;
    const page = getCurrentPage();
    dotsContainer.querySelectorAll('.carousel-dot').forEach((dot, i) => {
      dot.classList.toggle('active', i === page);
    });
  };

  const moveToIndex = (index) => {
    const maxIndex = Math.max(0, cards.length - cardsPerView);
    currentIndex = Math.min(Math.max(index, 0), maxIndex);
    const offset = -(currentIndex * (100 / cardsPerView));
    track.style.transform = `translateX(${offset}%)`;
    updateDots();
  };

  const goToPage = (page) => {
    moveToIndex(page * cardsPerView);
  };

  const nextSlide = () => {
    const maxIndex = Math.max(0, cards.length - cardsPerView);
    if (currentIndex >= maxIndex) {
      moveToIndex(0);
    } else {
      moveToIndex(currentIndex + 1);
    }
  };

  const prevSlide = () => {
    const maxIndex = Math.max(0, cards.length - cardsPerView);
    if (currentIndex <= 0) {
      moveToIndex(maxIndex);
    } else {
      moveToIndex(currentIndex - 1);
    }
  };

  // Progress bar animation
  const startProgressBar = () => {
    if (!progressBar || prefersReducedMotion) return;
    progressBar.style.width = '0%';
    progressBar.classList.remove('animating');

    // Force reflow
    void progressBar.offsetWidth;

    progressBar.classList.add('animating');
    progressBar.style.transitionDuration = `${autoPlayDuration}ms`;
    progressBar.style.width = '100%';
  };

  const resetProgressBar = () => {
    if (!progressBar) return;
    progressBar.classList.remove('animating');
    progressBar.style.width = '0%';
  };

  // Auto-play with progress
  const startAutoPlay = () => {
    stopAutoPlay();
    startProgressBar();
    autoPlayTimer = setInterval(() => {
      nextSlide();
      startProgressBar();
    }, autoPlayDuration);
  };

  const stopAutoPlay = () => {
    if (autoPlayTimer) {
      clearInterval(autoPlayTimer);
      autoPlayTimer = null;
    }
    resetProgressBar();
  };

  const restartAutoPlay = () => {
    stopAutoPlay();
    startAutoPlay();
  };

  // Pause on hover
  const carouselContainer = document.getElementById('testimonial-carousel');
  if (carouselContainer) {
    carouselContainer.addEventListener('mouseenter', stopAutoPlay);
    carouselContainer.addEventListener('mouseleave', startAutoPlay);
  }

  // Touch/swipe support
  let touchStartX = 0;
  let touchEndX = 0;

  if (carouselContainer) {
    carouselContainer.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoPlay();
    }, { passive: true });

    carouselContainer.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const diff = touchStartX - touchEndX;
      if (Math.abs(diff) > 50) {
        if (diff > 0) nextSlide();
        else prevSlide();
      }
      startAutoPlay();
    }, { passive: true });
  }

  // Navigation buttons
  const prevBtn = document.getElementById('carousel-prev');
  const nextBtn = document.getElementById('carousel-next');
  if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); restartAutoPlay(); });
  if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); restartAutoPlay(); });

  // Keyboard navigation
  if (carouselContainer) {
    carouselContainer.setAttribute('tabindex', '0');
    carouselContainer.setAttribute('role', 'region');
    carouselContainer.setAttribute('aria-label', 'Testimonial carousel');
    carouselContainer.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { prevSlide(); restartAutoPlay(); }
      if (e.key === 'ArrowRight') { nextSlide(); restartAutoPlay(); }
    });
  }

  // Initialize
  updateCardsPerView();
  buildDots();
  startAutoPlay();

  window.addEventListener('resize', () => {
    updateCardsPerView();
    moveToIndex(currentIndex);
    buildDots();
  });
}
