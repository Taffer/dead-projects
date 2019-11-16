// learnyounode ex. 4 - first async I/O
var fs = require("fs");

function readFile(err, data) {
	"use strict";
	if(err) {
		console.log("Curse you filesystem.");
		// How do you exit with an error?
	} else {
		var lines = data.split("\n");
		var count = lines.length;
		if(data[data.length - 1] !== "\n") {
			count--;
		}

		console.log(count);
	}
}

if(process.argv.length < 3) {
	console.log("Feed me a filename.");
	// How do you exit with an error?
} else {
	fs.readFile(process.argv[2], "utf8", readFile);
}
