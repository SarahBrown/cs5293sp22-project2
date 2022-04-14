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

    out_file = open("model.json", "w")
    json.dump(cuisines, out_file, indent = 6)
    out_file.close()

def make_json_model2():
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
                fuzz = fuzzy_ingred_match(ingredients.keys(), ingred)
                if (fuzz != None): # checks to see if a fuzzy match is in
                    if rec_cuisine in ingredients[fuzz]["cuisines_dict"].keys():
                        ingredients[fuzz]["cuisines_dict"][rec_cuisine] += 1
                        ingredients[fuzz]["total_ingred_count"] += 1
                    else:
                        ingredients[fuzz]["cuisines_dict"][rec_cuisine] = 1
                        ingredients[fuzz]["total_ingred_count"] = 1
                    if (ingred not in ingredients[fuzz]["fuzzy_list"]):
                        ingredients[fuzz]["fuzzy_list"].append(ingred)
                else:
                    ingredients[ingred] = {"cuisines_dict":{}, "fuzzy_list":[], "total_ingred_count": 0} # dict for cuisines and set for fuzzy matches
                    ingredients[ingred]["cuisines_dict"][rec_cuisine] = 1
                    ingredients[ingred]["total_ingred_count"] = 1
        
    for ingred_key in ingredients.keys():
        for cuisine_key in ingredients[ingred_key]["cuisines_dict"].keys():
            weight = num_recipes*ingredients[ingred_key]["total_ingred_count"]
            ingredients[ingred_key]["cuisines_dict"][cuisine_key] = ingredients[ingred_key]["cuisines_dict"][cuisine_key]/(weight)

    print("saving model....")
    out_file = open("model2.json", "w")
    json.dump(ingredients, out_file, indent = 6)
    out_file.close()

def make_json_model3():
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
    for key in keys:
        ratio = fuzz.token_sort_ratio(key,input)
        if (ratio > 75):
            #print(ratio)
            return key
    
    return None

def test_fuzzy():
    strings1 = ["banana","banana","rice krispies","rice krispies","Rice Krispies Cereal", "peanut", "mint sauce", "pepper"]
    strings2 = ["bananas", "banana peppers","Rice Krispies Cereal","crispy rice cereal","crispy rice cereal", "peanut butter", "marinara sauce","pepperoni"]
    strings3 = ["vegetable stock","vegetable broth","vegetables","pickled vegetables","vegetable juice","vegetable oil spray","mixed vegetables",
                  "root vegetables","vegetable slaw","vegetable bouillon","vegetable gumbo","other vegetables","vegetable soup"]
    for i in range(len(strings1)):
        ratio = fuzz.ratio(strings1[i].lower(),strings2[i].lower())
        partial_ratio = fuzz.partial_ratio(strings1[i].lower(),strings2[i].lower())
        token_sort_ratio = fuzz.token_sort_ratio(strings1[i],strings2[i])
        print(f"The ratios for {strings1[i]} and {strings2[i]}. Ratio -- {ratio}. Partial Ratio -- {partial_ratio}. TokenSortRatio -- {token_sort_ratio}.")

def find_closest_cuisine_cuisinedict(args, json_model):
    input_ingred = args.ingredient
    best_cuisine = None
    best_score = 0
    sum = 0

    for cuisine_key in json_model.keys():
        cur_score = 0
        for inp_ing in input_ingred: # if input ingredient matches key, use that
            if inp_ing in json_model[cuisine_key].keys():
                cur_score = cur_score + json_model[cuisine_key].get(inp_ing)

            else: # if input ingredient not in keys, try to find match
                fuzzy_match = fuzzy_ingred_match(json_model[cuisine_key].keys(), inp_ing)
                cur_score = cur_score + (json_model[cuisine_key].get(fuzzy_match) or 0)

                print(f"{inp_ing}--{fuzzy_match}")
                
        sum = sum + cur_score 
        if cur_score > best_score:
            best_score = cur_score
            best_cuisine = cuisine_key


    best_score=(round((best_score/sum),2))
    print(f"{best_cuisine}--{best_score}")

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
            # do fuzzy
            pass

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
# make_json_model3() # commented out when not making model (e.g. for turning in project)

# load indexed search stored in jsons
json_model = load_json_file('model3.json')

# find closest cuisine
find_closest_cuisine_ingreddict(args, json_model)


