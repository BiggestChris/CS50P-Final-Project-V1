from match2_functions import *
import pytest
import random
from unittest.mock import patch

def test_set_size():
    sys.argv = ["match2.py", "2", "2"]
    assert set_size() == (2, 2)
    sys.argv = ["match2.py", "4", "4"]
    assert set_size() == (4, 4)
    sys.argv = ["match2.py", "3", "10"]
    assert set_size() == (3, 10)
    sys.argv = ["match2.py", "3", "10", "11"]
    with pytest.raises(SystemExit):
        set_size()
    sys.argv = ["match2.py", "30", "100"]
    with pytest.raises(SystemExit):
        set_size()
    sys.argv = ["match2.py", "dog", "cat"]
    with pytest.raises(SystemExit):
        set_size()


def test_create_inital_objects():
    random.seed("0xBEEF")
    assert create_inital_objects((2,2)) == ({
        "a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"})


def test_create_grid_object():
    random.seed("0xBEEF")
    assert create_grid_object((2,2)) == {
        "a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}


def test_initialise():
    assert initialise([2, 1]) == ["🌴", "🌴"]
    assert initialise([5, 2]) == ["🌴", "🌴", "🍗", "🍗", "🚀", "🚀", "🐇", "🐇", "🐢", "🐢"]
    assert initialise([10, 2]) == ["🌴", "🌴", "🍗", "🍗", "🚀", "🚀", "🐇", "🐇", "🐢", "🐢", "🐉", "🐉", "🍅", "🍅", "🍕", "🍕", "🍇", "🍇", "🌊", "🌊"]
    with pytest.raises(ValueError):
        initialise([5,3])
        initialise([30,5])


def test_randomise():
    random.seed("0xBEEF")
    assert randomise(["🌴", "🌴", "🍗", "🍗"]) == ["🌴", "🍗", "🌴", "🍗"]


def test_map_to_grid():
    pics = ["🌴", "🌴", "🍗", "🍗", "🚀", "🚀", "🐇", "🐇", "🐢", "🐢"]
    assert map_to_grid(pics, [1, 10]) == {
        "a1": "🌴", "a2": "🌴", "a3": "🍗", "a4": "🍗", "a5": "🚀", "a6":  "🚀", "a7": "🐇", "a8": "🐇", "a9": "🐢",  "a10": "🐢"
        }
    assert map_to_grid(pics, [10, 1]) == {
        "a1": "🌴", "b1": "🌴", "c1": "🍗", "d1": "🍗", "e1": "🚀", "f1":  "🚀", "g1": "🐇", "h1": "🐇", "i1": "🐢",  "j1": "🐢"
        }
    assert map_to_grid(pics, [5, 2]) == {
        "a1": "🌴", "b1": "🌴", "c1": "🍗", "d1": "🍗", "e1": "🚀", "a2":  "🚀", "b2": "🐇", "c2": "🐇", "d2": "🐢",  "e2": "🐢"
        }
    assert map_to_grid(pics, [2, 5]) == {
        "a1": "🌴", "b1": "🌴", "a2": "🍗", "b2": "🍗", "a3": "🚀", "b3":  "🚀", "a4": "🐇", "b4": "🐇", "a5": "🐢",  "b5": "🐢"
        }


def test_initialise_reveal():
    assert initialise_reveal([1, 10]) == {
        "a1": "#", "a2": "#", "a3": "#", "a4": "#", "a5": "#", "a6":  "#", "a7": "#", "a8": "#", "a9": "#",  "a10": "#"
        }
    assert initialise_reveal([10, 1]) == {
        "a1": "#", "b1": "#", "c1": "#", "d1": "#", "e1": "#", "f1":  "#", "g1": "#", "h1": "#", "i1": "#",  "j1": "#"
        }
    assert initialise_reveal([5, 2]) == {
        "a1": "#", "b1": "#", "c1": "#", "d1": "#", "e1": "#", "a2":  "#", "b2": "#", "c2": "#", "d2": "#",  "e2": "#"
        }
    assert initialise_reveal([2, 5]) == {
        "a1": "#", "b1": "#", "a2": "#", "b2": "#", "a3": "#", "b3":  "#", "a4": "#", "b4": "#", "a5": "#",  "b5": "#"
        }


def test_print_first_table():                                       # Received help from DDB AI
    with patch('builtins.print') as mocked_print:
        print_first_table({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, (2,2))
    mocked_print.assert_called_with(tabulate([["","a","b"],["1","#","#"],["2","#","#"]], tablefmt="grid", colalign=("center","center")))

    with patch('builtins.print') as mocked_print:
        print_first_table({"a1": "🌴", "b1": "🍗", "c1": "🍗", "d1": "🌴"}, (4,1))
    mocked_print.assert_called_with(tabulate([["","a","b","c","d"],["1","#","#","#","#"]], tablefmt="grid", colalign=("center","center")))

    with patch('builtins.print') as mocked_print:
        print_first_table({"a1": "🌴", "b1": "🍗", "c1": "🚀", "d1": "🐇", "a2": "🌴", "b2": "🍗", "c2": "🚀", "d2": "🐇"}, (4,2))
    mocked_print.assert_called_with(tabulate([["","a","b","c","d"],["1","#","#","#","#"],["2","#","#","#","#"]], tablefmt="grid", colalign=("center","center")))


def test_grid_to_hash_table():
    assert grid_to_hash_table({
        "a1": "#", "a2": "#", "a3": "#", "a4": "#", "a5": "#", "a6":  "#", "a7": "#", "a8": "#", "a9": "#",  "a10": "#"
        }, [1, 10]) == [["","a"],["1","#"],["2","#"],["3","#"],["4","#"],["5","#"],["6","#"],["7","#"],["8","#"],["9","#"],["10","#"]]
    assert grid_to_hash_table({"a1": "#", "b1": "#", "a2": "#", "b2": "#"}, [2, 2]) == [["","a","b"], ["1","#","#"], ["2","#","#"]]


def test_recur_hash():
    table = [["","a","b"],["1"]]
    recur_hash(table, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"}, 97, 1)
    assert table == [["","a","b"],["1","#","#"]]

    table = [["","a","b"],["1","#","#"],["2"]]
    recur_hash(table, {"a1": "#", "b1": "#", "a2": "#", "b2": "#", "a3": "#", "b3": "#"}, 97, 2)
    assert table == [["","a","b"],["1","#","#"],["2","#","#"]]

    table = [["","a","b"],["1","#","#"],["2","#","#"],["3"]]
    recur_hash(table, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"}, 97, 3)
    assert table == [["","a","b"],["1","#","#"],["2","#","#"],["3"]]


def test_select_cells(monkeypatch):                                 # Received help from DDB AI
    inputs = iter(['a1', 'b1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert select_cells({"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}, {
        "a1": "#", "b1": "#", "a2": "#", "b2": "#"}, ["a1","b1","a2","b2"], (2,2)) == ["a1", "b1", "#"]

    inputs = iter(['a1', 'a2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert select_cells({"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}, {
        "a1": "#", "b1": "#", "a2": "#", "b2": "#"}, ["a1","b1","a2","b2"], (2,2)) == ["a1", "a2", "🌴"]

    inputs = iter(['a1', 'a1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        select_cells({"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}, {
        "a1": "#", "b1": "#", "a2": "#", "b2": "#"}, ["a1","b1","a2","b2"], (2,2))

    inputs = iter(['a5', 'a6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        select_cells({"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}, {
        "a1": "#", "b1": "#", "a2": "#", "b2": "#"}, ["a1","b1","a2","b2"], (2,2))


def test_key_input(monkeypatch):                                    # Received help from DDB AI
    inputs = iter(['b1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert key_input("Cell: ", ["a1","b1", "a2", "b2"], {"a1": "🌴", "b1": "#", "a2": "🌴", "b2": "#"}) == "b1"

    inputs = iter(['a5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        key_input("Cell: ", ["a1","b1", "a2", "b2"], {"a1": "🌴", "b1": "#", "a2": "🌴", "b2": "#"})

    inputs = iter(['a1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        key_input("Cell: ", ["a1","b1", "a2", "b2"], {"a1": "🌴", "b1": "#", "a2": "🌴", "b2": "#"})


def test_print_reveal_table():                                      # Received help from DDB AI
    with patch('builtins.print') as mocked_print:
        print_reveal_table({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"}, "a1", "b2", (2,2))
    mocked_print.assert_called_with(tabulate([["","a","b"],["1","🌴","#"],["2","#","🌴"]], tablefmt="grid", colalign=("center","center")))

    with patch('builtins.print') as mocked_print:
        print_reveal_table({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"}, "a2", "b1", (2,2))
    mocked_print.assert_called_with(tabulate([["","a","b"],["1","#","🍗"],["2","🍗","#"]], tablefmt="grid", colalign=("center","center")))

    with patch('builtins.print') as mocked_print:
        print_reveal_table({"a1": "🌴", "b1": "🍗", "c1": "🚀", "d1": "🐇", "a2": "🌴", "b2": "🍗", "c2": "🚀", "d2": "🐇"},
                           {"a1": "🌴", "b1": "#", "c1": "#", "d1": "🐇", "a2": "🌴", "b2": "#", "c2": "#", "d2": "🐇"},
                           "c1", "b2", (4,2))
    mocked_print.assert_called_with(tabulate([["","a","b","c","d"],["1","🌴","#","🚀","🐇"],["2","🌴","🍗","#","🐇"]], tablefmt="grid", colalign=("center","center")))


def test_reveal():
    assert reveal({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                  "a1", "b1", [2, 2]) == [["","a","b"], ["1","🌴","🍗"], ["2","#","#"]]
    assert reveal({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                  "b1", "a2", [2, 2]) == [["","a","b"], ["1","#","🍗"], ["2","🍗","#"]]


def test_recur_append():
    assert recur_append([["","a","b","c","d"],["1"]], 1, {"a1": "🌴", "b1": "🍗", "c1": "🍗", "d1": "🌴"}, {"a1": "#", "b1": "#", "c1": "#", "d1": "#"},
                 "a", 1, "a1", "b1") == [["","a","b","c","d"],["1", "🌴", "🍗", "#", "#"]]
    assert recur_append([["","a","b"],["1"]], 1, {"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                 "a", 1, "a1", "b2") == [["","a","b"],["1", "🌴", "#"]]
    assert recur_append([["","a","b"],["1", "🌴", "#"],["2"]], 2, {"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                 "a", 2, "a1", "b2") == [["","a","b"],["1", "🌴", "#"],["2", "#", "🌴"]]


def test_append_test():
    assert append_test({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                        "b1", "b1", "a2") == "🍗"
    assert append_test({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                        "a2", "b1", "a2") == "🍗"
    assert append_test({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, {"a1": "#", "b1": "#", "a2": "#", "b2": "#"},
                        "a2", "b1", "b2") == "#"


def test_match():
    assert match({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, "a1", "b1") == "#"
    assert match({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, "a1", "a2") == "#"
    assert match({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, "a1", "b2") == "🌴"
    assert match({"a1": "🌴", "b1": "🍗", "a2": "🍗", "b2": "🌴"}, "b1", "a2") == "🍗"
