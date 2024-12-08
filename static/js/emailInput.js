// #!/usr/bin/env node

// -----------------------------------------------------------------------
// emailInput.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

document.addEventListener("DOMContentLoaded", () => {
    // Select the email input element and its parent field
    const emailInput = document.querySelector("input[placeholder='Email']");
    const emailControl = emailInput.closest(".control");
    const emailField = emailInput.closest(".field");

    // Function to validate an email using regex
    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    // Add event listener for input event
    emailInput.addEventListener("input", () => {
        // Remove any existing status spans
        const existingIcon = emailControl.querySelector(".icon");
        if (existingIcon) existingIcon.remove();
        const existingHelp = emailField.querySelector(".help");
        if (existingHelp) existingHelp.remove();

        // Remove any existing classes
        emailInput.classList.remove("is-danger", "is-success");

        // Validate the email and add appropriate class and icon
        const iconSpan = document.createElement("span");
        iconSpan.classList.add("icon", "is-small", "is-right");
        const helpP = document.createElement("p");
        helpP.classList.add("help");

        if (isValidEmail(emailInput.value)) {
            emailInput.classList.add("is-success");
            iconSpan.innerHTML = '<i class="fas fa-check"></i>';
            helpP.classList.add("is-success")
            helpP.innerHTML = 'This email is valid.';
        } else {
            emailInput.classList.add("is-danger");
            iconSpan.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
            helpP.classList.add("is-danger")
            helpP.innerHTML = 'This email is invalid.';
        }

        // Append the icon span below the email input
        emailControl.appendChild(iconSpan);

        // Append the help paragraph to the email field
        emailField.appendChild(helpP);

    });
});