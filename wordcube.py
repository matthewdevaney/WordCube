import json
import random
import sys
import time

class Dictionary(object):

    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            self.words = json.load(f)

    def lookup_word(self, found_word):
        """check if the word is found in the dictionary"""

        # can I write an algorithim to search faster?
        if found_word in self.words.keys():
            return True
        else:
            return False

    def make_words(self, letters_list):
        pass


class Grid(object):

    def __init__(self):
        self.cells = {}
        self.gridsize = 5

    def display(self):
        print("""
        -------------------------------
        |  {}  |  {}  |  {}  |  {}  |  {}  |
        -------------------------------
        |  {}  |  {}  |  {}  |  {}  |  {}  |
        -------------------------------
        |  {}  |  {}  |  {}  |  {}  |  {}  |
        -------------------------------
        |  {}  |  {}  |  {}  |  {}  |  {}  |
        -------------------------------
        |  {}  |  {}  |  {}  |  {}  |  {}  |
        -------------------------------
        """.format(
            self.cells[(0, 0)], self.cells[(0, 1)], self.cells[(0, 2)], self.cells[(0, 3)], self.cells[(0, 4)],
            self.cells[(1, 0)], self.cells[(1, 1)], self.cells[(1, 2)], self.cells[(1, 3)], self.cells[(1, 4)],
            self.cells[(2, 0)], self.cells[(2, 1)], self.cells[(2, 2)], self.cells[(2, 3)], self.cells[(2, 4)],
            self.cells[(3, 0)], self.cells[(3, 1)], self.cells[(3, 2)], self.cells[(3, 3)], self.cells[(3, 4)],
            self.cells[(4, 0)], self.cells[(4, 1)], self.cells[(4, 2)], self.cells[(4, 3)], self.cells[(4, 4)]))

    def shake(self, cubes_list):
        """
        Randomly re-order the list of cubes, randomly select a char from each string in the list and
        assign each char to the next open cell in the gride
        """
        random.seed(10)
        # change the order cubes will be placed on the grid
        random.shuffle(cubes_list)
        # place all cubes on the grid
        for y in range(self.gridsize):
            for x in range(self.gridsize):
                self.cells[(x, y)] = random.sample(cubes_list.pop(0), 1)[0]

    def find_word(self, check_word):
        """Check if the the player's word is found on the grid"""

        # create an empty list to track which cells were used in the word to prevent duplicates
        cells_used = []

        # check each cell co-ordinate within the grid for the 1st letter of the word
        for x in range(self.gridsize):
            for y in range(self.gridsize):
                # print('{}: ({}, {})'.format(check_word[0], x, y))
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
                        # print('{}: ({}, {})'.format(check_word[0], x_pos + x, y + y_pos))
                        if len(check_word) == 1:
                            return True
                        else:
                            # add cell co-ordinate to list of used cells
                            cells_used.append((x_pos + x, y_pos + y))
                            # recursively check each letter in the chain
                            return self.walk(check_word[1:], cells_used, x_pos + x, y + y_pos)
        print(False)
        # stop searching when no adjacent letters can be found to chain
        return False


class Player(object):

    def __init__(self, player_name):
        self.name = player_name
        self.score = 0


class Word(object):

    def __init__(self, new_word, player_object):
        self.name = new_word
        self.player = player_object
        self.points = 0

    def word_score(self):
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


# create game objects
p = Player('Matthew')
d = Dictionary('words_dictionary.json')
g = Grid()

# game paramters
min_word_length = 3
game_length = 30

# create a blank list to store words found
found_words = []

# display game title and author
print('\n======================================================\n'
      '[][]   WordCube - Written By: Matthew Devaney   [][]\n'
      '======================================================\n'
      ''
      'Find as many words as possible in 30 seconds')

cubes = ['AAAFRS', 'AAEEEE', 'AAFIRS', 'ADENNN', 'AEEEEM', 'AEEGMU', 'AEGMNN', 'AFIRSY', 'BJKQXZ', 'CCNSTW',
              'CEIILT', 'CEILPT', 'CEIPST', 'DHHNOT', 'DHHLOR', 'DHLNOR', 'DDLNOR', 'EIIITT', 'EMOTTT', 'ENSSSU',
              'FIPRSY', 'GORRVW', 'HIPRRY', 'NOOTUW', 'OOOTTU']

g.shake(cubes)

end_time = time.time() + game_length


while time.time() < end_time:
    g.display()
    try_word = input('\nEnter Word: ')
    if len(try_word) < min_word_length:
        print('\n Word is too short. Must be at least 3 letters long.')
    elif try_word in found_words:
        print('\n Word was already found. Cannot guess the same word twice')
    elif not g.find_word(str.upper(try_word)):
        print('\n Word was not found in the cube')
    elif not d.lookup_word(str.lower(try_word)):
        print('\n Word was not found in the game dictionary')
    else:
        w = Word(try_word, p)
        print('Word found! {} scored {} points'.format(w.player.name, w.word_score()))
        found_words.append(w)

for n in range(len(found_words)):
    p.score += found_words[n].points

print('\nTime\'s up! {} scored {} points.'.format(p.name, p.score))
print('\nFound words:')

for n in range(len(found_words)):
    print('{}: {}'.format(found_words[n].name, found_words[n].points))

sys.exit(0)

"""
To Do List:
* Learn about threading so game stops immediately when timer is done
* Show the complete list of words not found by the player
"""


"""
4x4 grid cubes list
cubes_list = ['AACIOT', 'AHMORS', 'EGKLUY', 'ABILTY', 'ACDEMP', 'EGINTV', 'GILRUW', 'ELPSTU', 'DENOSW', 'ACELRS',
                'ABJMOQ', 'EEFHIY', 'EHINPS', 'DKNOTU', 'ADENVZ', 'BIFORX']
"""
