import numpy as np
import pygame
from pygame.draw import *
from random import randint

pygame.init()
pygame.font.init()

# initialisation of colors, which was in using
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 2)
ORANGE = (255, 131, 0)
GRAY = (125, 125, 125)
BLUE = (1, 199, 254)
dark_red = (130, 0, 0)
army_color = (75, 83, 32)
LIGHT = (200, 200, 230)
army_color_1 = (60, 65, 18)
SCREEN_SIZE = (800, 600)

# initialisation of sounds to play them during the game
begin_sound = pygame.mixer.Sound('Dendy.wav')
shoot_sound = pygame.mixer.Sound('Tank.wav')
motion_sound = pygame.mixer.Sound('Motion.wav')
boom_sound = pygame.mixer.Sound('Boom.wav')
die_smile_sound = pygame.mixer.Sound('Demon.wav')
angry_smile_sound = pygame.mixer.Sound('Monster.wav')
Manna_sound = pygame.mixer.Sound('Bubble.wav')
error_sound = pygame.mixer.Sound('error.wav')
collected_sound = pygame.mixer.Sound('reincarnation.wav')
bomb_sound = pygame.mixer.Sound('bomb_sound.wav')


def rand_color():
    """
    return random color
    """
    return randint(0, 180), randint(0, 180), randint(0, 180)


