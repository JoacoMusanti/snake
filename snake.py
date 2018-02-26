import pygame, sys, random

# adds a new block to the snake
def growSnake(snake, speed):
    prev_x, prev_y = snake[0]

    prev_x += speed[0]
    prev_y += speed[1]

    pygame.time.delay(10)

    nuevo = prev_x, prev_y

    snake.insert(0, nuevo)

# checks whether the snake has gone outside the playable field and if it has,
# make it come out from the other side
def checkBoundary(snake, width, height):
    for i in range(0, len(snake)):
        if snake[i][0] < 0:
            snake[i] = (width, snake[i][1])
        if snake[i][0] > width:
            snake[i] = (0, snake[i][1])
        if snake[i][1] < 0:
            snake[i] = (snake[i][0], height)
        if snake[i][1] > height:
            snake[i] = (snake[i][0], 0)

# draws a square for the food
def drawFood(foodCoords, color, screen):
    rect = pygame.Rect(foodCoords[0], foodCoords[1], 5, 5)

    pygame.draw.rect(screen, color, rect)

# generate a coordinate pair to place the food
# the food can't be placed inside the snake
def generateFood(snake, screen, color):
    tupla = (random.randint(0, 320), random.randint(0, 240))

    while tupla in snake:
        tupla = (random.randint(0, 320), random.randint(0, 240))
    
    drawFood(tupla, color, screen)

    return tupla

# detects whether a tuple hash crashed into another
def detectCollision(tupleOne, tupleTwo):
    if (((tupleOne[0] <= tupleTwo[0] <= tupleOne[0] + 4) or (tupleOne[0] <= tupleTwo[0] + 4 <= tupleOne[0] + 4)) and
        ((tupleOne[1] <= tupleTwo[1] <= tupleOne[1] + 4) or (tupleOne[1] <= tupleTwo[1] + 4 <= tupleOne[1] + 4))):
        return True
    
    return False

def gotFood(snake, foodCoords):
    if detectCollision(snake[0], foodCoords):
        return True
    
    return False

def initialize():
    snake = [(20,20), (20,19), (20,18), (20,17), (20,16), (20,15), (20,14), (20,13), (20,12)]
    speed = (0, 1)

    return snake, speed

pygame.init()

size = width, height = 320, 240

screen = pygame.display.set_mode(size)

white = 255,255,255
black = 0, 0, 0
red = 255, 0, 0

snake, speed = initialize()

running = True

foodCoords = generateFood(snake, screen, red)

while running:
    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = (-1, 0)
            if event.key == pygame.K_RIGHT:
                speed = (1, 0)
            if event.key == pygame.K_UP:
                speed = (0, -1)
            if event.key == pygame.K_DOWN:
                speed = (0, 1)

    # draw the snake on the screen using 5x5 rectangles for each block
    for i in range(len(snake)):
        x, y = snake[i]
        rect = pygame.Rect(x, y, 5, 5)
        pygame.draw.rect(screen, white, rect)

    # make it move by removing the last block of the snake and adding another one at the beginning
    snake.pop(len(snake)-1)

    growSnake(snake, speed)
    
    drawFood(foodCoords, red, screen)

    if gotFood(snake, foodCoords):
        growSnake(snake, speed)
        foodCoords = generateFood(snake, screen, red)    

    checkBoundary(snake, width, height)

    pygame.display.update()