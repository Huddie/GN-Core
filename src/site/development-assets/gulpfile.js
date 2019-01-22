var gulp = require('gulp');

var autoprefixer = require('autoprefixer');
var browserSync = require('browser-sync').create();
var postcss = require('gulp-postcss');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');

gulp.task('serve', function() {
    browserSync.init({
        server: true,
        online:true,
        tunnel: true,
        index: "index_success.html"
    });

    gulp.watch('./development-assets/scss/*.scss', ['css']);
    gulp.watch('./index.html').on('change', browserSync.reload);
    gulp.watch('./site-assets/js/*.js').on('change', browserSync.reload);
});

gulp.task('css', function () {
    var plugins = [
        autoprefixer({
            browsers: ['last 2 versions']
        })
    ];

    return gulp
        .src('./development-assets/scss/*.scss')
        .pipe(sourcemaps.init())
            .pipe(sass.sync().on('error', sass.logError))
            .pipe(postcss(plugins))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('site-assets/css/'))
        .pipe(browserSync.stream());
});

gulp.task('default', ['serve']);
