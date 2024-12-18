// #!/usr/bin/env node

// -----------------------------------------------------------------------
// navbar-transition.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.navbar-burger');
    const menu = document.querySelector('.navbar-menu');
    let isAnimating = false;
  
    const animateMenu = (show) => {
        if (isAnimating) return;
        isAnimating = true;
  
        const duration = 100; // Animation duration in milliseconds
        const start = performance.now();
        const startOpacity = show ? 0 : 1;
        const endOpacity = show ? 1 : 0;
        const startScale = show ? 0.95 : 1;
        const endScale = show ? 1 : 0.95;
  
        const step = (timestamp) => {
            const elapsed = timestamp - start;
            const progress = Math.min(elapsed / duration, 1);
    
            // Interpolate opacity and transform values
            const currentOpacity = startOpacity + (endOpacity - startOpacity) * progress;
            const currentScale = startScale + (endScale - startScale) * progress;
    
            menu.style.opacity = currentOpacity;
            menu.style.transform = `scale(${currentScale})`;
    
            if (progress < 1) {
            requestAnimationFrame(step);
            } else {
            if (!show) menu.style.display = 'none'; // Hide menu after animation
            isAnimating = false;
            }
        };
  
        if (show) {
            menu.style.display = 'flex'; // Show menu before animation
        }
        requestAnimationFrame(step);
    };
  
    burger.addEventListener('click', () => {
        const isActive = menu.style.display === 'flex';
        animateMenu(!isActive);
    });

    // Function to reset styles for larger screens
    const resetStyles = () => {
        if (window.innerWidth > 1024) {
        menu.style = ''; // Clear all inline styles
        menu.classList.remove('is-active'); // Ensure the active class is removed
        burger.classList.remove('is-active'); // Ensure the active class is removed
        }
    };

    // Listen for screen resize
    window.addEventListener('resize', resetStyles);

    // Initial check
    resetStyles();
});
  