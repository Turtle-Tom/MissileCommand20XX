
# Unique module
import pygame

# Custom modules
import random

# File macros
MISSILES_TO_ADD = 1
HIT_SIZE = 504

'''
CLASS
    Handles the generation, rendering, and functionality of missiles and clouds.
    Which image is rendered is based on two fields: growth and imageNum. The
    growth is incremented each frame of the game. If the growth is divisible by
    a described number, then imageNum is changed, thus changing the object's
    image. Using growth allows the program to continue which woud not be allowed
    by pygame.clock.wait, for example.
'''
class Level:
    loadImg = pygame.image.load # To reduce lookup time

    # Images; names self explanatory
    clouds = [
        loadImg("art/clouds/cloud2.png"),
        loadImg("art/clouds/cloud4.png"),
        loadImg("art/clouds/cloud6.png"),
        loadImg("art/clouds/cloud7.png"),
        loadImg("art/clouds/cloud9.png"),
        loadImg("art/clouds/cloud10.png"),
        loadImg("art/clouds/cloud11.png"),
    ]
    cloudsSpecial = [
        loadImg("art/clouds/special1.png"),
        loadImg("art/clouds/special2.png"),
    ]

    explosions = [
        loadImg("art/explosions/explosion1.png"),
        loadImg("art/explosions/explosion2.png"),
        loadImg("art/explosions/explosion3.png"),
        loadImg("art/explosions/explosion4.png"),
        loadImg("art/explosions/explosion5.png"),
        loadImg("art/explosions/explosion6.png"),
        loadImg("art/explosions/explosion7.png"),
        loadImg("art/explosions/explosion8.png")
    ]
    imgMissiles = [
        loadImg("art/missiles/missile1.png"),
        loadImg("art/missiles/missile2.png"),
        loadImg("art/missiles/missile3.png"),
        loadImg("art/missiles/missile4.png")
    ]
    greyMissiles = [
        loadImg("art/missiles/grey_missile1.png"),
        loadImg("art/missiles/grey_missile2.png"),
        loadImg("art/missiles/grey_missile3.png"),
        loadImg("art/missiles/grey_missile4.png")
    ]
    skull = loadImg("art/skull.png")

    # The value of this determines when an image is said to have hit the player
    MAX_IMG_SIZE = 328

    '''
    CONSTRUCTOR
        Parameters:
            Level self
            Game game - The game object creating the level. Called to decrement
                        the number of lives when player is hit.
            Surface window - The game Surface being drawn on to display levels
            int lvl - The current level number being generated. Determines
                      the number of missiles and clouds
            int screenWidth - width of window
            int screenHeight - height of window
            int difficulty - Signifies the difficulty of the game being played
                             which alters the color and the speed of the enemy
                             missiles. Value either 0 for Normal or 1 for Hard.
            int controls - Signifies the player's controls behavior of the game.
                           Value either 0 for Directional/Normal (move mouse up
                           to move crosshairs up) or 1 for Inverted (move mouse
                           down to move crosshairs up)

        Returns:
            Level object
    '''
    def __init__(self, game, window, lvl, screenWidth, screenHeight, difficulty, controls):
        self.game = game # Object that created level
        self.window = window # Surface to draw on
        self.lvl = lvl
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.difficulty = difficulty # 0 = normal ; 1 = hard. Used to control speed
        self.controls = controls # 0 = directional/normal ; 1 = inverted
        self.cloudList = self.genClouds(lvl)
        self.clouds = Level.clouds # images
        self.numMissiles = lvl + MISSILES_TO_ADD # Missiles per wave
        # Generate waves on levels >= 8 with even number of missiles
        if (self.numMissiles) >= 8 and (self.numMissiles) % 2 == 0:
            self.waves = 2
        # Just two for now
        # elif (self.numMissiles) > 3 and (self.numMissiles) % 3 == 0:
        #     self.waves = 3
        else:
            self.waves = 1
        self.missileList = self.genMissiles(lvl, self.waves)
        self.numDestroyed = 0 # Missiles destroyed
        self.numFinished = 0 # Missiles destroyed and done being drawn/animated
        self.animationFinished = False # True when all missiles are finished

    '''
    METHOD
        Parameters:
            Level self
            int lvl - The current level number that determines number of clouds

        The clouds are generated with random positions. To ensure they are
        somewhat spread out, a seed is used within the for loop whose number
        determines which quadrant of the screen it should be rendered in. If the
        screen were divided into four equal square areas, the quadrants are

        2 | 1
        --|--
        3 | 4

        A random number is also generated then floored to determine the integer-
        valued index of the cloud image lists that will be used for the cloud.

        Returns:
            List<Cloud> object
    '''
    def genClouds(self, lvl):
        # Cloud border
        border = Level.loadImg("art/clouds/border.png")
        border = pygame.transform.scale(border,
                                (self.screenWidth * 2, self.screenHeight * 2))
        borderX = int(self.screenWidth / 2) * -1
        borderY = int(self.screenHeight / 2) * -1
        borderCloud = Level.Cloud(border, 0, borderX, borderY,
                                        self.screenWidth, self.screenHeight)

        list_o_clouds = [borderCloud]

        seed = 0 # Seed can take 4 values, each corresponding to a quadrant
        rand = random.random # To reduce lookup time
        halfX = int(self.screenWidth / 2)
        halfY = int(self.screenHeight / 2)
        quarterX = int(self.screenWidth / 4)
        quarterY = int(self.screenHeight / 4)

        # randX and randY will be the initial distance from origin of
        # the window. halfX and halfY are added appropriately to push the
        # clouds into necessary quadrants. The idea behind these quadrants
        # is to ensure the clouds are spread out more.
        for i in range(lvl+2):
            if seed == 0: # Quardant 1
                randX = int(rand() * halfX) + halfX
                randY = int(rand() * self.screenHeight)

                if randY >= self.screenHeight / 2:
                    randY = randY - int(randY * 1.5)
            elif seed == 1: # Quadrant 2
                randX = int(rand() * self.screenWidth)
                randY = int(rand() * self.screenHeight)

                if randX >= self.screenWidth / 2:
                    randX = randX - int(randX * 1.5)
                if randY >= self.screenHeight / 2:
                    randY = randY - int(randY * 1.5)
            elif seed == 2: # Quadrant 3
                randX = int(rand() * self.screenWidth)
                randY = int(rand() * halfY) + halfY

                if randX >= self.screenWidth / 2:
                    randX = randX - int(randX * 1.5)
            elif seed == 3: # Quadrant 4
                randX = int(rand() * halfX) + halfX
                randY = int(rand() * halfY) + halfY

            randSize = rand() + 1 # Cloud's size

            randImage = int(rand() * len(self.clouds) - 0.01)
            if randImage < 1.2 and randImage > 1.1:
                randImage = int(rand() * len(self.cloudsSpecial) - 0.01)
                image = self.cloudsSpecial[randImage]
            else:
                image = self.clouds[randImage]

            list_o_clouds.append(Level.Cloud(image, randSize, randX, randY,
                    self.screenWidth, self.screenHeight))
            seed = (seed + 1) % 4

        return list_o_clouds


    '''
    METHOD
        Parameters:
            Level self
            int lvl - The current level number determining number of missiles
            int waves - The number of waves to generate for. Value is either 1
                        or 2. Each wave has the same number of missiles.

        The missiles are generated with random positions. To ensure they are
        somewhat spread out, the value of the index of the for loop is used to
        determine which quadrant of the screen it should be rendered in. The
        quadrants are the same as described above for clouds. The index of the
        for loop also determines which image to start with. The game looks
        a little odd if the missiles all have the exact same contrail image at
        the exact same time. The color of the missiles is greyed if the
        difficulty is set to Hard.

        Returns:
            List<Missile> object
    '''
    def genMissiles(self, lvl, waves):
        # Center missiles
        list_o_missiles = []
        rand = random.random # To reduce lookup time

        halfX = int(self.screenWidth / 2)
        halfY = int(self.screenHeight / 2)
        quarterX = int(self.screenWidth / 4)
        quarterY = int(self.screenHeight / 4)
        halfXMinEdge = halfX - int(Level.MAX_IMG_SIZE / 2)
        halfYMinEdge = halfY - int(Level.MAX_IMG_SIZE / 2)

        for i in range(self.numMissiles * waves):
            if i % 3 == 0: # Quadrant 1
                imageNum = 0

                randX = int(rand() * halfX) + halfXMinEdge
                randY = int(rand() * halfY)
            elif i % 3 == 1:
                seed = rand()
                if seed > 0.5: # Quadrant 2
                    imageNum = 1

                    randX = int(rand() * halfX)
                    randY = int(rand() * halfY)
                else: # Quadrant 3
                    imageNum = 2

                    randX = int(rand() * halfX)
                    randY = int(rand() * halfY) + halfYMinEdge
            elif i % 3 == 2: # Quadrant 4
                imageNum = 3

                randX = int(rand() * halfX) + halfXMinEdge
                randY = int(rand() * halfY) + halfYMinEdge

            if self.difficulty == 0 or self.difficulty == 2: # Normal or Easy
                list_o_missiles.append(Level.Missile(imageNum, Level.imgMissiles[imageNum],
                                randX, randY, self.screenWidth, self.screenHeight))
            elif self.difficulty == 1: # Hard
                list_o_missiles.append(Level.Missile(imageNum, Level.greyMissiles[imageNum],
                                randX, randY, self.screenWidth, self.screenHeight))

        return list_o_missiles

    '''
    METHOD
        Parameters:
            Level self
            int wave - Used to determine whether a new wave should be generated.

        The wave parameter is different from the current Level object's wave
        field, and comes from the Game object that created the Level object. It
        is the wave that was just completed. If that was not the last wave,
        reset fields to get ready to render next wave.

        Returns:
            bool
    '''
    def nextRender(self, wave):
        if wave == self.waves:
            return False
        else: # Reset fields for next wave
            self.numDestroyed = 0
            self.numFinished = 0
            self.animationFinished = False
            return True

    '''
    METHOD
        Parameters:
            Level self
            int mouseX - The current x-coordinate position of the player's mouse
            int mouseY - The current y-coordinate position of the player's mouse

        Renders the Level's clouds by drawing them on the Game window. The
        position of the clouds is based on the current position of the player's
        mouse. This gives an effect of looking around the sky in an area greater
        than the screen, but really the player area is still only the size of
        the screen and everything else moves while the crosshairs are static.
        How the clouds move are based on the controls setting.

        Returns:
            None
    '''
    def renderClouds(self, mouseX, mouseY):
        # Simulates moving the cursor, but really the cloud is moved
        # the mouse's (+/-) distance from its own position.
        # This distance is stored in xDiff and yDiff.
        for cloud in self.cloudList:
            # Directional controls
            if self.controls == 0:
                # How much the mouse has moved
                xDiff = mouseX - cloud.centerX
                yDiff = mouseY - cloud.centerY
                # Render image based on mouse position
                self.window.blit(cloud.image, (cloud.posX - xDiff, cloud.posY - yDiff))
            # Inverted controls
            elif self.controls == 1:
                # How much the mouse has moved
                xDiff = mouseX - cloud.centerX
                yDiff = mouseY - cloud.centerY
                # Render image based on mouse position
                self.window.blit(cloud.image, (cloud.posX + xDiff, cloud.posY + yDiff))


    '''
    METHOD
        Parameters:
            Level self
            Missile missile - The current missile being rendered/drawn
            int liveSpeed - Determines when to change the missile size/image.
                            The lower the number, the faster it changes due to
                            behavior using % below.

        Used for missiles not yet hit by the player. Controls the size of the
        missile image which simulates its speed as it "gets closer" to the
        player. Hard mode makes the missiles grow faster and colors them grey.

        Returns:
            None
    '''
    def liveMissile(self, missile, liveSpeed):
        if self.difficulty == 0: # Normal
            difInc = 0
        elif self.difficulty == 1: # Hard
            difInc = 2
        elif self.difficulty == 2: # Easy
            difInc = -2
        # Amount missile's size will grow based on growth value. Gives smoother
        # looking animation. 3 is base growth. Note image size increases to
        # simulate missile getting closer
        sizeInc = int(1.007**missile.growth) + 3 + difInc

        # Missile gets closer without hardcoding framerate for it
        if missile.growth % liveSpeed == 0: # Controls speed of animation
            missile.imageSize += sizeInc

            if self.difficulty == 0: # Normal
                missile.image = pygame.transform.scale(self.imgMissiles[missile.imageNum],
                            (missile.imageSize, missile.imageSize))
            elif self.difficulty == 1: # Hard
                missile.image = pygame.transform.scale(self.greyMissiles[missile.imageNum],
                            (missile.imageSize, missile.imageSize))
            elif self.difficulty == 2:
                missile.image = pygame.transform.scale(self.imgMissiles[missile.imageNum],
                            (missile.imageSize, missile.imageSize))

            # Gives smoke animation
            missile.imageNum = (missile.imageNum + 1) % 4


    '''
    METHOD
        Parameters:
            Level self
            Missile missle - The current missile being rendered/drawn
            int deadSpeed - Determines how long to display the skull image

        Used for missiles that were not hit by the player and have reached the
        player, thus decrementing a life. Controls the size and duration of the
        image which is a skull to signify the player was hit.

        Returns:
            None
    '''
    def killerMissile(self, missile, deadSpeed):

        # Adjust position of skull. Only first time otherwise shoots off screen
        if missile.imageNum == 0:
            missile.posX += int(missile.imageSize / 2)
            missile.posY += int(missile.imageSize / 2)
            missile.imageNum += 1

        # Controls how long the skull is displayed
        if missile.growth % deadSpeed == 0:
            missile.imageNum += 1

        missile.image = pygame.transform.scale(self.skull,
                        (int(missile.imageSize / 2), int(missile.imageSize / 2)))

    '''
    METHOD
        Parameters:
            Level self
            Missile missle - The current missile being rendered/drawn
            int deadSpeed - Determines when to change the explosion image.
                            The lower the number, the faster it changes due to
                            behavior using % below.

        Used for missiles that were hit by the player. Controls the duration of
        the each explosion image which alternates between a few at first. Then
        changes from a "ball of fire" animation to a "burning out" animation.
        Once finished, it is given an image of None so it skipped over in later
        renderings, improving processing time. It is also declared as finished
        so the level can be completed when all missiles are hit.

        Returns:
            None
    '''
    def deadMissile(self, missile, deadSpeed):
        imgs = len(Level.explosions)

        # First part of animation - Ball of fire
        if missile.imageNum < imgs and missile.growth <= 30:
            if missile.growth % deadSpeed == 0: # Controls speed of animation
                missile.image = pygame.transform.scale(self.explosions[missile.imageNum],
                            (missile.imageSize, missile.imageSize))

                # Animation
                if missile.growth < 30:
                    missile.imageNum = (missile.imageNum + 1) % 3
                else:
                    # Begin second part of animation
                    missile.imageNum = 3
        # second part of animation - Burning out
        elif missile.imageNum < imgs:
            if missile.growth % deadSpeed == 0: # Controls speed of animation
                missile.image = pygame.transform.scale(self.explosions[missile.imageNum],
                            (missile.imageSize, missile.imageSize))

                # Animation
                missile.imageNum += 1

        # On last animation the imageNum will go to 8 which is out of
        # bounds but never used
        if missile.imageNum == imgs:
            self.numFinished += 1 # Increment number done animating
            if self.numFinished != self.numMissiles:
                # Note to self: Don't do missile = None because you still
                # need
                missile.image = None


    '''
    METHOD
        Parameters:
            Level self
            int mouseX - The current x-coordinate position of the player's mouse
            int mouseY - The current y-coordinate position of the player's mouse
            int wave - The current wave from the Game being rendered.

        Controls the overall behavior/rendering of missiles from their initial
        display until when they are hit by the player or have hit the player.
        The comments within the method do a good job of explaining what is
        being processed.

        Returns:
            None
    '''
    def renderMissiles(self, mouseX, mouseY, wave):
        if self.lvl > 10: # Increase speed of live missiles if past level 10
            liveSpeed = 3
        else:
            liveSpeed = 5
        # Speed of hit missiles
        deadSpeed = 5

        # Number of explosion images
        imgs = len(Level.explosions)

        # Iterate through each missile in list
        for i in range(self.numMissiles*(wave-1),self.numMissiles*wave):
            missile = self.missileList[i] # Get Missile object

            if missile.image == None: # Skip if hit and animation complete
                continue

            missile.growth += 1 # Used to control speed of missile

            if not missile.explode: # Missile is live
                self.liveMissile(missile, liveSpeed)
            elif missile.hitPlayer: # Missile hit player
                self.killerMissile(missile, deadSpeed)
            else: # Missile was shot
                self.deadMissile(missile, deadSpeed)

            # Render image based on mouse position
            if missile.imageNum < imgs:

                # Directional controls
                if self.controls == 0:
                    xDiff = mouseX - missile.centerX
                    yDiff = mouseY - missile.centerY
                    missile.currPos = (missile.posX - xDiff, missile.posY - yDiff)
                    self.window.blit(missile.image, missile.currPos)
                # Inverted controls
                elif self.controls == 1:
                    xDiff = mouseX - missile.centerX
                    yDiff = mouseY - missile.centerY
                    missile.currPos = (missile.posX + xDiff, missile.posY + yDiff)
                    self.window.blit(missile.image, missile.currPos)

            # I know it's weird to have elif here but issues with rendering the
            # last explosion are occuring. Not game breaking but should be fixed
            elif missile.imageNum == imgs:
                missile.imageNum += 1 # For conditional elif directly below

            elif missile.imageNum > imgs:# Missile is done being renders
                # If missile hit player and skull animation finished
                if missile.hitPlayer:
                    missile.image = None # So it's skipped in further processing
                    self.numFinished += 1
                # If last missile destroyed and its animation is done
                if self.numFinished == self.numMissiles:
                    self.animationFinished = True

            # If missile has reached player for the first time (same location
            # while skull is drawn so it will otherwise keep decrementing lives)
            if missile.imageSize >= Level.MAX_IMG_SIZE and not missile.hitPlayer:
                self.game.decLives()
                self.remMissile(missile)
                missile.hitPlayer = True # Used to render skull above


    '''
    METHOD
        Parameters:
            Level self
            Surface window - The Game surface being drawn on to display game
            int width - window width
            int height - window height

        Draws the crosshairs at the center of the screen which are used by the
        player to aim. The game is designed to simulate the crosshairs moving
        over a larger area than the screen, but they are actually stationary
        while everything else moves.

        Returns:
            None
    '''
    def drawCrossHairs(self, window, width, height):
        pygame.draw.rect(window, (0, 0, 0), (int(width/2), int(height/2) - 15, 1, 30))
        pygame.draw.rect(window, (0, 0, 0), (int(width/2) - 15, int(height/2), 30, 1))


    '''
    METHOD
        Parameters:
            Level self
            Missile missile

        Removes a missile by declaring it as destroyed and exploding (the
        explosion animation doesn't happen until after this method is called).
        The missile's imageNum and growth fields are reset to 0 for the sake
        of rendering the explosion.

        Returns:
            None
    '''
    def remMissile(self, missile):
        self.numDestroyed += 1
        missile.explode = True
        missile.imageNum = 0
        missile.growth = 0


    '''
    INNER CLASS
        Provides a template for cloud objects. Only contains a constructor.
    '''
    class Cloud():

        '''
        CONSTRUCTOR
            Parameters:
                Cloud self
                pygame.Surface image - The image that was randomly selected to
                                       render/draw for the cloud
                int size - The size the cloud's image should be drawn as to
                           give more variation between clouds generated
                int posX - The x-coordinate of the cloud's position from origin
                           that changes as the player moves the mouse
                int posY - The y-coordinate of the cloud's position from origin
                           that changes as the player moves the mouse
                int screenW - The width of the play screen
                int screenH - The height of the play screen
        '''
        # Cloud border
        def __init__(self, image, size, posX, posY, screenW, screenH):
            self.image = pygame.transform.scale(image,
                         (image.get_width() + int(image.get_width() * size),
                          image.get_height() + int(image.get_height() * size)))
            self.size = size
            # To compare to mouse x-coordinate to find difference in movement
            self.centerX = int(screenW / 2)
            # To compare to mouse y-coordinate to find difference in movement
            self.centerY = int(screenH / 2)
            self.posX = posX # From origin
            self.posY = posY # From origin

    '''
    INNER CLASS
        Provides a template for missile objects. Only contains a constructor.
    '''
    class Missile():

        '''
        CONSTRUCTOR
            Parameters:
                Missile self
                int imageNum - The current index to be used for retrieving image
                pygame.Surface image - The image that was selected to
                                       render/draw for the cloud
                int posX - The x-coordinate of the missiles's position from
                           origin that changes as the player moves the mouse
                int posY - The y-coordinate of the missiles's position from
                           origin that changes as the player moves the mouse
                int screenW - The width of the play screen
                int screenH - The height of the play screen
        '''
        def __init__(self, imageNum, image, posX, posY, screenW, screenH):
            self.imageSize = 16 # Starting size of missiles
            self.imageNum = imageNum # Index to be used for retrieving image
            self.growth = 1 # To control rendering/animation speed
            self.image = pygame.transform.scale(image, (16, 16))
            # To compare to mouse x-coordinate to find difference in movement
            self.centerX = int(screenW / 2)
            # To compare to mouse y-coordinate to find difference in movement
            self.centerY = int(screenH / 2)
            self.posX = posX # From origin
            self.posY = posY # From origin
            self.currPos = (posX, posY) # Will hold current position on screen
            self.explode = False # Whether it has exploded from being hit
            self.hitPlayer = False # Whether it reached the player
