import project2

def test_find_closest_cuisine():
    ingred = ingredient=['country bread', 'garlic']
    json_model = project2.load_json_file("model.json")

    expected_cuisine = ("italian", 0.51)
    actual_cuisine = project2.find_closest_cuisine(ingred, json_model)

    # asserts that expected number of changes required matches actual number of changes required
    assert (expected_cuisine == actual_cuisine)
