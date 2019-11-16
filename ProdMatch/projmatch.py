#!/usr/bin/env python

'''
Match products to related listings.

If you're running pep8.py over this, ignore E501; 80 characters is just too
small for code on a modern screen.

Created on 2013-08-14

@author: chrish
'''

import json

# Fuzzy Wuzzy is a fuzzy string matching library for Python; you can
# find it here:
#
# https://github.com/seatgeek/fuzzywuzzy
from fuzzywuzzy import fuzz

# Product data and listing data; in a real app you could make these the
# defaults and allow passing overrides via the command-line, or whatever
# is appropriate.
PRODUCT_DATA = 'data/products.txt'
LISTING_DATA = 'data/listings.txt'
OUTPUT_DATA = 'results.txt'
NEGATIVE_DATA = 'negatives.txt'

# Data Formats
#
# Product:
#
# {
#   "product_name": String   // A unique id for the product
#   "manufacturer": String
#   "family": String         // optional grouping of products
#   "model": String
#   "announced-date": String // ISO-8601 formatted date string
# }
#
#Listing:
#
# {
#   "title": String         // description of product for sale
#   "manufacturer":  String // who manufactures the product for sale
#   "currency": String      // currency code, e.g. USD, CAD, GBP, etc.
#   "price": String         // price, e.g. 19.99, 100.00
# }
#
#Result:
#
# {
#   "product_name": String
#   "listings": Array[Listing]
# }


class Product(object):
    # Keep track of the manufacturers so we can reduce the search domain.
    Manufacturers = {}  # manufacturer: [list of Products]

    def __init__(self, json_data):
        ''' Create a Product from a dictionary provided by JSON.

        :param json_data: A dictionary as described in Data Formats, above.
        '''
        self.json_data = json_data  # Original data in original format.

        # Conveniences for matching.
        self.manufacturer = json_data['manufacturer'].lower()
        self.family = json_data['family'] if 'family' in json_data else None
        self.model = json_data['model'] if 'model' in json_data else None

        self.product_name = json_data['product_name']  # Original product name.
        self.name = ' '.join(self.product_name.split('_'))  # Plain text product name.

        if self.manufacturer in Product.Manufacturers:
            Product.Manufacturers[self.manufacturer].append(self)
        else:
            Product.Manufacturers[self.manufacturer] = [self]

    @staticmethod
    def load_json(json_file):
        ''' Load a JSON data file containing Product records.

        Returns a list of Product objects.

        :param json_file: File-like object containing the JSON data.
        '''
        # Note that this isn't robust and expects your data to be 100% clean.
        products = [Product(json.loads(x)) for x in json_file.readlines()]
        return products

    @staticmethod
    def in_manufacturers(listing):
        ''' Is this listing in the Manufacturers?

        Slightly fuzzy matchery to allow "Foo Canada" to work when we already
        know about "Foo" in our data. Hopefully this would also work with
        subsidiaries (like "Bar" and "Bar Media"). This might also trigger
        false positives ("Foo Pictures" and "Bar Pictures") in this method,
        but not in the match() method, which isn't as forgiving.

        Returns the matched hunk (or None if there's no match); use it as a
        key into the Manufacturers dictionary.
        '''
        for hunk in listing.manufacturer.split():
            if hunk in Product.Manufacturers:
                return hunk

        return None

    def match(self, listing):
        ''' Decide if this listing matches this product. In this version,
        we only match one Product at most ("A single price listing may match
        at most one product."), even though some listings are for items that
        are suitable for several products.

        Returns True or False.

        :param listing: A Listing object.
        '''
        # token_set_ratio() checks for all the 'words' in the first argument
        # existing in the second argument. Case-insensitive even. Exactly how
        # I was going to code it up until I found the fuzzywuzzy library,
        # which has the advantage of being previously debugged.
        score = fuzz.token_set_ratio(self.name, listing.title)
        if score == 100:
            # Exact fuzzy match on my product name inside the listing.
            return True

        manu_score = fuzz.token_set_ratio(self.manufacturer, listing.title)
        family_score = fuzz.token_set_ratio(self.family, listing.title) if self.family else 0
        model_score = fuzz.token_set_ratio(self.model, listing.title) if self.model else 0
        if ' ' in self.model and model_score < 100:
            # Canon SX130 IS vs. SX130IS...
            model_nospaces = ''.join(' '.split(self.model))
            if fuzz.token_set_ratio(model_nospaces, listing.title) == 100:
                model_score = 100

        if manu_score == 100 and family_score == 100 and model_score == 100:
            # Seems legit.
            return True

        # Generating false positives (for example 'Canon_IXUS_300_HS' is
        # matching "Canon PowerShot ELPH 300 HS (Black)". Turning this
        # off does make us miss "Canon NB-7L Lithium-Ion Battery for G10, G11,
        # G12 Cameras" unfortunately.
        #
        #if manu_score == 100 and model_score == 100:
        #    # People sometimes call things by manufacturer and model number.
        #    # Might be ambiguous though...
        #    return True

        if family_score == 100 and model_score == 100:
            # I'm typing on an IdeaPad Y500, for example.
            return True

        return False


