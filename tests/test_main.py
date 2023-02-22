from src.main import main, _construct_preferences_dict
import pytest

def test_simple():
    data = main(
           2, 
           ["guest_a", "guest_b", "guest_c"], 
           [
               {"preference": "avoid", "guests": ["guest_a", "guest_b"]},
               {"preference": "pair", "guests": ["guest_c", "guest_a"]}
            ]
    )

    assert len(data.keys()) == 2

    assert data["table_2"] == ["guest_b"]
    assert "guest_a" in data["table_1"]
    assert "guest_c" in data["table_1"]

def test_configuration_where_one_guest_has_no_preferences():
    data = main(
           2,
           ["guest_a", "guest_b", "guest_c", "guest_d", "guest_e"], 
           [
               {"preference": "avoid", "guests": ["guest_a", "guest_b"]},
               {"preference": "pair", "guests": ["guest_c", "guest_a"]},
               {"preference": "pair", "guests": ["guest_c", "guest_e"]},
               {"preference": "avoid", "guests": ["guest_e", "guest_b"]},
            ]
    )

    assert len(data.keys()) == 2

    assert "guest_c" in data["table_1"]
    assert "guest_a" in data["table_1"]
    assert "guest_e" in data["table_1"]
    assert "guest_d" in data["table_1"]

    assert "guest_b" in data["table_2"]


def test_configuration_3():
    preferences = [
        {"preference": "pair", "guests": ["guest_a", "guest_d"]},
        {"preference": "pair", "guests": ["guest_b", "guest_e"]},
        {"preference": "pair", "guests": ["guest_c", "guest_f"]},
        {"preference": "avoid", "guests": ["guest_a", "guest_b", "guest_c"]},
        {"preference": "avoid", "guests": ["guest_e", "guest_f", "guest_d"]}
    ]

    data = main(
        3,
        ["guest_a", "guest_b", "guest_c", "guest_d", "guest_e", "guest_f"],
        preferences
    )

    assert len(data.keys()) == 3

    assert "guest_f" in data["table_1"]
    assert "guest_c" in data["table_1"]

    assert len(data["table_1"]) == 2
    assert len(data["table_2"]) == 2
    assert len(data["table_3"]) == 2

def test_configuration_with_an_empty_table():
    data = main(
        2,
        ["guest_a", "guest_b"],
        [{"preference": "pair", "guests": ["guest_a", "guest_b"]}],
    )

    assert "guest_a" in data["table_1"]
    assert "guest_b" in data["table_1"]
    assert data["table_2"] == []

def test_simple_invalid_configuration():
    with pytest.raises(Exception) as e:
        main(
            1,
            ["guest_a", "guest_b"],
            [{"preference": "avoid", "guests": ["guest_a", "guest_b"]}]
        )

    assert str(e.value) == "Can't find a table for guest guest_a"


def test_construct_preferences_dict():
    preferences_dict = _construct_preferences_dict({"guests": ["guest_a", "guest_d"]})
    
    assert preferences_dict == {"guest_a": ["guest_d"], "guest_d": ["guest_a"]}
