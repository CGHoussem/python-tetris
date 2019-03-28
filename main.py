"""
    Title       : Tetris Game
    Author      : Houssem Ben Mabrouk (PxCode)
    Last edited : March 2019
"""
from random import choice
from tkinter import Tk, Canvas, Frame, ALL, PhotoImage, NW

# MATRIX[Y COORDINATE][X COORDINATE]
# TODO : FIX LINE BREAKING SHIT.. -_-
# TODO : ADD CEILING LIMIT (GAME OVER ..)

def init_matrix(matrix_width, matrix_height, y_offset=0, x_offset=0):
    """initialize a 2 dimensional array"""
    matrix = []
    for y_index in range(matrix_height):
        temp = []
        for x_index in range(matrix_width):
            block = Block()
            block.pos_x = x_index*Tetris.BLOCK_SIZE + x_offset*Tetris.BLOCK_SIZE
            block.pos_y = y_index*Tetris.BLOCK_SIZE + y_offset*Tetris.BLOCK_SIZE
            temp.append(block)
        matrix.append(temp)
    return matrix

def clamp(value, min_val, max_val):
    """clamp a value"""

    if value < min_val:
        return min_val
    if value > max_val:
        return  max_val
    return value

class Player:
    """Class describes the player data structure"""

    def __init__(self, player_name):
        self.__player_name = player_name
        self.__score = 0

    def get_player_name(self):
        """Returns the player's name"""
        return self.__player_name

    def get_score(self):
        """Returns the player's score"""
        return self.__score

    def add_score(self, value):
        """Adds a value the player's score"""
        self.__score += value

    def set_score(self, score):
        """Sets the player's score"""
        self.__score = score

class Block:
    """Block Structure Class"""

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.size = 30
        self.activated = False
        self.color = 'white'

    def draw(self, canvas, off_x=0, off_y=0):
        """draw a block"""
        canvas.create_rectangle(self.pos_x+off_x*Tetris.BLOCK_SIZE, self.pos_y+off_y*Tetris.BLOCK_SIZE,\
            self.pos_x+off_x*Tetris.BLOCK_SIZE+Tetris.BLOCK_SIZE, self.pos_y+off_y*Tetris.BLOCK_SIZE+Tetris.BLOCK_SIZE,\
                fill=self.color)

    def set_color(self, color):
        """Setter for the block color"""
        self.color = color

    def get_color(self):
        """Getter for the block color"""
        return self.color

    def is_activated(self):
        """returns True or False wether the block is active or not"""
        return self.activated

    def activate(self):
        """activates the block for later calculation"""
        self.activated = True

    def deactivate(self):
        """deactivates the block"""
        self.activated = False

    def get_pos_x(self):
        """Getter Pos X"""
        return self.pos_x

    def get_pos_y(self):
        """Getter Pos Y"""
        return self.pos_y

    def set_pos_x(self, pos_x):
        """Setter Pos X"""
        self.pos_x = pos_x

    def set_pos_y(self, pos_y):
        """Setter Pos Y"""
        self.pos_y = pos_y

    def __str__(self):
        if self.activate:
            return '1'
        else:
            return '0'

