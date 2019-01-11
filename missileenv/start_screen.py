
# Usual modules
import sys
import codecs # For score file
import os # Used for checking file existence

# Unique modules
import pygame

# Custom modules
import missile_command

pygame.init() # Initialize pygame

clock = pygame.time.Clock() # Used to control framerate

# File macros
BG_COLOR = (143, 175, 180)
SCREEN_COLOR = (31, 45, 46)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDING = 16
FLASH_FREQ = 30

# Main Surface
window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Images
loadImg = pygame.image.load # To reduce lookup time
tScale = pygame.transform.scale
    # Intro image
introImg = loadImg("art/intro_background.png")
introW = window.get_width()
ratio = 1.0 + (introImg.get_width() / float(window.get_width()))
introH = int(introImg.get_height() * (ratio))
introImg= tScale(introImg, (introW, introH))
introImgX = int(window.get_width()/2 - introImg.get_width()/2)
introImgY = int(window.get_height()/2 - introImg.get_height()/2)
    # Console menu
# Two images for flashing animation
console1 = loadImg("art/console1.png")
console2 = loadImg("art/console2.png")

consoleSize = int(window.get_height())
consoleX = int(window.get_width() / 2 - consoleSize / 2)
consoleY = int(window.get_height() / 2 - consoleSize / 2)

console1 = tScale(console1, (consoleSize, consoleSize))
console2 = tScale(console2, (consoleSize, consoleSize))

# Console screen Surface
consoleScreen = pygame.Surface((int(consoleSize / 1.91), int(consoleSize / 3.6)))
# Transparency is messing with allowing me to draw on it. Removing for now.
# consoleScreen.fill((255, 255, 255), None, pygame.BLEND_RGBA_MULT)
# consoleScreen.set_alpha(0)
consoleScreen.fill(SCREEN_COLOR)

screenX = consoleX + int(window.get_width() * 0.15)
screenY = consoleY + int(window.get_height() * 0.175)

fontSize = int(consoleScreen.get_height() / 10)

# Mouse settings
pyMouse = pygame.mouse # To reduce lookup time
pyMouse.set_visible(False)
pyMouse.set_pos((int(window.get_width()/2), int(window.get_height()/2)))

