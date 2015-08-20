var path = require('path');
var del = require('del');

var gulp = require('gulp');
var rename = require('gulp-rename');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');

// ***** Config ***** //

var paths = {
    scss: ['*/static-src/scss/*.scss', '!*/static-src/scss/_*.scss'],
    scss_watch: ['*/static-src/scss/*.scss'],
    js: ['*/static-src/js/*.js']
};

var copy = {
    js: {
        'slasyz_ru/static/js/jquery.min.js': 'bower_components/jquery/dist/jquery.min.js',
        'slasyz_ru/static/js/foundation.min.js': 'bower_components/foundation/js/foundation.min.js',
        'slasyz_ru/static/js/modernizr.min.js': 'bower_components/foundation/js/vendor/modernizr.js',
        'slasyz_ru/static/js/foundation.topbar.min.js': 'bower_components/foundation/js/foundation/foundation.topbar.js'
    },
    other: {}
};

var destDirs = {
    scss: 'css'
};

// ***** Make correct destination path. ***** //

function renameFile(filepath) {
    var arr = filepath.dirname.split(path.sep);
    arr[1] = 'static';// .../static-src/... -> .../static/...
    arr[2] = destDirs[arr[2]] || arr[2]; // .../scss/... -> .../css/...
    filepath.extname = '.min' + filepath.extname; // .../blog.js -> .../blog.min.js
    filepath.dirname = arr.join(path.sep);
}

// ***** Copy some stuff, uglify it and so on ***** //

gulp.task('scss', function() {
    gulp.src(paths.scss)
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(rename(renameFile))
        .pipe(gulp.dest('./'));
});

gulp.task('js', function() {
    gulp.src(paths.js)
        .pipe(uglify())
        .pipe(rename(renameFile))
        .pipe(gulp.dest('./'));
});

gulp.task('copylibs', function() {
    for (var key in copy.js) {
        gulp.src(copy.js[key])
            .pipe(uglify())
            .pipe(rename(key))
            .pipe(gulp.dest('./'))
    }
    for (var key in copy.other) {
        gulp.src(copy[key])
            .pipe(rename(key))
            .pipe(gulp.dest('./'))
    }
});

// ***** General tasks ***** //

gulp.task('clean', function(cb) {
    del(['*/static/js/*.js', '*/static/css/*.css'], cb);
});

gulp.task('watch', function () {
    gulp.watch(paths.scss_watch, ['scss']);
    gulp.watch(paths.js, ['js']);
});

gulp.task('build', ['scss', 'js', 'copylibs']);
gulp.task('default', ['watch', 'build']);
