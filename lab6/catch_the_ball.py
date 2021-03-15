import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 60  # shows, how often our screen will reload and show changes

# RGB-code for color, which was in use
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# list of colors for changing colors of objects
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

length_screen = 750
high_screen = 550
screen = pygame.display.set_mode((length_screen, high_screen))  # the name of the main surface
font = pygame.font.Font('freesansbold.ttf', 32)  # very useful font for creating some writings in the game
quit_button = pygame.font.Font('freesansbold.ttf', 32)  # for quit button, which will appear after the game
save_button = pygame.font.Font('freesansbold.ttf', 32)  # for save result button, which will appear after the game

# open file, where all results will be saved
score_file = open('scoreboard.txt', 'a')
# lists of coordinates for centres for circles
x_circle = []
y_circle = []

# list of radiuses of circles
radius = []

# Vx and Vy are the x_speed and y_speed of circles (how many pixels a change of dislocation for one round conclude)
Vx_circle = []
Vy_circle = []

# lists of coordinates for left high corners for circles
x_rectangle = []
y_rectangle = []

# Length_x_rectangle is a list with widths of rectangles and length_y_rectangle is a list with highs of rectangles
Length_x_rectangle = []
length_y_rectangle = []

# Vx and Vy are the x_speed and y_speed of circles (how many pixels a change of dislocation for one round conclude)
Vx_rectangle = []
Vy_rectangle = []

# bool list for disappearing objects
boom_circle = []
boom_rectangles = []

number_of_circles = 3
number_of_rectangles = 2


def fill_balls_and_rectangles():
    # filling lists of parameters for balls
    for i in range(number_of_circles):
        x_circle.append(randint(100, length_screen - 100))
        y_circle.append(randint(100, high_screen - 100))
        Vx_circle.append(10)
        Vy_circle.append(randint(-10, 10))
        radius.append(randint(30, 40))
        boom_circle.append(0)

    # filling lists of parameters for rectangles
    for i in range(number_of_rectangles):
        x_rectangle.append(randint(100, 500))
        y_rectangle.append(500)
        Length_x_rectangle.append(randint(30, 50))
        length_y_rectangle.append(randint(30, 50))
        Vx_rectangle.append(randint(10, 10))
        Vy_rectangle.append(11)
        boom_rectangles.append(0)


def new_ball():
    """
    this function creates circles in points according to x, y, which was set before and change these x and y
    """
    global x_circle, y_circle, radius, Vx_circle, Vy_circle, number_of_circles
    color = COLORS[randint(0, 5)]  # for changing colors

    for i in range(number_of_circles):
        # make balls dissapear or let them continue moving
        if boom_circle[i] == 1:
            x_circle[i] = randint(100, 650)
            y_circle[i] = randint(100, 500)
            boom_circle[i] = 0
        else:
            x_circle[i] += Vx_circle[i]
            y_circle[i] += Vy_circle[i]
        # drawing of ball number i
        circle(screen, color, (x_circle[i], y_circle[i]), radius[i])

        # conditions of change of the circles' direction becase of borders
        if (x_circle[i] >= 700 - radius[i]) or (x_circle[i] <= radius[i] + 10):
            Vx_circle[i] = -Vx_circle[i]
        if (y_circle[i] >= 500) or (y_circle[i] <= radius[i] + 10):
            Vy_circle[i] = -Vy_circle[i]


def new_rectangle():
    """
    this function creates circles in points according to x, y, which was set before and also change them
    """
    global x_rectangle, y_rectangle, Length_x_rectangle, length_y_rectangle, Vx_rectangle, Vy_rectangle, number_of_rectangles, time
    color = COLORS[randint(0, 5)]  # for changing colors
    var = 0  # some var, which will help to change rectangles' direction randomly
    for i in range(number_of_rectangles):
        # make rectangles disappear or let them continue moving
        if boom_rectangles[i] == 1:
            x_rectangle[i] = randint(100, 500)
            y_rectangle[i] = 500
            boom_rectangles[i] = 0
        else:
            x_rectangle[i] += Vx_rectangle[i]
            y_rectangle[i] += Vy_rectangle[i]
        # drawing rectangles
        rect(screen, color, (x_rectangle[i], y_rectangle[i], Length_x_rectangle[i], length_y_rectangle[i]))

        var = randint(1, 100)  # some var for finding random moment to change direction of our rectangle

        # conditions of random change of direction
        if ((abs(time - var) <= 10) or (time >= 100)) and (x_rectangle[i] < 690 - Length_x_rectangle[i]) and (
                x_rectangle[i] > Length_x_rectangle[i] + 15):
            time = 0
            Vx_rectangle[i] = - Vx_rectangle[i]

        # conditions of change of the rectangles' direction becase of borders
        if (x_rectangle[i] >= length_screen - 50 - Length_x_rectangle[i]) or (
                x_rectangle[i] <= Length_x_rectangle[i] + 9):
            Vx_rectangle[i] = -Vx_rectangle[i]
        if (y_rectangle[i] >= high_screen - 50 - length_y_rectangle[i]) or (
                y_rectangle[i] <= length_y_rectangle[i] + 9):
            Vy_rectangle[i] = -Vy_rectangle[i]


