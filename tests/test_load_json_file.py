import project2

def test_load_json_file():
    # asserts that model can be loaded properly
    model = project2.load_json_file("model.json")
    assert (model != None)