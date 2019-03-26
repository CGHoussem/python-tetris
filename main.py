"""
    Title       : Tetris Game
    Author      : Houssem Ben Mabrouk (PxCode)
    Last edited : March 2019
"""
from random import choice
from tkinter import Tk, Canvas, Frame, ALL, PhotoImage, NW

# MATRIX[Y COORDINATE][X COORDINATE]

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

    def drop(self):
        """drops the piece"""
        if self.blocks != None:
            pass

    def get_blocks(self):
        """Getter for the piece blocks"""
        return self.blocks

    def move_right(self):
        """Moves the piece to the right"""
        temp = []
        for row in self.blocks:
            for block in row:
                temp.append(block.get_pos_x())
        max_x = max(temp)
        can_move = True
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    if block.get_pos_x() == max_x and max_x + Tetris.BLOCK_SIZE >= 300:
                        can_move = False
        if can_move:
            for row in self.blocks:
                for block in row:
                    if block.get_pos_x() + Tetris.BLOCK_SIZE < 300:
                        block.set_pos_x(block.get_pos_x() + Tetris.BLOCK_SIZE)

    def move_left(self):
        """Moves the piece to the left"""
        temp = []
        for row in self.blocks:
            for block in row:
                temp.append(block.get_pos_x())
        min_x = min(temp)
        can_move = True
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    if block.get_pos_x() == min_x and min_x - Tetris.BLOCK_SIZE < 0:
                        can_move = False
        if can_move:
            for row in self.blocks:
                for block in row:
                    if block.get_pos_x() - Tetris.BLOCK_SIZE >= 0:
                        block.set_pos_x(block.get_pos_x() - Tetris.BLOCK_SIZE)

    def rotate(self):
        """Rotates the piece"""
        # TODO: fix rotation flaw (it happens when we move the
        # deactivated blocks out of the border)
        raise NotImplementedError

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
        debug_print(self.blocks)

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
        super().__init__(width=Tetris.PLATFORM_WIDTH, height=Tetris.PLATFORM_HEIGHT,\
            background='black')

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
        self.blocks = init_matrix(10, 18)

        self.bind_all('<Key>', self.__on_key_pressed)
        self.__current_job = self.after(Tetris.DELAY, self.tick)

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
            self.__current_piece.move_right()
        elif key == 'Left':
            self.__current_piece.move_left()
        elif key == 'Down':
            self.__current_piece.drop()
        elif key == 'Up':
            self.__current_piece.rotate()
        elif key == 'Escape':
            self.game_over()

    def tick(self):
        """creates a game cycle each timer event"""
        if self.__in_game:
            self.delete(ALL)
            self.__draw_platform()
            self.__draw_current_piece()
            self.__draw_ui()

            if not self.__is_colliding_with_platform(self.__current_piece.get_blocks()):
                self.__current_piece.gravity()
            else:
                self.__merge_current_piece()
                lines = self.__get_lines()
                if lines != None:
                    self.__lines += len(lines)
                    temp = self.__lines // 10
                    if temp >= 1 and temp != self.__level:
                        self.__level = self.__lines // 10
                        Tetris.DELAY = clamp(Tetris.DELAY - 150, 100, Tetris.DELAY)
                    self.__break_lines(lines)
                self.__current_piece = self.__next_piece
                self.__next_piece = self.__select_random_piece()
            self.__current_job = self.after(Tetris.DELAY, self.tick)
        else:
            self.game_over()

    def __get_lines(self):
        row_index = 0
        lines = []
        for row in self.blocks:
            count = 0
            row_index += 1
            for block in row:
                if block.is_activated():
                    count += 1
                else:
                    break
            if count == 10:
                lines.append(row)
        return lines

    def __break_lines(self, lines):
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

        # Breaking the lines
        for row in lines:
            for block in row:
                block.deactivate()

        # Dropping the hanging blocks
        # TODO: dropping the hanging blocks

    def __merge_current_piece(self):
        """Merges the current piece with the platform"""
        temp = self.__current_piece.get_blocks()
        for index_y, platform_row in enumerate(self.blocks):
            for index_x, platform_block in enumerate(platform_row):
                for index2_y, piece_row in enumerate(temp):
                    for index2_x, piece_block in enumerate(piece_row):
                        if piece_block.is_activated() and\
                        piece_block.get_pos_x() == platform_block.get_pos_x() and\
                        piece_block.get_pos_y() == platform_block.get_pos_y():
                            temp_color = temp[index2_y][index2_x].get_color()
                            self.blocks[index_y][index_x].set_color(temp_color)
                            self.blocks[index_y][index_x].activate()

    def __is_colliding_with_platform(self, blocks):
        """Checks the blocks are colliding with the platform"""
        # Collision with the bottom of the platform
        for row in blocks:
            for block in row:
                if block.is_activated() and block.get_pos_y() + Tetris.BLOCK_SIZE >= 18 * Tetris.BLOCK_SIZE:
                    return True
        # Collision with the activated blocks of the platform
        for platform_row in self.blocks:
            for platform_block in platform_row:
                for piece_row in blocks:
                    for piece_block in piece_row:
                        if platform_block.is_activated() and piece_block.is_activated()\
                        and platform_block.get_pos_x() == piece_block.get_pos_x()\
                        and platform_block.get_pos_y() == piece_block.get_pos_y() + Tetris.BLOCK_SIZE:
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
        """draws the ui (next_piece, score, level, lines)"""
        self.__draw_next_piece()
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
    BLOCK_SIZE = 30
    DELAY = 300

    # TODO: add custom font
    def __init__(self, player_name):
        super().__init__()

        self.master.title('Tetris - Houssem')
        self.platform = Platform(Player(player_name))
        self.pack()

def main():
    """Main Game Function"""
    root = Tk()
    root.resizable(False, False)
    player_name = input("Enter your name: ")
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

if __name__ == '__main__':
    main()
