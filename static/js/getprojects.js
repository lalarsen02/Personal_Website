// #!/usr/bin/env node

// -----------------------------------------------------------------------
// getprojects.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

function handleResponse(response) {
    // Insert the new HTML
    $("#resultsDiv").html(response);

    // Apply fade-in setup to newly inserted elements
    const newElements = $("#resultsDiv").find("h3, img");
    newElements.addClass("fade-in-up");

    // Scroll-based visibility logic
    const revealElements = () => {
        const elements = document.querySelectorAll("#resultsDiv .fade-in-up");
        elements.forEach((el) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight) {
                el.classList.add("visible");
            }
        });
    };

    // Add scroll listener and trigger the check immediately
    window.addEventListener("scroll", revealElements);
    revealElements();
}

let request = null;

function getResults(sort = 'recent') {
    if (request != null) request.abort();

    let url = `/getprojects?sort=${sort}`;

    request = $.ajax({
        type: "GET",
        url: url,
        success: handleResponse,
    });
}

function setup() {
    getResults();

    $("#recent").on("click", function () {
        getResults('recent');
    });

    $("#alpha").on("click", function () {
        getResults('alpha');
    });
}

$("document").ready(setup);
