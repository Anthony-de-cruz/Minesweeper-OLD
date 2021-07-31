import os, random, sys
import pygame, pygame_menu
from pygame_menu.examples import create_example_window


class startMenu():

    """Menu class"""

    def __init__(self):

        self.window = create_example_window("Minesweeper - Start Menu", (600, 400)) # To be hardcoded
        self.menu = pygame_menu.Menu(
                                    width = 600,
                                    height = 400,
                                    title = "Minesweeper",
                                    theme = pygame_menu.themes.THEME_DARK
                                    )
        self.field_width = self.menu.add.text_input("Width: ", default = "800")
        self.field_height = self.menu.add.text_input("Height:", default = "800")
        self.menu.add.button('Play', self.startGame)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu.enable()


    def startGame(self):

        print("Less gooo")
        self.menu.disable()


class mainGame():

    """Game class"""

    def __init__(self,):

        

        self.window = self.setupWindow()
    
    def setupWindow(self, field_width, field_height):

        self.field_width = field_width
        self.field_height = field_height

        pass







def main():

    pygame.init()

    start_menu = startMenu()

    #game = mainGame()

    # Begin the game with the start menu
    start_menu_active = True

    ## Main loop
    while True:


        if start_menu_active:
            start_menu.menu.mainloop(start_menu.window)

            start_menu_active = False




        ## Event Handler
        for event in pygame.event.get():


            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    print("ESC")


            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            




        # Update Screen
        pygame.display.flip()




if __name__ == "__main__":

    main()