def first_page():
    """
    first window of the game, which ask users name
    """
    screen.fill(WHITE)
    text3 = font.render('Please, write your nickname', True, RED, BLACK)
    text3Rect = text3.get_rect()
    text3Rect.center = (400, 200)
    screen.blit(text3, text3Rect)
    text3 = font.render('and push Enter', True, RED, BLACK)
    text3Rect.center = (400, 250)
    screen.blit(text3, text3Rect)
    rect(screen, BLACK, (0, 280, length_screen, 50))
    pygame.display.update()

    global done
    name = ''
    # reading the nickname
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                    rect(screen, BLACK, (0, 280, length_screen, 50))
                else:
                    name += event.unicode
            text4 = quit_button.render(name, True, GREEN, BLACK)
            text4Rect = text4.get_rect()
            text4Rect.center = (350, 300)
            screen.blit(text4, text4Rect)
            pygame.display.update()
    return name


def main_page():
    """
    this function realizes playing game
    """
    global done, number_of_available_clicks, number_of_score, text1, textRect, text, score, screen, x_circle, x_rectangle, y_circle, y_rectangle, time

    text1Rect = text1.get_rect()
    text1Rect.center = (550, 16)

    fill_balls_and_rectangles()

    while done:
        clock.tick(FPS)
        time += 1
        # drawing of score table
        screen.blit(text, textRect)
        screen.blit(text1, text1Rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # minus 1 click
                number_of_available_clicks -= 1

                # searching if circle had been reached by user
                for i in range(number_of_circles):
                    if (x_circle[i] - event.pos[0]) ** 2 + (y_circle[i] - event.pos[1]) ** 2 <= radius[i] ** 2:
                        boom_circle[i] = 1
                        score += 3
                        number_of_score = str(score)

                # searching if rectangle had been reached by user
                for i in range(number_of_rectangles):
                    if (event.pos[0] - x_rectangle[i] <= Length_x_rectangle[i]) and (
                            event.pos[0] - x_rectangle[i] >= 0) and (
                            event.pos[1] - y_rectangle[i] <= length_y_rectangle[i]) and (
                            event.pos[1] - y_rectangle[i] >= 0):
                        boom_rectangles.insert(i, 1)
                        score += 1
                        number_of_score = str(score)
        # for changing numbers of score and available clicks
        text1 = quit_button.render("Available attempts: " + str(number_of_available_clicks), True, GREEN, BLUE)
        text = font.render(text_score + number_of_score, True, GREEN, BLUE)
        # drawing of balls and rectangles
        new_ball()
        new_rectangle()
        pygame.display.update()
        screen.fill(BLACK)
        if number_of_available_clicks == 0:
            done = False


def last_page():
    global done, event, score, name
    screen.fill(WHITE)
    # Quit button
    quit_text = quit_button.render(quit, True, GREEN, RED)
    quit_textRect = quit_text.get_rect()
    quit_textRect.center = (300, 200)
    screen.blit(quit_text, quit_textRect)
    # Save result button
    save_text = save_button.render(save_res, True, GREEN, BLUE)
    save_textRect = save_text.get_rect()
    save_textRect.center = (450, 200)  # setting the position of the center of the save_res button
    screen.blit(save_text, save_textRect)
    # waiting for user to push buttons
    while not done:
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Quit button
                if (event.pos[0] >= 270) and (event.pos[0] <= 330) and (event.pos[1] >= 185) and (event.pos[1] <= 215):
                    done = True
                # Save result button
                if (event.pos[0] >= 360) and (event.pos[0] <= 540) and (event.pos[1] >= 185) and (event.pos[1] <= 215):
                    done = True
                    score_file.write(name + ': ' + str(score) + '\n')
    score_file.close()


time = 20
clock = pygame.time.Clock()
time += 1
finished = False
number_of_available_clicks = 30

quit = 'Quit'
save_res = 'Save result'
text = font.render('Score: 0', True, RED, BLACK)

score = 0
textRect = text.get_rect()

text_score = 'Score: '
number_of_score = '0'

done = False
name = first_page()

text1 = quit_button.render("Available attempts: " + str(number_of_available_clicks), True, GREEN, BLUE)

main_page()

last_page()

pygame.quit()