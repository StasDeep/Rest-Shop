var gulp = require('gulp');

var build = {
    path: 'build/'
};

var src = {
    path: 'app/**/*'
};

gulp.task('build', function () {
    return gulp.src(src.path)
               .pipe(gulp.dest(build.path))
});

gulp.task('default', ['build']);
