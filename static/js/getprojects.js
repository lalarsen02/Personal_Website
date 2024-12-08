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
