"""
    Title       : Tetris Game
    Author      : Houssem Ben Mabrouk (PxCode)
    Last edited : Avril 2019
"""
from random import choice
from sys import exit
from tkinter import ALL, NE, NW, Button, Canvas, Entry, Frame, PhotoImage, Tk

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

    if value <= min_val:
        return min_val
    if value >= max_val:
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

    def __get_block_coords(self, block):
        """Returns normalized coordinates"""
        return (block.get_pos_x() // Tetris.BLOCK_SIZE, block.get_pos_y() // Tetris.BLOCK_SIZE)

    def check_movement(self, direction, platform_blocks=None):
        """Checking if movement is safe or not"""
        for row in self.blocks:
            for block in row:
                if block.is_activated():
                    j, i = self.__get_block_coords(block)
                    if direction == -1:
                        temp = block.get_pos_x() - Tetris.BLOCK_SIZE
                        if temp < 0:
                            return False
                        if platform_blocks != None:
                            if platform_blocks[i][j-1].is_activated():
                                return False
                    elif direction == 1:
                        temp = block.get_pos_x() + Tetris.BLOCK_SIZE
                        if temp >= 300:
                            return False
                        if platform_blocks != None:
                            if platform_blocks[i][j+1].is_activated():
                                return False
        return True

    def move_right(self, platform_blocks=None):
        """Moves the piece to the right"""
        if self.check_movement(1, platform_blocks):
            for row in self.blocks:
                for block in row:
                    block.set_pos_x(block.get_pos_x() + Tetris.BLOCK_SIZE)

    def move_left(self, platform_blocks):
        """Moves the piece to the left"""
        if self.check_movement(-1, platform_blocks):
            for row in self.blocks:
                for block in row:
                    block.set_pos_x(block.get_pos_x() - Tetris.BLOCK_SIZE)

    def rotate(self, rotation_stage=None):
        """Rotates the piece"""
        raise NotImplementedError

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
        self.blocks[1][2].activate() # Pivot Point
        self.blocks[2][1].activate()
        self.blocks[2][2].activate()
        self.blocks[1][3].activate()

    def rotate(self, rotation_stage=None):
        if rotation_stage != None:
            self.rotation_stage = rotation_stage
        if self.rotation_stage == 0:
            self.blocks[2][1].deactivate()
            self.blocks[2][2].deactivate()
            self.blocks[0][2].activate()
            self.blocks[2][3].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            if self.check_movement(-1):
                self.blocks[2][3].deactivate()
                self.blocks[0][2].deactivate()
                self.blocks[2][1].activate()
                self.blocks[2][2].activate()
                self.rotation_stage = 0

class PieceZ(Piece):
    """Class for the piece Z"""

    def __init__(self):
        super().__init__('Z')
        self.color = 'green'
        self.blocks[1][2].activate() # Pivot Point
        self.blocks[1][1].activate()
        self.blocks[2][2].activate()
        self.blocks[2][3].activate()

    def rotate(self, rotation_stage=None):
        if rotation_stage != None:
            self.rotation_stage = rotation_stage
        if self.rotation_stage == 0:
            self.blocks[1][1].deactivate()
            self.blocks[2][3].deactivate()
            self.blocks[1][3].activate()
            self.blocks[0][3].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            if self.check_movement(-1):
                self.blocks[1][3].deactivate()
                self.blocks[0][3].deactivate()
                self.blocks[1][1].activate()
                self.blocks[2][3].activate()
                self.rotation_stage = 0

class PieceL(Piece):
    """Class for the piece L"""

    def __init__(self):
        super().__init__('L')
        self.color = 'orange'
        self.blocks[1][1].activate()
        self.blocks[2][1].activate()
        self.blocks[1][2].activate() # Pivot Point
        self.blocks[1][3].activate()

    def rotate(self, rotation_stage=None):
        if rotation_stage != None:
            self.rotation_stage = rotation_stage
        if self.rotation_stage == 0:
            self.blocks[1][1].deactivate()
            self.blocks[2][1].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[0][2].activate()
            self.blocks[2][2].activate()
            self.blocks[2][3].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            if self.check_movement(-1):
                self.blocks[0][2].deactivate()
                self.blocks[2][2].deactivate()
                self.blocks[2][3].deactivate()
                self.blocks[1][1].activate()
                self.blocks[1][3].activate()
                self.blocks[0][3].activate()
                self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[1][1].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[0][3].deactivate()
            self.blocks[0][1].activate()
            self.blocks[0][2].activate()
            self.blocks[2][2].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            if self.check_movement(1):
                self.blocks[0][1].deactivate()
                self.blocks[0][2].deactivate()
                self.blocks[2][2].deactivate()
                self.blocks[1][3].activate()
                self.blocks[1][1].activate()
                self.blocks[2][1].activate()
                self.rotation_stage = 0

class PieceJ(Piece):
    """Class for the piece J"""

    def __init__(self):
        super().__init__('J')
        self.color = '#ff1493'
        self.blocks[1][2].activate() # Pivot Point
        self.blocks[1][1].activate()
        self.blocks[1][3].activate()
        self.blocks[2][3].activate()

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[1][1].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[2][3].deactivate()
            self.blocks[0][2].activate()
            self.blocks[0][3].activate()
            self.blocks[2][2].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            if self.check_movement(-1):
                self.blocks[0][2].deactivate()
                self.blocks[0][3].deactivate()
                self.blocks[2][2].deactivate()
                self.blocks[0][1].activate()
                self.blocks[1][1].activate()
                self.blocks[1][3].activate()
                self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[0][1].deactivate()
            self.blocks[1][1].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[0][2].activate()
            self.blocks[2][1].activate()
            self.blocks[2][2].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            if self.check_movement(1):
                self.blocks[0][2].deactivate()
                self.blocks[2][1].deactivate()
                self.blocks[2][2].deactivate()
                self.blocks[1][1].activate()
                self.blocks[1][3].activate()
                self.blocks[2][3].activate()
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
        self.blocks[1][2].activate() # Pivot Point
        self.blocks[1][0].activate()
        self.blocks[1][1].activate()
        self.blocks[1][3].activate()
        self.color = 'cyan'

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[1][0].deactivate()
            self.blocks[1][1].deactivate()
            self.blocks[1][3].deactivate()
            self.blocks[0][2].activate()
            self.blocks[2][2].activate()
            self.blocks[3][2].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            if self.check_movement(-1) and self.check_movement(1):
                self.blocks[0][2].deactivate()
                self.blocks[2][2].deactivate()
                self.blocks[3][2].deactivate()
                self.blocks[1][0].activate()
                self.blocks[1][1].activate()
                self.blocks[1][3].activate()
                self.rotation_stage = 0

class PieceT(Piece):
    """Class for the piece T"""

    def __init__(self):
        super().__init__('T')
        self.blocks[1][2].activate() # Pivot Point
        self.blocks[1][1].activate()
        self.blocks[1][3].activate()
        self.blocks[2][2].activate()
        self.color = 'magenta'

    def rotate(self):
        if self.rotation_stage == 0:
            self.blocks[1][1].deactivate()
            self.blocks[0][2].activate()
            self.rotation_stage = 1
        elif self.rotation_stage == 1:
            if self.check_movement(-1):
                self.blocks[2][2].deactivate()
                self.blocks[1][1].activate()
                self.rotation_stage = 2
        elif self.rotation_stage == 2:
            self.blocks[1][3].deactivate()
            self.blocks[2][2].activate()
            self.rotation_stage = 3
        elif self.rotation_stage == 3:
            if self.check_movement(1):
                self.blocks[0][2].deactivate()
                self.blocks[1][3].activate()
                self.rotation_stage = 0

class Platform(Canvas):
    """Game Platform Class"""
    def __init__(self, player, root):
        super().__init__(width=Tetris.PLATFORM_WIDTH, height=Tetris.PLATFORM_HEIGHT\
            , background='black')
        self.focus_set()
        self.root = root
        self.__init_game(player)
        self.pack()

    def __init_game(self, player):
        """initializes the game"""
        self.__in_tutorial = True
        self.__in_game = True
        self.__in_menu = False
        self.__is_speed_up = False
        self.__player = player
        self.__lines = 0
        self.__level = 1
        self.__current_piece = self.__select_random_piece()
        self.__next_piece = self.__select_random_piece()
        self.__background = PhotoImage(file="bg.gif")
        self.__tutorial = PhotoImage(file="tutorial.gif")
        self.__game_over = PhotoImage(file="game_over.gif")
        self.__backup_delay = Tetris.DELAY
        self.blocks = init_matrix(Tetris.COLS, Tetris.ROWS)
        self.bind_all('<Key>', self.__on_key_pressed)
        self.bind('<KeyRelease>', self.__on_key_released)
        self.tutorial()

    def __select_random_piece(self):
        """Returns a random piece"""
        chosen_type = choice(Tetris.PIECE_TYPES)
        chosen_type = 'O'
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

    def __on_key_released(self, event):
        """handles keyboard key released"""
        key = event.keysym
        if key == 'Down':
            Tetris.DELAY = self.__backup_delay
            self.__is_speed_up = False

    def __on_key_pressed(self, event):
        """handles keyboard """
        key = event.keysym
        if key == 'Right':
            self.__current_piece.move_right(self.blocks)
            self.__update_screen()
        elif key == 'Left':
            self.__current_piece.move_left(self.blocks)
            self.__update_screen()
        elif key == 'Up':
            self.__current_piece.rotate()
            self.__update_screen()
        elif key == 'Down':
            if not self.__is_speed_up:
                self.__is_speed_up = True
                self.__backup_delay = Tetris.DELAY
                Tetris.DELAY = Tetris.SPEED_UP_DELAY
        elif key == 'Escape':
            if not self.__in_tutorial:
                self.game_over()
        elif key == 'Return':
            if self.__in_tutorial:
                self.after_cancel(self.__current_job)
                self.__in_tutorial = False
                self.__in_menu = False
                self.__current_job = self.after(Tetris.DELAY, self.__tick)
            elif not self.__in_game and not self.__in_menu:
                self.after_cancel(self.__current_job)
                self.destroy()
                self.__in_menu = True
                Menu(self.__player.get_player_name(), self.root)

    def __update_screen(self):
        """ Updates the screen """
        self.delete(ALL)
        self.__draw_platform()
        self.__draw_current_piece()
        self.__draw_ui()

    def __tick(self):
        """creates a game cycle each timer event"""
        if self.__in_game:
            self.__update_screen()

            # Checking if the current piece is colliding with the platform
            if not self.__is_colliding_with_platform():
                # Moving down the current piece by one block
                self.__current_piece.gravity()
            else:
                # Checking if the current piece is on the top limit
                if self.__check_game_over():
                    self.game_over()
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
        temp = self.__lines // Tetris.LINES_LEVEL_UP

        if temp >= 1 and temp + 1 != self.__level:
            self.__level = (self.__lines // Tetris.LINES_LEVEL_UP) + 1
            if self.__is_speed_up:
                Tetris.DELAY = self.__backup_delay
            Tetris.DELAY = clamp(Tetris.DELAY - 80, 50, Tetris.DELAY)
            self.__backup_delay = Tetris.DELAY

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

        # Deactiving the lines
        temp = []
        for row in lines:
            for block in row:
                temp.append(block.get_pos_y())
                block.deactivate()
        min_y_index = (min(temp)-1) // Tetris.BLOCK_SIZE

        # Dropping the hanging blocks
        for y_index in range(Tetris.ROWS-1-lines_sum, -1, -1):
            for x_index in range(Tetris.COLS-1, -1, -1):
                block = self.blocks[y_index][x_index]
                if y_index <= min_y_index and block.is_activated():
                    temp_b = Block()
                    temp_b.deactivate()
                    temp_b.set_pos_x(x_index)
                    temp_b.set_pos_y(y_index)
                    block.set_pos_y(block.get_pos_y() + Tetris.BLOCK_SIZE * lines_sum)
                    self.blocks[y_index + lines_sum][x_index] = block
                    self.blocks[y_index][x_index] = temp_b

    def __merge_current_piece(self):
        """Merges the current piece with the platform"""
        for row in self.__current_piece.get_blocks():
            for block in row:
                if block.is_activated():
                    x_index = block.get_pos_x() // Tetris.BLOCK_SIZE
                    y_index = block.get_pos_y() // Tetris.BLOCK_SIZE
                    self.blocks[y_index][x_index] = block

    def __check_game_over(self):
        """Checks if the spawned piece is overlapping on another piece"""
        for row in self.__current_piece.get_blocks():
            for block in row:
                if block.is_activated():
                    x_index = block.get_pos_x() // Tetris.BLOCK_SIZE
                    y_index = block.get_pos_y() // Tetris.BLOCK_SIZE
                    try:
                        if self.blocks[y_index][x_index].is_activated():
                            return True
                    except IndexError:
                        return False
        return False

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
            fill='white', font=('Arial', 10))
        self.create_text(425, 117, text='{}'.format(self.__player.get_score()),\
            fill='white', font=('Arial', 15))
        self.create_text(454, 332, text='{}'.format(self.__lines),\
            fill='white', font=('Arial', 15))
        self.create_text(454, 240, text='{}'.format(self.__level),\
            fill='white', font=('Arial', 15))

    def tutorial(self):
        """draws the screen of the tutorial"""
        self.delete(ALL)
        self.create_image(0, 0, anchor=NW, image=self.__tutorial)
        self.__current_job = self.after(1000, self.tutorial)

    def game_over(self):
        """Deletes all objects and draw end game information"""
        self.__in_game = False
        self.delete(ALL)
        self.after_cancel(self.__current_job)
        self.create_image(0, 0, anchor=NW, image=self.__game_over)
        self.create_text(275, 162+50, text='Joueur: {}'.format(self.__player.get_player_name()),\
            fill='white', font=('Arial', 15))
        self.create_text(275, 162+50*2, text='Niveau: {}'.format(self.__level),\
            fill='white', font=('Arial', 15))
        self.create_text(275, 162+50*3, text='Score: {}'.format(self.__player.get_score()),\
            fill='white', font=('Arial', 15))
        self.__current_job = self.after(1000, self.game_over)

class Menu(Canvas):
    """Menu Canvas"""
    def __init__(self, player_name, root):
        super().__init__(width=Tetris.PLATFORM_WIDTH, height=Tetris.PLATFORM_HEIGHT\
            , background='black')
        self.root = root
        self.player_name = player_name
        self.__background = PhotoImage(file='home.gif')
        self.__play_btn_img = PhotoImage(file='play_btn.gif')
        self.__exit_btn_img = PhotoImage(file='exit_btn.gif')
        self.focus_set()
        self.__init_menu()

        self.pack()

    def __init_menu(self):
        self.create_image(0, 0, anchor=NW, image=self.__background)
        self.__draw_buttons()

    def __draw_buttons(self):
        play_btn = Button(self, command=self.__play_game)
        play_btn.config(image=self.__play_btn_img, width=296, height=77, bd=0,\
            bg='black', activebackground='black')
        play_btn.place(relx=1, x=-127, y=201, anchor=NE)

        exit_btn = Button(self, command=self.root.destroy)
        exit_btn.config(image=self.__exit_btn_img, width=296, height=77, bd=0,\
            bg='black', activebackground='black')
        exit_btn.place(relx=1, x=-127, y=322, anchor=NE)

    def __play_game(self):
        self.delete(ALL)
        self.destroy()
        Platform(Player(self.player_name), self.root)

class Tetris(Frame):
    """Main Tetris Class"""
    PIECE_TYPES = ['O', 'I', 'S', 'Z', 'L', 'J', 'T']
    PLATFORM_WIDTH = 550
    PLATFORM_HEIGHT = 540
    LINES_LEVEL_UP = 4 # Chaque 4 ligne le joueur gagne un niveau
    ROWS = 18
    COLS = 10
    BLOCK_SIZE = 30
    DELAY = 500
    SPEED_UP_DELAY = 25

    def __init__(self, player_name, root):
        super().__init__()

        self.master.title('Tetris - Houssem - ISTY')
        self.menu = Menu(player_name, root)
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
    tetris_game = Tetris(player_name, root)
    root.mainloop()

if __name__ == '__main__':
    main()