class Gun:
    """
    Class for the movement and focusing of the gun
    """

    def __init__(self, coord=None, angle=0, maximum_power=80, minimum_power=10, gun_color=BLACK):
        """
        Setting of coordinates, direction, minimum's and maximum's power and color of the gun
        """
        if coord is None:
            coord = [30, SCREEN_SIZE[1] // 2]
        self.coord = coord
        self.angle = angle
        self.gun_color = gun_color
        self.minimum_power = minimum_power
        self.maximum_power = maximum_power
        self.active = False
        self.power = minimum_power

    def activate(self):
        """
        Gun's activating, change its color for red
        """
        self.active = True
        self.gun_color = RED

    def gun_power(self, add_power=4):
        """
        Add gun power after long touch of the mouse button
        """
        if self.active and self.power < self.maximum_power:
            self.power += add_power

    def set_angle(self, target_position):
        """
        Sets gun's direction according to the mouse position
        """
        self.angle = np.arctan2(target_position[1] - self.coord[1], target_position[0] - self.coord[0])

    def move(self, add_x, add_y, time=1):

        """
        Changes vertical position of the gun
        """
        if (self.coord[1] > 30 or add_y > 0) and (self.coord[1] < SCREEN_SIZE[1] - 30 or add_y < 0):
            self.coord[1] += add_y * time
        if (self.coord[0] > 30 or add_x > 0) and (self.coord[0] < SCREEN_SIZE[0] - 30 or add_x < 0):
            self.coord[0] += add_x * time

    def strike(self, not_manna_ball):
        """
        Creates ball, according to gun's direction and current charge power
        """

        speed = int(self.power * 1.3)
        angle = self.angle
        if not_manna_ball:
            ball = Ball(list(self.coord), [int(speed * np.cos(angle)), int(speed * np.sin(angle))], 0.8, 0.9)
        else:
            ball = Ball(list(self.coord), [int(speed * 0.7 * np.cos(angle)), int(speed * 0.7 * np.sin(angle))], 0.9,
                        0.9, ball_radius=60, color=LIGHT)
        # deactivating of the gun, set minimums power for the next reload
        self.power = self.minimum_power
        self.active = False
        self.gun_color = BLACK
        return ball

    def draw(self, screen_space):
        """
        Drawing the gun on the screen
        """
        gun_shape = []
        # add vectors for making gun's shape
        vec_1 = np.array([int(5 * np.cos(self.angle - np.pi / 2)), int(5 * np.sin(self.angle - np.pi / 2))])
        vec_2 = np.array([int(self.power * np.cos(self.angle)), int(self.power * np.sin(self.angle))])
        gun_position = np.array(self.coord)
        # setting shape of the gun for drawing it later
        gun_shape.append((gun_position + vec_1).tolist())
        gun_shape.append((gun_position + vec_1 + vec_2).tolist())
        gun_shape.append((gun_position + vec_2 - vec_1).tolist())
        gun_shape.append((gun_position - vec_1).tolist())
        # drawing the gun
        rect(screen_space, army_color, (self.coord[0] - 30, self.coord[1] - 20, 50, 40))
        rect(screen_space, BLACK, (self.coord[0] - 30, self.coord[1] + 15, 50, 10))
        rect(screen_space, BLACK, (self.coord[0] - 30, self.coord[1] - 25, 50, 10))
        circle(screen_space, army_color_1, (self.coord[0], self.coord[1]), 15)
        polygon(screen_space, self.gun_color, gun_shape)


class Ball:
    """
    Creates a ball, controls its movement
    """

    def __init__(self, coord, speed, reflection_decline_border, reflection_decline, ball_radius=20, color=None):
        """
        Set ball's parameters and their meanings
        """
        self.speed = speed
        self.coord = coord
        if color is None:
            color = rand_color()
        self.color = color
        self.is_alive = True
        self.ball_radius = ball_radius
        self.reflection_decline_border = reflection_decline_border
        self.reflection_decline = reflection_decline
        self.kicked = False

    def were_kicked(self):
        """
        return true if ball was kicked
        """
        self.kicked = True

    def move(self, time=1, gravitation=0):
        """
        Moving the ball according to it's speed and time step
        Change the ball's speed because of gravitation
        """
        self.speed[1] += gravitation
        for i in range(2):
            self.coord[i] += time * self.speed[i]
        self.check_corners()
        if (self.speed[0] ** 2 + self.speed[1] ** 2 < 6) or self.kicked:
            self.is_alive = False

    def check_corners(self):
        """
        Change ball's speed when the ball bumps into the screen borders
        """
        for i in range(2):
            if self.coord[i] < self.ball_radius:
                self.coord[i] = self.ball_radius
                self.speed[i] = - int(self.speed[i] * self.reflection_decline_border)
                self.speed[1 - i] = int(self.speed[1 - i] * self.reflection_decline)
            elif self.coord[i] > SCREEN_SIZE[i] - self.ball_radius:
                self.coord[i] = SCREEN_SIZE[i] - self.ball_radius
                self.speed[i] = - int(self.speed[i] * self.reflection_decline_border)
                self.speed[1 - i] = int(self.speed[1 - i] * self.reflection_decline)

    def draw(self, screen_space):
        """
        Draws the ball on appropriate surface
        """
        circle(screen_space, self.color, self.coord, self.ball_radius)


class Target(Ball):
    """
    Target class. Creates target, manages it's rendering and bumping with a ball event.
    """

    def __init__(self, coord=None, color=None, ball_radius=30):
        """
        Constructor method. Sets coordinate, color and ball_radius of the target.
        """
        if coord is None:
            coord = [randint(ball_radius, SCREEN_SIZE[0] - ball_radius),
                     randint(ball_radius, SCREEN_SIZE[1] - ball_radius)]
        self.coord = coord
        self.ball_radius = ball_radius
        self.speed = [randint(2, 5), randint(2, 4)]
        if color is None:
            color = rand_color()
        self.color = color
        super().__init__(self.coord, self.speed, 1, 1, self.ball_radius)

    def check_bumping(self, ball):
        """
        Checks if the ball bumped into target
        """
        minimum_distantion = self.ball_radius + ball.ball_radius
        distantion = sum([(self.coord[counter] - ball.coord[counter]) ** 2 for counter in range(2)]) ** 0.5
        return distantion <= minimum_distantion


class New_target(Ball):
    def __init__(self, color, coord=None, ball_radius=30):
        """
        Setting of coordinates, color and ball_radius of the target
        """
        if coord is None:
            coord = [randint(ball_radius, SCREEN_SIZE[0] - ball_radius),
                     randint(ball_radius, SCREEN_SIZE[1] - ball_radius)]
        self.coord = coord
        self.ball_radius = ball_radius
        self.speed = [randint(5, 8), randint(4, 7)]
        super().__init__(self.coord, self.speed, 1, 1, self.ball_radius)
        self.color = color
        self.time = 0

    def check_bumping(self, ball):
        """
        Checks if the ball bumped into target
        """
        minimum_distantion = self.ball_radius + ball.ball_radius
        distantion = sum([(self.coord[counter] - ball.coord[counter]) ** 2 for counter in range(2)]) ** 0.5

        return distantion <= minimum_distantion

    def change_color_condition(self):
        """
        return color condition
        """
        if self.color == dark_red:
            return True
        else:
            return False

    def change_color(self):
        """
        change a color
        """
        self.color = dark_red

    def draw_smile(self, screen_space):
        """
        drawing smile on the screen
        """
        circle(screen_space, BLACK, self.coord, self.ball_radius)
        circle(screen_space, self.color, self.coord, self.ball_radius - 1)

        # drawing of eyes
        for counter in range(1, 3, 1):
            circle(screen_space, BLACK,
                   (self.coord[0] + (self.ball_radius * (-1) ** counter) // 2, self.coord[1] - self.ball_radius // 3),
                   self.ball_radius // (2 + counter))
            circle(screen_space, RED,
                   (self.coord[0] + (self.ball_radius * (-1) ** counter) // 2, self.coord[1] - self.ball_radius // 3),
                   self.ball_radius // (2 + counter) - 1, self.ball_radius // (8 * counter))
        # drawing of mouth
        rect(screen_space, BLACK,
             (self.coord[0] - self.ball_radius // 2, self.coord[1] + self.ball_radius // 3, self.ball_radius,
              self.ball_radius // 7))
        # drawing of eyebrows
        for counter in range(2):
            line(screen_space, BLACK, (self.coord[0], self.coord[1] - self.ball_radius // 2),
                 (self.coord[0] + ((-1) ** counter) * self.ball_radius,
                  self.coord[1] - self.ball_radius // 2 - randint(counter + 1, counter + 3) * self.ball_radius // 5), 4)

    def motion(self):
        """
        make smile move
        """
        self.time += 0.5
        New_target.check_corners(self)
        for i in range(2):
            self.coord[i] += int(self.speed[i] * (np.cos(self.time + (np.pi * i) / 2) + 1))


class Bomb:
    """
    Class for the appearance of the book
    """

    def __init__(self, coord, length_book=160, high_book=200):
        """
        init bomb
        """
        book_surf = pygame.image.load('Engl.png')
        self.book_rect = book_surf.get_rect(bottomright=(400, 500))
        self.coord = coord
        self.time = 1
        self.scale = pygame.transform.scale(book_surf, (length_book, high_book))
        self.scale_rect = self.scale.get_rect(center=self.coord)

    def grow_shadow(self):
        """
        make shadow grow
        """
        self.time += 0.5
        rect(screen, GRAY, (self.coord[0] - 4 * int(self.time), self.coord[1] - 5 * int(self.time), 8 * int(self.time),
                            10 * int(self.time)))

    def insert_it(self):
        """
        make bomb sound
        """
        screen.blit(self.scale, self.scale_rect)
        bomb_sound.play()

    def time_limit(self):
        """
        do boom if increase time limit
        """
        if self.time >= 20:
            Bomb.insert_it(self)
            return True

    def check_crush(self, gun):
        """
        check gun's crush
        """
        if (abs(self.coord[0] - (gun.coord[0] - 5)) < 100) and (abs(self.coord[1] - gun.coord[1]) < 130):
            self.time = 0
            return True


class ScoreTable:
    """
    Class for scoretable
    """

    def __init__(self, smashed_targets=0, number_of_used_balls=0):
        """
        init scoretable
        """
        self.smashed_targets = smashed_targets
        self.number_of_used_balls = number_of_used_balls
        # set font for writing
        self.font = pygame.font.SysFont("dejavusansmono", 20)

    def score(self):
        """
        Score calculation by subtraction number of used balls and broken targets
        """
        return self.smashed_targets - self.number_of_used_balls

    def draw(self, screen_space, curr_level):
        """
        draw scoretable
        """
        # making list with strings about now user's score
        score_surface = [self.font.render("Targets hitted: {}".format(self.smashed_targets), True, BLACK),
                         self.font.render("Balls used: {}".format(self.number_of_used_balls), True, BLACK)]
        # conditions for changing color of the score string
        if self.score() >= 0:
            score_surface.append(self.font.render("Total score: {}".format(self.score()), True, BLUE))
        if self.score() < 0:
            score_surface.append(self.font.render("Total score: {}".format(self.score()), True, RED))

        score_surface.append(self.font.render("Level: {}".format(curr_level), True, ORANGE))
        # addition of strings in the right corner
        for counter in range(4):
            screen_space.blit(score_surface[counter], [10, 10 + 30 * counter])


def quit_condition(pressed_button):
    """
    return 1 if pressed quit button
    """
    finished = 0
    if pressed_button == pygame.QUIT:
        finished = 1
    return finished


motion = False


class Editor:
    """
    Class that manages user events, create targets, make balls move and check if they bumped into targets
    """

    def __init__(self, number_targets=1, number_new_targets=1):
        # init all gun characteristics
        self.key = None
        self.balls = []
        self.gun = Gun()
        self.targets = []
        self.new_targets = []
        self.score_table = ScoreTable()
        self.number_targets = number_targets
        self.number_new_targets = number_new_targets
        self.new_mission(level)
        self.time = 0
        self.coord = (randint(80, SCREEN_SIZE[0] - 80), randint(100, SCREEN_SIZE[0] - 200))
        self.bomb = Bomb(self.coord)
        self.manna = 0
        self.manna_increase = 1
        self.manna_collected = False

    def process(self, events, screen_space):
        """
        Focusing of the gun, move ball, look, if there were some strikes
        """
        donor = self.user_events(events)
        # look if the mouse was moved to change gun's orientation
        if pygame.mouse.get_focused():
            mouse_position = pygame.mouse.get_pos()
            self.gun.set_angle(mouse_position)

        self.move()
        self.strike()
        self.draw(screen_space)

        if (len(self.targets) == 0 and len(self.new_targets) == 0) and len(self.balls) == 0:
            self.new_mission(level)

        return donor

    def new_mission(self, curr_level):
        """
        Addition of new targets after destroying the old one
        """

        curr_level += 1
        # make balls even smaller because of the big count
        begin_sound.play()
        if self.score_table.score() < 0:
            for j in range(self.number_targets):
                self.targets.append(Target(ball_radius=30))
            for j in range(self.number_new_targets):
                self.new_targets.append(New_target(YELLOW, ball_radius=30))
        else:
            for j in range(self.number_targets):
                self.targets.append(Target(
                    ball_radius=randint(max(1, 30 - 2 * self.score_table.score()), 30 - self.score_table.score())))
            for j in range(self.number_new_targets):
                self.new_targets.append(New_target(YELLOW,
                                                   ball_radius=randint(max(1, 30 - 2 * self.score_table.score()),
                                                                       30 - self.score_table.score())))
        return curr_level

    def move(self):
        """
        Making balls fly with gravitation, raise the gun's power, removes dead balls
        """
        dead_balls = []
        for j, ball in enumerate(self.balls):
            ball.move(gravitation=5)
            if not ball.is_alive:
                dead_balls.append(j)
        for j, target in enumerate(self.targets):
            target.move(gravitation=0)
        for j, new_target in enumerate(self.new_targets):
            new_target.motion()
        # make balls disappear
        for j in reversed(dead_balls):
            self.balls.pop(j)
        self.gun.gun_power()

    def check_bomb(self):
        """
        Initiate bomb, looks if gun in bomb's area, finishes the game
        """
        donor = 0
        self.time += 1
        if self.time >= 40:
            self.bomb.grow_shadow()
            if self.bomb.time_limit():
                if self.bomb.check_crush(self.gun):
                    donor = 2
                self.time = 0
                coord = (randint(80, SCREEN_SIZE[0] - 80), randint(100, SCREEN_SIZE[0] - 200))
                self.bomb = Bomb(coord)
        return donor

    def move_machine(self, new_event):
        """
        move machine by wasd buttons
        """
        if new_event.key == pygame.K_f:
            pygame.key.set_repeat(1)
        if new_event.key == pygame.K_g:
            pygame.key.set_repeat(0)
        if new_event.key == pygame.K_w:
            self.gun.move(0, -20)
            motion_sound.play()
        if new_event.key == pygame.K_s:
            self.gun.move(0, 20)
            motion_sound.play()
        if new_event.key == pygame.K_d:
            self.gun.move(20, 0)
            motion_sound.play()
        if new_event.key == pygame.K_a:
            self.gun.move(-20, 0)
            motion_sound.play()

    def collect_manna(self):
        """
        update manna line
        """
        rect(screen, BLACK, (278, 8, 303, 13), 2)
        self.manna += self.manna_increase
        rect(screen, BLUE, (280, 10, 2 * self.manna, 10))
        self.manna_collected = Editor.stop_collect_manna(self)

    def stop_collect_manna(self):
        """
        stop and update manna
        """
        if self.manna == 149:
            collected_sound.play()
        if self.manna == 150:
            self.manna_increase = 0
            return True
        return False

    def user_events(self, events):
        """
        Analyze events from keyboard and mouse
        """
        donor = Editor.check_bomb(self)
        Editor.collect_manna(self)
        for new_event in events:
            donor = quit_condition(new_event.type)
            # make gun grow and become red
            if new_event.type == pygame.MOUSEBUTTONDOWN:
                if new_event.button == 1 or (new_event.button == 3 and self.manna_collected):
                    self.gun.activate()
                elif new_event.button == 3 and self.manna_collected == False:
                    error_sound.play()
            # create new ball with speed according to the gun's power and the direction according gun's direction
            elif new_event.type == pygame.MOUSEBUTTONUP:
                if new_event.button == 1:
                    self.balls.append(self.gun.strike(True))
                    shoot_sound.play()
                    self.score_table.number_of_used_balls += 1
                if new_event.button == 3 and self.manna_collected:
                    self.balls.append(self.gun.strike(False))
                    Manna_sound.play()
                    self.manna_collected = 0
                    self.manna = 0
                    self.manna_increase = 1

            # make gun move up and down on the screen
            elif new_event.type == pygame.KEYDOWN:
                if new_event.key == pygame.K_SPACE:
                    return True
                else:
                    Editor.move_machine(self, new_event)

        return donor

    def draw(self, screen_space):
        """
        Manage all drawing processes (balls', target's, gun's and score table's)
        """
        for target in self.targets:
            target.draw(screen_space)
        for ball in self.balls:
            ball.draw(screen_space)
        for new_target in self.new_targets:
            new_target.draw_smile(screen_space)
        self.gun.draw(screen_space)
        self.score_table.draw(screen_space, level)

    def strike(self):
        """
        Checks if balls bumped into targets, sets balls' alive trigger
        """
        strikes = []
        targets_strikes = []
        # make list with broken targets
        for counter, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check_bumping(ball):
                    strikes.append([counter, j])
                    targets_strikes.append(j)
        targets_strikes.sort()
        # making list with targets for deleting
        for j in reversed(targets_strikes):
            self.score_table.smashed_targets += 1
            self.targets.pop(j)
            boom_sound.play()

        strikes = []
        targets_strikes = []
        # make list with broken targets
        for counter, ball in enumerate(self.balls):
            for j, target in enumerate(self.new_targets):
                if target.check_bumping(ball) and target.change_color_condition():
                    strikes.append([counter, j])
                    targets_strikes.append(j)
                    die_smile_sound.play()

                elif (target.check_bumping(ball)) and not target.change_color_condition():
                    ball.were_kicked()
                    target.change_color()
                    angry_smile_sound.play()

        targets_strikes.sort()
        # making list with targets for deleting
        for j in reversed(targets_strikes):
            self.new_targets.pop(j)
            self.score_table.smashed_targets += 1


screen = pygame.display.set_mode(SCREEN_SIZE)

done = -1
level = 0
i = 0
clock = pygame.time.Clock()

edit_events = Editor(number_targets=3, number_new_targets=2)

# first page of the program
while done == -1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            done = 0
        screen.fill(ORANGE)
        font = pygame.font.SysFont("dejavusansmono", 30)
        score_surface_first = [font.render("Please, play with sound", True, WHITE),
                               font.render("WASD - move", True, WHITE),
                               font.render("F - boost on, G - boost off", True, WHITE),
                               font.render("LKM - standard shoot, RKM - big shoot", True, WHITE),
                               font.render("Press SPACE to start", True, WHITE)]
        for i in range(5):
            screen.blit(score_surface_first[i], [60, 60 + 50 * i])
        pygame.display.update()

# loop which make these program work repeatedly
while done == 0:
    clock.tick(15)
    screen.fill(WHITE)
    font = pygame.font.SysFont("dejavusansmono", 15)
    done = edit_events.process(pygame.event.get(), screen)
    pygame.display.flip()

if done == 2:
    # shows "Game over" table after tank's smashed by bomb
    screen.fill(RED)
    font = pygame.font.SysFont("dejavusansmono", 100)
    score_surface1 = font.render("Game Over", True, WHITE)
    screen.blit(score_surface1, [230, 210])
    pygame.display.update()
    while done != 0:
        for event in pygame.event.get():
            done = quit_condition(event.type)

pygame.quit()
