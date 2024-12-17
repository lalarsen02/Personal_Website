// #!/usr/bin/env node

// -----------------------------------------------------------------------
// getprojects.js
// Author: Louis Larsen
// -----------------------------------------------------------------------

"use strict";

function handleResponse(response) {
    $("#resultsDiv").html(response);
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