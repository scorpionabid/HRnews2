// Modern JavaScript və jQuery istifadə edərək təkmilləşdirilmiş versiya
$(document).ready(function() {
  // Qlobal dəyişənlər
  const MOBILE_BREAKPOINT = 768;
  let newsCounter = 1;
  let darkMode = localStorage.getItem('darkMode') === 'enabled';

  // 1. Responsive Content Management
  class ResponsiveManager {
      static init() {
          this.handleMainContent();
          $(window).on('resize', _.debounce(() => this.handleMainContent(), 250));
      }

      static handleMainContent() {
          const mainContent = $('main .col-lg-8');
          $(window).width() < MOBILE_BREAKPOINT ? mainContent.slideUp(300) : mainContent.slideDown(300);
      }
  }

  // 2. Enhanced News Management
  class NewsManager {
      static init() {
          this.setupInfiniteScroll();
          this.setupLazyLoading();
          this.setupNewsAnimations();
      }

      static setupInfiniteScroll() {
          let isLoading = false;
          $(window).scroll(_.debounce(function() {
              if ($(window).scrollTop() + $(window).height() > $(document).height() - 100 && !isLoading) {
                  isLoading = true;
                  NewsManager.loadMoreNews(() => isLoading = false);
              }
          }, 100));
      }

      static loadMoreNews(callback) {
          // API-dan xəbərləri yükləmək simulyasiyası
          setTimeout(() => {
              for (let i = 0; i < 3; i++) {
                  this.addNews({
                      title: `Yeni Xəbər ${newsCounter}`,
                      content: 'Xəbər məzmunu buraya...',
                      category: 'Ümumi',
                      date: new Date().toLocaleDateString()
                  });
                  newsCounter++;
              }
              callback?.();
          }, 800);
      }

      static setupLazyLoading() {
          const options = {
              root: null,
              rootMargin: '50px',
              threshold: 0.1
          };

          const observer = new IntersectionObserver((entries) => {
              entries.forEach(entry => {
                  if (entry.isIntersecting) {
                      const img = entry.target;
                      img.src = img.dataset.src;
                      observer.unobserve(img);
                  }
              });
          }, options);

          $('img[data-src]').each(function() {
              observer.observe(this);
          });
      }

      static setupNewsAnimations() {
          $('.news-card').each(function(index) {
              $(this).css({
                  'animation': `fadeInUp 0.5s ease forwards ${index * 0.2}s`,
                  'opacity': '0'
              });
          });
      }

      static addNews(newsData) {
          const template = `
              <div class="news-card card shadow-sm mb-4" style="opacity: 0">
                  <div class="card-body">
                      <h5 class="card-title">${newsData.title}</h5>
                      <p class="card-text">${newsData.content}</p>
                      <div class="d-flex justify-content-between align-items-center">
                          <small class="text-muted">${newsData.date}</small>
                          <div class="btn-group">
                              <button class="btn btn-sm btn-outline-primary share-btn">
                                  <i class="fas fa-share-alt"></i>
                              </button>
                              <button class="btn btn-sm btn-outline-primary bookmark-btn">
                                  <i class="fas fa-bookmark"></i>
                              </button>
                          </div>
                      </div>
                  </div>
              </div>
          `;
          $('#news-container').append(template);
          this.setupNewsAnimations();
      }
  }

  // 3. Enhanced UI Effects
  class UIManager {
      static init() {
          this.setupHoverEffects();
          this.setupScrollEffects();
          this.setupDarkMode();
          this.setupNewsTicker();
      }

      static setupHoverEffects() {
          $('.card').hover(
              function() {
                  $(this).addClass('hover-effect');
              },
              function() {
                  $(this).removeClass('hover-effect');
              }
          );
      }

      static setupScrollEffects() {
          const scrollButton = $('<button>', {
              id: 'scroll-top',
              class: 'btn btn-primary position-fixed',
              html: '<i class="fas fa-arrow-up"></i>',
              css: {
                  bottom: '20px',
                  right: '20px',
                  display: 'none',
                  zIndex: 1000
              }
          }).appendTo('body');

          $(window).scroll(_.throttle(function() {
              $(this).scrollTop() > 300 
                  ? scrollButton.fadeIn() 
                  : scrollButton.fadeOut();
          }, 100));

          scrollButton.click(() => {
              $('html, body').animate({ scrollTop: 0 }, 600);
          });
      }

      static setupDarkMode() {
          const toggle = $('<button>', {
              id: 'dark-mode-toggle',
              class: 'btn position-fixed',
              html: darkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>',
              css: {
                  top: '20px',
                  right: '20px',
                  zIndex: 1000
              }
          }).appendTo('body');

          if (darkMode) $('body').addClass('dark-mode');

          toggle.click(() => {
              $('body').toggleClass('dark-mode');
              darkMode = !darkMode;
              localStorage.setItem('darkMode', darkMode ? 'enabled' : null);
              toggle.html(darkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>');
          });
      }

      static setupNewsTicker() {
          const ticker = $('.news-ticker');
          let tickerItems = ticker.children();
          let currentItem = 0;

          setInterval(() => {
              $(tickerItems[currentItem]).fadeOut(400, function() {
                  currentItem = (currentItem + 1) % tickerItems.length;
                  $(tickerItems[currentItem]).fadeIn(400);
              });
          }, 3000);
      }
  }

  // 4. Social Media Integration
  class SocialManager {
      static init() {
          this.setupShareButtons();
          this.setupSocialMetrics();
      }

      static setupShareButtons() {
          $('.share-btn').click(function(e) {
              e.preventDefault();
              const newsUrl = window.location.href;
              const newsTitle = $(this).closest('.card').find('.card-title').text();

              const shareData = {
                  title: newsTitle,
                  text: 'Maraqlı xəbər paylaşıram',
                  url: newsUrl
              };

              if (navigator.share) {
                  navigator.share(shareData);
              } else {
                  // Alternativ paylaşma metodu
                  const socialLinks = `
                      <div class="social-share-popup">
                          <a href="https://facebook.com/share?url=${newsUrl}" target="_blank">
                              <i class="fab fa-facebook"></i>
                          </a>
                          <a href="https://twitter.com/intent/tweet?url=${newsUrl}&text=${newsTitle}" target="_blank">
                              <i class="fab fa-twitter"></i>
                          </a>
                          <a href="https://www.linkedin.com/shareArticle?url=${newsUrl}&title=${newsTitle}" target="_blank">
                              <i class="fab fa-linkedin"></i>
                          </a>
                      </div>
                  `;
                  $(this).after(socialLinks);
              }
          });
      }

      static setupSocialMetrics() {
          // Sosial media metriklərini yeniləmək
          setInterval(() => {
              $('.news-card').each(function() {
                  const shares = Math.floor(Math.random() * 100);
                  const likes = Math.floor(Math.random() * 500);
                  $(this).find('.social-metrics').html(`
                      <small class="text-muted">
                          ${shares} paylaşım · ${likes} bəyənmə
                      </small>
                  `);
              });
          }, 30000);
      }
  }

  // 5. Performance Optimizations
  class PerformanceManager {
      static init() {
          this.setupImageOptimization();
          this.setupCaching();
      }

      static setupImageOptimization() {
          $('img').each(function() {
              if (!this.complete) {
                  $(this).attr('loading', 'lazy');
                  $(this).on('error', function() {
                      $(this).attr('src', '/path/to/fallback-image.jpg');
                  });
              }
          });
      }

      static setupCaching() {
          // Local Storage cache
          const cache = {
              set: (key, value, ttl = 3600000) => {
                  const item = {
                      value: value,
                      timestamp: new Date().getTime() + ttl
                  };
                  localStorage.setItem(key, JSON.stringify(item));
              },
              get: (key) => {
                  const item = localStorage.getItem(key);
                  if (!item) return null;
                  
                  const parsed = JSON.parse(item);
                  if (new Date().getTime() > parsed.timestamp) {
                      localStorage.removeItem(key);
                      return null;
                  }
                  return parsed.value;
              }
          };

          // Cache istifadəsi
          window.newsCache = cache;
      }
  }

  // Initialize all managers
  ResponsiveManager.init();
  NewsManager.init();
  UIManager.init();
  SocialManager.init();
  PerformanceManager.init();

  // CSS Styles
  const styles = `
      .hover-effect {
          transform: translateY(-5px);
          box-shadow: 0 4px 15px rgba(0,0,0,0.1);
          transition: all 0.3s ease;
      }

      .dark-mode {
          background-color: #121212;
          color: #ffffff;
      }

      .dark-mode .card {
          background-color: #1e1e1e;
          border-color: #2d2d2d;
      }

      @keyframes fadeInUp {
          from {
              opacity: 0;
              transform: translateY(20px);
          }
          to {
              opacity: 1;
              transform: translateY(0);
          }
      }

      .social-share-popup {
          position: absolute;
          background: white;
          padding: 10px;
          border-radius: 5px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          z-index: 1000;
      }

      .social-share-popup a {
          margin: 0 10px;
          font-size: 20px;
      }
  `;

  $('<style>').text(styles).appendTo('head');
});

// JavaScript to enhance the search form functionality
document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.getElementById("search-form");
  const searchInput = document.getElementById("search-input");

  // Handle form submission
  searchForm.addEventListener("submit", function (event) {
      // Prevent submission if input is empty
      if (searchInput.value.trim() === "") {
          event.preventDefault(); // Stop form submission
          alert("{% trans 'Axtarış sorğusu boş ola bilməz. Zəhmət olmasa, bir söz daxil edin.' %}");
          return;
      }

      // Optionally, you can perform any additional checks or preprocess the query here.
  });

  // Add a quick clear button for UX improvement (optional)
  const clearButton = document.createElement("button");
  clearButton.type = "button";
  clearButton.textContent = "×";
  clearButton.style.position = "absolute";
  clearButton.style.right = "10px";
  clearButton.style.top = "50%";
  clearButton.style.transform = "translateY(-50%)";
  clearButton.style.border = "none";
  clearButton.style.background = "transparent";
  clearButton.style.cursor = "pointer";
  clearButton.style.display = "none"; // Initially hidden

  // Append the clear button to the form
  searchInput.parentElement.style.position = "relative";
  searchInput.parentElement.appendChild(clearButton);

  // Show/hide the clear button based on input value
  searchInput.addEventListener("input", function () {
      clearButton.style.display = searchInput.value ? "block" : "none";
  });

  // Clear input when the clear button is clicked
  clearButton.addEventListener("click", function () {
      searchInput.value = "";
      clearButton.style.display = "none";
      searchInput.focus(); // Refocus input
  });
});
