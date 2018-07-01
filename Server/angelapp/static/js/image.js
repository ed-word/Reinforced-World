var form = document.getElementById('upload_video')

function sendData(onReady, url) {
    var XHR = new XMLHttpRequest();
    var FD = new FormData(form);
    XHR.addEventListener("load", function (event) {

    });
    XHR.addEventListener("error", function (event) {
        alert('Oops! Something went wrong.');
    });
    XHR.open("POST", url);
    XHR.send(FD);

    XHR.onreadystatechange = function () {
        if (XHR.readyState === 4) {
            var response = JSON.parse(XHR.responseText)
            console.log('response', response)
            onReady(response)
        }
    }
}

function onCrashReady(response) {
    var replace = $('#image-preview-1')
    var remove = $(form)

    if (replace) {
        if (response.crash) {
            message = 'A crash has occurred'
        } else {
            message = 'A crash may not have occurred'
        }

        var video_tag = $('<image width="100%" height="480" src="' + response.image_url + '"/>')
        $(replace).append(video_tag)
        $('#crash-text').append($('<h3>' + message + '</h3><p> Probability - ' + response.certainty + ' % </p> <br> <br> '))
    }

    remove.hide()
    // sendData(onFireReady, '/check_fire')
}

$(form).on('submit', function (e) {
    e.preventDefault();
    sendData(onCrashReady, '/check_image_crash')
})