class Piece:
    """Piece Structure Class"""

    def __init__(self, piece_type):
        if piece_type == 'O' or piece_type == 'S' or\
            piece_type == 'Z' or piece_type == 'T':
            self.blocks = init_matrix(4, 4, -2)
        elif piece_type == 'L' or piece_type == 'J':
            self.blocks = init_matrix(4, 4, -1)
        else:
            self.blocks = init_matrix(4, 4)
        self.color = 'gray'
        self.rotation_stage = 0

    def draw(self, canvas, off_x=0, off_y=0):
        """draws the piece"""
        if self.blocks != None:
            for row in self.blocks:
                for block in row:
                    if block.is_activated():
                        block.set_color(self.color)
                        block.draw(canvas, off_x, off_y)

    def gravity(self):
        """moves the piece down by one block"""
        if self.blocks != None:
            for row in self.blocks:
                for block in row:
                    block.set_pos_y(block.get_pos_y() + Tetris.BLOCK_SIZE)

    def get_blocks(self):
        """Getter for the piece blocks"""
        return self.blocks

    def move_right(self, platform_blocks):
        """Moves the piece to the right"""
        # Checking for the platform limits
        temp = []
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    temp.append(block.get_pos_x())
        max_x = max(temp)
        if max_x + Tetris.BLOCK_SIZE < Tetris.COLS * Tetris.BLOCK_SIZE:
             # Checking for the platform blocks
            x_index, y_index = self.__get_righty()
            x_index //= Tetris.BLOCK_SIZE
            y_index //= Tetris.BLOCK_SIZE
            if not platform_blocks[y_index][x_index + 1].is_activated():
                for row in self.blocks:
                    for block in row:
                        block.set_pos_x(block.get_pos_x() + Tetris.BLOCK_SIZE)

    def move_left(self, platform_blocks):
        """Moves the piece to the left"""
        # Checking for the platform limits
        temp = []
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    temp.append(block.get_pos_x())
        min_x = min(temp)
        if min_x - Tetris.BLOCK_SIZE >= 0:
            # Checking for the platform blocks
            x_index, y_index = self.__get_lefty()
            x_index //= Tetris.BLOCK_SIZE
            y_index //= Tetris.BLOCK_SIZE
            if not platform_blocks[y_index][x_index - 1].is_activated():
                for row in self.blocks:
                    for block in row:
                        if block.get_pos_x() - Tetris.BLOCK_SIZE >= 0:
                            block.set_pos_x(block.get_pos_x() - Tetris.BLOCK_SIZE)

    def rotate(self):
        """Rotates the piece"""
       # TODO: fix rotation flaw (it happens when we move the
        # deactivated blocks out of the border)
        raise NotImplementedError

    def __get_lefty(self):
        temp = {}
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    temp[block.get_pos_x()] = block.get_pos_y()

        return (min(temp), temp[min(temp)])

    def __get_righty(self):
        temp = {}
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    temp[block.get_pos_x()] = block.get_pos_y()

        return (max(temp), temp[max(temp)])

class PieceS(Piece):
    """Class for the piece S"""

    def __init__(self):
        super().__init__('S')
        self.color = 'red'
        self.blocks[3][0].activate()
        self.blocks[2][1].activate()
        self.blocks[3][1].activate()
        self.blocks[2][2].activate()

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[3][0].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[1][0].activate()
            self.blocks[2][0].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[1][0].deactivate()
            self.blocks[3][1].deactivate()
            self.blocks[1][1].activate()
            self.blocks[1][2].activate()
            self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[2][0].deactivate()
            self.blocks[1][2].deactivate()
            self.blocks[2][2].activate()
            self.blocks[3][2].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            self.blocks[1][1].deactivate()
            self.blocks[3][2].deactivate()
            self.blocks[3][0].activate()
            self.blocks[3][1].activate()
            self.rotation_stage = 0

class PieceZ(Piece):
    """Class for the piece Z"""

    def __init__(self):
        super().__init__('Z')
        self.color = 'green'
        self.blocks[2][0].activate()
        self.blocks[2][1].activate()
        self.blocks[3][1].activate()
        self.blocks[3][2].activate()

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[3][1].deactivate()
            self.blocks[3][2].deactivate()
            self.blocks[1][1].activate()
            self.blocks[3][0].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[3][0].deactivate()
            self.blocks[2][0].deactivate()
            self.blocks[1][0].activate()
            self.blocks[2][2].activate()
            self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[1][1].deactivate()
            self.blocks[1][0].deactivate()
            self.blocks[1][2].activate()
            self.blocks[3][1].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            self.blocks[1][2].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[2][0].activate()
            self.blocks[3][2].activate()
            self.rotation_stage = 0

