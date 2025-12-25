/* ============================================
   CINEMA DARK MODE - Custom JavaScript
   Movie Review API
   ============================================ */

(function() {
    'use strict';

    // ============================================
    // Toast Notification System
    // ============================================
    class ToastNotification {
        constructor() {
            this.container = this.createContainer();
        }

        createContainer() {
            let container = document.querySelector('.toast-container');
            if (!container) {
                container = document.createElement('div');
                container.className = 'toast-container';
                document.body.appendChild(container);
            }
            return container;
        }

        show(message, type = 'info', duration = 5000) {
            const toast = document.createElement('div');
            toast.className = `custom-toast ${type}`;
            
            const icons = {
                success: 'fa-check-circle',
                error: 'fa-exclamation-circle',
                warning: 'fa-exclamation-triangle',
                info: 'fa-info-circle'
            };

            const titles = {
                success: 'Success',
                error: 'Error',
                warning: 'Warning',
                info: 'Info'
            };

            toast.innerHTML = `
                <div class="toast-header">
                    <div class="toast-title">
                        <i class="fas ${icons[type]}"></i>
                        <span>${titles[type]}</span>
                    </div>
                    <button class="toast-close" aria-label="Close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="toast-body">${message}</div>
            `;

            this.container.appendChild(toast);

            // Close button functionality
            const closeBtn = toast.querySelector('.toast-close');
            closeBtn.addEventListener('click', () => {
                this.remove(toast);
            });

            // Auto remove after duration
            setTimeout(() => {
                this.remove(toast);
            }, duration);

            return toast;
        }

        remove(toast) {
            toast.style.animation = 'fadeOut 0.3s ease-in forwards';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }

        success(message, duration) {
            return this.show(message, 'success', duration);
        }

        error(message, duration) {
            return this.show(message, 'error', duration);
        }

        warning(message, duration) {
            return this.show(message, 'warning', duration);
        }

        info(message, duration) {
            return this.show(message, 'info', duration);
        }
    }

    // Create global toast instance
    window.toast = new ToastNotification();

    // ============================================
    // Star Rating Component
    // ============================================
    class StarRating {
        constructor(element, options = {}) {
            this.element = element;
            this.options = {
                maxStars: options.maxStars || 5,
                initialRating: options.initialRating || 0,
                readonly: options.readonly || false,
                onRate: options.onRate || null
            };
            this.currentRating = this.options.initialRating;
            this.hoveredRating = 0;
            this.init();
        }

        init() {
            this.element.classList.add('star-rating');
            this.render();
            if (!this.options.readonly) {
                this.attachEvents();
            }
        }

        render() {
            this.element.innerHTML = '';
            for (let i = 1; i <= this.options.maxStars; i++) {
                const star = document.createElement('i');
                star.className = this.getStarClass(i);
                star.dataset.rating = i;
                this.element.appendChild(star);
            }
        }

        getStarClass(index) {
            const rating = this.hoveredRating || this.currentRating;
            if (index <= rating) {
                return 'fas fa-star active';
            }
            return 'far fa-star';
        }

        attachEvents() {
            const stars = this.element.querySelectorAll('i');
            
            stars.forEach(star => {
                // Click event
                star.addEventListener('click', () => {
                    const rating = parseInt(star.dataset.rating);
                    this.setRating(rating);
                });

                // Hover event
                star.addEventListener('mouseenter', () => {
                    const rating = parseInt(star.dataset.rating);
                    this.hoveredRating = rating;
                    this.updateStars();
                });
            });

            // Mouse leave
            this.element.addEventListener('mouseleave', () => {
                this.hoveredRating = 0;
                this.updateStars();
            });
        }

        setRating(rating) {
            this.currentRating = rating;
            this.updateStars();
            if (this.options.onRate) {
                this.options.onRate(rating);
            }
        }

        updateStars() {
            const stars = this.element.querySelectorAll('i');
            stars.forEach((star, index) => {
                star.className = this.getStarClass(index + 1);
            });
        }

        getRating() {
            return this.currentRating;
        }
    }

    // Export StarRating to global scope
    window.StarRating = StarRating;

    // ============================================
    // Initialize Star Ratings on Page Load
    // ============================================
    function initializeStarRatings() {
        const ratingElements = document.querySelectorAll('[data-star-rating]');
        ratingElements.forEach(element => {
            const readonly = element.hasAttribute('data-readonly');
            const initialRating = parseInt(element.getAttribute('data-rating')) || 0;
            const inputId = element.getAttribute('data-input');
            
            const starRating = new StarRating(element, {
                initialRating: initialRating,
                readonly: readonly,
                onRate: (rating) => {
                    if (inputId) {
                        const input = document.getElementById(inputId);
                        if (input) {
                            input.value = rating;
                        }
                    }
                }
            });
            
            // Store instance on element
            element.starRatingInstance = starRating;
        });
    }

    // ============================================
    // Skeleton Loader
    // ============================================
    function createSkeletonLoader(count = 6) {
        const container = document.createElement('div');
        container.className = 'skeleton-loader row';
        
        for (let i = 0; i < count; i++) {
            const skeleton = document.createElement('div');
            skeleton.className = 'col-md-6 col-lg-4 mb-4';
            skeleton.innerHTML = `
                <div class="skeleton-card">
                    <div class="skeleton-image"></div>
                    <div class="skeleton-content">
                        <div class="skeleton-title"></div>
                        <div class="skeleton-text"></div>
                        <div class="skeleton-text"></div>
                        <div class="skeleton-text"></div>
                    </div>
                </div>
            `;
            container.appendChild(skeleton);
        }
        
        return container;
    }

    window.createSkeletonLoader = createSkeletonLoader;

    // ============================================
    // Smooth Scroll
    // ============================================
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#') return;
                
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // ============================================
    // Animate on Scroll
    // ============================================
    function initAnimateOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('.animate-on-scroll').forEach(element => {
            observer.observe(element);
        });
    }

    // ============================================
    // Form Validation Enhancement
    // ============================================
    function enhanceFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');
        
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                if (!form.checkValidity()) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Show toast for validation error
                    toast.error('Please fill in all required fields correctly.');
                }
                
                form.classList.add('was-validated');
            }, false);
        });
    }

    // ============================================
    // Loading State Helper
    // ============================================
    class LoadingButton {
        constructor(button) {
            this.button = button;
            this.originalText = button.innerHTML;
            this.isLoading = false;
        }

        start(loadingText = 'Loading...') {
            if (this.isLoading) return;
            
            this.isLoading = true;
            this.button.disabled = true;
            this.button.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                ${loadingText}
            `;
        }

        stop() {
            this.isLoading = false;
            this.button.disabled = false;
            this.button.innerHTML = this.originalText;
        }
    }

    window.LoadingButton = LoadingButton;

    // ============================================
    // Django Messages to Toast Conversion
    // ============================================
    function convertDjangoMessages() {
        const messagesContainer = document.querySelector('.django-messages');
        if (!messagesContainer) return;

        const messages = messagesContainer.querySelectorAll('.alert');
        messages.forEach(message => {
            const text = message.textContent.trim();
            let type = 'info';
            
            if (message.classList.contains('alert-success')) type = 'success';
            else if (message.classList.contains('alert-danger')) type = 'error';
            else if (message.classList.contains('alert-warning')) type = 'warning';
            
            toast.show(text, type);
            message.remove();
        });

        // Hide the container if empty
        if (messagesContainer.children.length === 0) {
            messagesContainer.style.display = 'none';
        }
    }

    // ============================================
    // Copy to Clipboard Utility
    // ============================================
    function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                toast.success(successMessage);
            }).catch(err => {
                toast.error('Failed to copy to clipboard');
            });
        } else {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            
            try {
                document.execCommand('copy');
                toast.success(successMessage);
            } catch (err) {
                toast.error('Failed to copy to clipboard');
            }
            
            document.body.removeChild(textarea);
        }
    }

    window.copyToClipboard = copyToClipboard;

    // ============================================
    // Debounce Utility
    // ============================================
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    window.debounce = debounce;

    // ============================================
    // Format Date Utility
    // ============================================
    function formatDate(date, format = 'MMM DD, YYYY') {
        const d = new Date(date);
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        const day = d.getDate();
        const month = months[d.getMonth()];
        const year = d.getFullYear();
        
        return `${month} ${day}, ${year}`;
    }

    window.formatDate = formatDate;

    // ============================================
    // Initialize Everything on DOM Load
    // ============================================
    document.addEventListener('DOMContentLoaded', function() {
        // Initialize components
        initializeStarRatings();
        initSmoothScroll();
        initAnimateOnScroll();
        enhanceFormValidation();
        convertDjangoMessages();

        // Add click ripple effect to buttons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple');
                
                this.appendChild(ripple);
                
                setTimeout(() => ripple.remove(), 600);
            });
        });

        // Log initialization
        console.log('%c🎬 Cinema Dark Mode Initialized', 
                   'color: #FFD700; font-size: 16px; font-weight: bold;');
    });

    // ============================================
    // Add Ripple Effect CSS Dynamically
    // ============================================
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        .btn {
            position: relative;
            overflow: hidden;
        }
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 215, 0, 0.3);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }
        @keyframes ripple-animation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);

})();
