# cs5293sp22-project2

### Author: Sarah Brown

# Directions to Install and Use Package
To download and use package, follow the steps below:

1. git clone https://github.com/SarahBrown/cs5293sp22-project2.git
2. cd cs5293sp22-project2/
3. pipenv install
4. Run via pipenv with one of the following example commands:
pipenv run python project2.py --N 5 --ingredient paprika --ingredient banana --ingredient 'rice krispies'
pipenv run python project2.py --N 5 --ingredient 'country bread' --ingredient 'garlic'

# Web or External Libraries
For this project I used several packages from the standard library and some external libraries. These included argparse, json, os, and sys. In addition, the external librarie fuzzywuzzy was imported for string comparisons. Due to fuzzywuzzy causing a warning (Using slow pure-python SequenceMatcher), python-Levenshtein was also added to the Pipfile.

# Functions and Approach to Development
This project takes specific ingredients from the command line and uses them to predict the cuisine of the food. In addition, by taking another variable, N, from the user, the N-closest recipes can be found. That is, the recipes that would take the fewest changes to switch to. This project was implemented with various functions, first by processing arguments.

After the arguments were processed, the yummly.json data was processed by using the json package. This data was then used to create weights for each ingredient per cuisine. These weights were then combined with the processed arguments to determine the likelihood of the igredients combining to be the various cuisines. In a similar manner, weights were found for the N-closest recipes by determing the number of insertions/deletions to get matching ingredient lists. Finally, the output was then stored in a dictionary and dumped out to stdout via json.dump.

## Functions
### add_arguments()
The arguments taken in are a list of ingredients and a number N for the N-closest foods. These arguments were added in the add_arguments() function via argparse.

#### Argparse Flags
* --"ingredient", type=str, required=True, action='append', help="Ingredients to predict type of cuisine and similar meals for.
* "--N", type=int, required=True, help="Top-N closest foods."

### load_json_file()
This function takes a file_name, opens it, and processes it using the json package. This takes the JSON file and returns a dictionary that can be used.

### fuzzy_ingred_match()
This function takes a list of strings and an input string and compares them to try and find fuzzy matches. The list of strings and the input string are both composed of ingredient names. This function is used within other functions to find near matches while avoiding matches that are not close enough. This function makes use of the fuzzywuzzy package and in particular the token_sort_ratio function.

The fuzzywuzzy package uses a ratio function to compute the standard Levenshtein distance between two different strings. However, the token_sort_ratio not only compares the distances in that manner, but also sorts the tokens alphabetically and joins them together. This function was selected after testing other fuzzywuzzy ratio results. 

A threshold is then applied to the ratio result from fuzzywuzzy's token_set_ratio.  This threshold is a value of 75/100, which was determined via testing. Below are two example lists of strings, these lists were used to determine which fuzzywuzzy function to use as well as what threshold to use. Such a threshold allows banana to match bananas, rice krispies to match Rice Krispies Cereal, but does not allow banana to match banana peppers or peanut to match peanut butter.
* strings1 = ["banana","banana","rice krispies","rice krispies","Rice Krispies Cereal", "peanut", "mint sauce", "pepper"]
* strings2 = ["bananas", "banana peppers","Rice Krispies Cereal","crispy rice cereal","crispy rice cereal", "peanut butter", "marinara sauce","pepperoni"]

However, one issue was found with these examples was that rice krispies matched Rice Krispies Cereal, but rice krispies did not match cripsy rice cereal. While these did not match, Rice Krispies Cereal did match cripsy rice cereal. Since these matched instead, the token_sort_ratio was applied twice. The first time, the function loops through the list of strings and compares those to the input string. Afterwards, any matches found with the first past are compared again to the list of strings to find any additional fuzzy matches.

By looping through twice like this, many fuzzy matches were found while avoiding others that did not actually match.

### count_changes_list()
This function takes two lists and counts how many insertions or deletions would be needed to make the lists equivalent. This function is used in other functions that were created to help find the N-closest recipes. This is calculated by looping through the elements in both lists and adding up how many differences there are.

### make_json_model()
This function loops through each recipe in the yummly dataset and counts how many of each ingredient type there is. More specifically, how many of each ingredient exists for each cuisine type. By counting the number of ingredients, weights can then be assigned and added together to calculate the score of a specific set of ingredients passed in via the command line.

This model is created and stored in a dictionary. By storing this model in a dictionary, it is easy to save out to a JSON file and then load back in to other functions. Saving the model allows it to be used without being created each time the python file is run. 

