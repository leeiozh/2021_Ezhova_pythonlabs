import numpy as np
import pygame
from pygame.draw import *
from random import randint

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SCREEN_SIZE = (800, 600)


def rand_color():
    return randint(0, 200), randint(0, 200), randint(0, 200)


class Ball:
    """
    Creates a ball, controls it's movement
    """

    def __init__(self, coord, speed, ball_radius=20, color=None):
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

    def move(self, time=1, gravitation=0):
        """
        Moving the ball according to it's speed and time step
        Change the ball's speed because of gravitation
        """
        self.speed[1] += gravitation
        for i in range(2):
            self.coord[i] += time * self.speed[i]
        self.check_corners()
        if self.speed[0] ** 2 + self.speed[1] ** 2 < 6:
            self.is_alive = False

    def check_corners(self, reflection_decline_border=0.8, reflection_decline=0.9):
        """
        Change ball's speed when the ball bumps into the screen borders
        """
        for i in range(2):
            if self.coord[i] < self.ball_radius:
                self.coord[i] = self.ball_radius
                self.speed[i] = - int(self.speed[i] * reflection_decline_border)
                self.speed[1 - i] = int(self.speed[1 - i] * reflection_decline)
            elif self.coord[i] > SCREEN_SIZE[i] - self.ball_radius:
                self.coord[i] = SCREEN_SIZE[i] - self.ball_radius
                self.speed[i] = - int(self.speed[i] * reflection_decline_border)
                self.speed[1 - i] = int(self.speed[1 - i] * reflection_decline)

    def draw(self, screen_face):
        """
        Draws the ball on appropriate surface.
        """
        circle(screen_face, self.color, self.coord, self.ball_radius)


class Gun:
    """
    Class for the movement and focusing of the gun
    """

    def __init__(self, coord=None, angle=0, maximum_power=80, minimum_power=10, gun_color=BLACK):
        """
        Setting of coordinates, direction, minimums and maximums power and color of the gun
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

    def move(self, add_power):
        """
        Changes vertical position of the gun
        """
        if (self.coord[1] > 30 or add_power > 0) and (self.coord[1] < SCREEN_SIZE[1] - 30 or add_power < 0):
            self.coord[1] += add_power

    def strike(self):
        """
        Creates ball, according to gun's direction and current charge power
        """
        speed = int(self.power * 1.3)
        angle = self.angle
        ball = Ball(list(self.coord), [int(speed * np.cos(angle)), int(speed * np.sin(angle))])
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
        polygon(screen_space, self.gun_color, gun_shape)


class Target:
    """
    Creates target, manages it's rendering and bumping with a ball event.
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

        if color is None:
            color = rand_color()
        self.color = color

    def check_bumping(self, ball):
        """
        Checks if the ball bumped into target
        """
        minimum_distantion = self.ball_radius + ball.ball_radius
        distantion = sum([(self.coord[i] - ball.coord[i]) ** 2 for i in range(2)]) ** 0.5
        return distantion <= minimum_distantion

    def draw(self, screen_space):
        """
        Draws the target on the screen
        """
        circle(screen_space, self.color, self.coord, self.ball_radius)


class ScoreTable:
    """
    Class for scoretable
    """

    def __init__(self, smashed_targets=0, number_of_used_balls=0):
        self.smashed_targets = smashed_targets
        self.number_of_used_balls = number_of_used_balls
        # set font for writing
        self.font = pygame.font.SysFont("dejavusansmono", 25)

    def score(self):
        """
        Score calculation by subtraction number of used balls and broken targets
        """
        return self.smashed_targets - self.number_of_used_balls

    def draw(self, screen_space):
        # making list with strings about now user's score
        score_surface = [self.font.render("Targets hitted: {}".format(self.smashed_targets), True, BLACK),
                         self.font.render("Balls used: {}".format(self.number_of_used_balls), True, BLACK)]
        # conditions for changing color of the score string
        if self.score() >= 0:
            score_surface.append(self.font.render("Total score: {}".format(self.score()), True, GREEN))
        if self.score() < 0:
            score_surface.append(self.font.render("Total score: {}".format(self.score()), True, RED))
        # addition of strings in the right corner
        for i in range(3):
            screen_space.blit(score_surface[i], [10, 10 + 30 * i])


def quit_condition(pressed_button):
    """
    condition of quit by exit button
    """
    finished = False
    if pressed_button == pygame.QUIT:
        finished = True
    return finished


class editor:
    """
    Class that manages user events, create targets, make balls move and check if they bumped into targets
    """

    def __init__(self, number_targets=1):
        # init all gun characteristics
        self.balls = []
        self.gun = Gun()
        self.targets = []
        self.score_table = ScoreTable()
        self.number_targets = number_targets
        self.new_mission()

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

        if len(self.targets) == 0 and len(self.balls) == 0:
            self.new_mission()

        return donor

    def new_mission(self):
        """
        Addition of new targets after destroying the old one
        """
        # make balls even smaller because of the big count
        if self.score_table.score() < 0:
            for i in range(self.number_targets):
                self.targets.append(Target(ball_radius=30))
        else:
            for i in range(self.number_targets):
                self.targets.append(Target(
                    ball_radius=randint(max(1, 30 - 2 * self.score_table.score()), 30 - self.score_table.score())))

    def move(self):
        """
        Making balls fly with gravitation, raise the gun's power, removes dead balls
        """
        dead_balls = []
        for j, ball in enumerate(self.balls):
            ball.move(gravitation=5)
            if not ball.is_alive:
                dead_balls.append(j)
        for j in reversed(dead_balls):
            self.balls.pop(j)
        self.gun.gun_power()

    def user_events(self, events):
        """
        Analyze events from keyboard, mouse, etc.
        """
        donor = False
        for event in events:
            donor = quit_condition(event.type)
            # make gun grow and become red
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.gun.activate()
            # create new ball with speed according to the gun's power and the direction according gun's direction
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.balls.append(self.gun.strike())
                    self.score_table.number_of_used_balls += 1
            # make gun move up and down on the screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.gun.move(-5)
                elif event.key == pygame.K_DOWN:
                    self.gun.move(5)

        return donor

    def draw(self, screen_space):
        """
        Manage all drawing processes (balls', target's, gun's and score table's)
        """
        for target in self.targets:
            target.draw(screen_space)
        for ball in self.balls:
            ball.draw(screen_space)

        self.gun.draw(screen_space)
        self.score_table.draw(screen_space)

    def strike(self):
        """
        Checks if balls bumped into targets, sets balls' alive trigger
        """
        strikes = []
        targets_strikes = []
        # make list with broken targets
        for i, ball in enumerate(self.balls):
            for j, target in enumerate(self.targets):
                if target.check_bumping(ball):
                    strikes.append([i, j])
                    targets_strikes.append(j)
        targets_strikes.sort()
        # making list with targets for deleting
        for j in reversed(targets_strikes):
            self.score_table.smashed_targets += 1
            self.targets.pop(j)


screen = pygame.display.set_mode(SCREEN_SIZE)

done = False
clock = pygame.time.Clock()

edit_events = editor(number_targets=3)
# loop which make these program work repeatedly
while not done:
    clock.tick(15)
    screen.fill(WHITE)
    done = edit_events.process(pygame.event.get(), screen)
    pygame.display.flip()

pygame.quit()
