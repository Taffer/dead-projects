// learnyounode #7
var http = require("http");

if(process.argv.length < 3) {
	console.log("Pass me a URL.");
	// exit!
} else {
  http.get(process.argv[2], function(response) {
    "use strict";
    response.setEncoding("utf8");

    response.on("data", function(data) {
      console.log(data);
    });
    response.on("error", function(error) {
      console.log("Error: " + error);
      return;
    });
    response.on("end", function() {
      return;
    });
  });
}
