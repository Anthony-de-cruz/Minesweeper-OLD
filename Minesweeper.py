import pygame
import os
import sys
import random



def main():

    """Main"""

    pygame.init()

    ## Dimentions
    # Play area width and height will be the mine field graphical dimentions
    # whereas columns and rows will be the number of tiles
    playarea_width, playarea_height = 800, 800
    columns, rows = 20, 20
    
    # Window width and height will be the actual window itself
    window_width = playarea_width
    window_height = playarea_height

    # Sizes for each tile
    tile_width = int(playarea_width / columns)
    tile_height = int(playarea_height / rows)

    # Top bar thickness is determined by window height, which is then added
    topbar_thickness = int(window_height / 20)
    window_height += topbar_thickness

    # Number of mines
    mine_count = 30
    flag_count = mine_count

    # Mines are generated once you have clicked the first tile as to
    # avoid clicking on a mine first time
    initial_uncover = False

    ## Colours dictionary
    colours = {
        "Black": (20,20,20),
        "White": (255,255,255),
        "Grey":  (60,60,60),
        "Green": (0,150,0),
    }

    ## Fonts
    # Font Syntax: font name, size, bold, italic
    # Render syntax: text, antialiasing, colour
    #//text = proximity_font.render("Hellooooooo", True, colours["White"])
    proximity_font = pygame.font.SysFont("Verdana", int(tile_height / 2), False, False)
    proximity_font_dimentions = {}
    
    for number in range(8):
        proximity_font_dimentions[str(number)] = proximity_font.size(str(number))
    
    print(f"""\nWindow Geometry:
    Window width:{window_width}
    Window height:{window_height}
    Top bar thickness:{topbar_thickness}
    Tile width:{tile_width}
    Tile height:{tile_height}
    Proximity font dimentions:
    {proximity_font_dimentions}""")

    window = setupWindow(window_width,window_height, topbar_thickness)

    grid = createGrid(columns, rows)
    #//print(grid)
    


    ## Main Loop
    while True:


        ## Event Handler
        for event in pygame.event.get():


            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                clicked_x = mouse_position[0] // tile_width
                clicked_y = (mouse_position[1] // tile_height) - 1

                # Left click
                if event.button == 1:
                    print("Left click")

                    if initial_uncover == False:

                        createMinefield(grid, columns, rows, mine_count, clicked_x, clicked_y)

                        initial_uncover = True

                    # Check to see if it is in the grid
                    if f"{clicked_x},{clicked_y}" in grid:

                        print(f"{clicked_x},{clicked_y}")

                        # Check to see if it is covered
                        if grid[f"{clicked_x},{clicked_y}"][2]:

                            print("Uncover")

                            uncover(grid, columns, rows, clicked_x, clicked_y)
                            
                    
                    else:
                        print("Not in grid")
                    
                    
                # Right Click
                if event.button == 3:
                    print("Right click")

                    # Check to see if it is in the grid
                    if f"{clicked_x},{clicked_y}" in grid:

                        print(f"{clicked_x},{clicked_y}")

                        # Check to see if it is covered
                        if grid[f"{clicked_x},{clicked_y}"][2]:

                            print("Flag")

                            flag(grid, columns, rows, clicked_x, clicked_y)

                            

                        
                    
                print(mouse_position, event.button,"\n")

            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        drawScreen(window,
                   window_width, window_height,
                   tile_width, tile_height,
                   topbar_thickness,
                   colours,
                   grid, columns, rows,
                   proximity_font, proximity_font_dimentions)

        
       
        # Update display
        pygame.display.flip()



def setupWindow(window_width, window_height, topbar_thickness):

    """Setup the window"""
    
	# Create and center window
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption(("Minesweeper"))
    window = pygame.display.set_mode((window_width, window_height))

    return window



def createGrid(columns, rows):

    """Create new grid dictionary"""

    grid = {}

    for x in range(columns):
        for y in range(rows):
            # Each tile will be it's own key containing a list 3 elements:
            # [Is mine (True/False), Mines in proximity(int) , Is covered (True/False), Is flagged (True/False)]
            grid[f"{x},{y}"] = [False, 0, True, False]
    
    return grid



def createMinefield(grid, columns, rows, mine_count, clicked_x, clicked_y):

    """Fill in field with mines"""

    #todo prevent generation in proximity of starting tile so you don't click on a number

    # Temporary instance of the rotation_list, will likely move this elsewhere since it is
    # used both in createMinefield() and uncover()
    rotation_list = [(-1, -1),(0, -1),(1, -1),(1, 0),(1, 1),(0, 1),(-1, 1),(-1, 0)]

    # While loop to create a mine mine_count number of times
    while mine_count > 0:

        random_x = random.randint(0, columns - 1)
        random_y = random.randint(0, rows - 1)

        # Check that a mine isn't being generated where the user clicked or ontop of another mine
        if (
            (random_x, random_y) != (clicked_x, clicked_y)
            and grid[f"{random_x},{random_y}"][0] != True
            ):

            grid[f"{random_x},{random_y}"][0] = True

            mine_count -= 1

            # A loop to increase the mines in proximity count for all surrounding tiles
            for rotation in range(8):
                
                # Check that it isn't trying to access a non existant tile
                if (
                        random_x + rotation_list[rotation][0] >= 0 
                    and random_y + rotation_list[rotation][1] >= 0
                    and random_x + rotation_list[rotation][0] <= columns - 1
                    and random_y + rotation_list[rotation][1] <= rows -1
                    ):

                        # Increase mines in proximity
                        grid[(f"{random_x + rotation_list[rotation][0]},"
                              f"{random_y + rotation_list[rotation][1]}")][1] += 1



def uncover(grid, columns, rows, x, y):

    """Recursive function to uncover an area when clicked"""

    # This is a list containing the offset for all the tiles around a given tile, might redo this later
    rotation_list = [(-1, -1),(0, -1),(1, -1),(1, 0),(1, 1),(0, 1),(-1, 1),(-1, 0)]

    # For loop to check around the clicked tile clockwise starting from the top left
    if grid[f"{x},{y}"][2]:
        grid[f"{x},{y}"][2] = False

        # If not a mine or in proximity of a mine
        if grid[f"{x},{y}"][1] == 0 and grid[f"{x},{y}"][0] == False:

            

            for rotation in range(8):
                
                # Check that it isn't trying to access a non existant tile
                if (
                        x + rotation_list[rotation][0] >= 0
                    and y + rotation_list[rotation][1] >= 0
                    and x + rotation_list[rotation][0] <= columns - 1
                    and y + rotation_list[rotation][1] <= rows - 1
                    ):
                    
                        uncover(grid, columns, rows, 
                        x + rotation_list[rotation][0],
                        y + rotation_list[rotation][1])

                pass

def flag(grid, columns, rows, x, y):

    """Flag a mine"""

    if grid[f"{x},{y}"][2] == True:

        if grid[f"{x},{y}"][3] == True: grid[f"{x},{y}"][3] = False

        elif grid[f"{x},{y}"][3] == False: grid[f"{x},{y}"][3] = True

        
        
        

def drawScreen(window, window_width, window_height,
               tile_width, tile_height,
               topbar_thickness,
               colours,
               grid, columns, rows,
               proximity_font, proximity_font_dimentions):

    """Draw the screen"""

    # Background fill
    window.fill(colours["Black"])

    # Stats Bar
    pygame.draw.rect(window,
	(colours["Black"]),
	(0, 0, window_width, topbar_thickness))

    pygame.draw.rect(window,
    (colours["Green"]),
    (200,200, 40,40))
    

    for x in range(columns):
        for y in range(rows):

            # If covered, draw as so
            if grid[f"{x},{y}"][2] == True:

                pygame.draw.rect(window,
                (colours["Green"]),
                (x * tile_width, y * tile_height + topbar_thickness , tile_width, tile_height))

                
                # If flagged, draw as so
                if grid[f"{x},{y}"][3] == True:

                    pygame.draw.rect(window,
                    (colours["Grey"]),
                    (x * tile_width, y * tile_height + topbar_thickness , tile_width - 5, tile_height - 5))
                    
            
            # If not covered and not a mine, draw as so
            elif grid[f"{x},{y}"][2] == False and grid[f"{x},{y}"][0] == False:

                text = proximity_font.render(str(grid[f"{x},{y}"][1]), True, colours["White"])
                
                #proximity_font_dimentions[str(grid[f"{x},{y}"][1])][0] / 2 for the width centering
                #proximity_font_dimentions[str(grid[f"{x},{y}"][1])][1] / 4 for the height centering
                window.blit(text,
                (x * tile_width + tile_width / 2 - int(proximity_font_dimentions[str(grid[f"{x},{y}"][1])][0] / 2),
                 y * tile_height + tile_width / 2 + topbar_thickness / 2 + int(proximity_font_dimentions[str(grid[f"{x},{y}"][1])][1] / 4)))

            # If not covered and is a mine, draw as so
            elif grid[f"{x},{y}"][2] == False and grid[f"{x},{y}"][0] == True:

                text = proximity_font.render(("B"), True, colours["White"])
                
                #proximity_font_dimentions[str(grid[f"{x},{y}"][1])][0] / 2 for the width centering
                #proximity_font_dimentions[str(grid[f"{x},{y}"][1])][1] / 4 for the height centering
                window.blit(text,
                (x * tile_width + tile_width / 2 - int(proximity_font_dimentions[str(grid[f"{x},{y}"][1])][0] / 2),
                 y * tile_height + tile_width / 2 + topbar_thickness / 2 + int(proximity_font_dimentions[str(grid[f"{x},{y}"][1])][1] / 4)))



if __name__ == "__main__":

    main()