'''
CLASS
    Handles the behavior of the main menu of the game. A Menu object is created
    to contain specific information on it, and runMenu must be called to start
    it. Displays options such as starting the game or changing settings.
'''
class Menu():
    # Preset mixer values. Last one, buffersize, is usually a bad default
    pygame.mixer.pre_init(44100, -16, 2, 256)
    pygame.mixer.init()

    # Audio
        # Main
    # music = pygame.mixer.music.load('sounds/main.ogg')
    music = pygame.mixer.Sound('sounds/console_trim.ogg')
    musicChannel = pygame.mixer.Channel(1)
        # Blip
    blip = pygame.mixer.Sound("sounds/blip.ogg")
    effectsChannel = pygame.mixer.Channel(2)
    effectsChannel.set_volume(effectsChannel.get_volume() / 3)

    # Intro screen
    introFont1 = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize*5).render("MISSILE", True, BLACK)
    x1 = introImgX + int(introImg.get_width()/2) - int(introFont1.get_width()/2)
    y1 = introImgY + int(introImg.get_height()/3)

    introFont2 = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize*5).render("COMMAND", True, BLACK)
    x2 = introImgX + int(introImg.get_width()/2) - int(introFont2.get_width()/2)
    y2 = y1 + introFont1.get_height() + fontSize

    introFont3 = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize*6).render("20XX", True, BLACK)
    x3 = introImgX + int(introImg.get_width()/2) - int(introFont3.get_width()/2)
    y3 = y2 + introFont2.get_height() + fontSize

    # Menu selections
        # Start Game
    startFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Start Mission", True, WHITE)

    startFontX = screenX + PADDING
    startFontY = screenY + PADDING

        # Settings
    optionFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Settings", True, WHITE)

    optionFontX = screenX + PADDING
    optionFontY = screenY + fontSize * 2 + PADDING

        # Scores
    scoreFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("High Scores", True, WHITE)

    scoreFontX = screenX + PADDING
    scoreFontY = screenY + fontSize * 4 + PADDING

        # Quit
    quitFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Quit", True, WHITE)

    quitFontX = screenX + PADDING
    quitFontY = screenY + fontSize * 6 + PADDING

    '''
    CONSTRUCTOR
        Parameters:
            Menu self

        Contains two inner objects that hold information on settings and scores.
        The settings are later passed to the game so it may behave accordingly.

        Returns:
            Menu object
    '''
    def __init__(self):
        self.settings = Settings(self)
        self.highScores = HighScores(self)
        self.effectsChannel = Menu.effectsChannel


    '''
    METHOD
        Parameters:
            Menu self

        Called to quit out of the program. Exits pygame and closes window.

        Returns:
            None
    '''
    def quitGame(self):
        pygame.quit()
        sys.exit()


    '''
    METHOD
        Parameters:
            Menu self
            int selection - The current menu option represented as an int. The
                            selector is drawn according to the selection, as it
                            is used to specify which option the player is
                            currently focusing on.

        Renders the selector animation used to show which menu option currently
        has focus. It is drawn based on the selection given, altering the height
        of the vertical line as well as the position of the box and vertical
        line. If you don't know what I mean by vertical line, box, and
        horizontal line, the run the game because I don't know how to explain it
        best without sounding confusing. It kind of looks like the lines and
        pound/hashtag sign below
         ____________
        | opt1 |     |
        | opt2 #-----|
        | opt3       |
        |____________|

        Returns
            None
    '''
    def renderSelector(self, selection):
        screen = consoleScreen # Surface object on top of computer image
        selXL = int(screen.get_width() * 0.6) # Leftmost
        selYT = 0 # Topmost
        selYB = selection * (fontSize * 2) + PADDING + int(fontSize / 2) # Bottommost
        selXR = screen.get_width() # Rightmost
        lineWeight = 4
        boxSize = 20
        # Gets added below which actually adds a negative number
        boxOffset = int(lineWeight / 2) - int(boxSize / 2)

        screen.fill(SCREEN_COLOR)

        # Vertical line
        pygame.draw.rect(screen, WHITE, (selXL, selYT, lineWeight, selYB))
        # Horizontal line
        pygame.draw.rect(screen, WHITE, (selXL, selYB, selXR, lineWeight))
        # Box
        pygame.draw.rect(screen, WHITE, (selXL + boxOffset, selYB + boxOffset,
                                              boxSize, boxSize))


    def playMusic(self):
        Menu.musicChannel.play(Menu.music, loops=-1)
        self.musicPlaying = True


    def playBlip(self):
        if self.settings.playEffects:
            Menu.effectsChannel.play(Menu.blip)


    '''
    METHOD
        Parameters:
            Menu self

        Considered the main loop of the menu portion of the game, this method
        handles the following:
            * Renders an image of a computer with flashing lights
            * Renders text on the computer screen as options
            * Renders an option selector
            * Handles input from keyboard by player to go through options and
              make selections
            * Controls the framerate of the menu screen
            * Allows the player to start or quit the game by selecting the
              appropriate options on the screen

        Returns:
            None
    '''
    def runMenu(self):
        animationCounter = 0 # Used to alternate between two console images
        consoles = [console1, console2] # List of the two images
        consoleIndex = 0 # Index for default starting image
        console = consoles[consoleIndex] # Default console image
        selection = 0 # Current option that has focus represented by an int
        input = -1 # The selection made by the user. Controls when to exit loop

        while input == -1:
            if animationCounter == FLASH_FREQ:
                consoleIndex = (consoleIndex + 1) % 2 # Change index
                console = consoles[consoleIndex] # Change image
                animationCounter = 0 # Reset (don't want too large an int)
            animationCounter += 1

            window.fill(BG_COLOR)
            window.blit(console, (consoleX, consoleY)) # Image
            window.blit(consoleScreen, (screenX, screenY)) # Surface
            window.blit(Menu.startFont, (Menu.startFontX, Menu.startFontY))
            window.blit(Menu.optionFont, (Menu.optionFontX, Menu.optionFontY))
            window.blit(Menu.scoreFont, (Menu.scoreFontX, Menu.scoreFontY))
            window.blit(Menu.quitFont, (Menu.quitFontX, Menu.quitFontY))
            self.renderSelector(selection) # selector that goes on consoleScreen

            # Get list of events since last update
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.playBlip()
                        # Focus on next option with overflow going back to top
                        selection = (selection + 1) % 4
                    elif event.key == pygame.K_UP:
                        self.playBlip()
                        # Focus on next option with overflow going to bottom
                        selection = (selection - 1) % 4
                    elif event.key == pygame.K_RETURN:
                        self.playBlip()
                        # Player selected an option
                        input = selection
                    elif event.key == pygame.K_ESCAPE:
                        self.quitGame()

            # Needed to show display changes
            pygame.display.update()

            # Framerate
            clock.tick(30)

        if input == 0: # Run game
            game = missile_command.Game(self, self.settings.difficulty, self.settings.controls)
            game.runGame()
        elif input == 1: # Display settings screen
            self.settings.runSettings()
        elif input == 2:
            self.highScores.runScores()
        elif input == 3: # Quit
            self.quitGame()


    def runIntro(self):
        x = 0
        while x <= 150:
            x += 1
            window.fill(BLACK)
            window.blit(introImg, (introImgX, introImgY))
            window.blit(Menu.introFont1, (Menu.x1, Menu.y1))
            window.blit(Menu.introFont2, (Menu.x2, Menu.y2))
            window.blit(Menu.introFont3, (Menu.x3, Menu.y3))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()
            clock.tick(30)

        self.playMusic()
        self.runMenu()



