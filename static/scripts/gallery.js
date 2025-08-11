$(document).ready(function(){
    // Django returns 'Python JSON' which uses single-quotes which isn't compatable with JS-JSON
    // Processing Python JSON into legit-JSON
    const imageArray = $("#image-data").text()
    const processedImageArray = imageArray.replaceAll("'", '"')
    const images = JSON.parse(processedImageArray);

    let index = 0;

    function updateGallery() {
    const leftIndex = ((index - 1) + images.length) % images.length
    const centreIndex = (index) % images.length
    const rightIndex = (index + 1) % images.length

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


