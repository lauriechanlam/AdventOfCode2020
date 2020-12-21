import utils
import re
from collections import *
import copy
import itertools


def read_input(filename):
    return utils.read(filename, 'string')


def parse_line(line):
    parts = line.split(' (contains ')
    ingredients = set(parts[0].split(' '))
    allergens = set(parts[1][:-1].split(', '))
    return ingredients, allergens



class Stack:
    def __init__(self, foods, debug=False):
        self.stack = []  # allergen: ingredient
        self.foods = foods
        self.allergens = set().union(*itertools.chain(food[1] for food in foods))
        self.ingredients = set().union(*itertools.chain(food[0] for food in foods))
        self.debug = debug

    def contains(self, allergen):
        return allergen in [s[0] for s in self.stack]

    def can_add(self, allergen, ingredient):
        # return allergen not in [s[0] for s in self.stack] and ingredient not in [s[1] for s in self.stack]
        contains_all = [food for food in self.foods if allergen in food[1]]
        contains_ing = [food for food in self.foods if ingredient in food[0]]

        if not all(al in contains_ing for al in contains_all):
            return False
        return True

    def push(self, allergen, ingredient):
        self.stack.append((allergen, ingredient))
        if self.debug:
            print(self.stack)

    def pop(self):
        self.stack.pop()
        if self.debug:
            print(self.stack)

    def is_full(self):
        return len(self.stack) == len(self.allergens)

    def fill(self):
        for allergen in self.allergens:
            if allergen in [s[0] for s in self.stack]:
                continue
            for ingredient in self.ingredients:
                if ingredient in [s[1] for s in self.stack]:
                    continue
                if self.can_add(allergen, ingredient):
                    self.push(allergen, ingredient)
                    self.fill()
                    if self.is_full():
                        return self
                    self.pop()

    def ingredients_with_no_allergens(self):
        return [ingredient for ingredient in self.ingredients if ingredient not in [s[1] for s in self.stack]]

    def count_ing_with_no_allergens(self):
        n = 0
        ingredients = self.ingredients_with_no_allergens()
        for food in self.foods:
            ing_list = food[0]
            for ing in ing_list:
                if ing in ingredients:
                    n += 1
        return n

    # def __repr__(self):
    #     return '\n'.join(['Stack ({})'.format(self.next)] + [
    #         ' '.join(['({} {} {})'.format(tile['id'], tile['rotation'], tile['flip'])
    #                   if isinstance(tile, dict) else '(XXXX X XXXX)' for tile in row])
    #         for row in self.stack])



class Part2(utils.Part):
    WRONG = [109]

    def __init__(self):
        super().__init__('mxmxvkd,sqjhc,fvjkl')

    def run(self, input, is_test):
        foods = [parse_line(line) for line in input.splitlines()]

        stack = Stack(foods)
        stack.fill()
        s = stack.stack
        t = sorted(s, key=lambda x: x[0])
        return ','.join([i[1] for i in t])



class Part1(utils.Part):
    WRONG = [109]

    def __init__(self):
        super().__init__(5)

    def run(self, input, is_test):
        foods = [parse_line(line) for line in input.splitlines()]

        stack = Stack(foods)
        stack.fill()
        print(stack.ingredients_with_no_allergens())
        print(stack.count_ing_with_no_allergens())
        return stack.count_ing_with_no_allergens()
        s = stack.stack



        s = {ing: allergen for (allergen, ing) in s}

        n = 0
        for food in foods:
            ing = food[0]
            n += sum(i in s for i in ing)
        return n if n not in Part1.WRONG else None

        allergens = set().union(*itertools.chain(food[1] for food in foods))
        ingredients = set().union(*itertools.chain(food[0] for food in foods))

        ing_per_allergen = {}
        for allergen in allergens:
            foods_containing_allergen = [food[0] for food in foods if allergen in food[1]]
            ingredients = set().union(foods_containing_allergen[0])
            for ing in foods_containing_allergen:
                ingredients = ingredients.intersection(ing)
            if len(ingredients) == 1:
                ing_per_allergen[allergen] = ingredients.pop()




        ing_per_allergen = defaultdict(set)
        for food in foods:
            ingredients = food[0]
            allergens = food[1]
            for allergen in allergens:
                ing_per_allergen[allergen] = ing_per_allergen[allergen].union(ingredients)
        print(ing_per_allergen)


