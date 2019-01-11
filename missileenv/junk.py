class Cloud:
    MAX_SIZE = 500
    VAR_SIZE = 200

    def __init__(self, window, posX, posY, size, colorInt):
        self.window = window
        if int(size*100) % 2 == 0:
            self.posX = posX
        else:
            self.posX = -posX
        if int(posY*100) % 2 == 0:
            self.posY = posY
        else:
            self.posY = -posY
        self.sizeX = int(size * Cloud.MAX_SIZE)
        self.sizeY = int(size * Cloud.MAX_SIZE * 0.5)
        self.color = 250-colorInt
        self.seed = int(size * Cloud.VAR_SIZE)
        # Used to minimize calculations in drawCloud()
        self.s2 = int(self.seed/2)
        self.s3 = int(self.seed/3)
        self.s4 = int(self.seed/4)

    def drawCloud(self):
        drawRect = pygame.draw.rect
        # Main cloud body
        drawRect(self.window, (self.color, self.color, self.color),
                         (self.posX, self.posY, self.sizeX, self.sizeY))
        if self.seed > 50: # Variation on top-left and bottom-right and extra
            # Top-left
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX-self.seed, self.posY-self.s3,
                              self.seed*2, self.seed))
            # Bottom-right
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX+self.sizeX-self.s2,
                              self.posY+self.sizeY-self.s2,
                              self.seed, self.seed))
            # Extra
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX-self.seed, self.posY+self.sizeY+self.seed,
                              self.seed, self.s3))
        else: # Variation on bottom-left and top right and extra
            # Bottom-left
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX-self.seed,
                              self.posY+self.sizeY-self.s3,
                              self.seed*2, self.seed))
            # Top-right
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX+self.sizeX-self.s2,
                              self.posY-self.s4,
                              self.seed, self.seed))
            # Extra
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX-self.seed,
                              self.posY+self.s2-self.seed,
                              self.seed, self.s3))

        # Gives variation. Desperately needed. Looks dumb otherwise
        if self.color % 3 == 0:
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX+self.s2, self.posY-self.seed, int(self.sizeX/2), int(self.sizeY/3)))
        elif self.color % 4 == 0:
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX-int(self.seed*1.25), self.posY,
                              self.seed*2, self.seed*2))
        else:
            drawRect(self.window, (self.color, self.color, self.color),
                             (self.posX, self.posY-self.s3,
                              self.seed*2, self.seed))

    def setPosByMouse(self, x, y):
        self.posX += x
        self.posY += y
        self.drawCloud()
        pygame.display.update()
