# Minesweeper
[Minesweeper.py](Minesweeper.py):<br/>
 - A simple version of Minesweeper built on [Python 3](https://www.python.org) + [Pygame](https://www.pygame.org)

[Minesweeper Rewrite.py](Minesweeper-Rewrite.py):<br/>
 - A simple version of Minesweeper built on [Python 3](https://www.python.org) + [Pygame](https://www.pygame.org) + [Pygame_Menu](https://github.com/ppizarror/pygame-menu) that is a code overhaul of [Minesweeper.py](Minesweeper.py) including a new menu system.


![alt text](screenshot.png)
## For old:
### To Do:

- Fleshed out Flagging system:
    
  - Tally total flags and compare to total mines
    
- Game end state:
    
  - Game over screen
  - Game win screen
    
- Game statistics:
    
  - Time
  - Number of mines remaining
  - Total Flags
  - Dimentions
    
- Mine generation overhaul:
    
  - Balance an actually good number of mines
  - Make sure mines spawn in completable formations (such as 9 mines in a 3x3 space)
        
- Difficulties:
    
  - Mine densities ect
        
- Graphics overhaul:

  - Create animations for flagging and uncovering,
  - Create different colour themes
    
- Function improvement:
    
  - Figure out how to lower function parameters and organisation, 13 parameters for drawScreen() ain't good

### Done:
        
- Added an actual flag sprite,
- Ensured playable area upon mine generation
- Created main application setup,
- Created inputs/outputs,
- Created graphics,
- Basic mine generation,
- Basic flagging,
- Basic uncovering
