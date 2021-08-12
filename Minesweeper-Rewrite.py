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
            #todo Also alter acceptable parameters further to
            #todo prevent more breaking
        
        else:
            self.menu.disable()
            return True


# ---------------------------------------------------------------------------- #
#                                  Game Object                                 #
# ---------------------------------------------------------------------------- #

class minesweeper():

    """Game class"""

    def __init__(self, field_width, field_height, field_columns, field_rows, difficulty, COLOURS):

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

        # Difficulty as selected in the start menu and set the flag count accordingly
        self.difficulty = difficulty
        self.flag_count = difficulty[1]

        # Colours constant dictionary
        self.COLOURS = COLOURS

        # List for the different coordinate offsets for an 8 pointed turn around a point
        # I'm not really sure if that's a great way of doing it but it works for now
        self.rotation_list = [(-1, -1),(0, -1),(1, -1),(1, 0),(1, 1),(0, 1),(-1, 1),(-1, 0)]

        # Set uncovered bool for enacting mine generation
        self.uncovered = False


        self.setupWindow()
        self.setupGrid()
        self.loadAssets()


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
                # [
                # Is mine (True/False),
                # Mines in proximity(int),
                # Status ("uncovered"/"covered"/"flagged")
                # ]
                self.grid[f"{x},{y}"] = [False, 0, "covered"]


    def loadAssets(self):

        """Method to load assets including images and fonts"""

        ## Images
        #* Change path to assets/flag.png when compiling

        # Load flag icon and scaled to 70% of a tile
        self.flag_icon = pygame.transform.smoothscale(
        pygame.image.load(os.path.join(os.path.dirname(__file__), 'assets','flag.png')),
        (int(self.tile_width  * 0.7), int(self.tile_height * 0.7)))

        ## Fonts
        # Font Syntax: font name, size, bold, italic

        # Set the font size to be the smallest out of the tile width and height
        if self.tile_width <= self.tile_height: font_size = int(self.tile_width / 2)
        elif self.tile_width >= self.tile_height: font_size = int(self.tile_height / 2)

        self.tile_font = pygame.font.SysFont("Verdana", font_size, False, False)
        self.timer_font = pygame.font.SysFont("Verdana", font_size, False, False)
        
        # Render of the B, this is done here rather than in drawScreen() as this should
        # be unchanging so it is a waste to re render it when drawing each time
        # Render syntax: text, antialiasing, colour
        self.tile_font_bomb_render = self.tile_font.render(
                                                            "B", 
                                                            True, 
                                                            self.COLOURS["White"]
                                                        )


    def generateMinefield(self, clicked_x, clicked_y):

        """Method to generate minefield"""
        
        mines_to_place = self.difficulty[1]
        
        while mines_to_place > 0:

            random_x = random.randint(0, self.field_columns - 1)
            random_y = random.randint(0, self.field_rows - 1)

            # Check to see if the random coords are not where the user clicked or
            # where a mine has already been placed
            if (
                    (random_x, random_y) != (clicked_x, clicked_y) and
                    self.grid[f"{random_x},{random_y}"][0] != True
            ):

                # Check to see if the random coords are in proximity of where the
                # user clicked, if so, don't place a mine there
                in_proximity = False
                for rotation in self.rotation_list:

                    if (
                        (random_x + rotation[0], random_y + rotation[0]) ==
                        (clicked_x, clicked_y)
                    ): in_proximity = True
                
                if in_proximity: continue

                # Set a mine
                self.grid[f"{random_x},{random_y}"][0] = True

                mines_to_place -= 1

                # Loop to update all surrounding tiles with new mines in proximity
                for rotation in self.rotation_list:
                
                    # Check that it isn't trying to access a non existant tile
                    if (
                            random_x + rotation[0] >= 0 
                        and random_y + rotation[1] >= 0
                        and random_x + rotation[0] <= self.field_columns - 1
                        and random_y + rotation[1] <= self.field_rows -1
                        ):

                            # Increase mines in proximity
                            self.grid[(f"{random_x + rotation[0]},"
                                    f"{random_y + rotation[1]}")][1] += 1


    def mouseInputs(self, mouse):

        """Method to handle mouse inputs"""

        self.mouse_position = pygame.mouse.get_pos()

        clicked_x = self.mouse_position[0] // self.tile_width
        clicked_y = (self.mouse_position[1] // self.tile_height) - 1

        # Check to see if the tile set has a minefield
        if self.uncovered:
            # Identify which button is being pressed and act accordingly
            if mouse.button == 1:
                        print("Left Click")

                        if f"{clicked_x},{clicked_y}" in self.grid:

                            if self.grid[f"{clicked_x},{clicked_y}"][2] == "covered":

                                self.grid[f"{clicked_x},{clicked_y}"][2] = "uncovered"
                                #todo Uncover
                                print("  Uncovered")

                            elif self.grid[f"{clicked_x},{clicked_y}"][2] == "flagged":

                                print(self.flag(clicked_x, clicked_y))

                            else: print("  Already uncovered")
                        
                        else: print("  Outside grid")

            elif mouse.button == 3:
                        print("Right Click")

                        if f"{clicked_x},{clicked_y}" in self.grid:
                            
                            if (
                                self.grid[f"{clicked_x},{clicked_y}"][2] == "covered" or
                                self.grid[f"{clicked_x},{clicked_y}"][2] == "flagged"
                            ):
                                print(self.flag(clicked_x, clicked_y))


                        else: print("  Outside grid")
                        

        # Create a new mine field
        else:
            self.generateMinefield(clicked_x, clicked_y)
            self.uncovered = True

        print(
                f"  {self.mouse_position[0]}, {self.mouse_position[0]}\n" +
                f"  {clicked_x}, {clicked_y}"
            )


    def uncover(self):

        """Method to uncover an area recursively when clicked"""

        #todo
        pass


    def flag(self, x, y):

        """Method to control the flagging of tiles"""

        if self.grid[f"{x},{y}"][2] == "covered":

            self.grid[f"{x},{y}"][2] = "flagged"
            self.flag_count += 1
            return "  Flagged"

        elif self.grid[f"{x},{y}"][2] == "flagged":

            self.grid[f"{x},{y}"][2] = "covered"
            self.flag_count -= 1
            return "  Unflagged"


    def drawScreen(self):

        """Method to draw the screen"""

        # Fill background
        self.window.fill(self.COLOURS["Black"])

        # Stats Bar
        pygame.draw.rect(self.window,
        (self.COLOURS["Black"]),
        (0, 0, self.window_width, self.topbar_thickness))

        # Draw Grid
        for x in range(self.field_columns):
            for y in range(self.field_rows):

                if self.grid[f"{x},{y}"][2] == "covered":

                    pygame.draw.rect(self.window,
                    (self.COLOURS["Green"]),
                    (
                        x * self.tile_width,
                        y * self.tile_height + self.topbar_thickness,
                        self.tile_width,
                        self.tile_height
                    ))
                
                elif self.grid[f"{x},{y}"][2] == "flagged":

                    pygame.draw.rect(self.window,
                    (self.COLOURS["Grey"]),
                    (
                        x * self.tile_width + int(self.tile_width * 0.1),
                        y * self.tile_height + self.topbar_thickness +
                        int(self.tile_height * 0.1),
                        self.tile_width - int(self.tile_width * 0.2),
                        self.tile_height - int(self.tile_height * 0.2)
                    ))
                    #todo draw flag
                
                # If uncovered and not a mine and has a mine in proximity
                elif (
                        self.grid[f"{x},{y}"][2] == "uncovered" and 
                        self.grid[f"{x},{y}"][0] == False and 
                        self.grid[f"{x},{y}"][1] != 0
                    ):

                    tile_font_render = self.tile_font.render(
                                                                        str(self.grid[f"{x},{y}"][1]), 
                                                                        True, 
                                                                        self.COLOURS["White"]
                                                                    )
                    # Draw number of mines in proximity
                    self.window.blit(tile_font_render, (
                        x * self.tile_width + self.tile_width / 2 - 
                        int(self.tile_font.size(str(self.grid[f"{x},{y}"][1]))[0] / 2),
                        y * self.tile_height + self.tile_width / 2 +
                        int(self.tile_font.size(str(self.grid[f"{x},{y}"][1]))[1] / 2) +
                        self.topbar_thickness / 2)
                        )

                # If uncovered and is a mine
                elif (
                        self.grid[f"{x},{y}"][2] == "uncovered" and 
                        self.grid[f"{x},{y}"][0] == True
                    ):

                    # Draw bomb "B"
                    self.window.blit(self.tile_font_bomb_render, (
                        x * self.tile_width + self.tile_width / 2 - 
                        int(self.tile_font.size(str(self.grid[f"{x},{y}"][1]))[0] / 2),
                        y * self.tile_height + self.tile_width / 2 +
                        int(self.tile_font.size(str(self.grid[f"{x},{y}"][1]))[1] / 2) +
                        self.topbar_thickness / 2)
                        )



            #todo
            pass

# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #

def main():

    pygame.init()

    int_chars = [0,1,2,3,4,5,6,7,8,9]
    start_menu = startMenu(int_chars)
    start_menu_enabled = True

    COLOURS = {
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
                                    COLOURS
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


        game.drawScreen()

        # Update Screen
        pygame.display.flip()




if __name__ == "__main__":

    main()