class Listing(object):
    def __init__(self, json_data):
        ''' Create a Listing from a dictionary provided by JSON.

        :param json_data: A dictionary as described in Data Formats, above.
        '''
        self.json_data = json_data  # Original data in original format.

        # Conveniences for matching.
        self.manufacturer = json_data['manufacturer'].lower()
        self.title = json_data['title']

    @staticmethod
    def load_json(json_file):
        ''' Load a JSON data file containing Listing records.

        Returns a list of Listing objects.

        :param json_file: File-like object containing the JSON data.

        This is the same code as in Product; you'd want to factor it out if
        you were going to repeat it any more than this. Two options for
        doing that would be to create a superclass (say, JsonObject) or
        make an object factory function that takes the class and the
        json_file as arguments.
        '''
        # Note that this isn't robust and expects your data to be 100% clean.
        listings = [Listing(json.loads(x)) for x in json_file.readlines()]
        return listings


def write_results(output_file, results):
    ''' Write the results as JSON data.

    :param output_file: File-like object to store the data.
    :param results: Dictionary of results.
    '''
    # Sort by product name. Might be handy to sort by price instead, or you
    # could do that in a front-end presenting the data instead of here.
    keys = results.keys()
    keys.sort()
    for product_name in keys:
        if len(results[product_name]) == 0:
            # Skip empty results in the output. You might not want to do this.
            continue

        # Doing it this way makes the output file match the one-line-per-
        # object style of the two input files. You could just do a
        # json.dump(results, output_file) if you didn't need to do that.
        json.dump({product_name: [x.json_data for x in results[product_name]]}, output_file)
        output_file.write('\n')


def search_products(listing, products):
    ''' Search for a matching product for this listing.

    :param listing: The listing we want to match.
    :param products: A list of Products to search.
    '''
    for product in products:
        if product.match(listing):
            return product

    return None


def main():
    ''' Chug through the data.

    You could make this more generally useful by adding command-line argument
    processing to indicate input files, output file, level of verbosity, etc.
    '''
    print 'Warning, this takes about 40 minutes to run (Python 2.7.3 on a Core i7).'

    # Load and Pythonize the data.
    with open(PRODUCT_DATA) as product_file:
        products = Product.load_json(product_file)
        print 'Loaded %s products.' % (len(products))
    with open(LISTING_DATA) as listing_file:
        listings = Listing.load_json(listing_file)
        print 'loaded %s listings.' % (len(listings))

    print 'Found %s standard manufacturers.' % (len(Product.Manufacturers))

    results = {x.product_name: [] for x in products}  # dictionary of product_name: [listings]
    negatives = []  # Listings that didn't match a product.

    # For each listing, try to find a suitable product.  If this wasn't
    # Python, you could thread this bit for a nice performance gain
    # (probably linear for a typical 4+ core CPU unless your implementation
    # has excessive contention while reading the products data).
    manu_hits = 0
    for listing in listings:
        hunk = Product.in_manufacturers(listing)
        if hunk:
            # We can search a smaller subset of products! Without this we're
            # looking at ~15 million product vs. listing comparisons, worst
            # case.
            manu_hits += 1
            match = search_products(listing, Product.Manufacturers[hunk])
        else:
            # Bummer, we need to search for a matching product.
            match = search_products(listing, products)

        if match is not None:
            # We found a product that we're confident matches this listing.
            results[match.product_name].append(listing)
        else:
            # This didn't match.
            negatives.append(listing)

    print 'Failed to match %s listings (%s%%).' % (len(negatives), int(float(len(negatives)) / float(len(listings)) * 100.0))
    print 'Searched for %s (%s%%) in manufacturers list.' % (manu_hits, int(float(manu_hits) / float(len(listings)) * 100.0))

    # Save our results.
    with open(OUTPUT_DATA, 'w') as output_file:
        write_results(output_file, results)

    # Save the negative matches for seeing how well the program is doing.
    with open(NEGATIVE_DATA, 'w') as negs:
        json.dump([x.json_data for x in negatives], negs)


if __name__ == '__main__':
    main()
