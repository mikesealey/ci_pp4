$(document).ready(function(){
    // Django returns 'Python JSON' which uses single-quotes which isn't compatable with JS-JSON
    // Processing Python JSON into legit-JSON
    const images = JSON.parse($('#image-data').text());

    let index = -1;

    function updateGallery() {
    const leftIndex = (index + images.length) % images.length
    const centreIndex = (index + 1) % images.length
    const rightIndex = (index + 2) % images.length

    $("#left-image").attr("src", images[leftIndex].url)
    $("#centre-image").attr("src", images[centreIndex].url)
    $("#right-image").attr("src", images[rightIndex].url)
    $("#img-counter").text(`${index+1}/${images.length}`)
    }

    $("#left-image").on("click", () => {
    index = (index - 1 + images.length) % images.length;
    updateGallery()
    });

    $("#centre-image").on("click", () => {
    index = (index - 1 + images.length) % images.length;
    updateGallery()
    });

    $("#right-image").on("click", () => {
    index = (index + 1) % images.length
    updateGallery()
    });

    updateGallery()
})


