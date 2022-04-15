import project2

def test_find_N_foods():
    ingred = ingredient=['country bread', 'garlic']
    N = 2
    json_model = project2.load_json_file("model.json")

    expected_N = [{"id":38051, "score":1},{"id":15453, "score":0.5}]
    actual_N = project2.find_N_foods(N, ingred, json_model)

    # asserts that expected number of changes required matches actual number of changes required
    assert (expected_N == actual_N)
