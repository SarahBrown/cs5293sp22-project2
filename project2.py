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
    num_recipes = len(yummy_json)

    cuisines = {}
    for recipe in yummy_json:
        rec_cuisine = recipe["cuisine"]
        rec_ingredients = recipe["ingredients"]

        # adds cuisine to cuisine dict if it was not in dict already
        if rec_cuisine not in cuisines.keys():
            cuisines[rec_cuisine] = {}
        
        # loops through recipe's ingredients
        for ingred in rec_ingredients:
            # adds ingredient to individual cuisine dict if it was not in dict already
            if ingred not in cuisines[rec_cuisine].keys():
                cuisines[rec_cuisine][ingred] = 1 # sets specific ingredient to 1 
            else:
                cuisines[rec_cuisine][ingred] = cuisines[rec_cuisine][ingred] + 1 # incrememnts ingredient ammount

    for cuisine_key in cuisines.keys():
        for ingred in cuisines[cuisine_key].keys():
            cuisines[cuisine_key][ingred] = cuisines[cuisine_key][ingred]/num_recipes

    return cuisines

def fuzzy_ingred_match():
    pass


"""Uses search to predict cuisine and find N-closest foods"""
# gets arguments passed in via argparse
args = add_arguments()
input_ingred = args.ingredient
input_N = args.N

# creates database for searching
cuisines = process_dataset()

best_cuisine = None
best_score = 0
sum = 0
for cuisine_key in cuisines.keys():
    print(f"----------{cuisine_key}----------")
    print(f"{input_ingred[0]}--{cuisines[cuisine_key].get(input_ingred[0])}")
    print(f"{input_ingred[1]}--{cuisines[cuisine_key].get(input_ingred[1])}")
    print(f"{input_ingred[2]}--{cuisines[cuisine_key].get(input_ingred[2])}")
    print(f"------------------------------")
    cur_score = (cuisines[cuisine_key].get(input_ingred[0]) or 0) + (cuisines[cuisine_key].get(input_ingred[1]) or 0) + (cuisines[cuisine_key].get(input_ingred[2]) or 0)
    sum = sum + cur_score 
    if cur_score > best_score:
        best_score = cur_score
        best_cuisine = cuisine_key

print(best_cuisine)
print(round((best_score/sum),2))

