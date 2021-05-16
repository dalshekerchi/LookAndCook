"""
Description
===============================

"""
from typing import Dict, List
import data_type


def ingredients_sort(data: Dict[str, list], user_ingredients: list, graph: data_type.Graph) -> List[
    tuple]:
    """Return a list of tuples containing the recipe ids and other attributes of recipes
     from data sorted in decreasing order of number of ingredients used from user_ingrdnts.

     NOTE: The recipes returned may contain ingredients extra than user_ingredients.

     Step 1 in the recipe search algorithm.
    """
    recipe_occurrence = {}
    sorted_recipes = []

    for item in user_ingredients:
        neighbours = graph.get_neighbours(item.strip())  # neighbours = set of recipe ids

        assert all([x in graph.get_all_vertices('recipe') for x in neighbours])

        for recipe in neighbours:
            if recipe in recipe_occurrence:
                recipe_occurrence[recipe] += 1
            else:
                recipe_occurrence[recipe] = 1

    sorted_recipe_ids = sorted(recipe_occurrence.items(), key=lambda x: x[1], reverse=True)

    for item in sorted_recipe_ids:
        sorted_recipes.append((item[0], data[item[0]]))
        # use list instead of dictionary to maintain sort order

    return sorted_recipes[:100]


def time_bound(data: List[tuple], max_mins: int) -> List[tuple]:
    """Return a list of recipes from data which have a total cooking time less than or equal to
    max_mins.

    Step 2 in the recipe search algorithm. Uses output from the function ingredients_sort as input.
    """
    if max_mins == 0:
        return data

    else:
        sorted_recipes = []

        for item in data:
            total_time = item[1][6]

            if total_time != "X":
                total_time = total_time.replace(" ", "")  # remove the whitespace
                day, hour, minute = _split_time(total_time)

                minutes = (24 * 60 * int(day)) + (60 * int(hour)) + int(minute)

                if minutes <= max_mins:
                    sorted_recipes.append(item)

        return sorted_recipes


def time_sort(data: List[tuple], dec_ord: bool = False) -> List[tuple]:
    """Return a list of recipes from data sorted in increasing or decreasing order
    of the total time of the recipes depending on dec_ord. The total time of the recipes
    returned is less than the maximum minutes max_mins.

    If total time of a recipe is not available, do not include it in the return value.

    Step 3 in the recipe search algorithm. Uses output from the function time_bound as input.
    """
    times = {}
    sorted_recipes = []

    for item in data:  # item = (recipe id, other attributes)
        total_time = item[1][6]

        if total_time != "X":
            total_time = total_time.replace(" ", "")  # remove the whitespace
            day, hour, minute = _split_time(total_time)

            minutes = (24 * 60 * int(day)) + (60 * int(hour)) + int(minute)
            times[item[0]] = (minutes, item[1])  # convert time to mins

    # sort by value
    if dec_ord:
        sorted_times = sorted(times.items(), key=lambda x: x[1][0], reverse=True)
    else:
        sorted_times = sorted(times.items(), key=lambda x: x[1][0])

    for item in sorted_times:
        sorted_recipes.append((item[0], item[1][1]))
        # use list instead of dictionary to maintain sort order

    return sorted_recipes


def _split_time(time: str) -> list[str]:
    """Return the given time in [day, hour, min] format."""
    assert time != 'X'
    time_lst = []

    if 'd' in time:  # manage day
        time_lst = time.split("d")
    else:
        time_lst.extend(['0', time])

    assert len(time_lst) == 2

    if 'h' in time_lst[1]:  # manage hour
        mixed_time = time_lst[1]
        time_lst.extend(time_lst[1].split("h"))
        time_lst.remove(mixed_time)
    else:
        time_lst.append(time_lst[1])
        time_lst[1] = '0'
        # pass

    assert len(time_lst) == 3

    if 'm' in time_lst[2]:  # manage min
        time_lst[2] = time_lst[2].strip("m")
    else:
        time_lst[2] = "0"

    return time_lst
