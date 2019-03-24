"""
    Title       : Tetris Game
    Author      : Houssem Ben Mabrouk (PxCode)
    Last edited : March 2019
"""
from tkinter import Tk, Canvas, Frame, ALL
from random import randint

PLATFORM_WIDTH = 300
PLATFORM_HEIGHT = 540
BLOCK_SIZE = 30
DELAY = 750
PIECES_TYPE = ['O', 'I', 'S', 'Z', 'L', 'J', 'T']

def init_matrix(matrix_width, matrix_height, y_offset=0, x_offset=0):
    """initialize a 2 dimensional array"""

    matrix = []
    for x in range(matrix_width):
        temp = []
        for y in range(matrix_height):
            block = Block()
            block.pos_x = x*BLOCK_SIZE + x_offset*BLOCK_SIZE
            block.pos_y = y*BLOCK_SIZE + y_offset*BLOCK_SIZE
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

class Block:
    """Block Structure Class"""

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.size = 30
        self.activated = False
        self.color = 'white'

    def draw(self, canvas):
        """draw a block"""
        canvas.create_rectangle(self.pos_x, self.pos_y, self.pos_x+BLOCK_SIZE, \
            self.pos_y+BLOCK_SIZE, fill=self.color)

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

    def draw(self, canvas):
        """draws the piece"""
        if self.blocks != None:
            for row in self.blocks:
                for block in row:
                    if block.is_activated():
                        block.set_color(self.color)
                        block.draw(canvas)

    def gravity(self):
        """drops the piece by one row"""

        if self.blocks != None:
            for row in self.blocks:
                for block in row:
                    block.set_pos_y(block.get_pos_y() + BLOCK_SIZE)

    def get_blocks(self):
        """Getter for the piece blocks"""
        return self.blocks

    def move_right(self):
        """Moves the piece to the right"""
        print("move piece to the right")
        if not Platform.is_colliding_with_platform(self.blocks):
            for row in self.blocks:
                for block in row:
                    block.set_pos_x(block.get_pos_x() + BLOCK_SIZE)

    def move_left(self):
        """Moves the piece to the left"""
        print("move piece to the left")
        if not Platform.is_colliding_with_platform(self.blocks):
            for row in self.blocks:
                for block in row:
                    block.set_pos_x(block.get_pos_x() - BLOCK_SIZE)

    def rotate(self):
        """Rotates the piece"""
        print("rotate piece")
        raise NotImplementedError

class PieceS(Piece):
    """Class for the piece S"""

    def __init__(self):
        super().__init__('S')
        self.color = 'red'
        self.blocks[0][3].activate()
        self.blocks[1][2].activate()
        self.blocks[1][3].activate()
        self.blocks[2][2].activate()

    def rotate(self):
        pass

class PieceZ(Piece):
    """Class for the piece Z"""

    def __init__(self):
        super().__init__('Z')
        self.color = 'green'
        self.blocks[0][2].activate()
        self.blocks[1][2].activate()
        self.blocks[1][3].activate()
        self.blocks[2][3].activate()

    def rotate(self):
        pass

class PieceL(Piece):
    """Class for the piece L"""

    def __init__(self):
        super().__init__('L')
        self.color = 'orange'
        self.blocks[0][1].activate()
        self.blocks[0][2].activate()
        self.blocks[0][3].activate()
        self.blocks[1][3].activate()
        self.blocks[1][1].activate()

    def rotate(self):
        pass

class PieceJ(Piece):
    """Class for the pieces L and J"""

    def __init__(self):
        super().__init__('J')
        self.color = '#ffc0cb'
        self.blocks[0][3].activate()
        self.blocks[1][3].activate()
        self.blocks[1][2].activate()
        self.blocks[1][1].activate()

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[0][3].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[1][1].deactivate()
            self.blocks[0][1].activate()
            self.blocks[0][2].activate()
            self.blocks[2][2].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[0][1].deactivate()
            self.blocks[0][2].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[1][1].activate()
            self.blocks[2][1].activate()
            self.blocks[1][3].activate()
            self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[1][1].deactivate()
            self.blocks[2][1].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[0][2].activate()
            self.blocks[2][2].activate()
            self.blocks[2][3].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            self.blocks[0][2].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[2][3].deactivate()
            self.blocks[0][3].activate()
            self.blocks[1][3].activate()
            self.blocks[1][1].activate()
            self.rotation_stage = 0

class PieceO(Piece):
    """Class for the piece O"""

    def __init__(self):
        super().__init__('O')
        self.blocks[1][2].activate()
        self.blocks[2][2].activate()
        self.blocks[1][3].activate()
        self.blocks[2][3].activate()
        self.color = 'yellow'

    def rotate(self):
        pass

class PieceI(Piece):
    """Class for the piece I"""

    def __init__(self):
        super().__init__('I')
        self.blocks[0][0].activate()
        self.blocks[0][1].activate()
        self.blocks[0][2].activate()
        self.blocks[0][3].activate()
        self.color = 'cyan'

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[0][1].deactivate()
            self.blocks[0][2].deactivate()
            self.blocks[0][3].deactivate()
            self.blocks[1][0].activate()
            self.blocks[2][0].activate()
            self.blocks[3][0].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            self.blocks[0][1].activate()
            self.blocks[0][2].activate()
            self.blocks[0][3].activate()
            self.blocks[1][0].deactivate()
            self.blocks[2][0].deactivate()
            self.blocks[3][0].deactivate()
            self.rotation_stage = 0

