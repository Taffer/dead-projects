// learnyounode ex. 5 - filtered ls
var fs = require("fs");

// Help me Stack Overflow, you're my only hope.
//
// http://stackoverflow.com/questions/280634/endswith-in-javascript
//
// Note that this is a bad practice:
//
// http://jslinterrors.com/extending-prototype-of-native-object
//
// Note also that I'm doing it anyway, as it ought to be part of the
// standard String object.
/*eslint no-extend-native:0*/
String.prototype.endsWith = function(suffix) {
  "use strict";
  return this.indexOf(suffix, this.length - suffix.length) !== -1;
};

if(process.argv.length < 4) {
	console.log("Pass me a directory and a file extension.");
	// exit!
} else {
	var ext = "." + process.argv[3];
	fs.readdir(process.argv[2], function(err, list) {
    "use strict";
		if(!err) {
			for(var i = 0; i < list.length; i++) {
				if(list[i].endsWith(ext)) {
					console.log(list[i]);
				}
			}
		}
	});
}
