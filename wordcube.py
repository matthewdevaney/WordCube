import random
import time

# random.shuffle


class Grid(object):

    def __init__(self):
        self.letters = {}

    def display(self):
        print("""
        -----------------------------------------
        |  {}  |  {}  |  {}  |  {}  |
        -----------------------------------------
        |  {}  |  {}  |  {}  |  {}  |
        -----------------------------------------
        |  {}  |  {}  |  {}  |  {}  |
        -----------------------------------------
        |  {}  |  {}  |  {}  |  {}  |
        -----------------------------------------
        """.format(self.letters[(0, 0)], self.letters[(0, 1)], self.letters[(0, 2)], self.letters[(0, 3)],
                   self.letters[(1, 0)], self.letters[(1, 1)], self.letters[(1, 2)], self.letters[(1, 3)],
                   self.letters[(2, 0)], self.letters[(2, 1)], self.letters[(2, 2)], self.letters[(2, 3)],
                   self.letters[(3, 0)], self.letters[(3, 1)], self.letters[(3, 2)], self.letters[(3, 3)]))

    def shake(self, cubes_list):
        random.seed(11)
        random.shuffle(cubes_list)
        for y in range(4):
            for x in range(4):
                self.letters[(x, y)] = random.sample(cubes_list[x + y], 1)

    def find_word(self, my_word):
        for x in range(4):
            for y in range(4):
                print('{}: ({}, {})'.format(my_word[0], x, y))
                if my_word[0] in self.letters[(x, y)]:
                    if self.walk(my_word[1:], x, y):
                        return True
                    else:
                        pass
        return False

    def walk(self, my_word, x_pos, y_pos):
        for x in range(-1, 2):
            for y in range(-1, 2):
                print('{}: ({}, {})'.format(my_word[0],x_pos + x, y_pos + y))
                if my_word[0] in self.letters[(x_pos + x, y_pos + y)]:
                    if len(my_word) == 1:
                        return True
                    else:
                        return self.walk(my_word[1:], x_pos + x, y_pos + y)
        print(False)
        return False

cubes_list = ['AACIOT', 'AHMORS', 'EGKLUY', 'ABILTY', 'ACDEMP', 'EGINTV', 'GILRUW', 'ELPSTU', 'DENOSW', 'ACELRS',
                'ABJMOQ', 'EEFHIY', 'EHINPS', 'DKNOTU', 'ADENVZ', 'BIFORX']

# start_time = time.time()
# time.sleep(1)
# print(time.time()-start_time)

g = Grid()
g.shake(cubes_list)
g.display()
print(g.find_word('COATS'))
