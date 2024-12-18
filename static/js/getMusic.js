// #!/usr/bin/env node

// -----------------------------------------------------------------------
// getprojects.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

function handleResponse(response) {
    $("#resultsDiv").html(response);

    // apply fade in and transition animations
    const newElements = $("#resultsDiv").find("p, figure");
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

function getResults(music='rock') {
    if (request != null) request.abort();

    let url = `/getmusic?music=${music}`;

    request = $.ajax({
        type: "GET",
        url: url,
        success: handleResponse,
    });
}

function setup() {
    getResults();

    $("#rock").on("click", function () {
        getResults('rock');
    });

    $("#theater").on("click", function () {
        getResults('theater');
    });

    $("#orchestra").on("click", function () {
        getResults('orchestra');
    });

    $("#songs").on("click", function () {
        getResults('songs');
    });
}

$("document").ready(setup);