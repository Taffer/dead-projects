// learnyounode #2 - baby steps
var total = 0;

var idx = 2;
while(idx < process.argv.length) {
	total += Number(process.argv[idx]);
	idx++;
}

console.log(total);