This function loops through all of the recipes in the dataset. Per each recipe, it then loops over its ingredients. If the ingredient already exists in the ingredient dictionary, the ingredient's cuisine section is then incremented. In addition, the total ingredient count for that particular ingredient is incremented. If the ingredient does not exist in the dictionary, it is added and initialized.

After each recipe has been included, the dictionary is then looped over again per ingredient and a weight is assigned. This weight is calculated as follows: (number of times ingredient shows up in cuisine)/(total number of recipes*number of times ingredient shows up in total). All of these weights are stored back in the ingredient dictionary and are saved to a JSON file.

An example entry, if the ingredient dictionary only contained romaine lettuce, is shown below.
{
      "romaine lettuce": {
            "cuisines_dict": {
                  "greek": 7.0542449733078225e-06,
                  "korean": 9.043903811933105e-07,
                  "mexican": 1.8630441852582198e-05,
                  "thai": 3.617561524773242e-06,
                  "southern_us": 1.447024609909297e-06,
                  "french": 2.1705369148639453e-06,
                  "cajun_creole": 2.1705369148639453e-06,
                  "italian": 5.968976515875849e-06,
                  "vietnamese": 3.074927296057256e-06,
                  "spanish": 7.235123049546485e-07,
                  "indian": 5.426342287159863e-07,
                  "chinese": 2.3514149911026074e-06,
                  "irish": 1.8087807623866212e-07
            },
            "total_ingred_count": 139
      }
}

### find_closest_cuisine()
This function uses the created model and the fuzzy_ingred_match function to find the closest cuisine match provided the ingredients entered as arguments. 

To start, each input ingredient is looped over and is checked to see if an EXACT match exists in the JSON model keys. If an exact match is found, the weight assigned to this key is added to a score. This is done for each cuisine to determine which cuisine has the highest score when all of the weights are summed. 

If an exact match is not found, the fuzzy_ingred_match function is then used. The model's keys are compared against the input ingredient. If a fuzzy match is found, the sum is then updated with its weight.

After sums are calculated for each cuisine, the scores are normalized. The scores are normalized by adding up all of the sums for the different cuisines. The individual cuisine scores are then divided by this sum and the result is rounded to two decimal points. This list is then sorted by the cuisine score, highest to lowest. The top score is taken from this sorted list and is returned as the closest match for the cuisine of the entered ingredients.

### find_N_foods()
This function is used to find the top N-closest foods to the entered ingredients based on an entered value for N. 

This is done by taking the entered input ingredients and finding the fuzzy matches that are in the list of all of the yummly ingredients. This list comes from the created JSON model. By fuzzy matching this accounts for ingredients that might be entered in as variables differently than they are stored as ingredients in the yummly dataset.

This list of matches is then taken and compared to the ingredients in the different recipes. If an input ingredient is in a recipe, that recipe is added to a set. If there are matches, the score is then calculated.

This is done by comparing the list of matches found in the recipe to all of the recipe's ingredients. This is done with the count_changes_lists function mentioned previously. The matched ingredients are also compared to the input ingredients via the command line. This second comparison is not done with fuzzy matching. The two distances calculated via the count_changes_lists function are then added together.

This value of change is double checked to make sure that it is not 0, for a perfect match, and then is inverted (1/change) and rounded to 2 decimal places. All of these scores for the various recipes with matching ingredients are then added to a list. This list is then sorted by score, highest to lowest. Finally, the top N-highest scores are filtered and returned.

# Assumptions Made and Known Bugs
Some ingredients I was unsure if they were technically fuzzy matches due to my cooking knowledge. For example, when finding how best to match rice krispies, rice krispies cereal, and crispy rice cereal, I found another ingredient called puffed rice. On investigation it turned out that the cuisines of all the recipes that contained puffed rice were Indian. It also appears based on google searches that puffed rice is different from rice krispies. However, there is no guarantee that there are some other ingredients in the model that will not fuzzy match to user input that should.

There are no known bugs.

# Tests
Tests are performed with PyTest and local data. Tests are also set up with Github Actions and PyTest to run automatically when code is pushed to the repository.

Due to the nature of the dataset, the majority of these test that used the provided dataset are regression tests to ensure that the code continues to work as expected. These values were confirmed by searching the dataset to confirm that the values made sense.

Functions that compared lists (fuzzy_ingred_match, count_changes_lists) were tested with smaller lists that could be confirmed by hand. 

load_json_file was tested to make sure that the model was loaded properly.

make_json_model() is not tested as it is specified in the requirements that the model should be loaded and not created.