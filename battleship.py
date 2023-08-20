""" File: battleship.py
    Author: Ishika Patel
    Course: CSC120
    Purpose: This program create 2 classes: Board and Ship where both interact
             with each other to replicate one side of the battleship board.
"""
class Board:
    """
    This class represents the board where all ships are located and where
    changes to ships will occur.

       The constructor checks and sets a size variabe representing the
       size of the board. It checks to ensure size is a positive integer.
       The all_ships field contains a list of all the ships. It also
       creates an empty grid to start out with. All variables are private.

    The class defines several helpful methods and fields:
        add_ship() - adds each ship to the board

        print() - prints the board each time a change is made

        print_large() - prints the board if size is >9

        has_been_used(positons) - returns True if a position has
            already been used; returns False otherwise

        attempt_move(positions) - checks if position has been hit or missed;
            also checks if all ships have been sunk resulting in gameover
    """
    def __init__(self, size):
        assert size > 0
        self._size = size
        self._all_ships = []

        grid = []
        for i in range(self._size):
            temp = []
            for j in range(self._size):
                temp.append('.')
            grid.append(temp)

        self._grid = grid

    def add_ship(self, ship, position):
        temp = []

        # checks to make sure ship does not fall outside of grid
        for tup in ship._new_shape:
            assert 0 <= tup[0] + position[0] < self._size and 0 <= tup[1] + \
            position[1] <= self._size
            tup = (tup[0] + position[0], tup[1] + position[1])

            assert self._grid[tup[0]][tup[1]] == '.'
            temp.append(tup)

        ship._new_shape = temp
        self._all_ships.append(ship)

        for tup in ship._new_shape:
            for i in range(len(self._grid)):
                for j in range(len(self._grid[i])):

                    # saves first letter of ship name to grid array
                    if (i, j) == tup:
                        self._grid[i][j] = ship._name[0]

    def print(self):
        if self._size <= 10:
            print('  +' + '--'*self._size + '-+')

            for i in range(self._size-1, -1, -1):
                print(i, '| ', end='')

                for j in range(self._size-1, -1, -1):
                    print(self._grid[self._size - j - 1][i], '', end= '')
                print('|')

            print('  +' + '--'*self._size + '-+')
            print('    ', end='')

            for i in range(self._size):
                print(i, '', end='')
            print('\n')

        else:
            self.print_large()

    def print_large(self):
        print('   +' + '--'*self._size + '-+')
        for i in range(self._size-1, -1, -1):
            if i <= 9:
                print('', i, '| ', end='')
            else:
                print(i, '| ', end='')
            for j in range(self._size-1, -1, -1):
                print(self._grid[self._size - j - 1][i], '', end= '')
            print('|')
        print('   +' + '--'*self._size + '-+')
        print('                         ', end='')

        i = 1
        while i < int(str(self._size)[0]):
            for j in range(0, 10):
                print(i, '', end='')
            i += 1

        for i in range(int(str(self._size)[1])):
            print(int(str(self._size)[0]), '', end ='')

        i = 1
        print('\n     ', end='')
        while i <= int(str(self._size)[0]):
            for j in range(0, 10):
                print(j, '', end='')
            i += 1

        for i in range(int(str(self._size)[1])):
            print(i, '', end='')
        print('\n')

    def has_been_used(self, position):
        # checks to make sure position doesn't lie outside of the board
        assert 0 <= position[0] <= self._size and 0 <= position[1] <=self._size

        for i in range(self._size):
            for j in range(self._size):
                if (i, j) == position:
                    if self._grid[i][j] == 'o' or self._grid[i][j] == 'X' \
                    or self._grid[i][j] == '*':
                        return True
        return False

    def attempt_move(self, position):
        # checks to make sure position does not fall outside of board
        assert 0 <= position[0] <= self._size and 0 <= position[1] <=self._size
        assert not self.has_been_used(position)

        for i in range(self._size):
            for j in range(self._size):
                if (i, j) == position:
                    for each_ship in self._all_ships:
                        if self._grid[i][j] == '.':
                            self._grid[i][j] = 'o'
                            return 'Miss'

                        elif self._grid[i][j] == each_ship._name[0]:
                            self._grid[i][j] = '*'
                            index = each_ship._new_shape.index((i, j))

                            # saves updated results of each ship for ship list
                            each_ship._shape_info = \
                            each_ship._shape_info[:index] + '*' + \
                            each_ship._shape_info[index+1:]

                            if each_ship._shape_info == \
                            '*'*len(each_ship._shape_info):

                                if each_ship._shape_info == \
                                '*'*len(each_ship._new_shape):

                                    for coord in each_ship._new_shape:
                                        self._grid[coord[0]][coord[1]] = 'X'
                                return f'Sunk ({each_ship._name})'
                            else:
                                return 'Hit'

class Ship:
    """
    This class represents a ship on the board that will be created
    and added to the board.

        The constructor contains priv variables including:
            _name = name of the ship
            _shape = list of original coords of each part of the shape
            _new_shape = list of updated coords that correspond to
                coord points on the board
            _shape_info = the length of the ship; keeps track of which
                coord points have been hit at by user

    The class defines several helpful methods and fields:
        print() - prints info about which parts of ship have
            been hit

        is_sunk() - returns True if all coords of a ship have
            been hit at; returns False otherwise

        rotate(amount) - rotates each ship object a certain amount;
            saves the newly rotated coordinats of each part of ship
            to a new list
    """
    def __init__(self, name, shape):
        self._name = name
        self._shape = shape
        self._new_shape = shape
        self._shape_info = self._name[0]*len(self._shape)

    def print(self):
        print(format(self._shape_info, '10'), self._name)

    def is_sunk(self):
        if self._shape_info == '*'*len(self._new_shape):
            return True
        return False

    def rotate(self, amount):
        assert 0 <= amount <= 3
        if amount == 0:
            self._new_shape = self._shape

        temp = []
        for coord in self._new_shape:
            first_coord, second_coord = coord[0], coord[1]
            if amount == 0:
                coord = (first_coord, second_coord)
            if amount == 1:
                coord = (second_coord, -first_coord)

            elif amount == 2:
                coord = (-first_coord, -second_coord)

            elif amount == 3:
                coord = (-second_coord, first_coord)
            temp.append(coord)
        self._new_shape = temp










