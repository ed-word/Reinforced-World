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

    XHR.onreadystatechange = function(){
        if(XHR.readyState === 4){
            var response = JSON.parse(XHR.responseText)
            console.log('response', response)
            onReady(response)
        }
    }
}

function onCrashReady(response){
    var replace = $('#video-preview-1')
    var remove = $(form)

    if (replace) {
        if (response.crash) {
            message = 'A crash has occurred'
        } else {
            message = 'A crash may not have occurred'
        }

        var video_tag = $('<video width="100%" height="480" controls> <source src="' + response.video_url + '"></source> </video>')
        $(replace).append(video_tag)
        $('#crash-text').append($('<h3>' + message + '</h3><p> Probability - ' + response.certainty + ' % </p> <br> <br> '))
    }

    remove.hide()
    sendData(onFireReady, '/check_fire')
}

function onFireReady(response){
    if(response.fire){
        var video_tag = $('<video width="100%" height="480" controls> <source src="' + response.video_url + '"></source> </video>')
        $('#video-preview-2').append(video_tag)
        $('#crash-text-2').append($('<h3>A fire has broken out</h3> <br> <br> '))
        $("html, body").animate({
            scrollTop: document.body.scrollHeight
        }, "slow");
    }
}

$(form).on('submit', function(e){
    e.preventDefault();
    sendData(onCrashReady, '/check_crash')
})