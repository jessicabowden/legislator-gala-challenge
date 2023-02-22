import argparse
import json
from collections import defaultdict
from enum import Enum


PreferenceEnum = Enum('PreferenceEnum', ['avoid', 'pair'])


def _construct_preferences_dict(planner_preference: dict[str, list[str]]) -> dict[str, list]:
    preferences = {}

    for i, guest in enumerate(planner_preference["guests"]):
        excluded_list = planner_preference["guests"][:i] + planner_preference["guests"][i+1:]
        preferences[guest] = excluded_list

    return preferences


def main(num_tables: int, guest_list: list[str], planner_preferences: list[dict]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for i in range(num_tables):
        result[f'table_{i+1}'] = []

    avoid_preferences = defaultdict(list)
    pair_preferences = defaultdict(list)

    for planner_preference in planner_preferences:
        if planner_preference["preference"] == PreferenceEnum.avoid.name:
            avoid_preferences.update(_construct_preferences_dict(planner_preference))
        if planner_preference["preference"] == PreferenceEnum.pair.name:
            pair_preferences.update(_construct_preferences_dict(planner_preference))
    
    while guest_list:
        current_guest = guest_list[-1]
        avoid_prefs = avoid_preferences.get(current_guest, [])
        pair_prefs = pair_preferences.get(current_guest, [])
        checked_tables = 0

        for table, guests in result.items():
            can_add_to_table = True

            # checks if any of the guests at current table can't sit with the current guest in O(1)
            if (bool(set(guests) & set(avoid_prefs))):
                can_add_to_table = False

            # now perform the same check for each of the current guests' preferred seating partners
            for pair in pair_prefs:
                if (bool(set(guests) & set(avoid_preferences.get(pair, [])))):
                    can_add_to_table = False

            if can_add_to_table:
                result[table].append(current_guest)
                guest_list.pop()

                result[table].extend(pair_prefs)

                # update the guest list to no longer include the guests' pair preferences
                updated_list = list(set(guest_list) - set(pair_prefs))
                guest_list = updated_list

                break
            else:
                # if we can't find a table for the user, increment the counter so we don't get stuck
                checked_tables += 1
                if checked_tables >= num_tables:
                    raise Exception(f'Can\'t find a table for guest {current_guest}')

    return result

if __name__ == "__main__":
    # Example:
    # poetry run python src/main.py -n 3 -g guest_a guest_b guest_c -p "[{\"preference\": \"avoid\", \"guests\": [\"guest_a\", \"guest_b\"]}, {\"preference\": \"pair\", \"guests\": [\"guest_c\", \"guest_a\"]}]"

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_tables', type=int)
    parser.add_argument('-g', '--guest_list', nargs='*', type=str)
    parser.add_argument('-p', '--preferences', type=json.loads)
    args = parser.parse_args()

    result = main(args.num_tables, args.guest_list, args.preferences)

    with open('output.json', 'w+') as f:
        json.dump(result, f)

