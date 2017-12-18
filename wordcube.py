import collections
from collections import OrderedDict
import os
import json
import random
import sys
import time


class Dictionary(object):
    """object with all valid words"""

    def __init__(self, json_path):
        """create a new dictionary object from a JSON"""
        with open(json_path, 'r') as f:
            self.words = json.load(f)

    def lookup_word(self, found_word):
        """check if the word is found in the dictionary"""
        if found_word in self.words.keys():
            return True
        else:
            return False


class Display(object):
    """object holding what will be displayed on the screen"""

    def __init__(self, cells_size, words_size):
        """create a new display object"""
        self.cells = {}
        for x in range(cells_size):
            for y in range(cells_size):
                self.cells[(x, y)] = ' '

        self.words = {}
        for x in range(words_size):
            self.words[x] = Word('')
            self.words[x].points = ''

        self.notification = ''
        self.score = 0
        self.image = ''

    def draw(self):
        """draw text-based graphics on the screen"""
        os.system('cls')
        self.image = """
        ======================================================

              WordCube - Written By Matthew Devaney   

        ======================================================        

                                                Score {}
        -------------------------------
        |  {}  |  {}  |  {}  |  {}  |  {}  |         {} {}   {} {}   {} {}
        -------------------------------         {} {}   {} {}   {} {}
        |  {}  |  {}  |  {}  |  {}  |  {}  |         {} {}   {} {}   {} {}
        -------------------------------         {} {}   {} {}   {} {}
        |  {}  |  {}  |  {}  |  {}  |  {}  |         {} {}   {} {}   {} {}
        -------------------------------         {} {}   {} {}   {} {}
        |  {}  |  {}  |  {}  |  {}  |  {}  |         {} {}   {} {}   {} {}
        -------------------------------         {} {}   {} {}   {} {}
        |  {}  |  {}  |  {}  |  {}  |  {}  |         {} {}   {} {}   {} {}
        -------------------------------         {} {}   {} {}   {} {}

        {}
        """.format(
            self.score,
            self.cells[(0, 0)], self.cells[(0, 1)], self.cells[(0, 2)], self.cells[(0, 3)], self.cells[(0, 4)],
            self.words[0].name, self.words[0].points, self.words[10].name, self.words[10].points,
            self.words[20].name, self.words[20].points, self.words[1].name, self.words[1].points,
            self.words[11].name, self.words[11].points, self.words[21].name, self.words[21].points,
            self.cells[(1, 0)], self.cells[(1, 1)], self.cells[(1, 2)], self.cells[(1, 3)], self.cells[(1, 4)],
            self.words[2].name, self.words[2].points, self.words[12].name, self.words[12].points,
            self.words[22].name, self.words[22].points, self.words[3].name, self.words[3].points,
            self.words[13].name, self.words[13].points, self.words[23].name, self.words[23].points,
            self.cells[(2, 0)], self.cells[(2, 1)], self.cells[(2, 2)], self.cells[(2, 3)], self.cells[(2, 4)],
            self.words[4].name, self.words[4].points, self.words[14].name, self.words[14].points,
            self.words[24].name, self.words[24].points, self.words[5].name, self.words[5].points,
            self.words[15].name, self.words[15].points, self.words[25].name, self.words[25].points,
            self.cells[(3, 0)], self.cells[(3, 1)], self.cells[(3, 2)], self.cells[(3, 3)], self.cells[(3, 4)],
            self.words[6].name, self.words[6].points, self.words[16].name, self.words[16].points,
            self.words[26].name, self.words[26].points, self.words[7].name, self.words[7].points,
            self.words[17].name, self.words[17].points, self.words[27].name, self.words[27].points,
            self.cells[(4, 0)], self.cells[(4, 1)], self.cells[(4, 2)], self.cells[(4, 3)], self.cells[(4, 4)],
            self.words[8].name, self.words[8].points, self.words[18].name, self.words[18].points,
            self.words[28].name, self.words[28].points, self.words[9].name, self.words[9].points,
            self.words[19].name, self.words[19].points, self.words[29].name, self.words[29].points,
            self.notification)

        print(self.image)

    def reset(self, cells_size, words_size):
        """reset the display object for the next game"""

        # reset cells holding letters to blank
        for x in range(cells_size):
            for y in range(cells_size):
                self.cells[(x, y)] = ' '

        # reset the list of words found to blank
        for x in range(words_size):
            self.words[x] = Word('')
            self.words[x].points = ''

        # clear all other variables
        self.notification = ''
        self.score = 0
        self.image = ''


