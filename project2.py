# python libraries
import argparse
import json
import os

#external libraries

def add_arguments():
    """Function to add and parse arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingredient", type=str, required=True,action='append', 
                            help="Ingredients to predict type of cuisine and similar meals for.")
    parser.add_argument("--N", type=int, required=True,
                            help="Top-N closest foods.")
        
    # get and return args
    args = parser.parse_args()
    return args

def load_dataset():
    """Function to open and convert json dataset."""
    json_file = open('yummly.json','r')
    json_parsed = json.load(json_file)
    return json_parsed

def process_dataset():
    """Function to BLAH."""
    # load yummly dataset
    yummy_json = load_dataset()

    cuisines = {}
    print(yummy_json[0])
    for recipe in yummy_json:
        cuisines


"""Uses search to predict cuisine and find N-closest foods"""
# gets arguments passed in via argparse
args = add_arguments()
print(args)

# creates database for searching
process_dataset()