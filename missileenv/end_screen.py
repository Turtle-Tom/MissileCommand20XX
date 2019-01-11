
# Usual packages
import sys

# Unique packages
import pygame

# Custom modules
import missile_command

pygame.init() # Initialize pygame

# File macros and fields
ORIGIN = (0, 0)
FONT_SIZE = 40
DEFAULT_SCREEN_W = 1000 # 16:10 res
DEFAULT_SCREEN_H = 625 # 16:10 res
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY = (0, 135, 255)
GG_BUTTON_BACK = (255, 204, 0)
BTN_PADDING = 16
bP2 = int(BTN_PADDING / 2)
bP4 = int(BTN_PADDING / 4)

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
isFull = False

alphaNumKeys = [
    pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
    pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f,
    pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r,
    pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
    pygame.K_y, pygame.K_z,
    pygame.K_UNDERSCORE, pygame.K_MINUS, pygame.K_PERIOD, pygame.K_DOLLAR,
    pygame.K_HASH, pygame.K_AMPERSAND, pygame.K_EXCLAIM, pygame.K_SPACE
]

# To reduce lookup time
loadImg = pygame.image.load
tScale = pygame.transform.scale
fontF = pygame.font.Font
pyMouse = pygame.mouse
# Mouse settings
pyMouse.set_visible(True)

# Images
    # Button border
ggBtnBorder = loadImg("art/button_border.png").convert()

    # Mouse
mouse = loadImg("art/mouse.png").convert()
mouse = pygame.transform.rotate(mouse, 45)
mouse = tScale(mouse, (FONT_SIZE, FONT_SIZE))

'''
METHOD
    Parameters:
        Game self

    Displays a 'Game Over' screen once the player has lost all of their
    lives. The user can either start a new game, go to the main menu, or
    exit. Additional statements within the function give a fade-in effect
    before the 'Game Over' screen is displayed.

    Returns:
        None
'''