class PieceL(Piece):
    """Class for the piece L"""

    def __init__(self):
        super().__init__('L')
        self.color = 'orange'
        self.blocks[1][0].activate()
        self.blocks[2][0].activate()
        self.blocks[3][0].activate()
        self.blocks[3][1].activate()

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[3][0].deactivate()
            self.blocks[3][1].deactivate()
            self.blocks[1][1].activate()
            self.blocks[1][2].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[1][0].deactivate()
            self.blocks[2][0].deactivate()
            self.blocks[2][2].activate()
            self.blocks[3][2].activate()
            self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[1][1].deactivate()
            self.blocks[1][2].deactivate()
            self.blocks[3][0].activate()
            self.blocks[3][1].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            self.blocks[2][2].deactivate()
            self.blocks[3][2].deactivate()
            self.blocks[1][0].activate()
            self.blocks[2][0].activate()
            self.rotation_stage = 0

class PieceJ(Piece):
    """Class for the pieces L and J"""

    def __init__(self):
        super().__init__('J')
        self.color = '#ff1493'
        self.blocks[3][0].activate()
        self.blocks[3][1].activate()
        self.blocks[2][1].activate()
        self.blocks[1][1].activate()

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[3][0].deactivate()
            self.blocks[3][1].deactivate()
            self.blocks[1][1].deactivate()
            self.blocks[1][0].activate()
            self.blocks[2][0].activate()
            self.blocks[2][2].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[1][0].deactivate()
            self.blocks[2][0].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[1][1].activate()
            self.blocks[1][2].activate()
            self.blocks[3][1].activate()
            self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[1][1].deactivate()
            self.blocks[1][2].deactivate()
            self.blocks[3][1].deactivate()
            self.blocks[2][0].activate()
            self.blocks[2][2].activate()
            self.blocks[3][2].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            self.blocks[2][0].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[3][2].deactivate()
            self.blocks[3][0].activate()
            self.blocks[3][1].activate()
            self.blocks[1][1].activate()
            self.rotation_stage = 0

class PieceO(Piece):
    """Class for the piece O"""

    def __init__(self):
        super().__init__('O')
        self.blocks[2][1].activate()
        self.blocks[2][2].activate()
        self.blocks[3][1].activate()
        self.blocks[3][2].activate()
        self.color = 'yellow'

    def rotate(self):
        pass

class PieceI(Piece):
    """Class for the piece I"""

    def __init__(self):
        super().__init__('I')
        self.blocks[0][0].activate()
        self.blocks[1][0].activate()
        self.blocks[2][0].activate()
        self.blocks[3][0].activate()
        self.color = 'cyan'

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[0][0].deactivate()
            self.blocks[1][0].deactivate()
            self.blocks[2][0].deactivate()
            self.blocks[3][1].activate()
            self.blocks[3][2].activate()
            self.blocks[3][3].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[3][1].deactivate()
            self.blocks[3][2].deactivate()
            self.blocks[3][3].deactivate()
            self.blocks[0][0].activate()
            self.blocks[1][0].activate()
            self.blocks[2][0].activate()
            self.rotation_stage = 0

class PieceT(Piece):
    """Class for the piece T"""

    def __init__(self):
        super().__init__('T')
        self.blocks[2][0].activate()
        self.blocks[2][1].activate()
        self.blocks[2][2].activate()
        self.blocks[3][1].activate()
        self.color = 'magenta'

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[2][2].deactivate()
            self.blocks[1][1].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[3][1].deactivate()
            self.blocks[2][2].activate()
            self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[2][0].deactivate()
            self.blocks[3][1].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            self.blocks[1][1].deactivate()
            self.blocks[2][0].activate()
            self.rotation_stage = 0

