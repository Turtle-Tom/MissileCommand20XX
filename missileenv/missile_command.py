
'''
   #############################################################################
   #           ___  ___   ______   ______   ______   __       ______           #
   #          |   \/   | |_    _| |   ___| |   ___| |  |     |  ____|          #
   #          |  \__/  |  _|  |_   \__  \   \__  \  |  |___  |  __|            #
   #          |__|  |__| |______| |______| |______| |______| |______|          #
   #    ______   _____   ___  ___   ___  ___   _______   ____  __   ______     #
   #   |   ___| |  _  | |   \/   | |   \/   | |   _   | |    \|  | |   _  \    #
   #   |  |___  | |_| | |  \__/  | |  \__/  | |  |_|  | |  |\    | |  |_|  |   #
   #   |______| |_____| |__|  |__| |__|  |__| |__| |__| |__| \___| |______/    #
   #                     ______   _____  __   ___ __   ___                     #
   #                    |_     | |  _  | \  \/  / \  \/  /                     #
   #                     /   /_  | |_| |  |    |   |    |                      #
   #                    |______| |_____| /__/\__\ /__/\__\                     #
   #                                                                           #
   #    MISSILE COMMAND 20XX                                                   #
   #                                                                           #
   #    Dev:                                    Thomas J. Marlowe              #
   #    Date of v1 Completion:                  12..2018                       #
   #    Copyright Specification:                None! Steal my code I guess.   #
   #                                                                           #
   #    This project was done for personal enjoyment, skill building, and      #
   #    the hope of bringing some joy to others through a unique form of       #
   #    expression that has thankfully become commonplace in this day and      #
   #    age of 20XX.                                                           #
   #                                                                           #
   #    This project was not done for academic studies/grades (thank           #
   #    goodness because that woud have sucked the fun out of it). This        #
   #    project was also not done for professional reason of any kind or to    #
   #    gain monetary value.                                                   #
   #                                                                           #
   #    Inspiration for this project came from three sources:                  #
   #        1. The Missile Command sweatshirt my wife bought me. It is one     #
   #           of my favorite pieces of clothing, and I think the game is      #
   #           very fun.                                                       #
   #        2. My wife herself, as well as those I also care about deeply. I   #
   #           hope to use the skills I learn everyday to become the best      #
   #           coder/developer/engineer I can be. That way I can make them     #
   #           proud, and I can hopefully afford to enjoy more time with       #
   #           them, increase their quality of life, and be financially        #
   #           stable enough to help them in their times of need.              #
   #        3. I truely love writting code. I am very appreciative of that     #
   #           fact because of the benefits it can bring not just              #
   #           financially, but also mentally. I also love video games.        #
   #           They have brought me happiness all throughout my life, and      #
   #           have created wonderful memories with friends and family.        #
   #    Sorry for being a bit mushy, but this is the largest and most fun      #
   #    project I have done for personal reasons. I usually only write short   #
   #    programs to learn a new skill or two.                                  #
   #                                                                           #
   #    Thank you to the users for playing, and thank you to those interested  #
   #    enough in my code for reading it.                                      #
   #                                                                           #
   #############################################################################
Bleed 31:30
'''

# Usual modules
import sys

# Unique modules
import pygame

# Custom modules
import level
import end_screen

# File variables
EndScreen = end_screen.EndScreen

