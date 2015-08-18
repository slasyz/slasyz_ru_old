var path = require('path');
var del = require('del');

var gulp = require('gulp');
var rename = require('gulp-rename');
var sass = require('gulp-sass');
var uglify = require('gulp-uglify');

var paths = {
    scss: ['*/static-src/scss/*.scss', '!*/static-src/scss/_*.scss'],
    js: ['*/static-src/js/*.js']
};

var copy = {
    'slasyz_ru/static/js/jquery.min.js': 'bower_components/jquery/dist/jquery.min.js',
    'slasyz_ru/static/js/foundation.min.js': 'bower_components/foundation/js/foundation.min.js',
    'slasyz_ru/static/js/modernizr.min.js': 'bower_components/foundation/js/vendor/modernizr.js'
};

var destDirs = {
    scss: 'css'
};

function renameFile(filepath) {
    var arr = filepath.dirname.split(path.sep);
    arr[1] = 'static';
    arr[2] = destDirs[arr[2]] || arr[2];
    filepath.extname = '.min' + filepath.extname;
    filepath.dirname = arr.join(path.sep);
}

gulp.task('clean', function(cb) {
    del(['*/static/js/*.js', '*/static/css/*.css'], cb);
});

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

gulp.task('copy', function() {
    for (var key in copy) {
        gulp.src(copy[key])
            .pipe(rename(key))
            .pipe(gulp.dest('./'))
    }
});

gulp.task('watch', function () {
    gulp.watch(paths.scss, ['scss']);
    gulp.watch(paths.js, ['js']);
});

gulp.task('build', ['scss', 'js', 'copy']);
gulp.task('default', ['watch', 'build']);
