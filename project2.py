# python libraries
import argparse
import json
import os

#external libraries
from fuzzywuzzy import fuzz

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

def load_json_file(file_name):
    """Function to open and convert json dataset."""
    json_file = open(file_name,'r')
    json_parsed = json.load(json_file)
    return json_parsed

def make_json_model():
    """Function to BLAH."""
    # load yummly dataset
    yummy_json = load_json_file('yummly.json')
    num_recipes = len(yummy_json)

    print("making model....")
    ingredients = {}
    for recipe in yummy_json:
        rec_cuisine = recipe["cuisine"]
        rec_ingredients = recipe["ingredients"]

        for ingred in rec_ingredients:
            # adds cuisine to cuisine dict if it was not in dict already
            if ingred in ingredients.keys():
                if rec_cuisine in ingredients[ingred]["cuisines_dict"].keys():
                    ingredients[ingred]["cuisines_dict"][rec_cuisine] += 1
                    ingredients[ingred]["total_ingred_count"] += 1
                else:
                    ingredients[ingred]["cuisines_dict"][rec_cuisine] = 1
                    ingredients[ingred]["total_ingred_count"] = 1

            else:            
                ingredients[ingred] = {"cuisines_dict":{}, "total_ingred_count": 0} # dict for cuisines and set for fuzzy matches
                ingredients[ingred]["cuisines_dict"][rec_cuisine] = 1
                ingredients[ingred]["total_ingred_count"] = 1
        
    for ingred_key in ingredients.keys():
        for cuisine_key in ingredients[ingred_key]["cuisines_dict"].keys():
            weight = num_recipes*ingredients[ingred_key]["total_ingred_count"]
            ingredients[ingred_key]["cuisines_dict"][cuisine_key] = ingredients[ingred_key]["cuisines_dict"][cuisine_key]/(weight)

    print("saving model....")
    out_file = open("model3.json", "w")
    json.dump(ingredients, out_file, indent = 6)
    out_file.close()

def fuzzy_ingred_match(keys, input):
    """Function to compare a list of strings/keys to an input to find a fuzzy string match."""
    first_matches = []
    second_matches = []

    for key in keys:
        ratio = fuzz.token_sort_ratio(key,input)
        if (ratio > 75):
            first_matches.append([key, ratio])


    for match in first_matches:
        for key in keys:
            ratio = fuzz.token_sort_ratio(key,match[0])
            if (ratio > 75):
                second_matches.append([key, ratio])

    second_matches = sorted(second_matches, key=lambda x:x[1], reverse=True)
    return second_matches

def find_closest_cuisine_ingreddict(args, json_model):
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
                matched_ing = match[0]
                for cuisine in json_model[matched_ing]["cuisines_dict"]:
                    if cuisine in cuisine_scores:
                        cuisine_scores[cuisine] += json_model[matched_ing]["cuisines_dict"][cuisine]
                    else:
                        cuisine_scores[cuisine] = json_model[inp_ing]["cuisines_dict"][cuisine]

    # normalize cuisine scores
    sum_scores = 0
    for cuisine_key in cuisine_scores.keys():
        sum_scores += cuisine_scores[cuisine_key]

    for cuisine_key in cuisine_scores.keys():
        cuisine_scores[cuisine_key] = round((cuisine_scores[cuisine_key]/sum_scores),4)

    # sort by score
    scores_list = sorted(cuisine_scores.items(), key=lambda x:x[1], reverse=True)
    for score in scores_list:
        print(score)


def find_N_foods(args, json_model):
    N = args.N

"""Uses search to predict cuisine and find N-closest foods"""
# gets arguments passed in via argparse
args = add_arguments()

# # creates indexed search for searching
# make_json_model() # commented out when not making model (e.g. for turning in project)

# load indexed search stored in jsons
json_model = load_json_file('model3.json')

# find closest cuisine
find_closest_cuisine_ingreddict(args, json_model)