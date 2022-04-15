# python libraries
import argparse
import json
import os
import sys

#external libraries
from fuzzywuzzy import fuzz

def add_arguments():
    """Function to add and parse arguments from command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--ingredient", type=str, required=True, action='append', 
                            help="Ingredients to predict type of cuisine and similar meals for.")
    parser.add_argument("--N", type=int, required=True,
                            help="Top-N closest foods.")
        
    # get and return args
    args = parser.parse_args()
    return args

def load_json_file(file_name):
    """Function to open and convert json dataset."""
    json_file = open(file_name,'r')
    json_parsed = json.load(json_file)
    return json_parsed

def fuzzy_ingred_match(keys, input):
    """Function to compare a list of strings/keys to an input to find a fuzzy string match."""
    first_matches = []
    second_matches = []

    for key in keys:
        ratio = fuzz.token_sort_ratio(key,input)
        if (ratio > 75):
            first_matches.append(key)

    for match in first_matches:
        for key in keys:
            ratio = fuzz.token_sort_ratio(key,match)
            if (ratio > 75):
                second_matches.append(key)

    return second_matches

def count_changes_lists(list1, list2):
    """Compares changes needed to make list1 into list2"""
    inserts = 0
    deletes = 0

    for list1_ele in list1:
        if (list1_ele not in list2):
            deletes += 1
    
    for list2_ele in list2:
        if (list2_ele not in list1):
            inserts += 1
    
    change = inserts+deletes
    return(change)

def make_json_model():
    """Function to construct a searchable json model."""
    # load yummly dataset
    yummy_json = load_json_file('yummly.json')
    num_recipes = len(yummy_json)

    # makes model
    ingredients = {}
    for recipe in yummy_json:
        # gets recipe's ingredients and cuisine data
        rec_cuisine = recipe["cuisine"]
        rec_ingredients = recipe["ingredients"]

        # loops through ingredients in recipe and adds them to ingredient dictionary
        for ingred in rec_ingredients:
            # increments or inits ingredient count for cuisine and total ingredient if it is already in dictionary
            if ingred in ingredients.keys():
                if rec_cuisine in ingredients[ingred]["cuisines_dict"].keys():
                    ingredients[ingred]["cuisines_dict"][rec_cuisine] += 1
                    ingredients[ingred]["total_ingred_count"] += 1
                else:
                    ingredients[ingred]["cuisines_dict"][rec_cuisine] = 1
                    ingredients[ingred]["total_ingred_count"] = 1

            # adds ingredient and sets count to 1 if it was not already in dictionary
            else:            
                ingredients[ingred] = {"cuisines_dict":{}, "total_ingred_count": 0} # dict for cuisines and set for fuzzy matches
                ingredients[ingred]["cuisines_dict"][rec_cuisine] = 1
                ingredients[ingred]["total_ingred_count"] = 1
        
    # changes values to be weighted values by dividing by the total number of times ingrident shows up
    for ingred_key in ingredients.keys():
        for cuisine_key in ingredients[ingred_key]["cuisines_dict"].keys():
            weight = num_recipes*ingredients[ingred_key]["total_ingred_count"]
            ingredients[ingred_key]["cuisines_dict"][cuisine_key] = ingredients[ingred_key]["cuisines_dict"][cuisine_key]/(weight)

    # outputs model
    out_file = open("model.json", "w")
    json.dump(ingredients, out_file, indent = 6)
    out_file.close()

def find_closest_cuisine(args, json_model):
    input_ingred = args.ingredient
    cuisine_scores = {}

    for inp_ing in input_ingred:
        if inp_ing in json_model.keys():
            for cuisine in json_model[inp_ing]["cuisines_dict"]:
                if cuisine in cuisine_scores:
                    cuisine_scores[cuisine] += json_model[inp_ing]["cuisines_dict"][cuisine]
                else:
                    cuisine_scores[cuisine] = json_model[inp_ing]["cuisines_dict"][cuisine]

        else:
            matches = fuzzy_ingred_match(json_model.keys(), inp_ing)
            for match in matches:
                matched_ing = match
                for cuisine in json_model[matched_ing]["cuisines_dict"]:
                    if cuisine in cuisine_scores:
                        cuisine_scores[cuisine] += json_model[matched_ing]["cuisines_dict"][cuisine]
                    else:
                        cuisine_scores[cuisine] = json_model[matched_ing]["cuisines_dict"][cuisine]

    # normalize cuisine scores
    sum_scores = 0
    for cuisine_key in cuisine_scores.keys():
        sum_scores += cuisine_scores[cuisine_key]

    for cuisine_key in cuisine_scores.keys():
        cuisine_scores[cuisine_key] = round((cuisine_scores[cuisine_key]/sum_scores),2)

    # sort by score
    scores_list = sorted(cuisine_scores.items(), key=lambda x:x[1], reverse=True) # sorted by score, highest to lowest
    return (scores_list[0]) # returns top score

def find_N_foods(args, json_model):
    input_ingred = args.ingredient
    yummy_json = load_json_file('yummly.json')
    N = args.N
    closest_N = []
    output = []

    fuzzy_matches = input_ingred.copy()
    for inp_ing in input_ingred:
        matches = fuzzy_ingred_match(json_model.keys(), inp_ing)
        for match in matches:
            if match not in fuzzy_matches:
                fuzzy_matches += matches
    
    for recipe in yummy_json:
        rec_ingredients = recipe["ingredients"]
        ingred_matches = set()

        # checks for fuzzy matches for input ingredients in recipe's ingredients
        for inp in fuzzy_matches:
            if (inp in rec_ingredients):
                ingred_matches.add(inp)

        num_matches = len(ingred_matches)
        if (num_matches > 0):
            change_matches_recipe = count_changes_lists(ingred_matches, rec_ingredients)
            change_matches_input = count_changes_lists(ingred_matches, input_ingred) # does not fuzzy match
            change = change_matches_recipe + change_matches_input
            if (change == 0):
                score = 1
            else:
                score = round((1/change),2)
            closest_N.append([recipe["id"], score]) # id, score            

    closest_N = sorted(closest_N, key=lambda x:x[1], reverse=True) # sorted by score, highest to lowest
    closest_N = closest_N[:N]
    for close in closest_N:
        output.append({"id":close[0], "score": close[1]})
    return output
            
"""Uses search to predict cuisine and find N-closest foods"""
# gets arguments passed in via argparse
args = add_arguments()

# # creates indexed search for searching
# make_json_model() # commented out when not making model (e.g. for turning in project)

# load indexed search stored in jsons
json_model = load_json_file('model.json')

# find closest cuisine
cuisine = find_closest_cuisine(args, json_model)
# find closest N foods
closest_N = find_N_foods(args, json_model)
# format output
output_dict = {"cuisine": cuisine[0],"score": cuisine[1], "closest": closest_N}
# dump output to stdout 
json.dump(output_dict, sys.stdout, indent = 2)