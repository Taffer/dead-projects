// LearnYouNode exercise 6
//
// Module with a filtered_ls function inside.

var fs = require("fs");
var path = require("path");

/* List files in pathname that end with .extension.
 * Callback(err, data) is sent a list of matching files.
 *
 * TODO: Figure out or look up standard Node documentation conventions.
 */
function filteredLs(pathname, extension, callback) {
  "use strict";

	fs.readdir(pathname, function(err, list) {
    var files = [];

    if(err) {
      return callback(err);
    }

    var ext = "." + extension;
    list.forEach(function(file) {
      if(path.extname(file) === ext) {
        files.push(file);
      }
    });

    callback(null, files);
  });
}

module.exports = filteredLs;
