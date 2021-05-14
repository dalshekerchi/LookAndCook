"""CSC111 Final Project, Data Reading

Description
===============================
This module reads the raw data from the csv file and converts it into a usable format.
===============================

This file is provided solely for the personal and private use of TA's and professors
teaching CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Dana Alshekerchi, Nehchal Kalsi, Kathy Lee, Audrey Yoshino.
"""

from __future__ import annotations
from typing import Dict, Tuple, List
import csv

RECIPES_FILE = "data/clean_recipes.csv"
REVIEWS_FILE = "data/reviews.csv"

# Key measurement words to remove from ingredients
WORDS_TO_REMOVE = {'packages', 'cups', 'cup', 'tablespoons', 'tablespoon', 'teaspoon',
                   'teaspoons', 'packets', 'pounds', 'pound', 'inch', 'ounces', 'drops',
                   'dashes', 'jar', 'dash', 'envelope', 'container', 'package', 'crushed',
                   'ounce', 'cans', 'can', 'loaves', 'bottle', 'packet', 'tube', 'bottle',
                   'sheets', 'recipe', 'peeled and chopped', 'bunch'}

# Key words of ingredients to remove
REMOVE_INGREDIENTS1 = {'marinate', 'low fat', 'breakfast', 'england', ' 2', 'fry', 'side',
                       'low sodium', 'Dry Mix Ingredients', 'kosher for passover', '2',
                       'mexico', 'raw', 'drained and mashed', 'without shells', 'bake',
                       'peeled and segmented', 'peeled and shredded', 'pan drippings',
                       'dessert', 'cubed', '(optional)', 'drained and chopped',
                       'Glaze', 'rinsed and dried', 'divided', 'thick circles',
                       'washed and cubed', 'mashed', 'fat free', 'Southern Comfort',
                       'peeled and julienned', 'lunch', 'chopped', 'stemmed and rinsed',
                       's thick', 'y', 'chopped', 'drained and finely chopped', 'top round',
                       'julienned', 'cleaned', 'boil', 'calories', 'party', 'gluten', 'Filling',
                       't', 'or less Grenadine (', 'ground', 'casings removed', 'chili', 'snow',
                       'chill'}
REMOVE_INGREDIENTS2 = {'rinsed and torn', 'and dried', 'rating',
                       'peeled and cubed', 'split', 'for topping', 'warmed', '\x99'}


def read_recipes(file: str) -> Dict[str, list]:
    """Read the given file and return a dictionary with recipe id mapping to
    other attributes of the recipe stored in a list.

    Based upon the clean_recipes.csv file.
    """
    recipe_dict = {}

    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)

        for row in reader:
            dict_val = []   # list containing recipe attributes
            index = 0

            for inner_row in row[:9]:
                if index == 0:
                    if "''" in inner_row:
                        inner_row = inner_row.replace("''", "'").strip("'")
                        dict_val.append(inner_row.strip())
                    else:
                        dict_val.append(inner_row.strip())

                elif index == 7:  # ingredients
                    ingredients = inner_row.split(',')
                    cleaned_ing = [x.strip() for x in ingredients]
                    dict_val.append(set(cleaned_ing))

                elif index == 8:    # directions
                    sntnc = row[8].strip("'")
                    if not sntnc[-2:] == "**":
                        sntnc = sntnc + "**"    # to split every bullet point
                    directions = list(sntnc.split('**'))[:-1]

                    for x in directions:
                        if "''" in x:
                            directions[directions.index(x)] = x.replace("''", "'")

                    dict_val.append(directions)

                else:
                    dict_val.append(inner_row.strip())

                index += 1
                recipe_dict[row[9].strip()] = dict_val  # remove extra space before assigning

    return recipe_dict


def get_ing_amounts(file: str) -> Dict[str, list]:
    """Read the given file and return a dictionary with recipe id mapping to
    the ingredients and their amounts.

    Based upon the recipes.csv file.
    """
    recipe_dict = {}

    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)

        for row in reader:
            dict_val = []  # list containing ingredients
            index = 0

            for _ in row[:9]:
                if index == 7:  # ingredients
                    all_ings = row[8].strip("'")
                    if not all_ings[-2:] == "**":
                        all_ings = all_ings + "**"  # to split every bullet point
                    dict_val.extend(list(all_ings.split('**'))[:-1])
                    for x in dict_val:
                        if "''" in x:
                            dict_val[dict_val.index(x)] = x.replace("''", "'")

                    recipe_dict[row[1].strip()] = dict_val  # remove extra space before assigning

                index += 1

    return recipe_dict


def get_ingredients(data: Dict[str, list]) -> set:
    """Return a set of ingredients given data complying to the
    format the function 'read_recipes' returns data in."""
    ing = set()

    for i in data:
        ing.update(data[i][7])

    return ing


def get_review_scores(file: csv) -> Dict[str, float]:
    """Return a dictionary of recipe ids mapping to respective user ratings obtained
    from the given file.

    Based upon the clean_recipes.csv file.
    """
    unclean_reviews_dict = {}   # recipe_id: [score, length]
    # 'length' for counting occurrences and taking average

    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)

        for row in reader:
            row = row[0].split(",")
            if row[0] in unclean_reviews_dict:
                unclean_reviews_dict[row[0]][0] += int(float(row[2]))
                unclean_reviews_dict[row[0]][1] += 1
            else:
                unclean_reviews_dict[row[0]] = [int(float(row[2])), 1]

    reviews_dict = {x: round(unclean_reviews_dict[x][0] / unclean_reviews_dict[x][1], 1)
                    for x in unclean_reviews_dict}

    return reviews_dict


