$(document).ready(function () {
    // Fetches privacy policy and swaps markdown into html

    $.get('/static/docs/privacy_policy.md', function(data) {
        const html = marked.parse(data);
        $('#policy-container').html(html);
        // if value is returned from privacy policy, hide the "oops" placeholder, add the PrivPol, and add the download button
        if (data) {
            $("#policy-placeholder").text("")

            $('#policy-placeholder').append('<a href="/static/docs/privacy_policy.md" download="privacy_policy.md"></a>')
            $('#policy-placeholder a').last().append('<button id="download-policy" class="btn btn-primary">Download Privacy Policy</button>')

        }
    });

    

});