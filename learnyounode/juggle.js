// learnyounode #9
var http = require("http");
var BufferList = require("bl");

if(process.argv.length < 5) {
  throw new Error("Give me three URLs.");
}

function ResponseCollector() {
  "use strict";

  this.buffer = new BufferList();
  this.done = false;

  this.responseHandler = function(response, this=this) {
    response.setEncoding("utf8");
    response.on("error", console.error);
    response.on("end", function() {
      this.done = true;
    });
    response.pipe(this.buffer);
  };
}

var collectors = [];
for(var idx = 0; idx < 3; idx++) {
  var collector = new ResponseCollector();
  collectors.push(collector);
  http.get(process.argv[idx + 2], collector.responseHandler);
}

var timer = setInterval(function() {
  "use strict";
  var done = 0;
  collectors.forEach(function(element, index, array) {
    if(element.done) {
      done++;
    }
  });
  console.log("done = " + done);
  if(done > 2) {
    collectors.forEach(function(element, index, array) {
      console.log(element.buffer.toString());
    });
    clearInterval(timer);
  }
}, 100);
