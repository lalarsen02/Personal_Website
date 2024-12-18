// #!/usr/bin/env node

// -----------------------------------------------------------------------
// transitions.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const elements = document.querySelectorAll("h1, h2, h3, h4, p, figure, li");
  
    elements.forEach((el) => {
        el.classList.add("fade-in-up");
    });
  
    const revealElements = () => {
        elements.forEach((el) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.classList.add("visible");
            }
        });
    };
  
    window.addEventListener("scroll", revealElements);
    revealElements();
});