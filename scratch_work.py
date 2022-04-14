def test_fuzzy():
    strings1 = ["banana","banana","rice krispies","rice krispies","Rice Krispies Cereal", "peanut", "mint sauce", "pepper", "rice krispies", "crispy rice cereal"]
    strings2 = ["bananas", "banana peppers","Rice Krispies Cereal","crispy rice cereal","crispy rice cereal", "peanut butter", "marinara sauce","pepperoni", "puffed rice", "puffed rice"]

    for i in range(len(strings1)):
        ratio = fuzz.ratio(strings1[i].lower(),strings2[i].lower())
        partial_ratio = fuzz.partial_ratio(strings1[i].lower(),strings2[i].lower())
        token_sort_ratio = fuzz.token_sort_ratio(strings1[i],strings2[i])
        print(f"The ratios for {strings1[i]} and {strings2[i]}. Ratio -- {ratio}. Partial Ratio -- {partial_ratio}. TokenSortRatio -- {token_sort_ratio}.")

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