var path = require('path');

var srcDir = 'static_src';
var destDir = 'static';

var App = function(dir, options) {
    this.dir = dir;
    this.options = options || {};
    this.appName = this.options.appName || path.basename(dir);
    this.sourceFiles = path.join('.', this.dir, srcDir);
};
App.prototype = Object.create(null);
App.prototype.scssIncludePaths = function() {
    return [this.sourceFiles];
};
App.prototype.scssSources = function() {
    // Assume that any scss we care about is always within the expected
    // "appname/static_url/appname/scss/" folder.
    // NB: this requires the user to adhere to sass's underscore prefixing
    // to tell the compiler what files are includes.
    return path.join(this.sourceFiles, this.appName, '/scss/**/*.scss')
};

// All the Wagtail apps that contain static files
var apps = [
    new App('wagtail/admin'),
    new App('wagtail/documents'),
    new App('wagtail/embeds'),
    new App('wagtail/images'),
    new App('wagtail/snippets'),
    new App('wagtail/wagtailusers'),
    new App('wagtail/contrib/wagtailstyleguide'),
    new App('wagtail/contrib/settings', {
        'appName': 'wagtailsettings',
    }),
    new App('wagtail/contrib/modeladmin', {
        'appName': 'wagtailmodeladmin',
    }),
];

module.exports = {
    apps: apps,
    srcDir: srcDir,
    destDir: destDir,
    // Determines whether the pipeline is used in production or dev mode.
    isProduction: process.env.NODE_ENV === 'production',
};