'''
CLASS
    Very similar to the Menu class but for displaying and handling a screen for
    game settings.
'''
class Settings():

    # Used to break out of the while loop before returning to main screen
    exit = False

    # Settings selections
        # Menu
    menuFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Main Screen", True, WHITE)

    menuFontX = screenX + PADDING
    menuFontY = screenY + PADDING

        # Difficulty
    diffFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Difficulty:", True, WHITE)
    diffFontE = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Easy", True, WHITE)
    diffFontN = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Normal", True, WHITE)
    diffFontH = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Hard", True, WHITE)

    diffFontX = screenX + PADDING
    diffFontY = screenY + fontSize * 2 + PADDING
    diffOptionX = screenX + PADDING * 3
    diffOptionY = screenY + fontSize * 3 + PADDING

        # Controls
    controlFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Controls:", True, WHITE)
    controlFontD = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Directional", True, WHITE)
    controlFontI = pygame.font.Font("fonts/space_age/space_age.ttf",
                    fontSize).render("Inverted", True, WHITE)

    controlFontX = screenX + PADDING
    controlFontY = screenY + fontSize * 4 + PADDING
    controlOptionX = screenX + PADDING * 3
    controlOptionY = screenY + fontSize * 5 + PADDING

        # Music
    musicFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                                    fontSize).render("Music:", True, WHITE)
    musicOn = pygame.font.Font("fonts/space_age/space_age.ttf",
                                        fontSize).render("ON", True, WHITE)
    musicOff = pygame.font.Font("fonts/space_age/space_age.ttf",
                                        fontSize).render("OFF", True, WHITE)

    musicFontX = screenX + PADDING
    musicFontY = screenY + fontSize * 6 + PADDING
    musicOptionX = screenX + PADDING * 3
    musicOptionY = screenY + fontSize * 7 + PADDING

        # Sound Effects
    effectsFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                                fontSize).render("Effects:", True, WHITE)
    effectsOn = pygame.font.Font("fonts/space_age/space_age.ttf",
                                        fontSize).render("ON", True, WHITE)
    effectsOff = pygame.font.Font("fonts/space_age/space_age.ttf",
                                        fontSize).render("OFF", True, WHITE)

    effectsFontX = screenX + PADDING
    effectsFontY = screenY + fontSize * 8 + PADDING
    effectsOptionX = screenX + PADDING * 3
    effectsOptionY = screenY + fontSize * 9 + PADDING


    '''
    CONSTRUCTOR
        Parameters:
            Settings self
            Menu menu - The Menu object that this object belongs to. Used to
                        reference back to run main menu screen once the player
                        is satisfied with the settings.

        The player's choice (or default) settings are stored within this.

        Returns:
            Settings object
    '''
    def __init__(self, mainMenu):
        self.menu = mainMenu # Menu object
        self.difficulty = 0 # 0 = Normal; 1 = Hard; 2 = Easy
        self.controls = 0 #  0 = Directional; 1 = Inverted
        self.playMusic = True # True = on; False = off
        self.playEffects = True # True = on; False = off


    def playBlip(self):
        if self.playEffects:
            self.menu.effectsChannel.play(Menu.blip)


    '''
    METHOD
        Parameters:
            Settings self
            int selection - The setting selected by the player to change,
                            represented by an integer.

        Allows the player to either exit back to the main menu or change the
        available settings including difficulty and controls.

        Returns:
            None
    '''
    def selectionAction(self, selection, move=pygame.K_RIGHT):
        if selection == 0: # Return to main menu
            Settings.exit = True # Used for exiting settings main loop
        elif selection == 1: # Change difficulty
            if move == pygame.K_RIGHT:
                self.difficulty = (self.difficulty + 1) % 3
            elif move == pygame.K_LEFT:
                self.difficulty = (self.difficulty - 1) % 3
        elif selection == 2: # Change controls
            self.controls = (self.controls + 1) % 2
        elif selection == 3: # Change music sound
            self.playMusic = not self.playMusic
        elif selection == 4: # Change effects sound
            self.playEffects = not self.playEffects

    '''
    METHOD
        Parameters:
            Menu self
            int selection - The current menu option represented as an int. The
                            selector is drawn according to the selection, as it
                            is used to specify which option the player is
                            currently focusing on.

        Renders the selector animation used to show which menu option currently
        has focus. It is drawn based on the selection given, altering the height
        of the vertical line as well as the position of the box and vertical
        line. If you don't know what I mean by vertical line, box, and
        horizontal line, the run the game because I don't know how to explain it
        best without sounding confusing. It kind of looks like the lines and
        pound/hashtag sign below
         ____________
        | opt1 |     |
        | opt2 #-----|
        | opt3       |
        |____________|

        Returns
            None
    '''
    def renderSelector(self, selection):
        screen = consoleScreen
        selXL = int(screen.get_width() * 0.6) # Leftmost
        selYT = 0 # Topmost
        selYB = selection * (fontSize * 2) + PADDING + int(fontSize / 2) # Bottommost
        selXR = screen.get_width() # Rightmost
        lineWeight = 4
        boxSize = 20
        # Gets added below which actually adds a negative number
        boxOffset = int(lineWeight / 2) - int(boxSize / 2)

        screen.fill(SCREEN_COLOR)

        # Vertical line
        pygame.draw.rect(screen, WHITE, (selXL, selYT, lineWeight, selYB))
        # Horizontal line
        pygame.draw.rect(screen, WHITE, (selXL, selYB, selXR, lineWeight))
        # Box
        pygame.draw.rect(screen, WHITE, (selXL + boxOffset, selYB + boxOffset,
                                              boxSize, boxSize))

    '''
    METHOD
        Parameters:
            Settings self

        Considered the main loop of the menu portion of the game, this method
        handles the following:
            * Renders an image of a computer with flashing lights
            * Renders text on the computer screen as options
            * Renders an option selector
            * Handles input from keyboard by player to go through options and
              make selections
            * Controls the framerate of the settings screen
            * Allows the player to change the difficulty and controls

        Returns:
            None
    '''
    def runSettings(self):
        animationCounter = 0 # For alternating between console images
        consoles = [console1, console2] # list of images
        consoleIndex = 0 # Default index for retrieving image
        console = consoles[consoleIndex] # Default image
        selection = 0 # Default option focused on

        while not Settings.exit:
            if animationCounter == FLASH_FREQ:
                consoleIndex = (consoleIndex + 1) % 2 # Change index
                console = consoles[consoleIndex]
                animationCounter = 0 # Reset so it doesn't get too large
            animationCounter += 1 # Controls speed of flashing animation

            window.fill(BG_COLOR)
            window.blit(console, (consoleX, consoleY))
            window.blit(consoleScreen, (screenX, screenY))
            # return to main menu font
            window.blit(Settings.menuFont, (Settings.menuFontX, Settings.menuFontY))

            # Difficulty font
            window.blit(Settings.diffFont, (Settings.diffFontX, Settings.diffFontY))
            if self.difficulty == 0: # Normal
                window.blit(Settings.diffFontN, (Settings.diffOptionX, Settings.diffOptionY))
            elif self.difficulty == 1: # Hard
                window.blit(Settings.diffFontH, (Settings.diffOptionX, Settings.diffOptionY))
            elif self.difficulty == 2:
                window.blit(Settings.diffFontE, (Settings.diffOptionX, Settings.diffOptionY))

            # Controls font
            window.blit(Settings.controlFont, (Settings.controlFontX, Settings.controlFontY))
            if self.controls == 0: # Directional
                window.blit(Settings.controlFontD, (Settings.controlOptionX, Settings.controlOptionY))
            elif self.controls == 1: # Inverted
                window.blit(Settings.controlFontI, (Settings.controlOptionX, Settings.controlOptionY))

            # Music font
            window.blit(Settings.musicFont, (Settings.musicFontX, Settings.musicFontY))
            if self.playMusic == True:
                window.blit(Settings.musicOn, (Settings.musicOptionX, Settings.musicOptionY))
            elif self.playMusic == False:
                window.blit(Settings.musicOff, (Settings.musicOptionX, Settings.musicOptionY))

            # Sound effects font
            window.blit(Settings.effectsFont, (Settings.effectsFontX, Settings.effectsFontY))
            if self.playEffects == True:
                window.blit(Settings.effectsOn, (Settings.effectsOptionX, Settings.effectsOptionY))
            elif self.playEffects == False:
                window.blit(Settings.effectsOff, (Settings.effectsOptionX, Settings.effectsOptionY))

            self.renderSelector(selection)

            # Get list of events since last update
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.playBlip()
                        # Move focus to option below overflowing back to top
                        selection = (selection + 1) % 5
                    elif event.key == pygame.K_UP:
                        self.playBlip()
                        # Move focus to option above overflowing to bottom
                        selection = (selection - 1) % 5
                    elif event.key == pygame.K_RETURN:
                        self.playBlip()
                        # Player indicated a selection
                        self.selectionAction(selection)
                    elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        if selection != 0:
                            self.playBlip()
                            # Left/right arrows can be used to change settings
                            self.selectionAction(selection, move=event.key)

            # Needed to show display changes
            pygame.display.update()

            # Framerate
            clock.tick(30)

        Settings.exit = False # So the user can access them again after exiting
        self.menu.runMenu()


