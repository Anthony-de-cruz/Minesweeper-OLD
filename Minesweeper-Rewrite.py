import os, random, sys
import pygame, pygame_menu

# ---------------------------------------------------------------------------- #
#                               Start Menu Object                              #
# ---------------------------------------------------------------------------- #

class startMenu():

    """Menu class"""

    def __init__(self, int_chars):

        self.int_chars = int_chars

        # Setup window
        pygame.display.set_caption(("Minesweeper - Start Menu"))
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.window = pygame.display.set_mode((700, 500))

        # Set default field dimentions
        self.field_width = 800
        self.field_height = 800
        self.field_columns = 20
        self.field_rows = 20

        # Set difficulty list and default difficulty
        self.difficulty_list = [("Hard", 80),("Normal", 60),("Easy", 40)]
        self.difficulty = self.difficulty_list[1]

        # Create menu widgets
        self.menu = pygame_menu.Menu(
                                        width = 700,
                                        height = 500,
                                        title = "Minesweeper",
                                        theme = pygame_menu.themes.THEME_DARK
                                    )

        self.menu.add.text_input(
                                    "Field Width: ",
                                    default = "800",
                                    maxchar = 4,
                                    valid_chars = self.int_chars,
                                    onchange = self.setFieldWidth
                                )
        self.menu.add.text_input(
                                    "Field Height: ",
                                    default = "800",
                                    maxchar = 4,
                                    valid_chars = self.int_chars,
                                    onchange = self.setFieldHeight
                                )
        self.menu.add.text_input(
                                    "Field Columns: ",
                                    default = "20",
                                    maxchar = 2,
                                    valid_chars = self.int_chars,
                                    onchange = self.setFieldColumns
                                )
        self.menu.add.text_input(
                                    "Field Rows: ",
                                    default = "20",
                                    maxchar = 2,
                                    valid_chars = self.int_chars,
                                    onchange = self.setFieldRows
                                )

        self.menu.add.selector(
                                "Difficulty: ",
                                self.difficulty_list,
                                onchange = self.setDifficulty,
                            )

        self.menu.add.button('Play', self.startGame)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.enable()

    # Text entry and selector value functions
    def setFieldWidth(self, value):
        if value != "": self.field_width = int(value)
        else: self.field_width = 0

    def setFieldHeight(self, value):
        if value != "": self.field_height = int(value)
        else: self.field_height = 0

    def setFieldColumns(self, value):
        if value != "": self.field_columns = int(value)
        else: self.field_columns = 0

    def setFieldRows(self, value):
        if value != "": self.field_rows = int(value)
        else: self.field_rows = 0

    def setDifficulty(self, difficulty, _):
        self.difficulty = difficulty[1]

# ---------------------------------- Methods --------------------------------- #

    def startGame(self):

        """Method to begin the game"""

        print("Less gooo")

        if (
                self.field_width < self.field_columns or
                self.field_height < self.field_width or
                self.field_columns <= 0 or
                self.field_rows <= 0
            ):
            
            print("Invalid entries")
            return False
            #todo Make sure this error is visible to the user
        
        else:
            print("all good in the hood")
            self.menu.disable()
            return True


# ---------------------------------------------------------------------------- #
#                                  Game Object                                 #
# ---------------------------------------------------------------------------- #

class minesweeper():

    """Game class"""

    def __init__(self, field_width, field_height, field_columns, field_rows, difficulty):

        # Game dimentions
        self.field_width = field_width
        self.field_height = field_height
        self.field_columns = field_columns
        self.field_rows = field_rows

        self.tile_width = int(self.field_width / self.field_columns)
        self.tile_height = int(self.field_height / self.field_rows)

        self.topbar_thickness = int(field_height / 20)

        self.window_width = self.field_width
        self.window_height = self.field_height + self.topbar_thickness

        # Difficulty
        self.difficulty = difficulty

        # Set uncovered bool for enacting mine generation
        self.uncovered = False

        self.window = self.setupWindow()
        self.grid = self.setupGrid()

        

# ---------------------------------- Methods --------------------------------- #

    def setupWindow(self):

        """Method to setup game window"""

        self.field_width
        self.field_height

        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(("Minesweeper"))
        os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    def setupGrid(self):

        """Method to setup grid table"""

        self.grid = {}

        for x in range(self.field_columns):
            for y in range(self.field_rows):
                # Each tile will be it's own key containing a list 4 elements:
                # (
                # Is mine (True/False),
                # Mines in proximity(int),
                # Is covered (True/False),
                # Is flagged (True/False)
                # )
                self.grid[f"{x},{y}"] = (False, 0, True, False)
    
    def generateMinefield(self):

        """Method to generate minefield"""
        #todo do 
        pass

    def mouseInputs(self, mouse):

        """Method to handle mouse inputs"""

        self.mouse_position = pygame.mouse.get_pos()

        clicked_x = self.mouse_position[0] // self.tile_width
        clicked_y = (self.mouse_position[1] // self.tile_height) - 1

        if self.uncovered:
            # Identify which button is being pressed and act accordingly
            if mouse.button == 1:
                        print("Left Click")

            elif mouse.button == 3:
                        print("Right Click")
        
        else:
            self.generateMinefield()
            self.uncovered = True

        print(
                f"  {self.mouse_position[0]}, {self.mouse_position[0]}\n" +
                f"  {clicked_x}, {clicked_y}"
            )
        
        def drawScreen(self):
            #todo do
            pass

# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #

def main():

    pygame.init()

    int_chars = [0,1,2,3,4,5,6,7,8,9]
    start_menu = startMenu(int_chars)
    start_menu_enabled = True

    colours = {
        "Black": (20,20,20),
        "White": (255,255,255),
        "Grey":  (60,60,60),
        "Green": (0,150,0)
    }

# --------------------------------- Main Loop -------------------------------- #

    ## Main loop
    while True:

        ## Toggle Start menu
        while start_menu_enabled:
            
            # Returns true or false depending on whether or not
            # the user entries are valid
            if start_menu.menu.mainloop(start_menu.window):
            
                print(
                        f"{start_menu.field_width},{start_menu.field_height}\n"
                        + f"{start_menu.field_columns},{start_menu.field_rows}\n"
                        + f"{start_menu.difficulty}"
                )

                game = minesweeper(
                                    start_menu.field_width,
                                    start_menu.field_height,
                                    start_menu.field_columns,
                                    start_menu.field_rows,
                                    start_menu.difficulty,
                                    colours
                                )

                start_menu_enabled = False


        ## Event Handler
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    print("ESC")
                    # to activate in game menu which is to be made
            
            elif event.type == pygame.MOUSEBUTTONDOWN:

                game.mouseInputs(event)


            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        # Update Screen
        pygame.display.flip()




if __name__ == "__main__":

    main()