class PieceT(Piece):
    """Class for the piece T"""

    def __init__(self):
        super().__init__('T')
        self.blocks[0][2].activate()
        self.blocks[1][2].activate()
        self.blocks[2][2].activate()
        self.blocks[1][3].activate()
        self.color = 'magenta'

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[2][2].deactivate()
            self.blocks[1][1].activate()
        elif self.rotation_stage == 1:
            self.blocks[1][3].deactivate()
            self.blocks[2][2].activate()
        elif self.rotation_stage == 2:
            self.blocks[0][2].deactivate()
            self.blocks[1][3].activate()
        elif self.rotation_stage == 3:
            self.blocks[1][1].deactivate()
            self.blocks[0][2].activate()
            self.rotation_stage = -1
        self.rotation_stage += 1

class Platform(Canvas):
    """Game Platform Class"""

    def __init__(self):
        super().__init__(width=PLATFORM_WIDTH, height=PLATFORM_HEIGHT, background='black')

        self.init_game()
        self.pack()

    def init_game(self):
        """initializes the game"""

        self.in_game = True
        self.lines = 0
        self.score = 0
        self.current_piece = self.select_random_piece()
        self.blocks = init_matrix(10, 18)

        self.bind_all('<Key>', self.on_key_pressed)
        self.after(DELAY, self.tick)

    def select_random_piece(self):
        index = randint(0, len(PIECES_TYPE)-1)
        #piece_type = PIECES_TYPE[index]
        piece_type = 'J'
        print("Piece Type : ", piece_type)
        if piece_type == 'O':
            return PieceO()
        elif piece_type == 'I':
            return PieceI()
        elif piece_type == 'S':
            return PieceS()
        elif piece_type == 'Z':
            return PieceZ()
        elif piece_type == 'L':
            return PieceL()
        elif piece_type == 'J':
            return PieceJ()
        elif piece_type == 'T':
            return PieceT()

    def on_key_pressed(self, event):
        """handles piece movement"""

        key = event.keysym
        if key == 'Right':
            self.current_piece.move_right()
            pass
        elif key == 'Left':
            self.current_piece.move_left()
        elif key == 'Down':
            pass
        elif key == 'R' or key == 'r':
            self.current_piece.rotate()
        elif key == 'Escape':
            self.game_over()

    def tick(self):
        """creates a game cycle each timer event"""

        if self.in_game:
            self.draw_platform()
            self.draw_current_piece()
            if not self.is_colliding_with_platform(self.current_piece.get_blocks()):
                self.current_piece.gravity()
            else:
                self.merge_current_piece()
                self.current_piece = self.select_random_piece()
            self.after(DELAY, self.tick)
        else:
            self.game_over()

    def merge_current_piece(self):
        """Merges the current piece with the platform"""
        temp = self.current_piece.get_blocks()
        for index_x, platform_row in enumerate(self.blocks):
            for index_y, platform_block in enumerate(platform_row):
                for index2_x, piece_row in enumerate(temp):
                    for index2_y, piece_block in enumerate(piece_row):
                        if piece_block.is_activated() and \
                            piece_block.get_pos_x() == platform_block.get_pos_x() and \
                            piece_block.get_pos_y() == platform_block.get_pos_y():
                            temp_color = temp[index2_x][index2_y].get_color()
                            self.blocks[index_x][index_y].set_color(temp_color)
                            self.blocks[index_x][index_y].activate()

    @staticmethod
    def is_colliding_with_platform(blocks):
        """Checks the blocks are colliding with the platform"""
        # TODO needs to be changed in the future
        temp = blocks[-1:][0]
        for block in temp:
            if block.is_activated() and block.get_pos_y() + BLOCK_SIZE >= 18 * BLOCK_SIZE:
                return True
        return False

    def draw_current_piece(self):
        """draws the current piece"""
        if self.current_piece != None:
            self.current_piece.draw(self)

    def draw_platform(self):
        """draws the platform"""
        for row in self.blocks:
            for block in row:
                block.draw(self)

    def tutorial(self):
        """draws the screen of the tutorial"""
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, \
            text='Fléche gauche : Pousser la piéce à gauche\n\
                Fléche droite : Pousser la piéce à droite\n\
                    ', fill='white')

    def game_over(self):
        """deletes all objects and draws game over message"""

        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, \
            text='Game Over avec score {}'.format(self.score), fill='white')
        self.after(DELAY, self.exit_game)

    def __print_blocks(self):
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    print('1', end=' ')
                else:
                    print('0', end=' ')
            print('')
        print('-'*20)

    def exit_game(self):
        """exists the game"""

        exit(0)

class Tetris(Frame):
    """Main Tetris Class"""

    def __init__(self):
        super().__init__()

        self.master.title('Tetris - Houssem')
        self.platform = Platform()
        self.pack()

def main():
    """Main Game Function"""
    root = Tk()
    root.resizable(False, False)
    tetris_game = Tetris()
    root.mainloop()

main()
