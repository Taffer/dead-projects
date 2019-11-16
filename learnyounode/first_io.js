// learnyounode ex. 3 - first I/O
var fs = require("fs");

if(process.argv.length < 3) {
	console.log("Feed me a filename.");

	// How do you exit with an error?
} else {
	var buff = fs.readFileSync(process.argv[2]);
	var buffStr = buff.toString();
	var lines = buffStr.split("\n");
	var count = lines.length;
	if(buffStr[buffStr.length - 1] !== "\n") {
		count--;
	}

	console.log(count);
}
