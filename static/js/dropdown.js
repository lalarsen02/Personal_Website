// #!/usr/bin/env node

// -----------------------------------------------------------------------
// dropdown.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', (event) => {
        // Check if the clicked element is a dropdown or inside a dropdown
        const dropdown = event.target.closest('.dropdown');
        if (dropdown) {
            dropdown.classList.toggle('is-active');
        }
    });

    // Attach event listeners to dropdown items using event delegation
    document.addEventListener('mouseover', (event) => {
        const dropdownItem = event.target.closest('.dropdown-item');
        if (dropdownItem) {
            dropdownItem.classList.add('is-active');
        }
    });

    document.addEventListener('mouseout', (event) => {
        const dropdownItem = event.target.closest('.dropdown-item');
        if (dropdownItem) {
            dropdownItem.classList.remove('is-active');
        }
    });

    document.addEventListener('click', (event) => {
        // Check if the clicked element is a dropdown item
        const dropdownItem = event.target.closest('.dropdown-item');
        if (dropdownItem) {
            // Find all dropdown items in the same dropdown menu and remove the check icon
            const dropdownMenu = dropdownItem.closest('.dropdown-menu');
            dropdownMenu.querySelectorAll('.dropdown-item .icon.is-small').forEach(icon => {
                icon.innerHTML = ''; // Clear the icon
            });

            // Add the check icon to the selected dropdown item
            const iconSpan = dropdownItem.querySelector('.icon.is-small');
            if (iconSpan) {
                iconSpan.innerHTML = '<i class="fas fa-check" aria-hidden="true"></i>';
            }
        }
    });
});
