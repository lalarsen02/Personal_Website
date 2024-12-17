// #!/usr/bin/env node

// -----------------------------------------------------------------------
// music.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tabs ul li');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('is-active'));

            tab.classList.add('is-active');
        });
    });
});
  