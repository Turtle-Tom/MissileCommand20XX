
import pygame

import random

MISSILES_TO_ADD = 1
HIT_SIZE = 376

class Level:
    loadImg = pygame.image.load # To reduce lookup time
    clouds = [
        loadImg("art/cloud1.png"),
        loadImg("art/cloud2.png"),
        loadImg("art/cloud3.png"),
        loadImg("art/cloud4.png"),
    ]
    cloudsSpecial = [
        loadImg("art/cloud_car.png"),
        loadImg("art/cloud_sail.png"),
        loadImg("art/cloud_duck.png")
    ]
    explosions = [
        loadImg("art/explosion1.png"),
        loadImg("art/explosion2.png"),
        loadImg("art/explosion3.png"),
        loadImg("art/explosion4.png"),
        loadImg("art/explosion5.png"),
        loadImg("art/explosion6.png"),
        loadImg("art/explosion7.png"),
        loadImg("art/explosion8.png")
    ]
    centerMissiles = [
        loadImg("art/missile1.png"),
        loadImg("art/missile2.png"),
        loadImg("art/missile3.png"),
        loadImg("art/missile4.png")
    ]
    skull = loadImg("art/skull.png")

    MAX_IMG_SIZE = 328

    def __init__(self, game, window, lvl, screenWidth, screenHeight, difficulty, controls):
        self.game = game
        self.window = window
        self.lvl = lvl
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.difficulty = difficulty
        self.controls = controls
        self.cloudList = self.genClouds(lvl)
        self.storm = self.genStorm(lvl) # 0: no storm | 1: cloud cover | 2: storm
        self.clouds = Level.clouds
        self.numMissiles = lvl + MISSILES_TO_ADD # Missiles per wave
        if (self.numMissiles) >= 4 and (self.numMissiles) % 2 == 0:
            self.waves = 2
        elif (self.numMissiles) > 3 and (self.numMissiles) % 3 == 0:
            self.waves = 3
        else:
            self.waves = 1
        self.missileList = self.genMissiles(lvl, self.waves)
        self.numDestroyed = 0
        self.numFinished = 0
        self.animationFinished = False

    def genStorm(self, lvl):
        return


    def genClouds(self, lvl):
        list_o_clouds = []
        if False:
            return []
        else:
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
            for i in range(lvl+4):
                if seed == 0: # Quardant 1
                    randX = int(rand() * halfX) + halfX
                    randY = int(rand() * halfY)
                elif seed == 1: # Quadrant 2
                    randX = int(rand() * halfX)
                    randY = int(rand() * halfY)
                elif seed == 2: # Quadrant 3
                    randX = int(rand() * halfX)
                    randY = int(rand() * halfY) + halfY
                elif seed == 3: # Quadrant 4
                    randX = int(rand() * halfX) + halfX
                    randY = int(rand() * halfY) + halfY

                randSize = rand() # Cloud's size

                randImage = int(rand() * len(self.clouds) - 0.01)
                image = self.clouds[randImage]

                list_o_clouds.append(Level.Cloud(image, randSize, randX, randY,
                        seed, self.screenWidth, self.screenHeight))
                seed = (seed + 1) % 4

        return list_o_clouds

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

            list_o_missiles.append(Level.Missile(imageNum, Level.centerMissiles[imageNum],
                                    randX, randY, self.screenWidth, self.screenHeight))

        return list_o_missiles

    def nextRender(self, wave):
        if wave == self.waves:
            return False
        else: # Reset fields for next wave
            self.numDestroyed = 0
            self.numFinished = 0
            self.animationFinished = False
            return True

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

    def renderMissiles(self, mouseX, mouseY, wave):
        liveSpeed = 10
        deadSpeed = 5
        imgs = len(Level.explosions)
        for i in range(self.numMissiles*(wave-1),self.numMissiles*wave):
            missile = self.missileList[i]

            if missile.image == None:
                continue

            missile.growth += 1 # Used to control speed of missile

            if not missile.explode: # Missile is live
                if self.lvl > 10:
                    liveSpeed = 7
                # Missile gets closer without hardcoding framerate for it
                if missile.growth % liveSpeed == 0: # Controls speed of animation
                    if missile.imageSize > 132:
                        missile.imageSize += 16
                    elif missile.imageSize > 92:
                        missile.imageSize += 8
                    else:
                        missile.imageSize += 4

                    missile.image = pygame.transform.scale(self.centerMissiles[missile.imageNum],
                                (missile.imageSize, missile.imageSize))

                    # Gives smoke animation
                    missile.imageNum = (missile.imageNum + 1) % 4
            else: # Missile was shot
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

            elif missile.imageNum == imgs:
                missile.imageNum += 1 # For conditional elif directly below

            elif missile.imageNum > imgs:
                # If last missile destroyed and its animation is done
                if self.numFinished == self.numMissiles:
                    self.animationFinished = True

            if missile.imageSize >= Level.MAX_IMG_SIZE and not missile.explode: # Prevent multiple damage
                self.game.decLives()
                self.remMissile(missile)


    def drawCrossHairs(self, window, width, height):
        pygame.draw.rect(window, (0, 0, 0), (int(width/2), int(height/2) - 15, 1, 30))
        pygame.draw.rect(window, (0, 0, 0), (int(width/2) - 15, int(height/2), 30, 1))


    def remMissile(self, missile):
        self.numDestroyed += 1
        missile.explode = True
        missile.imageNum = 0
        missile.growth = 0


    class Cloud():

        def __init__(self, image, size, posX, posY, seed, screenW, screenH):
            self.image = pygame.transform.scale(image,
                         (image.get_width() + int(image.get_width() * size),
                          image.get_height() + int(image.get_height() * size)))
            self.size = size
            self.centerX = int(screenW / 2) # To compare to mouse x
            self.centerY = int(screenH / 2) # To compare to mouse y
            self.posX = posX
            self.posY = posY


    class Missile():

        def __init__(self, imageNum, image, posX, posY, screenW, screenH):
            self.imageSize = 16
            self.imageNum = imageNum
            self.growth = 1
            self.image = pygame.transform.scale(image, (16, 16))
            self.centerX = int(screenW / 2)
            self.centerY = int(screenH / 2)
            self.posX = posX
            self.posY = posY
            self.currPos = (posX, posY) # Will hold screen position
            self.explode = False
