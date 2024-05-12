from match2_objects import *
import pytest
import random
from unittest.mock import patch
from tabulate import tabulate

def test_grid_creation():
    random.seed("0xBEEF")
    grid = Grid((2,2))
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "#", "b1": "#", "a2": "#", "b2": "#"}
    assert grid.table == [["", "a", "b"],["1", "#", "#"],["2", "#", "#"]]
    assert grid.keys == ["a1", "b1", "a2", "b2"]

    grid = Grid((5,2))
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "#", "b1": "#", "c1": "#", "d1": "#", "e1": "#", "a2":  "#", "b2": "#", "c2": "#", "d2": "#",  "e2": "#"}
    assert grid.table == [["", "a", "b", "c", "d", "e"],["1", "#", "#", "#", "#", "#"],["2", "#", "#", "#", "#", "#"]]
    assert grid.keys == ["a1", "b1", "c1", "d1", "e1", "a2", "b2", "c2", "d2", "e2"]

    with pytest.raises(ValueError):
        grid = Grid((3,5))
    with pytest.raises(ValueError):
        grid = Grid((16,2))
    with pytest.raises(ValueError):
        grid = Grid(("dog","cat"))
    with pytest.raises(ValueError):
        grid = Grid((0, 0))
    with pytest.raises(ValueError):
        grid = Grid((-3, 4))
    with pytest.raises(ValueError):
        grid = Grid((-3, -4))
    with pytest.raises(TypeError):
        grid = Grid((3,4), "cat")

def test_grid_immutability():
    grid = Grid((2, 2))
    with pytest.raises(AttributeError):
        grid.grid = {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    with pytest.raises(AttributeError):
        grid.reveal = {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    with pytest.raises(AttributeError):
        grid.keys = ["a1", "a2", "a3", "a4"]
    with pytest.raises(AttributeError):
        grid.table = [["", "a"],["1", "#"],["2", "#"],["3", "#"], ["4", "#"]]

def test_reveal_cell():
    random.seed("0xBEEF")
    grid = Grid((2, 2))
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "#", "b1": "#", "a2": "#", "b2": "#"}
    grid.reveal_cell("a1")
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "🌴", "b1": "#", "a2": "#", "b2": "#"}
    grid.reveal_cell("b1")
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "🌴", "b1": "🍗", "a2": "#", "b2": "#"}

    grid = Grid((5, 2))
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "#", "b1": "#", "c1": "#", "d1": "#", "e1": "#", "a2":  "#", "b2": "#", "c2": "#", "d2": "#",  "e2": "#"}
    grid.reveal_cell("a1")
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "🌴", "b1": "#", "c1": "#", "d1": "#", "e1": "#", "a2":  "#", "b2": "#", "c2": "#", "d2": "#",  "e2": "#"}
    grid.reveal_cell("b2")
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "🌴", "b1": "#", "c1": "#", "d1": "#", "e1": "#", "a2":  "#", "b2": "🚀", "c2": "#", "d2": "#",  "e2": "#"}

    grid = Grid((2, 2))
    with pytest.raises(ValueError):
        grid.reveal_cell("z26")
    with pytest.raises(ValueError):
        grid.reveal_cell("cat")

def test_unreveal_cell():
    random.seed("0xBEEF")
    grid = Grid((2, 2))
    grid.reveal_cell("a1")
    grid.reveal_cell("b1")
    grid.reveal_cell("a2")
    grid.reveal_cell("b2")
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    grid.unreveal_cell("b1")
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "🌴", "b1": "#", "a2": "🌴", "b2": "🍗"}
    grid.unreveal_cell("a2")
    assert grid.grid == {"a1": "🌴", "b1": "🍗", "a2": "🌴", "b2": "🍗"}
    assert grid.reveal == {"a1": "🌴", "b1": "#", "a2": "#", "b2": "🍗"}

    grid = Grid((5, 2))
    grid.reveal_cell("a1")
    grid.reveal_cell("a2")
    grid.reveal_cell("b1")
    grid.reveal_cell("b2")
    grid.reveal_cell("c1")
    grid.reveal_cell("c2")
    grid.reveal_cell("d1")
    grid.reveal_cell("d2")
    grid.reveal_cell("e1")
    grid.reveal_cell("e2")
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    grid.unreveal_cell("b2")
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "#", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    grid.unreveal_cell("e1")
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "#", "a2":  "🚀", "b2": "#", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    grid.unreveal_cell("a1")
    assert grid.grid == {"a1": "🌴", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "🐇", "a2":  "🚀", "b2": "🚀", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}
    assert grid.reveal == {"a1": "#", "b1": "🐢", "c1": "🍗", "d1": "🍗", "e1": "#", "a2":  "🚀", "b2": "#", "c2": "🐇", "d2": "🌴",  "e2": "🐢"}

    grid = Grid((2, 2))
    with pytest.raises(ValueError):
        grid.unreveal_cell("z26")
    with pytest.raises(ValueError):
        grid.unreveal_cell("cat")

def test_print():
    grid = Grid((2, 2))
    with patch('builtins.print') as mocked_print:
        print(str(grid))
    mocked_print.assert_called_with(tabulate([["","a","b"],["1","#","#"],["2","#","#"]], tablefmt="grid", colalign=("center","center")))

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

def test_select_cells(monkeypatch):                                 # Received help from DDB AI
    grid = Grid((2, 2))

    inputs = iter(['a1', 'b1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert select_cells(grid) == ["a1", "b1"]

    inputs = iter(['a1', 'a2'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert select_cells(grid) == ["a1", "a2"]

    inputs = iter(['a1', 'a1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        select_cells(grid)

    inputs = iter(['a5', 'a6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        select_cells(grid)


def test_key_input(monkeypatch):                                    # Received help from DDB AI
    grid = Grid((2, 2))
    grid.reveal_cell("a1")
    grid.reveal_cell("a2")

    inputs = iter(['b1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert key_input("Cell: ", grid) == "b1"

    inputs = iter(['a5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        key_input("Cell: ", grid)

    inputs = iter(['a1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with pytest.raises(StopIteration):
        key_input("Cell: ", grid)