class HighScores():

    # Used to break out of the while loop before returning to main screen
    exit = False

    scrollYPos = 0 # Used to change position of fonts so scrolling is allowed

    # board is a Surface used to display scores. The following are variables
    # used to define position and size before Surface creation
    boardWidth = int(consoleScreen.get_width() * 0.8)
    boardHeight = int(consoleScreen.get_height() * 0.55)
    #boardPosX = int(consoleScreen.get_width() / 2 - boardWidth / 2) # Center
    boardPosX = PADDING
    boardPosY = fontSize * 2

    board = pygame.Surface((boardWidth, boardHeight))

    # High Scores Font
    scoreFont = pygame.font.Font("fonts/space_age/space_age.ttf", fontSize)
    pygame.font.Font.set_underline(scoreFont, True)
    scoreFont = scoreFont.render("High Scores", True, WHITE)

    scoreFontX = int(consoleScreen.get_width() / 2 - scoreFont.get_width() / 2)
    scoreFontY = PADDING

    # Menu Font
    menuFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    int(fontSize * 0.75)).render("EXIT", True, WHITE)

    menuFontX = screenX + PADDING
    menuFontY = screenY + consoleScreen.get_height() - fontSize * 2

    # Arrows
    arrowPlain = tScale(loadImg("art/arrow_plain.png"), (fontSize, fontSize))
    arrowPress = tScale(loadImg("art/arrow_press.png"), (fontSize, fontSize))
        # Up
    arrowUpPlain = arrowPlain
    arrowUpPress = arrowPress
    arrowUpX = boardPosX + boardWidth + PADDING
    arrowUpY = boardPosY + boardHeight - fontSize*2 - PADDING
        # Down
    arrowDownPlain = pygame.transform.rotate(arrowPlain, 180)
    arrowDownPress = pygame.transform.rotate(arrowPress, 180)
    arrowDownX = boardPosX + boardWidth + PADDING
    arrowDownY = boardPosY + boardHeight - fontSize - PADDING


    def __init__(self, mainMenu):
        self.menu = mainMenu # Menu object
        self.scoreFileStr = "gg_scores.txt"
        self.scoreList = self.genList()


    def playBlip(self):
        if self.menu.settings.playEffects:
            self.menu.effectsChannel.play(Menu.blip)


    def genList(self):
        list_o_scores = []

        if os.path.exists("score_files/gg_scores.txt"):
            file = codecs.open('score_files/gg_scores.txt', 'rU', 'utf-8')

            for line in file:
                if len(line) > 1:
                    line = line.rstrip().decode().split(', ')
                    list_o_scores.append(line)

            file.close() # Close file once finished

        return list_o_scores


    def addScore(self, playerName, score):
        added = False
        diff = self.menu.settings.difficulty
        if diff == 0:
            difficulty = "Normal"
        elif diff == 1:
            difficulty = "Hard"
        elif diff == 2:
            difficulty = "Easy"

        # Add new score to HighScores object list
        if len(self.scoreList) > 0:
            for line in self.scoreList:
                if score > int(line[1]):
                    insertLine = [playerName, score, difficulty]
                    index = self.scoreList.index(line)
                    self.scoreList.insert(index, insertLine)
                    added = True
                    break

            if not added:
                self.scoreList.append([playerName, score, difficulty])
        else:
            self.scoreList.append([playerName, score, difficulty])

        # Rewrites updated list to file (There's probably a way to insert the
        # new score while keeping list sorted but idk. Maybe append to list then
        # sort list once it's retrieved in genList())
        if os.path.exists("score_files/gg_scores.txt"):
            file = codecs.open('score_files/gg_scores.txt', 'r+U', 'utf-8')
        else:
            file = codecs.open('score_files/gg_scores.txt', 'w+U', 'utf-8')

        file.truncate(0) # Clears file

        for line in self.scoreList:
            # Create line
            writeLine = "%s, %d, %s\n" %(str(line[0]), int(line[1]), str(line[2]))
            # Encode line to unicode
            writeLine = writeLine.encode()
            # Append encoded line to file
            file.write(writeLine)

        file.close() # Close file once finished

        return


    def renderSelector(self):
        screen = consoleScreen
        selXL = int(screen.get_width() * 0.2) # Leftmost
        selYT = consoleScreen.get_height() - int(fontSize * 1.5) # Topmost
        selYB = screen.get_height() # Bottommost
        selXR = screen.get_width() # Rightmost
        lineWeight = 4
        boxSize = 16
        # Gets added below which actually adds a negative number
        boxOffset = int(lineWeight / 2) - int(boxSize / 2)

        screen.fill(SCREEN_COLOR)

        # Vertical line
        pygame.draw.rect(screen, WHITE, (selXL, selYT, lineWeight, selYB))
        # Horizontal line
        pygame.draw.rect(screen, WHITE, (selXL, selYT, selXR, lineWeight))
        # Box
        pygame.draw.rect(screen, WHITE, (selXL + boxOffset, selYT + boxOffset,
                                              boxSize, boxSize))


    def renderScoreBoard(self, lower, upper):
        HighScores.board.fill(SCREEN_COLOR)

        for i in range(lower, upper):
            if i < len(self.scoreList):
                line = self.scoreList[i]
                lineStr = "%s: %d - %s" %(str(line[0]), int(line[1]), str(line[2]))

                l = pygame.font.Font("fonts/space_age/space_age.ttf",
                            int(fontSize * 0.75)).render(lineStr, True, WHITE)

                HighScores.board.blit(l, (PADDING, PADDING + fontSize * (i - lower)))

        consoleScreen.blit(HighScores.board,
                            (HighScores.boardPosX, HighScores.boardPosY))


    def scrollUp(self, lower, upper):
        if lower > 0:
            lower -= 1
            upper -= 1

        return (lower, upper)


    def scrollDown(self, lower, upper):
        if upper < len(self.scoreList):
            lower += 1
            upper += 1

        return (lower, upper)


    def runScores(self):
        animationCounter = 0 # For alternating between console images
        consoles = [console1, console2] # list of images
        consoleIndex = 0 # Default index for retrieving image
        console = consoles[consoleIndex] # Default image
        selection = 0 # Default option focused on
        lower = 0 # Lower index bound for scores to display
        upper = 4 # Upper index bounds for scores to display

        scrollingUp = False
        scrollingDown = False

        while not HighScores.exit:
            if animationCounter == FLASH_FREQ:
                consoleIndex = (consoleIndex + 1) % 2 # Change index
                console = consoles[consoleIndex]
                animationCounter = 0 # Reset so it doesn't get too large
            animationCounter += 1 # Controls speed of flashing animation

            window.fill(BG_COLOR)

            window.blit(console, (consoleX, consoleY))
            window.blit(consoleScreen, (screenX, screenY))
            # Return to main menu font
            window.blit(HighScores.menuFont,
                                (HighScores.menuFontX, HighScores.menuFontY))

            self.renderSelector()
            self.renderScoreBoard(lower, upper)
            consoleScreen.blit(HighScores.scoreFont,
                                (HighScores.scoreFontX, HighScores.scoreFontY))

            # Arrows
            if scrollingUp:
                consoleScreen.blit(HighScores.arrowUpPress,
                                    (HighScores.arrowUpX, HighScores.arrowUpY))
            else:
                consoleScreen.blit(HighScores.arrowUpPlain,
                                    (HighScores.arrowUpX, HighScores.arrowUpY))

            if scrollingDown:
                consoleScreen.blit(HighScores.arrowDownPress,
                                (HighScores.arrowDownX, HighScores.arrowDownY))
            else:
                consoleScreen.blit(HighScores.arrowDownPlain,
                                (HighScores.arrowDownX, HighScores.arrowDownY))

            # Get list of events since last update
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.playBlip()
                        scrollingDown = True
                        lower, upper = self.scrollDown(lower, upper)
                    elif event.key == pygame.K_UP:
                        self.playBlip()
                        scrollingUp = True
                        lower, upper = self.scrollUp(lower, upper)
                    elif event.key == pygame.K_RETURN:
                        self.playBlip()
                        self.menu.runMenu()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        scrollingUp = False
                    elif event.key == pygame.K_DOWN:
                        scrollingDown = False

            # Needed to show display changes
            pygame.display.update()

            # Framerate
            clock.tick(30)

        Settings.exit = False # So the user can access them again after exiting
        self.menu.runMenu()



# Allows game to be started by typing 'python start_screen.py' into terminal
if __name__ == "__main__":
    game_menu = Menu()
    game_menu.runIntro()