class Platform(Canvas):
    """Game Platform Class"""
    def __init__(self, player):
        super().__init__(width=Tetris.PLATFORM_WIDTH, height=Tetris.PLATFORM_HEIGHT\
            , background='black')
        self.focus_set()
        self.__init_game(player)
        self.pack()

    def __init_game(self, player):
        """initializes the game"""
        self.__in_game = True
        self.__player = player
        self.__lines = 0
        self.__level = 1
        self.__current_piece = self.__select_random_piece()
        self.__next_piece = self.__select_random_piece()
        self.__background = PhotoImage(file="bg.gif")
        self.blocks = init_matrix(Tetris.COLS, Tetris.ROWS)

        self.bind_all('<Key>', self.__on_key_pressed)
        self.__current_job = self.after(Tetris.DELAY, self.__tick)

    def __select_random_piece(self):
        """Returns a random piece"""
        chosen_type = choice(Tetris.PIECE_TYPES)
        if chosen_type == 'O':
            return PieceO()
        elif chosen_type == 'I':
            return PieceI()
        elif chosen_type == 'S':
            return PieceS()
        elif chosen_type == 'Z':
            return PieceZ()
        elif chosen_type == 'L':
            return PieceL()
        elif chosen_type == 'J':
            return PieceJ()
        elif chosen_type == 'T':
            return PieceT()

    def __on_key_pressed(self, event):
        """handles piece movement"""
        key = event.keysym
        if key == 'Right':
            self.__current_piece.move_right(self.blocks)
        elif key == 'Left':
            self.__current_piece.move_left(self.blocks)
        elif key == 'Up':
            self.__current_piece.rotate()
        elif key == 'Escape':
            self.game_over()

    def __tick(self):
        """creates a game cycle each timer event"""
        if self.__in_game:
            self.delete(ALL)
            self.__draw_platform()
            self.__draw_current_piece()
            self.__draw_ui()

            # Checking if the current piece is colliding with the platform
            if not self.__is_colliding_with_platform():
                # Moving down the current piece by one block
                self.__current_piece.gravity()
            else:
                # Merging the current piece with the platform
                self.__merge_current_piece()
                # Searching for completed lines
                temp_lines = self.__get_lines()
                if len(temp_lines) > 0:
                    self.__lines += len(temp_lines)
                    # Clearing the lines
                    self.__break_lines(temp_lines)
                    temp_lines.clear()
                    # Leveling UP
                    self.__level_up()
                # Setting the current piece and generating a new next piece
                self.__current_piece = self.__next_piece
                self.__next_piece = self.__select_random_piece()
            # Looping the 'tick' function
            self.__current_job = self.after(Tetris.DELAY, self.__tick)
        else:
            self.game_over()

    def __level_up(self):
        """ Checking for level up, if so levels up the player"""
        temp = self.__lines // Tetris.COLS
        if temp >= 1 and temp != self.__level:
            self.__level = self.__lines // Tetris.COLS
            Tetris.DELAY = clamp(Tetris.DELAY - 100, 100, Tetris.DELAY)

    def __get_lines(self):
        lines = []
        for row in self.blocks:
            count = 0
            for block in row:
                if block.is_activated():
                    count += 1
                else:
                    break
            if count == Tetris.COLS:
                lines.append(row)
        return lines

    def __break_lines(self, lines):
        """Breaking the lines and dropping the other blocks by how many blocks broken"""
        lines_sum = len(lines)

        # Rewarding the player
        # Following: Original BPS scoring system
        if lines_sum == 1:
            self.__player.add_score(40 * self.__level)
        elif lines_sum == 2:
            self.__player.add_score(100 * self.__level)
        elif lines_sum == 3:
            self.__player.add_score(300 * self.__level)
        elif lines_sum == 4:
            self.__player.add_score(1200 * self.__level)

        # Breaking lines
        for row in lines:
            for block in row:
                block.deactivate()

        # Dropping the hanging blocks
        for reversed_y_index, row in enumerate(reversed(self.blocks)):
            for x_index, block in enumerate(row):
                if block.is_activated() and 17-reversed_y_index + lines_sum <= 17:
                    temp_b = Block()
                    temp_b.deactivate()
                    temp_b.set_pos_x(x_index)
                    temp_b.set_pos_y(17-reversed_y_index)
                    block.set_pos_y(block.get_pos_y() + Tetris.BLOCK_SIZE * lines_sum)
                    self.blocks[17-reversed_y_index + lines_sum][x_index] = block
                    self.blocks[17-reversed_y_index][x_index] = temp_b

    def __merge_current_piece(self):
        """Merges the current piece with the platform"""
        for row in self.__current_piece.get_blocks():
            for block in row:
                if block.is_activated():
                    x_index = block.get_pos_x() // Tetris.BLOCK_SIZE
                    y_index = block.get_pos_y() // Tetris.BLOCK_SIZE
                    self.blocks[y_index][x_index] = block

    def __is_colliding_with_platform(self):
        """Checks the blocks are colliding with the platform"""
        # Collision Detection
        for row in self.__current_piece.get_blocks():
            for block in row:
                if block.is_activated():
                    x_index = block.get_pos_x() // Tetris.BLOCK_SIZE
                    y_index = block.get_pos_y() // Tetris.BLOCK_SIZE
                    if y_index + 1 >= Tetris.ROWS or self.blocks[y_index+1][x_index].is_activated():
                        return True
        return False

    def __draw_current_piece(self):
        """draws the current piece"""
        if self.__current_piece != None:
            self.__current_piece.draw(self)

    def __draw_next_piece(self):
        """draws the next piece"""
        if isinstance(self.__next_piece, (PieceI, PieceL, PieceJ)):
            self.__next_piece.draw(self, 13, 13)
        elif isinstance(self.__next_piece, (PieceS, PieceZ, PieceO, PieceT)):
            self.__next_piece.draw(self, 12, 14)

    def __draw_platform(self):
        """draws the platform"""
        self.create_image(0, 0, anchor=NW, image=self.__background)
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    block.draw(self)

    def __draw_ui(self):
        """draws the ui (next_piece, player name, score, level, lines)"""
        self.__draw_next_piece()
        self.create_text(425, 10, text='{}'.format(self.__player.get_player_name()),\
            fill='white', font=('Game Over', 50))
        self.create_text(425, 117, text='{}'.format(self.__player.get_score()),\
            fill='white', font=('Game Over', 50))
        self.create_text(454, 332, text='{}'.format(self.__lines),\
            fill='white', font=('Game Over', 50))
        self.create_text(454, 240, text='{}'.format(self.__level),\
            fill='white', font=('Game Over', 50))

    def tutorial(self):
        """draws the screen of the tutorial"""
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, \
            text='Fléche gauche : Pousser la piéce à gauche\n\
                Fléche droite : Pousser la piéce à droite\n\
                    ', fill='white')

    def game_over(self):
        """deletes all objects and draws game over message"""
        self.after_cancel(self.__current_job)
        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, \
            text='Game Over avec score {}'.format(self.__player.get_score()),\
                fill='white', font=('Game Over', 60))
        self.__current_job = self.after(3000, self.exit_game)

    def exit_game(self):
        """exists the game"""
        exit(0)

