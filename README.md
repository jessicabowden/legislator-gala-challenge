# Running

This project uses [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) to manage dependencies.

To run the tests:
```
  poetry run pytest tests/test_main.py
```

To run the main function:
```
  poetry run python src/main.py -n 3 -g guest_a guest_b guest_c -p '[{"preference": "avoid", "guests": ["guest_a", "guest_b"]}, {"preference": "pair", "guests": ["guest_c", "guest_a"]}]'
```

# Overview

- The Annual Legislator's Gala is here, it's the one night where members of congress all gather in one ballroom in DC, and discuss the results of the legislative session that had just passed. The event planners are as nervous as they are excited, knowing that they need to boil the seating chart down to a science because if the wrong pair are seated at the same table, tempers will flare. Additionally, some members of congress want to have constructive conversations about how the past year went, so the planners want to create a memorable night by seating them at the same table
- So, you are tapped on the shoulder to build a system where given a list of legislators, a number of tables, and an optional param for preferred/avoided seating from the planner, it produces a seating chart for that night.

# Inputs

- your method will take the following:
    - num_tables: an integer, representing the number of tables at the gala
    - guest_list: an array of strings, representing the entire list of invited guests at the event
    - planner_preferences: an array of dicts with in the following format
        
        ```json
        [
        	{
        		"preference": "avoid",
        		"guests": ["name_1", "name_2"]
        	},
        	{
        		"preference": "pair",
        		"guests": ["name_2", "name_3"]
        	}
        ]
        ```
        
- a few notes about the inputs
    - num_tables will always be a positive integer (≥1)
    - guest_list will contain all the guests that may be mentioned in planner_preferences
    - in planner_preferences, note the following:
        - the planner may choose to have a single politician avoid one or more people, but be paired with another set of people (i.e. names in the "guests" part of the dicts are not unique across the entire param)
        - you may assume that the number of seats per table are flexible if a legislator needs to be moved elsewhere, or for any other reason.
        - in the event where you come across an instance where the planner's preference could not be met, handle it in any way you see fit and leave your reasoning as a comment in the code.

# Outputs

- your algorithm is expected to output a dictionary to a JSON file named "output.json" in the following format:

```json
{
	"table_1": ["name_1", "name_2", "name_3"]
	"table_2": ["name_4", "name_5", "name_6", "name_7"]
}
```

# General & Submission Info

- this will be a two hour exercise that you'll be doing, we will give you 48 hours to complete it.
- You may use any language you'd like, but note that the person reviewing your submission may not work with your language of choice, so ensure that the code is as readable and organized as possible.
- The deliverables of this challenge are going to be a file for your source code, and a test file that runs your source code through different scenarios.
- There are no limits to your testing, add as many tests as you like to make sure that all cases are handled or covered.
- You'll be forking this repository on GitHub, and your submission will be to your own fork.