class Grid(object):
    """object holding the location of letters"""

    def __init__(self, grid_size):
        """create a new grid object"""
        self.cells = {}
        self.grid_size = grid_size

    def shake(self, cubes_list):
        """
        Randomly re-order the list of cubes, randomly select a char from each string in the list and
        assign each char to the next open cell in the gride
        """
        # random.seed(15)
        # change the order cubes will be placed on the grid
        random.shuffle(cubes_list)
        # place all cubes on the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.cells[(x, y)] = random.sample(cubes_list.pop(0), 1)[0]

    def find_all_words(self, dictionary_object):
        """find all possible words in the grid and output to a txt file"""

        # create an empty ordered dictionary
        od = collections.OrderedDict()

        # load the ordered dictionary with valid words from the game dictionary that are found in the grid
        for word in dictionary_object.words.keys():
            if len(word) >= 3 and self.find_word(str.upper(word)):
                w = Word(word)
                w.score()
                od[w.name] = w.points

        # sort the ordered dictionary in descending order by points
        od = OrderedDict(sorted(od.items(), key=lambda t: t[1], reverse=True))

        return od

    def find_word(self, check_word):
        """Check if the the player's word is found on the grid"""

        # create an empty list to track which cells were used in the word to prevent duplicates
        cells_used = []

        # check each cell co-ordinate within the grid for the 1st letter of the word
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                #  uncomment to debug print('{}: ({}, {})'.format(check_word[0], x, y))
                if check_word[0] in self.cells[(x, y)]:
                    # add cell co-ordinate to list of used cells
                    cells_used.append((x, y))
                    # look for the next letter in the chain
                    if self.walk(check_word[1:], cells_used, x, y):
                        return True
        return False

    def walk(self, check_word, cells_used, x_pos, y_pos):
        """Check if all letters in the word are in a chain of touching cells in the grid"""

        # look at all cells vertically, horizontally and diagonally adjacent for the next letter in the chain
        for x in range(-1, 2):
            for y in range(-1, 2):
                # must be a valid grid position, cannot a previously used cell and do not check the current cell
                if (x_pos + x, y + y_pos) in list(self.cells.keys()) and \
                        (x_pos + x, y + y_pos) not in cells_used and \
                        (x, y) is not (0, 0):
                    if check_word[0] in self.cells[(x_pos + x, y + y_pos)]:
                        # stop searching when the last letter in the word is successfully chained
                        # uncomment to debug print('{}: ({}, {})'.format(check_word[0], x_pos + x, y + y_pos))
                        if len(check_word) == 1:
                            return True
                        else:
                            # add cell co-ordinate to list of used cells
                            cells_used.append((x_pos + x, y_pos + y))
                            # recursively check each letter in the chain
                            if self.walk(check_word[1:], cells_used, x_pos + x, y + y_pos):
                                return True
        # stop searching when no adjacent letters can be found to chain
        return False


class Word(object):
    """object holding words found by the player and points scored for the word"""

    def __init__(self, new_word):
        """create a new word object"""
        self.name = new_word
        self.points = 0

    def score(self):
        """determine the score of a word object"""
        if len(self.name) == 3:
            self.points = 1
        elif len(self.name) == 4:
            self.points = 2
        elif len(self.name) == 5:
            self.points = 3
        elif len(self.name) == 6:
            self.points = 5
        elif len(self.name) == 7:
            self.points = 10
        elif len(self.name) >= 8:
            self.points = 10 + (5 * (len(self.name) - 7))