class Tetris(Frame):
    """Main Tetris Class"""
    PIECE_TYPES = ['O', 'I', 'S', 'Z', 'L', 'J', 'T']
    PLATFORM_WIDTH = 550
    PLATFORM_HEIGHT = 540
    ROWS = 18
    COLS = 10
    BLOCK_SIZE = 30
    DELAY = 200

    # TODO: importing custom font
    def __init__(self, player_name):
        super().__init__()

        self.master.title('Tetris - Houssem')
        self.platform = Platform(Player(player_name))
        self.pack()

def main():
    """Main Game Function"""
    root = Tk()
    root.resizable(False, False)
    size = 0
    while size < 3:
        player_name = input("ENTER YOUR NAME: ")
        size = len(player_name)
    player_name = player_name.upper()
    tetris_game = Tetris(player_name)
    root.mainloop()

def debug_print(matrix):
    """Debug function"""
    for row in matrix:
        for col in row:
            if col.is_activated():
                print('1 ', end='')
            else:
                print('0 ', end='')
        print()

def debug_print_reversed(matrix):
    """Debug function"""
    for row in reversed(matrix):
        for col in row:
            if col.is_activated():
                print('1 ', end='')
            else:
                print('0 ', end='')
        print()

if __name__ == '__main__':
    main()
