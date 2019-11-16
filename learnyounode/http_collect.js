// learnyounode #8
var http = require("http");
var bl = require("bl");

if(process.argv.length < 3) {
  console.error("Pass me a URL.");
  throw new Error("Pass me a URL.");
}

http.get(process.argv[2], function(response) {
  "use strict";
  response.pipe(bl(function(err, data) {
    if(err === null) {
      console.log(data.length);
      console.log(data.toString("utf8"));
    } else {
      console.error(err);
    }
  }));
});
