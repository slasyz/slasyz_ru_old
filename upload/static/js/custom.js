$(document).foundation();
var in_span = false;

// If you change this, you need change also static result rendering in upload.html
var success_template = '\
    <div class="columns small-12"> \
        <input type="url" onclick="this.select();" value="%text%" /> \
    </div>';
var error_template = '\
    <div class="columns small-12"> \
        <div data-alert class="alert-box failure"> \
            %text% \
            <a href="#" class="close">&times;</a> \
        </div> \
    </div> \
';

function prevent(ev){
    ev.stopPropagation();
    ev.preventDefault();
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
function write_result(status, text){
    regexp = new RegExp('\%text\%', 'g');
    $('.progress').fadeTo(500, 0);

    if (status == 'success') {
        var nw = $( success_template.replace(regexp, text) );
        $('#select-button').addClass('success');
        $('#select-button span').text('Done!');
    } else if (status == 'error') {
        var nw = $( success_template.replace(regexp, text) ); // error_template, actually
        $('#select-button').addClass('alert');
        $('#select-button span').text('Error!');
    }

    $('#results').append(nw);
    setTimeout(function(){
        $('#select-button').removeClass('success');
        $('#select-button').removeClass('alert');
        $('#select-button span').text('Select file');
    }, 2000);
}

function completeUpload(xhr, status) {
    json = JSON.parse(xhr.responseText);
    text = ''

    if (status == 'success') {
        text = json['link']
    } else if (status == 'error') {
        if (json['error']) {
            text = json['error']
        } else {
            text = 'Unknown error, sorry!';
        }
    }

    write_result(status, text)
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
            write_result('error', 'File is too big');
        } else {
            var formdata = new FormData();
            formdata.append('fileup', file);
            formdata.append('password', $('#password').val());

            $.ajax('upload-ajax/', {
                async: true,
                xhr: function(){
                    var xhr = $.ajaxSettings.xhr();
                    xhr.upload.addEventListener('progress', uploadProgress, false);
                    return xhr;
                },
                complete: completeUpload,
                data: formdata,
                processData: false,
                contentType: false,
                headers: {'X-FILE-NAME': file.name, 'X-CSRFToken': csrftoken},
                type: 'POST',
            });
        }
    }
}

$('#submit-button').hide(0);

$('#select-button span').on('dragenter', function(ev){ prevent(ev); in_span = true; })
$('#select-button span').on('dragleave', function(ev){ prevent(ev); in_span = false; })

$('#select-button').on('dragenter', function(ev){
    prevent(ev);
    $('#select-button').addClass('secondary');
    $('#select-button span').text('Drop it here!');
});
$('#select-button').on('dragleave', function(ev){
    prevent(ev);
    if (!in_span) {
        $(this).removeClass('secondary');
        $(this).children('span').text('Select file');
    }
});

$('#select-button').on('dragover', prevent);
$('#select-button, #select-button span').on('drop', function(ev){
    prevent(ev);
    upload(ev.originalEvent.dataTransfer.files);
    $('#select-button').removeClass('secondary');
    $('#select-button span').text('Select file');
});
$('#select-button input').change(function(ev){
    upload(ev.target.files);

    $(this).wrap('<form>').closest('form').get(0).reset();
    $(this).unwrap();
});
$('form').submit(prevent);