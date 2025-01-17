$(document).ready(function() {
    // Check if graph data is present
    if (typeof hasGraphData !== 'undefined' && hasGraphData) {
        // Hide the form div
        $("#formContainer").addClass("hidden");
    }
});