import project2

def test_fuzzy_ingred_match():
    test_strings = ["bananas", "banana peppers","Rice Krispies Cereal","crispy rice cereal","crispy rice cereal", "peanut butter", "marinara sauce","pepperoni"]
    test_input = "banana"

    # test that bananas is found when entering banana
    expected_matches = ["bananas"]
    actual_matches = project2.fuzzy_ingred_match(test_strings, test_input)
    assert(actual_matches == expected_matches)

    # test that matches for rice krispies are found
    test_input = "rice krispies"
    expected_matches = ["Rice Krispies Cereal","crispy rice cereal","crispy rice cereal"]
    actual_matches = project2.fuzzy_ingred_match(test_strings, test_input)
    assert (actual_matches == expected_matches)