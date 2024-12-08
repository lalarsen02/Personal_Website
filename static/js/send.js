// #!/usr/bin/env node

// -----------------------------------------------------------------------
// send.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

document.querySelector(".button.is-link").addEventListener("click", async function (e) {
    e.preventDefault();

    var error = false;

    // Add is-loading to the button when clicked
    const button = e.target;
    button.classList.add("is-loading");

    // Targets the top of the second column
    const notificationContainer = document.querySelector(".contact .column:nth-child(2)");
    // Clear all existing notifications
    const existingNotifications = notificationContainer.querySelectorAll(".notification");
    existingNotifications.forEach(notification => {
        notification.remove();
    });

    await new Promise((resolve) => setTimeout(resolve, 1000));

    const name = document.querySelector("input[placeholder='Name']").value;
    const email = document.querySelector("input[placeholder='Email']").value;
    const message = document.querySelector("textarea[placeholder='Message']").value;

    // Highlight empty fields with is-danger class
    const nameInput = document.querySelector("input[placeholder='Name']");
    const emailInput = document.querySelector("input[placeholder='Email']");
    const messageInput = document.querySelector("textarea[placeholder='Message']");

    // Find closest fields to the inputs
    const nameField = nameInput.closest(".field");
    const emailField = emailInput.closest(".field");
    const messageField = messageInput.closest(".field");

    // Ensure no duplicate help messages
    if (nameField.querySelector(".help.is-danger")) {
        nameField.querySelector(".help.is-danger").remove();
    }
    if (emailField.querySelector(".help.is-danger")) {
        emailField.querySelector(".help.is-danger").remove();
    }
    if (messageField.querySelector(".help.is-danger")) {
        messageField.querySelector(".help.is-danger").remove();
    }

    // Helper function to add a notification
    const addNotification = (type, message) => {
        // Create a new notification
        const notification = document.createElement("div");
        notification.className = `notification ${type}`;
        notification.innerHTML = `
        <button class="delete"></button>
        ${message}
        `;

        // Add event listener to close button
        notification.querySelector(".delete").addEventListener("click", () => {
        notification.remove();
        });

        // Insert the notification at the top of the second column
        notificationContainer.prepend(notification);
    };

    // Function to validate an email using regex
    const isValidEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    if (!isValidEmail(email)) {
        const emailHelp = document.createElement("p");
        emailHelp.classList.add("help", "is-danger", "none");
        emailHelp.innerHTML = "This email is invalid.";

        emailInput.classList.add("is-danger");
        emailField.appendChild(emailHelp);

        addNotification("is-danger", "Failed to Send Email. Email is invalid. Email addresses should follow username@domain.com.");
        button.classList.remove("is-loading");
        error = true;
    }

    if (!name || !email || !message) {
        // Create help texts below inputs
        const nameHelp = document.createElement("p");
        nameHelp.classList.add("help", "is-danger");
        nameHelp.innerHTML = "Name is required.";

        const emailHelp = document.createElement("p");
        emailHelp.classList.add("help", "is-danger", "none");
        emailHelp.innerHTML = "Email is required.";

        const messageHelp = document.createElement("p");
        messageHelp.classList.add("help", "is-danger");
        messageHelp.innerHTML = "Message is required.";

        // Add validation
        if (!name) {
            nameInput.classList.add("is-danger");
            nameField.appendChild(nameHelp);

            // Remove the is-danger class and help text once the user starts typing
            nameInput.addEventListener("input", () => {
                if (nameInput.value.trim() !== "") {
                nameInput.classList.remove("is-danger");
                nameHelp.remove();
                }
            });
        }
        if (!email) {
            emailInput.classList.add("is-danger");
            emailField.appendChild(emailHelp);

            // Remove the is-danger class and help text once the user starts typing
            emailInput.addEventListener("input", () => {
                if (emailInput.value.trim() !== "") {
                emailHelp.remove();
                }
            });
        }
        if (!message) {
            messageInput.classList.add("is-danger");
            messageField.appendChild(messageHelp);

            // Remove the is-danger class and help text once the user starts typing
            messageInput.addEventListener("input", () => {
                if (messageInput.value.trim() !== "") {
                messageInput.classList.remove("is-danger");
                messageHelp.remove();
                }
            });
        }

        // Show notification and remove loading button
        addNotification("is-danger", "Failed to Send Email. Please fill out all fields.");
        button.classList.remove("is-loading");
        error = true;
    }

    if (error) {
        return;
    }

    try {
        const response = await fetch("/send_email", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, message }),
        });

        const result = await response.json();
        if (response.ok) {
            addNotification("is-success", result.message);
        } else {
            addNotification("is-danger", result.message);
        }
    } catch (error) {
        addNotification("is-danger", "Failed to send email. Please try again later.");
        console.error(error);
    } finally {
        button.classList.remove("is-loading");
    }
});
