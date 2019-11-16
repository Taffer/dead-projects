ProdMatch
=========

Fuzzy matching product names against listings.

This uses the FuzzyWuzzy (https://github.com/seatgeek/fuzzywuzzy) library to try doing some fuzzy matching of product listings against a set of known products.

It's pretty slow in Python (takes about 40 minutes to run on my laptop, unfortunately). Reimplementing in something else that works better with threading would be a big win, I think.

- chrish, August 18, 2013
