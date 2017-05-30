import pygame, sys
from pygame.locals import *
FPS = 200
width = 400
height = 300
thickness = 10
psize = 50
poffset = 20
black     = (0  ,0  ,0  )
white     = (255,255,255)

#Draws the arena the game will be played in.
def drawArena():
    display.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(display, white, ((0,0),(width,height)), *2)
    #Draw centre line
    pygame.draw.line(display, white, ((width/2),0),((width/2),height), (thickness/4))


#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > height - thickness:
        paddle.bottom = height - thickness
    #Stops paddle moving too high
    elif paddle.top < thickness:
        paddle.top = thickness
    #Draws paddle
    pygame.draw.rect(display, white, paddle)


#draws the ball
def drawBall(ball):
    pygame.draw.rect(display, white, ball)

#moves the ball returns new position
def moveBall(ball, ballX, ballY):
    ball.x += ballX
    ball.y += ballY
    return ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballX, ballY):
    if ball.top == (thickness) or ball.bottom == (height - thickness):
        ballY = ballY * -1
    if ball.left == (thickness) or ball.right == (width - thickness):
        ballX = ballX * -1
    return ballX, ballY

#Checks is the ball has hit a paddle, and 'bounces' ball off it.
def checkHitBall(ball, paddle1, paddle2, ballX):
    if ballX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: return 1

#Checks to see if a point has been scored returns new score
def checkPointScored(paddle1, ball, score, ballX):
    #reset points if left wall is hit
    if ball.left == thickness:
        return 0
    elif ball.right == width - thickness:
        score += 1
        return score
    #if no points scored, return score unchanged
    else: return score

#Artificial Intelligence of computer player
def artificialIntelligence(ball, ballX, paddle2):
    #If ball is moving away from paddle, center bat
    if ballX == -1:
        if paddle2.centery < (height/2):
            paddle2.y += 1
        elif paddle2.centery > (height/2):
            paddle2.y -= 1
    #if ball moving towards bat, track its movement.
    elif ballX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -=1
    return paddle2

#Displays the current score on the screen
def displayScore(score):
    resultSurf = BASICFONT.render('Score = %s' %(score), True, white)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (width - 150, 25)
    display.blit(resultSurf, resultRect)

#Main function
def main():
    pygame.init()
    global display
    ##Font information
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    display = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Pong')

    #Initiate variable and set starting positions
    #any future changes made within rectangles
    ballX = width/2 - thickness/2
    ballY = height/2 - thickness/2
    playerOnePosition = (height - psize) /2
    playerTwoPosition = (height - psize) /2
    score = 0

    #Keeps track of ball direction
    ballX = -1 ## -1 = left 1 = right
    ballY = -1 ## -1 = up 1 = down

    #Creates Rectangles for ball and paddles.
    paddle1 = pygame.Rect(poffset,playerOnePosition, thickness,psize)
    paddle2 = pygame.Rect(width - poffset - thickness, playerTwoPosition, thickness,psize)
    ball = pygame.Rect(ballX, ballY, thickness, thickness)

    #Draws the starting position of the Arena
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0) # make cursor invisible

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey

        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballX, ballY)
        ballX, ballY = checkEdgeCollision(ball, ballX, ballY)
        score = checkPointScored(paddle1, ball, score, ballX)
        ballX = ballX * checkHitBall(ball, paddle1, paddle2, ballX)
        paddle2 = artificialIntelligence (ball, ballX, paddle2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
