$(document).foundation();

// If you change this, you need change also static result rendering in index.html
// TODO: move these two variables to index.html and include them by django

var success_template = '\
    <div class="columns small-12"> \
        <a class="close-button" onclick="$(this).parent().remove();" title="Close">&times;</a> \
        <a class="success-file" href="%link%">%short_name%</a> \
        <input class="success-url" type="url" onclick="this.select();" value="%link%" /> \
    </div>';
var error_template = '\
    <div class="columns small-12"> \
        <a class="close-button" onclick="$(this).parent().remove();" title="Close">&times;</a> \
        <span class="error-file">%short_name%</span> \
        <div class="error-text">%error%</div> \
    </div>';

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
function write_result(status, json){
    $('.progress').fadeTo(500, 0);
    if (status == 'success') {
        tpl = success_template;
        tpl = tpl.replace(regexp('%short_name%'), json['short_name']);
        tpl = tpl.replace(regexp('%link%'), json['link']);
        var nw = $(tpl);
        $('#select-button').addClass('success')
                           .text('Done!');
    } else if (status == 'error') {
        tpl = error_template;
        if (!json['short_name']) { json['short_name'] = 'Upload error'; }
        if (!json['error']) { json['error'] = 'Unknown error'; }
        tpl = tpl.replace(regexp('%short_name%'), json['short_name']);
        tpl = tpl.replace(regexp('%error%'), json['error']);
        var nw = $(tpl);
        $('#select-button').addClass('alert')
                           .text('Error!');
    }

    $('#results').append(nw);
    setTimeout(function(){
        $('#select-button').removeClass('success')
                           .removeClass('alert')
                           .text('Select file');
    }, 2000);
}

function completeUpload(xhr, status) {
    json = JSON.parse(xhr.responseText);
    write_result(status, json);
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
            json = {error: 'File is too big', short_name: 'Upload error'};
            write_result('error', json);
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