def export_solution(puzzle_string, solution_od, found_words):
    """output a txt file showing the puzzle and solution to the program path"""
    with open('solution.txt', 'w') as f:
        f.write('{}\n\nSolution:\n'.format(puzzle_string))
        for key, value in solution_od.items():
            f.write('{}: {}'.format(key, value))
            if key in found_words:
                f.write(' <')
            f.write('\n')


def main():
    """main program loop"""

    # game paramters
    game_length = 10
    grid_size = 5
    min_word_length = 3
    word_list_size = 30

    # create a blank list to store words found
    found_words = []

    # create game objects
    d = Dictionary('words_dictionary.json')
    ds = Display(grid_size, word_list_size)
    g = Grid(grid_size)

    while True:

        # list of letters on cubes
        cubes = ['AAAFRS', 'AAEEEE', 'AAFIRS', 'ADENNN', 'AEEEEM', 'AEEGMU', 'AEGMNN', 'AFIRSY', 'BJKQXZ', 'CCNSTW',
                 'CEIILT', 'CEILPT', 'CEIPST', 'DHHNOT', 'DHHLOR', 'DHLNOR', 'DDLNOR', 'EIIITT', 'EMOTTT', 'ENSSSU',
                 'FIPRSY', 'GORRVW', 'HIPRRY', 'NOOTUW', 'OOOTTU']

        # randomly place letters from cubes on the grid
        g.shake(cubes)
        ds.cells = g.cells

        # determine what time the game should end at
        end_game_time = time.time() + game_length

        # player finds as many words as possible until time runs out
        while time.time() < end_game_time:
            ds.draw()
            try_word = input('\nEnter Word: ')
            # check word length
            if len(try_word) < min_word_length:
                ds.notification = '\'{}\' is too short. Must be at least 3 letters long.'.format(try_word)
            # check for duplicates
            elif try_word in found_words:
                ds.notification = '\'{}\' was already found. Cannot guess the same word twice'.format(try_word)
            # check for word in the cube
            elif not g.find_word(str.upper(try_word)):
                ds.notification = '\'{}\' was not found in the cube'.format(try_word)
            # check for word in the dictionary
            elif not d.lookup_word(str.lower(try_word)):
                ds.notification = '\'{}\' was not found in the game dictionary'.format(try_word)
            # add words that meet all conditions to the list of found words and calculate a score
            else:
                found_words.append(try_word)
                w = Word(try_word)
                w.score()
                ds.notification = '{} found! scored {} points'.format(w.name, w.points)
                ds.words[len(found_words)-1] = w
                ds.score += w.points

        # notify the player time has run out and show the final result
        ds.notification = ds.notification + '\n\n\nTime\'s up! Thank you for playing WordCube.'
        ds.draw()

        # export the puzzle and solution to a txt file in the program directory if desired by the player
        while True:

            menu_selection = input('Would you like to export the puzzle\'s solution? (Y)es (N)o ')

            if str.upper(menu_selection) == 'Y':
                solution_ordered_dict = g.find_all_words(d)
                export_solution(ds.image, solution_ordered_dict, found_words)
                break
            elif str.upper(menu_selection) == 'N':
                break
            else:
                print('\nInvalid input. Must answer \'Y\' or \'N\'\n')

        # ask the player if they would like to play another game
        while True:

            menu_selection = input('\nWould you like to play another game? (Y)es (N)o ')

            if str.upper(menu_selection) == 'Y':
                break
            elif str.upper(menu_selection) == 'N':
                sys.exit(0)
            else:
                print('\nInvalid input. Must answer \'Y\' or \'N\'\n')

        # reset game variables
        ds.reset(grid_size, word_list_size)
        found_words = []


main()


"""
To Do List:
* Figure out why I can't just import from collections import OrderedDict
* Learn about threading so game stops immediately when timer is done (StackOverflow)
* Find a better dictionary: Scrabble dictionary, Webster's dictionary, Oxford dictionary
* Search faster from the JSON dictionary
"""