'''
CLASS
    Handles the vast majority of the program's functionality including
    initialization, event handling, external object creation, and contains the
    main loop of the program. A Game object is created to start a game, and a
    function contained within it, runGame(), is used to run it.
'''
class Game():
    # Preset mixer values. Last one, buffersize, is usually a bad default
    pygame.mixer.pre_init(44100, -16, 2, 256)
    pygame.mixer.init()
    pygame.init()

    # Class variables/macros
    numMissilesDisplay = 0
    numLivesDisplay = 2
    clock = pygame.time.Clock() # Used to control framerate

    ORIGIN = (0, 0)
    SKY = (0, 135, 255)
    ICON_TO_EDGE_PX = 4
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLACK_ALPHA_O = (0, 0, 0, 255) # O for "omg it's opaque"
    ALPHA_SET = 150
    LEVEL_FONT_COLOR = (255, 255, 255)
    MAX_ALPHA_VAL = 255
    FRAMERATE = 30

    # Main Surface
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Audio
        # Main
    # music = pygame.mixer.music.load('sounds/main.ogg')
    music = pygame.mixer.Sound('sounds/t4.ogg')
    musicChannel = pygame.mixer.Channel(1)
        # Explosion
    explosion = pygame.mixer.Sound("sounds/explosion.ogg")
    effectsChannel = pygame.mixer.Channel(2)

    # Images
    loadImg = pygame.image.load # To reduce lookup time
    tScale = pygame.transform.scale
        # UI icons
    iSize = 40
    icons = [
        # Lives
        tScale(loadImg("art/usr_icon_line.png").convert(), (iSize, iSize)),
        tScale(loadImg("art/usr_icon_plain.png").convert(), (iSize, iSize)),
        # Missiles
        tScale(loadImg("art/enemy_line.png").convert(), (iSize, iSize)),
        tScale(loadImg("art/enemy_plain.png").convert(), (iSize, iSize))
    ]

        # Button border
    ggBtnBorder = loadImg("art/button_border.png").convert()

        # LevelScreen
    levelScreen = loadImg("art/level_screen.png").convert()
    # Allows transparency effect. Image wasn't quite dark enough.
    levelScreen.fill((255, 255, 255, ALPHA_SET), None, pygame.BLEND_RGBA_MULT)
    ratio = levelScreen.get_width() / window.get_width()
    levelScreen = tScale(levelScreen, (window.get_width(), window.get_height()))

    # Unique surface used to fade-in level screen. For some reason an image
    # works while a regular Surface object does not? Idk pygame alpha values
    # are horrible and need an update. Use .convert() so you can set alphas
    fadeSurface = loadImg("art/black_screen.jpg").convert()
    fadeSurface = tScale(fadeSurface, (window.get_width(), window.get_height())).convert()
        # Mouse
    mouse = loadImg("art/mouse.png").convert()
    mouse = pygame.transform.rotate(mouse, 45)
    mouse = tScale(mouse, (iSize, iSize))

    # Mouse settings
    pyMouse = pygame.mouse # To reduce lookup time
    pyMouse.set_visible(False)
    pyMouse.set_pos((int(window.get_width()/2), int(window.get_height()/2)))


    '''
    CONSTRUCTOR
        Parameters:
            Game self

        Constructor to set object variables used either to help reduce
        lookup times (e.g. width = window.get_width()) or for Game specific
        details such as the user's score

        Returns:
            Game object
    '''
    def __init__(self, menu, difficulty, controls):
        self.difficulty = difficulty # 0 = normal ; 1 = hard; 2 = easy
        self.controls = controls # 0 = directional ; 1 = inverted
        self.width = Game.window.get_width()
        self.height = Game.window.get_height()
        self.lvl = None
        self.wave = 1
        self.score = 0
        self.currLevel = 0
        self.ammo = 0
        self.menu = menu # Main menu screen
        self.endScreen = EndScreen(self, self.width, self.height, self.score)


    '''
    METHOD
        Parameters:
            Game self

        Called when the user decides to quit the game or when game is over due
        to loss of player lives. Shuts down pygame and closes the application.

        Returns:
            None
    '''
    def quitGame(self):
        pygame.quit()
        sys.exit()


    '''
    METHOD
        Parameters:
            Game self

        Displays the main screen of Missile Command 20XX. Users select options
        access the scoreboard, begin the game, or exit from here.

        Returns:
            int - Specifies how difficult the game should be based on
                the macros above, NORMAL or HARD. Hard difficulty limits
                players' ammunition and slightly increases enemy missle speed.
    '''
    def gameStartScreen(self):
        return


    '''
    METHOD
        Parameters:
            Game self
            (int, int) pos - A tuple representing the mouse's position when the
                user clicked to shoot the enemy missile.

        Determines if the crosshairs wer over an enemy missile when clicked.
        If it was, then the missile is considered destroyed by calling the
        current Level object's function to remove it. If the controls are
        inverted, the screen's center is subtracted from the mouse position.
        This creates the point where the crosshairs are to check against the
        bounds of the enemy missile. If the controls are directional, mouse
        position is just checked.

        Returns:
            bool - True if the user hit the target, false otherwise.
    '''
    def checkAim(self, pos):
        for missile in self.lvl.missileList:
            if self.controls == 1: # Inverted
                centerX = int(self.width / 2)
                centerY = int(self.height / 2)
                pos = (centerX, centerY)

                if missile.image != None and not missile.explode:
                    if pos[0] <= missile.currPos[0] + missile.imageSize and \
                        pos[0] >= missile.currPos[0] and \
                        pos[1] <= missile.currPos[1] + missile.imageSize and \
                        pos[1] >= missile.currPos[1]:

                        self.lvl.remMissile(missile)
                        return True

            elif self.controls == 0:
                if missile.image != None and not missile.explode:
                    if pos[0] <= missile.posX + missile.imageSize and \
                        pos[0] >= missile.posX and \
                        pos[1] <= missile.posY + missile.imageSize and \
                        pos[1] >= missile.posY:

                        self.lvl.remMissile(missile)
                        return True

        return False


    '''
    METHOD
        Parameters:
            Game self

        Called by the current level object to signify a missile hit the player,
        and that the number of lives both displayed and that the player has
        should thus be decremented.

        Returns:
            None
    '''
    def decLives(self):
        Game.numLivesDisplay -= 1


    '''
    METHOD
        Parameters:
            Game self

        Generates a new level either when the game starts or after another level
        is completed. This increments the current level and resets some
        variables. It retrieves the background of the inter-level displays and
        places text on them showing the level being entered. It thus has a loop
        for pygame objects to be displayed and updated. Additional statements
        within the function give a fade-in effect before the inter-level display
        is shown.

        Returns:
            Level - A new Level object created based on the new current level
                being entered.
    '''
    def genNewLevel(self):
        self.wave = 1 # Reset waves
        self.currLevel += 1 # Increment level before passing it to Level object
        wD2 = int(self.width / 2)
        hD2 = int(self.height / 2)
        # Center mouse on screen
        Game.pyMouse.set_pos((int(Game.window.get_width()/2),
                                               int(Game.window.get_height()/2)))

        # Generate new level
        newLevel = level.Level(self, Game.window, self.currLevel, self.width,
                                    self.height, self.difficulty, self.controls)
        print("Level: %d" %(self.currLevel))

        # Retrieve number of missiles to destory from new level
        Game.numMissilesDisplay = newLevel.numMissiles
        # Number of missiles also determines ammo amount
        self.ammo = newLevel.numMissiles

        ready = False # Used to exit level screen loop when user is ready
        lvlString = "LEVEL %s" %(self.currLevel) # To add to level screen
        fontSize = int(self.width * 0.125)
        # Create Font object to blit onto level screen
        font = pygame.font.Font("fonts/space_age/space_age.ttf",
                        fontSize).render(lvlString, True, Game.LEVEL_FONT_COLOR)

        # Get positions that will center the font on the screen
        fontDispX = int(wD2) - int(font.get_width() / 2)
        fontDispY = int(hD2) - int(fontSize / 2)

        # Countdown font
        countDown = 5
        countSize = int(fontSize / 2)
        readyFont = pygame.font.Font("fonts/space_age/space_age.ttf",
            countSize).render(("Ready: "), True, Game.LEVEL_FONT_COLOR)
        readyDispX = int(wD2) - int(readyFont.get_width() / 2)
        readyDispY = fontDispY + fontSize
        countDispX = readyDispX + readyFont.get_width()
        # Used to control countdown speed. Using clock messes with fade-in
        timer = 5

        alpha = 0 # Transparency value to be incremented

        while not ready:
            # No need for this to be in a loop. No updating is done until exit.
            #   Edit: Maybe still not but this is what I ended up with while
            #   getting fade-in to work...
            Game.window.fill(Game.BLACK)
            Game.window.blit(Game.levelScreen, Game.ORIGIN)
            Game.window.blit(font, (fontDispX, fontDispY))
            Game.window.blit(readyFont, (readyDispX, readyDispY))

            countFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                countSize).render(str(countDown), True, Game.LEVEL_FONT_COLOR)

            Game.window.blit(countFont, (countDispX, readyDispY))

            if alpha < 250:
                # Increase transparency of fadeSurface
                Game.fadeSurface.set_alpha(Game.MAX_ALPHA_VAL - alpha)
                Game.window.blit(Game.fadeSurface, Game.ORIGIN)
                alpha += 15
            elif alpha >= 150: # Start decrementing count down
                if timer % 120 == 0:
                    countDown -= 1
                timer += 5

            if countDown == -1:
                ready = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quitGame()
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        ready = True

            pygame.display.update()
            Game.clock.tick(Game.FRAMERATE)

        return newLevel

    '''
    METHOD
        Parameters:
            Game self

        Considered the main loop of the game, this method does the following:
            * Controls the rendering of all game objects/images
            * Displays the ingame UI (e.g. lives icons)
            * Tracks the postion of the user's mouse
            * Handles events suchs as key-presses and mouse-clicks
            * Checks game progress to see if the level has been beaten or if the
              game has been lost
            * Controls the maximum framerate of the game based on the value
              given to the macro, FRAMERATE, above
            * Exits the loop when the game has been lost, then calls gameEnd()

        Returns:
            None
    '''
    def runGame(self):
        if self.menu.settings.playMusic:
            Game.musicChannel.play(Game.music, loops=-1)
        # pygame.mixer.music.play(-1)
        while True:
            if (self.currLevel == 0): # If first level, then start game
                self.lvl = self.genNewLevel()

            # Sky background color
            Game.window.fill(Game.SKY)

            mouseX, mouseY = Game.pyMouse.get_pos()

            # Clouds
            self.lvl.renderClouds(mouseX, mouseY)

            # Missiles
            if self.lvl.numDestroyed == self.lvl.numMissiles and self.lvl.animationFinished:
                # Either render next self.wave or gernerate next level
                newWave = self.lvl.nextRender(self.wave)
                # Wait so end of level/wave isn't so abrupt
                pygame.time.wait(500)
                if newWave:
                    # wave will be passed to the render function in the Level
                    # object, thus rendering the next wave of missiles
                    self.wave += 1
                    self.ammo = self.lvl.numMissiles # Reset for new wave
                else:
                    self.lvl = self.genNewLevel()
                    continue

            self.lvl.renderMissiles(mouseX, mouseY, self.wave)

            # Crosshairs
            self.lvl.drawCrossHairs(Game.window, self.width, self.height)

            # Lives icons
            if Game.numLivesDisplay < 0 and self.lvl.animationFinished:
                break # Game Over; exit loop

            for i in range(Game.numLivesDisplay):
                Game.window.blit(Game.icons[0],
                      (self.width - (Game.iSize * (i+1)), Game.ICON_TO_EDGE_PX))

            # Score
                # Create score Font based on current score
            scoreFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                 Game.iSize).render("SCORE: %d" %(self.score), True, Game.BLACK)
            scoreLen = len("SCORE: %d" %(self.score)*Game.iSize)
            Game.window.blit(scoreFont, (self.width-scoreLen, self.height-Game.iSize))

            # Ammo for Hard mode
            if self.difficulty == 1: # Hard
                    # Create ammo Font based on current ammo remaining
                ammoFont = pygame.font.Font("fonts/space_age/space_age.ttf",
                    Game.iSize).render("AMMO: %d" %(self.ammo), True, Game.BLACK)
                ammoLen = len("AMMO: %d" %(self.ammo)*Game.iSize)
                Game.window.blit(ammoFont, (self.width - ammoLen, self.height-Game.iSize*2))

            # Enemy icons
            enemyRow = 0
            enemyCol = 0
            for i in range(self.lvl.numMissiles - self.lvl.numDestroyed):
                if i != 0 and i % 10 == 0:
                    enemyRow += Game.ICON_TO_EDGE_PX + Game.iSize
                    enemyCol = 0
                Game.window.blit(Game.icons[2], (0 + (Game.iSize * enemyCol),
                                            Game.ICON_TO_EDGE_PX + enemyRow))
                enemyCol += 1

            # Get list of events since last update
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.playMusic()
                        self.menu.runMenu()
                # Checking for button up is used so user can't hold mouse down
                # to constantly shoot like a machine gun.
                elif event.type == pygame.MOUSEBUTTONUP: # Shot made
                    if self.difficulty == 1:
                        if self.ammo > 0:
                            self.ammo -= 1
                            pos = Game.pyMouse.get_pos()
                            hit = self.checkAim(pos)
                            if hit:
                                self.score += 10
                                if self.menu.settings.playEffects:
                                    Game.explosion.play()
                    else:
                        pos = Game.pyMouse.get_pos()
                        hit = self.checkAim(pos)
                        if hit:
                            if self.menu.settings.playEffects:
                                Game.effectsChannel.play(Game.explosion)
                            self.score += 10

            # Needed to show display changes
            pygame.display.update()

            # Framerate
            Game.clock.tick(Game.FRAMERATE)

        # Wait so user doesn't accidentally click something in 'Game Over' screen
        pygame.time.wait(1000)

        # Load 'Game Over' screen
        self.endScreen.setScore(self.score)
        pygame.mixer.stop()
        self.endScreen.gameEnd(False)


    def resetVars(self):
        Game.numMissilesDisplay = 0
        Game.numLivesDisplay = 2
        self.lvl = None
        self.wave = 1
        self.score = 0
        self.currLevel = 0

        self.runGame()
