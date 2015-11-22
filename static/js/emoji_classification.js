window.addEventListener("DOMContentLoaded", function() {
    // Grab elements, create settings, etc.
    var canvas = document.getElementById("canvas"),
        context = canvas.getContext("2d"),
        video = document.getElementById("video"),
        videoObj = { "video": true },
        errBack = function(error) {
            console.log("Video capture error: ", error.code);
        };

    // Put video listeners into place
    if(navigator.getUserMedia) { // Standard
        navigator.getUserMedia(videoObj, function(stream) {
            video.src = stream;
            video.play();
        }, errBack);
    } else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
        navigator.webkitGetUserMedia(videoObj, function(stream){
            video.src = window.URL.createObjectURL(stream);
            video.play();
        }, errBack);
    }
    else if(navigator.mozGetUserMedia) { // Firefox-prefixed
        navigator.mozGetUserMedia(videoObj, function(stream){
            video.src = window.URL.createObjectURL(stream);
            video.play();
        }, errBack);
    }

    document.getElementById("snap").addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
    });

    document.getElementById("gen_image").addEventListener("click", function(){
        var image = convertCanvasToImage(canvas);
        $("#emoji").innerHTML = classify_face(image);
    })

}, false);

// Converts canvas to an image
function convertCanvasToImage(canvas) {
    var image = canvas.toDataURL("image/jpeg");
    console.log(image);
    return image;
}

function classify_face(image) {
    $.ajax({
        type: "POST",
        url: "http://clemence.cloudapp.net/facemoji",
        data: {
            data: image
        }
    })
}
