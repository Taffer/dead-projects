// learnyounode ex. 6 - modular

filteredLs = require("./modular_module"); /*eslint no-undef:0*/

if(process.argv.length < 4) {
	console.log("Pass me a directory and a file extension.");
	// exit!
} else {
  filteredLs(process.argv[2], process.argv[3], function(err, data) {
    "use strict";
    if(err) {
      console.log(err);
    } else {
      data.forEach(function(filename) {
        console.log(filename);
      });
    }
  });
}