class EndScreen():

    def __init__(self, game, width, height, score):
        self.window = window
        self.game = game # Main game object
        self.width = width # Window width
        self.height = height # Window height
        self.score = score # Final score


    def setScore(self, score):
        self.score = score


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


    def ggRestart(self):
        pyMouse.set_visible(False)
        self.game.resetVars()


    def ggMenu(self):
        self.game.menu.playMusic()
        self.game.menu.runMenu()


    def addNewScore(self, playerName):
        # Save score if name provided
        if len(playerName) > 0:
            self.game.menu.highScores.addScore(playerName, self.score)
        # else put a warning by name


    def checkSave(self, mouseX, mouseY, saveDispX, saveDispY, saveBtnWidth,
                                    saveBtnHeight, saveBorder, saveFont, saveBtn):
        readySave = False

        if mouseX < saveDispX + saveBtnWidth and \
            mouseX > saveDispX and mouseY > saveDispY and \
            mouseY < saveDispY + saveBtnHeight:
            readySave = True

            saveBtn.fill(GG_BUTTON_BACK)
            saveBtn.blit(saveBorder, ORIGIN)
            saveBtn.blit(saveFont, (bP2, bP4))
        else:
            readySave = False
            saveBtn.fill(GG_BUTTON_BACK)
            saveBtn.blit(saveFont, (bP2, bP4))

        return readySave

    def checkRestart(self, mouseX, mouseY, restartDispX, restartDispY,
        restartBtnWidth, restartBtnHeight, restartBorder, restartFont, restartBtn):
        readyRestart = False

        if mouseX < restartDispX + restartBtnWidth and \
            mouseX > restartDispX and mouseY > restartDispY and \
            mouseY < restartDispY + restartBtnHeight:
            readyRestart = True

            restartBtn.fill(GG_BUTTON_BACK)
            restartBtn.blit(restartBorder, ORIGIN)
            restartBtn.blit(restartFont, (bP2, bP4))
        else:
            readyRestart = False
            restartBtn.fill(GG_BUTTON_BACK)
            restartBtn.blit(restartFont, (bP2, bP4))

        return readyRestart


    def checkMenu(self, mouseX, mouseY, menuDispX, menuDispY, menuBtnWidth,
                                menuBtnHeight, menuBorder, menuFont, menuBtn):
        readyMenu = False

        if mouseX < menuDispX + menuBtnWidth and \
            mouseX > menuDispX and mouseY > menuDispY and \
            mouseY < menuDispY + menuBtnHeight:
            readyMenu = True

            menuBtn.fill(GG_BUTTON_BACK)
            menuBtn.blit(menuBorder, ORIGIN)
            menuBtn.blit(menuFont, (bP2, bP4))
        else:
            readyMenu = False
            menuBtn.fill(GG_BUTTON_BACK)
            menuBtn.blit(menuFont, (bP2, bP4))

        return readyMenu


    def checkQuit(self, mouseX, mouseY, quitDispX, quitDispY, quitBtnWidth,
                                quitBtnHeight, quitBorder, quitFont, quitBtn):
        readyQuit = False

        if mouseX < quitDispX + quitBtnWidth and \
            mouseX > quitDispX and mouseY > quitDispY and \
            mouseY < quitDispY + quitBtnHeight:
            readyQuit = True

            quitBtn.fill(GG_BUTTON_BACK)
            quitBtn.blit(quitBorder, ORIGIN)
            quitBtn.blit(quitFont, (bP2, bP4))
        else:
            readyQuit = False
            quitBtn.fill(GG_BUTTON_BACK)
            quitBtn.blit(quitFont, (bP2, bP4))

        return readyQuit


    def gameEnd(self, scoreEntered):
        window = self.window

        # Fonts / Buttons
            # Player name font
        nameText = "Player Name:"
        nameFont = fontF("fonts/space_age/space_age.ttf",
                                FONT_SIZE).render(nameText, True, WHITE)

        nameDispX = int(self.width / 2 - nameFont.get_width())# / 2 - FONT_SIZE * 6)
        nameDispY = FONT_SIZE

            # Input box
        inputBox = pygame.Surface((nameFont.get_width() + BTN_PADDING,
                                   nameFont.get_height() + bP2))

        inputDispX = nameDispX + nameFont.get_width() + bP2
        inputDispY = nameDispY

        cursor = fontF("fonts/space_age/space_age.ttf",
                                int(FONT_SIZE*1.5)).render("I", True, BLACK)

            # Total score font
        scoreFont = fontF("fonts/space_age/space_age.ttf",
                    FONT_SIZE).render("SCORE: " + str(self.score), True, WHITE)

        scoreDispX = int(self.width / 2 - scoreFont.get_width() / 2)
        scoreDispY = FONT_SIZE * 2

            # Save font
        saveFont = fontF("fonts/space_age/space_age.ttf",
                                FONT_SIZE).render("SAVE", True, WHITE)

        saveDispX = int(self.width / 2 - saveFont.get_width() / 2)
        saveDispY = FONT_SIZE * 3

            # Save button
        saveBtn = pygame.Surface((saveFont.get_width() + BTN_PADDING,
                                 saveFont.get_height() + bP2))
        saveBtnWidth = saveBtn.get_width()
        saveBtnHeight = saveBtn.get_height()
        saveBorder = tScale(ggBtnBorder, (saveBtnWidth, saveBtnHeight))

            # Main font
        ggString = "GAME OVER"
        fontSize = int(self.width * 0.125)
        font = fontF("fonts/space_age/space_age.ttf",
                            fontSize).render(ggString, True, WHITE)
        fontDispX = int(self.width / 2) - int(font.get_width() / 2)
        fontDispY = int(self.height / 2) - int(fontSize / 2)

            # Restart font
        restartText = "RESTART"
        restartFont = fontF("fonts/space_age/space_age.ttf",
                                FONT_SIZE*2).render(restartText, True, WHITE)
        restartDispX = FONT_SIZE * 2
        restartDispY = self.height - restartFont.get_height() - FONT_SIZE

            # Restart button
        restartBtn = pygame.Surface((restartFont.get_width()+BTN_PADDING,
                                            restartFont.get_height()+bP2))
        restartBtnWidth = restartBtn.get_width()
        restartBtnHeight = restartBtn.get_height()
        restartBorder = tScale(ggBtnBorder, (restartBtnWidth, restartBtnHeight))

            # Menu font
        menuText = "MENU"
        menuFont = fontF("fonts/space_age/space_age.ttf",
                                FONT_SIZE*2).render(menuText, True, WHITE)

        menuDispX = int(self.width / 2)
        menuDispY = self.height - menuFont.get_height() - FONT_SIZE

            # Menu button
        menuBtn = pygame.Surface((menuFont.get_width()+BTN_PADDING,
                                  menuFont.get_height() + bP2))
        menuBtnWidth = menuBtn.get_width()
        menuBtnHeight = menuBtn.get_height()
        menuBorder = tScale(ggBtnBorder, (menuBtnWidth, menuBtnHeight))

            # Quit font
        quitText = "QUIT"
        quitFont = fontF("fonts/space_age/space_age.ttf",
                                FONT_SIZE*2).render(quitText, True, WHITE)
        quitDispX = self.width - quitFont.get_width() - FONT_SIZE * 2
        quitDispY = self.height - quitFont.get_height() - FONT_SIZE

            # Quit button
        quitBtn = pygame.Surface((quitFont.get_width()+BTN_PADDING,
                                                quitFont.get_height()+bP2))
        quitBtnWidth = quitBtn.get_width()
        quitBtnHeight= quitBtn.get_height()
        quitBorder = tScale(ggBtnBorder, (quitBtnWidth, quitBtnHeight))

        # Controlling variables
        readySave = False
        saveScore = False

        readyRestart = False
        restartGG = False

        readyMenu = False
        returnToMenu = False

        readyQuit = False
        quitGG = False

        currState = "" # Holds player name as it's typed
        cursorCount = 0
        cursorFreq = 40
        cursorShowing = False

        while not (saveScore or restartGG or returnToMenu or quitGG):
            mouseX, mouseY = pyMouse.get_pos()

            # Save handler
            readySave = self.checkSave(mouseX, mouseY, saveDispX, saveDispY,
                        saveBtnWidth, saveBtnHeight, saveBorder, saveFont, saveBtn)
             # Restart handler
            readyRestart = self.checkRestart(mouseX, mouseY, restartDispX, restartDispY,
                restartBtnWidth, restartBtnHeight, restartBorder, restartFont, restartBtn)
            # Menu handler
            readyMenu = self.checkMenu(mouseX, mouseY, menuDispX, menuDispY,
                        menuBtnWidth, menuBtnHeight, menuBorder, menuFont, menuBtn)
            # Quit handler
            readyQuit = self.checkQuit(mouseX, mouseY, quitDispX, quitDispY,
                            quitBtnWidth, quitBtnHeight, quitBorder, quitFont, quitBtn)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
                elif event.type == pygame.KEYUP: # Get name being typed
                    key = event.key

                    if key in alphaNumKeys and len(currState) < 12:
                        currState += pygame.key.name(event.key).upper()
                    elif key == pygame.K_BACKSPACE and len(currState) > 0:
                        currState = currState[:len(currState) - 1]
                    elif key == pygame.K_RETURN:
                        if len(currState) > 0:
                            readySave = True
                            saveScore = True
                    elif key == pygame.K_f:
                        if isFull:
                            window = pygame.display.set_mode((0, 0), [DEFAULT_SCREEN_W, DEFAULT_SCREEN_H])
                            isFull = False
                        else:
                            window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            Game.isfull = True

            # One will be True if mouse is over a button
            if pygame.mouse.get_pressed()[0]:
                saveScore = readySave
                restartGG = readyRestart
                returnToMenu = readyMenu
                quitGG = readyQuit

            window.fill(SKY)
            inputBox.fill(WHITE)

            # If a score was not yet saved
            if not scoreEntered:
                window.blit(nameFont, (nameDispX, nameDispY))
                playerName = fontF("fonts/space_age/space_age.ttf",
                                    FONT_SIZE).render(currState, True, BLACK)

                # Text box
                inputBox.blit(playerName, (bP2, bP4))
                cursorCount += 1
                if cursorCount % cursorFreq == 0:
                    cursorShowing = not cursorShowing

                if cursorShowing:
                    inputBox.blit(cursor, (playerName.get_width() + bP2, -bP4))

                window.blit(inputBox, (inputDispX, inputDispY))
                # </ Text box

                window.blit(saveBtn, (saveDispX, saveDispY))

            window.blit(scoreFont, (scoreDispX, scoreDispY))
            window.blit(font, (fontDispX, fontDispY))
            window.blit(menuBtn, (menuDispX, menuDispY))
            window.blit(quitBtn, (quitDispX, quitDispY))
            window.blit(restartBtn, (restartDispX, restartDispY))
            window.blit(mouse, (mouseX-10, mouseY-10))

            pygame.display.update()

        # Execute option selected
        if quitGG:
            self.quitGame()
        elif restartGG:
            self.ggRestart()
        elif returnToMenu:
            self.ggMenu()
        elif saveScore:
            self.addNewScore(currState)
            self.gameEnd(True)