def get_reviews(file: csv) -> Dict[str, list]:
    """Return a dictionary of recipe ids mapping to respective user reviews obtained
    from the given file.

    Based on reviews.csv file.
    """
    reviews_dict = {}  # recipe_id: [reviews]

    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader)

        for row in reader:
            if len(row) == 4 and '...' not in row[3]:
                if row[0] in reviews_dict:
                    reviews_dict[row[0]].append('"' + row[3].replace("''", "'").strip("'") + '"')
                else:
                    reviews_dict[row[0]] = ['"' + row[3].replace("''", "'").strip("'") + '"']

    return reviews_dict


def clean_ingredients(data: Dict[str, list]) -> None:
    """Mutate the provided dictionary by cleaning the ingredients (removing measurements and
    strings that aren't ingredients).

    Additionally, ensure the names of all the recipes don't have unnecessary quotations
    surrounding them.
    """
    for recipe in data:
        ingredients = data[recipe][7]
        ingredients_to_remove, ingredients_to_add = clean_ingredient_set(ingredients)

        for ingredient in ingredients_to_remove:
            # Remove all the unnecessary ingredients: did not mutate in the for loop because of
            # possible errors
            ingredients.remove(ingredient)

        for ingredient in ingredients_to_add:
            if ingredient is not None and ingredient != '':
                final_ingredient = ingredient

                if final_ingredient[0] == ' ':
                    # Ensure the ingredient we are adding does not have an unnecessary space at the
                    # beginning
                    final_ingredient = ingredient[1:]

                if final_ingredient not in {'y', 'to tast', 't'}:
                    ingredients.add(final_ingredient)

        capitalized = set()

        # Capitalize all ingredients in the ingredients corresponding to a given recipe
        for ingredient in ingredients:
            capitalize = ingredient.capitalize()
            capitalized.add(capitalize)

        data[recipe][7] = capitalized

        # Ensure the provided recipe name doesn't have unnecessary quotations around it
        name = data[recipe][0]

        if name[0] == "'":
            data[recipe][0] = name[1: -1]


def clean_ingredient_set(ingredients: set) -> Tuple:
    """Helper function for clean_ingredients.

    Return a tuple where the first element is a set of unclean ingredients to remove from the
    original set and the second element is a set of cleaned ingredients to add to the original set.
    """
    ingredients_to_remove = set()
    ingredients_to_add = set()

    for ingredient in ingredients:
        new_ingredient = None
        remove = check_remove(ingredient)

        if ingredient == '':
            # If the ingredient is an empty string, remove it.
            ingredients_to_remove.add(ingredient)

        elif ingredient[-1] == ':' or ingredient.isupper() or ingredient in REMOVE_INGREDIENTS1:
            # If a label has incorrectly been classified as an ingredient or the entire
            # string is not an ingredient, remove it.
            ingredients_to_remove.add(ingredient)

        elif ')' in ingredient:
            # Remove parenthesis if in ingredient
            beginning = ingredient.index(')')
            new_ingredient = ingredient[beginning + 2:]

        elif ingredient[0] == ' ':
            # If the ingredient has a space at the beginning of it's string, remove the space
            new_ingredient = ingredient[1:]
            ingredients_to_remove.add(ingredient)

        elif any(character.isdigit() for character in ingredient):
            # If there is a number indicating the quantity of an ingredient, remove it (and the
            # space following it).
            numbers = [character for character in ingredient if character.isdigit()]
            number_index = ingredient.index(numbers[-1])

            new_ingredient = ingredient[number_index + 2:]
            ingredients_to_remove.add(ingredient)

        if remove[1]:
            ingredients_to_remove.add(ingredient)
            new_ingredient = None

        # Finally, check the ingredient doesn't contain any measurement key words.
        elif ingredient != 'canola oil' and remove[0][0]:
            word = remove[0][1]
            beginning = ingredient.index(word)
            word_end_index = beginning + len(word)
            new_ingredient = ingredient[word_end_index + 1:]
            ingredients_to_remove.add(ingredient)

        if new_ingredient is not None:
            if 'to taste' in new_ingredient:
                # If the substring 'to taste' is in the ingredient, remove the 'to taste'
                index = new_ingredient.index('to taste')
                new_ingredient = new_ingredient[:index - 1]
        else:
            if 'to taste' in ingredient:
                # If the substring 'to taste' is in the ingredient, remove the 'to taste'
                index = ingredient.index('to taste')
                new_ingredient = ingredient[:index - 1]
                ingredients_to_remove.add(ingredient)

        ingredients_to_add.add(new_ingredient)

    return (ingredients_to_remove, ingredients_to_add)


def check_remove(ingredient: str) -> \
        List[List, bool]:
    """Helper function for clean_ingredient_set.

    Returns a list of booleans. The first nested list indicates whether there is a
    'measurement word' in the provided ingredient and (if so) contains the measurement word
    at the first index.
    The second element is a boolean that indicates whether there is a word from REMOVE_INGREDIENTS2
    present in the provided ingredient.
    """
    remove = [[False], False]

    for word in WORDS_TO_REMOVE:
        # Remove measurements using key words
        if word in ingredient:
            remove[0][0] = True
            remove[0].append(word)

    for word in REMOVE_INGREDIENTS2:
        # Remove entire ingredients if they aren't food items
        if word in ingredient:
            remove[1] = True

    return remove
