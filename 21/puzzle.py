import utils
import functools
from collections import defaultdict


def parse_line(line):
    parts = line.split(' (contains ')
    ingredients = set(parts[0].split(' '))
    allergens = set(parts[1][:-1].split(', '))
    return ingredients, allergens


def read_input(filename):
    text = utils.read(filename, 'string')
    return [parse_line(line) for line in text.splitlines()]


class Stack:
    def __init__(self, foods):
        self.stack = []  # (allergen, ingredient)
        self.foods = foods

        self.allergens = defaultdict(set)    # { allergen:   set(food_indices) }
        self.ingredients = defaultdict(set)  # { ingredient: set(food_indices) }

        def add_food(index):
            def add(dic, val):
                dic[val].add(index)
                return dic
            return add

        for food_index, (ingredients, allergens) in enumerate(foods):
            self.allergens = functools.reduce(add_food(food_index), allergens, self.allergens)
            self.ingredients = functools.reduce(add_food(food_index), ingredients, self.ingredients)

    def can_add(self, allergen, ingredient):
        return self.allergens[allergen].issubset(self.ingredients[ingredient])

    def push(self, allergen, ingredient):
        self.stack.append((allergen, ingredient))

    def pop(self):
        self.stack.pop()

    def is_full(self):
        return len(self.stack) == len(self.allergens)

    def fill(self):
        for allergen in self.allergens:
            if allergen in [allergen for allergen, ingredient in self.stack]:
                continue
            for ingredient in self.ingredients:
                if ingredient in [ingredient for allergen, ingredient in self.stack]:
                    continue
                if self.can_add(allergen, ingredient):
                    self.push(allergen, ingredient)
                    self.fill()
                    if self.is_full():
                        return self
                    self.pop()

    def count_safe_ingredients(self):
        dangerous_ingredients = [ingredient for allergen, ingredient in self.stack]
        safe_ingredients = set(self.ingredients.keys()).difference(dangerous_ingredients)
        return sum(len(safe_ingredients.intersection(ingredients)) for ingredients, allergens in self.foods)

    def list_dangerous_ingredients(self):
        sorted_list = sorted(self.stack, key=lambda x: x[0])
        return ','.join([ingredient for allergen, ingredient in sorted_list])


class Part1(utils.Part):

    def __init__(self):
        super().__init__(5)

    def run(self, foods, is_test):
        stack = Stack(foods).fill()
        return stack.count_safe_ingredients()


class Part2(utils.Part):

    def __init__(self):
        super().__init__('mxmxvkd,sqjhc,fvjkl')

    def run(self, foods, is_test):
        allergen_ingredient_list = Stack(foods).fill().stack
        sorted_list = sorted(allergen_ingredient_list, key=lambda x: x[0])
        return ','.join([ingredient for allergen, ingredient in sorted_list])