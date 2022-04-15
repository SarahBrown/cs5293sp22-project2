import project2

def test_count_changes_lists():
    test_list1 = ["bananas", "banana peppers","Rice Krispies Cereal","crispy rice cereal","crispy rice cereal", "peanut butter", "marinara sauce","pepperoni"]
    test_list2 = ["bananas", "Rice Krispies Cereal","crispy rice cereal","crispy rice cereal", "peanut butter", "marinara sauce"]

    expected_change = 2
    actual_change = project2.count_changes_lists(test_list1, test_list2)

    # asserts that expected number of changes required matches actual number of changes required
    assert (expected_change == actual_change)
