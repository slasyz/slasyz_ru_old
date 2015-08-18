$(document).foundation();

function regexp(r){
    return new RegExp(r.replace('%', '\\%'), 'g');
}
function prevent(ev){
    ev.stopPropagation();
    ev.preventDefault();

    // this workaround for firefox taken from
    // http://stackoverflow.com/questions/14194324/firefox-firing-dragleave-when-dragging-over-text
    try {
        if (ev.relatedTarget.nodeType == 3) return true;
    } catch(err) {}
    if (ev.target === ev.relatedTarget) return true;
    return false;
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function write_result(status, html_res){
    $('.progress').fadeTo(500, 0);
    if (status == 'success') {
        $('#select-button').removeClass('primary')
                           .addClass('success')
                           .text('Done!');
    } else if (status == 'error') {
        $('#select-button').removeClass('primary')
                           .addClass('alert')
                           .text('Error!');
    }

    var nw = $(html_res);
    $('#results').append(nw);
    setTimeout(function(){
        $('#select-button').removeClass('success')
                           .removeClass('alert')
                           .addClass('primary')
                           .text('Select file');
    }, 2000);
}

function completeUpload(xhr, status) {
    write_result(status, xhr.responseText);
}
function uploadProgress(ev){
    var percent = parseInt(ev.loaded / ev.total * 100);
    $('.meter').width(percent+'%');
}
function upload(files){
    for (i=0; i<files.length; i++) {
        $('.meter').width(0);
        $('.progress').fadeTo(500, 1);
        var file = files[i];
        var csrftoken = getCookie('csrftoken');

        if (file.size > $('#max_file_size').val()) {
            write_result('error', toobig_html);
        } else {
            var formdata = new FormData();
            formdata.append('fileup', file);
            formdata.append('password', $('#password').val());

            $.ajax('upload-ajax/', {
                xhr: function(){
                    var xhr = $.ajaxSettings.xhr();
                    xhr.upload.addEventListener('progress', uploadProgress, false);
                    return xhr;
                },
                complete: completeUpload,
                data: formdata,
                processData: false,
                contentType: false,
                headers: {'X-FILE-NAME': unescape(encodeURIComponent(file.name)), 'X-CSRFToken': csrftoken},
                type: 'POST',
            });
        }
    }
}

$('#submit-button').hide(0);
$('#select-button').on('dragenter', function(ev){
    if (prevent(ev)) {return};
    console.log('#select-button - dragenter');
    $('#select-button').removeClass('primary')
                       .addClass('secondary')
                       .text('Drop it here!');
});
$('#select-button').on('dragleave', function(ev){
    if (prevent(ev)) {return};
    console.log('#select-button - dragleave');
    $('#select-button').addClass('primary')
                       .removeClass('secondary')
                       .text('Select file');
});

$('#select-button').on('dragover', prevent);
$('#select-button').on('drop', function(ev){
    prevent(ev);
    upload(ev.originalEvent.dataTransfer.files);
    $('#select-button').addClass('primary')
                       .removeClass('secondary')
                       .text('Select file');
});
$('#fileup').change(function(ev){
    upload(ev.target.files);
    $(this).wrap('<form>').closest('form').get(0).reset();
    $(this).unwrap();
});
$('form').submit(prevent);