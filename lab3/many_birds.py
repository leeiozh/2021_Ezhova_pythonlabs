import pygame
import numpy as np
import pygame.draw as draw
from math import sin


def draw_background(surf, length, height):
    """
    Функция раскрашивает фон картинки
    :param surf: поверхность, которую надо раскрасить
    :param length: ширина поверхности
    :param height: высота картинки
    :return: функция ничего не возвращает
    """
    draw.rect(surf, (33, 33, 120), (0, 0, length, 0.1 * height))
    draw.rect(surf, (141, 95, 211), (0, 0.1 * height, length, 0.05 * height))
    draw.rect(surf, (205, 135, 222), (0, 0.15 * height, length, 0.1 * height))
    draw.rect(surf, (222, 135, 170), (0, 0.25 * height, length, 0.15 * height))
    draw.rect(surf, (255, 153, 85), (0, 0.4 * height, length, 0.1 * height))
    draw.rect(surf, (0, 102, 128), (0, 0.5 * height, length, 0.5 * height))


def draw_seabirds(surf, color, length, height):
    """
    Функция рисует птичку в небе
    :param surf: поверхность, на которой нужно нарисовать птичку
    :param color: цвет птички
    :param length: ширина поверхности
    :param height: высота поверхности
    :return: функция ничего не возвращает
    """
    for i in range(2):
        draw.arc(surf, color, (0.13 * length, 0.033 * height + i, 100, 128), np.pi / 3, 7 * np.pi / 9)
        draw.arc(surf, color, (0.235 * length, 0.02 * height + i, 100, 128), np.pi / 3, 7 * np.pi / 9)


def print_seabirds(length, height):
    """
    Функция вызывает функцию, рисующую птичку, и помещает эту птичку на дополнительную поверхность. Далее на основе
    этой поверхности создаются другие, отображающие птичек других размеров, и размещает их по небу
    :param length: ширина поверхности
    :param height: высота поверхности
    :return: функция ничего не возвращает
    """
    draw_seabirds(surface, white, length, height)

    surface2 = pygame.transform.rotate(surface, -20)
    surface3 = pygame.transform.rotate(surface, 0)
    big_seabird = pygame.transform.rotate(surface2, -20)
    medium_seabird = pygame.transform.scale(surface3, (200, 200))
    small_seabird = pygame.transform.scale(surface2, (150, 150))
    roten_small_seabird = pygame.transform.rotate(small_seabird, 20)

    screen.blit(surface3, (0, 0))
    screen.blit(big_seabird, (0.07 * length, 0.04 * height))
    screen.blit(surface2, (-0.11 * length, 0.2 * height))

    screen.blit(medium_seabird, (0.7 * length, 0.14 * height))
    screen.blit(medium_seabird, (0.76 * length, 0.3 * height))
    screen.blit(medium_seabird, (0.6 * length, 0.2 * height))
    screen.blit(medium_seabird, (0.55 * length, 0.24 * height))
    screen.blit(medium_seabird, (0.27 * length, 0.23 * height))
    screen.blit(medium_seabird, (0.09 * length, 0.11 * height))
    screen.blit(medium_seabird, (-0.127 * length, 0.1 * height))
    screen.blit(medium_seabird, (0.58 * length, 0.05 * height))
    screen.blit(medium_seabird, (0.36 * length, 0.013 * height))

    screen.blit(roten_small_seabird, (0.18 * length, 0.13 * height))
    screen.blit(roten_small_seabird, (0.09 * length, 0.18 * height))
    screen.blit(roten_small_seabird, (0.05 * length, 0.13 * height))
    screen.blit(roten_small_seabird, (0.42 * length, 0.3 * height))

    screen.blit(small_seabird, (-0.05 * length, 0.17 * height))
    screen.blit(small_seabird, (0.18 * length, 0.3 * height))
    screen.blit(small_seabird, (0.36 * length, 0.1 * height))
    screen.blit(small_seabird, (0.36 * length, 0.26 * height))


def draw_wings(surf, wings_surface, x_0, y_0):
    """
    Функция рисует на дополнительной поверхности wings_surf крылья птицы
    :param surf: базовая поверхность
    :param wings_surface: дополнительная поверхность
    :param x_0: координата по х верхнего конца крыла
    :param y_0: координата по у верхнего конца крыла
    :return: функция ничего не возвращает
    """
    wings_part_1 = []
    wings_part_2 = []
    wings_part_3 = []
    black_wings_part_1 = []
    black_wings_part_3 = []
    black_wings_part_2 = []

    for x in range(0, 142, 1):
        re = [x + x_0, y_0 - 6 + (93 / (3 * np.pi)) * (np.sin(3 * x * np.pi / 142) + 3 * x * np.pi / 142)]
        black_re = [x + x_0 - 1, y_0 - 6 + (93 / (3 * np.pi)) * (np.sin(3 * x * np.pi / 142) + 3 * x * np.pi / 142)]
        wings_part_1.append(re)
        black_wings_part_1.append(black_re)
        ra = [x + x_0 + 50, y_0 + 93 * (x ** 4) / (142 ** 4)]
        black_ra = [x + x_0 + 51, y_0 + 93 * (x ** 4) / (142 ** 4)]
        wings_part_2.insert(0, ra)
        black_wings_part_2.insert(0, black_ra)
        ry = [x + x_0, y_0 - 20 + 10000000 * 1.7 * 93 * (x ** (1 / 2)) / (142 ** 4)]
        black_ry = [x + x_0 + 1, y_0 - 20 + 10000000 * 1.7 * 93 * (x ** (1 / 2)) / (142 ** 4)]
        black_wings_part_3.insert(0, black_ry)
        wings_part_3.insert(0, ry)
    wings_part_1.append([192, 87 + y_0])
    wings_part_1.append([192, 86 + y_0])

    for x in range(0, 141, 1):
        if x < 38:
            wings_part_1.append(wings_part_2[x])
            black_wings_part_1.append(black_wings_part_2[x])
        else:
            wings_part_1.append(wings_part_3[x])
            black_wings_part_1.append(black_wings_part_3[x])
    draw.polygon(wings_surface, black, black_wings_part_1)
    draw.polygon(wings_surface, white, wings_part_1)

    draw.polygon(surf, white, ((190, 480), (140, 440), (125, 500), (190, 510)))


def draw_legs(surf_2, surf_1, length, width):
    """
    Функция рисует на дополнительных поверхностях ноги птицы
    :param surf_2: поверхность, на которой будет нарисована желтая часть лапок и черный контур вокруг лапок
    :param surf_1: поверхность, на которой будут нарисованы ноги без желтой части лапок
    :param length: длина белой части ноги
    :param width: ширина белой части ноги
    :return: функция ничего не возвращает
    """
    draw.ellipse(surf_2, white, (45, 10, 20, 50))
    draw.ellipse(surf_1, white, (0, 0, 30, 60))
    draw.polygon(surf_2, black,
                 [(width - 1, length), (width - 16, length + 10), (width - 31, length + 29),
                  (width - 5, length + 11), (width - 1, length + 36), (width + 4, length + 19),
                  (width + 1, length + 11),
                  (width + 1, length + 9), (width + 19, length + 34), (width + 18, length + 19),
                  (width + 11, length + 11), (width + 7, length + 4), (width + 36, length + 30),
                  (width + 29, length + 14), (width + 11, length)])
    draw.polygon(surf_2, (234, 211, 114),
                 [(width + 0, length), (width - 15, length + 10), (width - 30, length + 28),
                  (width - 5, length + 10), (width, length + 35), (width + 3, length + 20),
                  (width, length + 10),
                  (width + 2, length + 8), (width + 20, length + 33), (width + 17, length + 20),
                  (width + 10, length + 10), (width + 7, length + 4), (width + 35, length + 29),
                  (width + 28, length + 14), (width + 10, length)])


def print_albatross(x_0, y_0, length, height):
    """
    Функция рисует птицу. Она вызывает функции, рисующие крылья и лапы и рисует тело и остальные части птицы
     на дополнительных поверхностях, которые потом отображает на главном экране.
    :param x_0: координата по х верхнего конца крыла
    :param y_0: координата по у верхнего конца крыла
    :param length: ширина экрана
    :param height: длина экрана
    :return: функция ничего не возвращает
    """
    draw_wings(screen, wings_surf, x_0, y_0)
    draw_legs(leg1_surf, leg_surf, 58, 50)

    wings_surf2 = pygame.transform.rotate(wings_surf, -15)
    leg2_surf = pygame.transform.rotate(leg1_surf, 25)
    leg0_surf = pygame.transform.rotate(leg_surf, 12)

    draw.polygon(alba_surf, white, (
        (0.345 * length, 0.623 * height), (0.254 * length, 0.571 * height), (0.227 * length, 0.649 * height),
        (0.345 * length, 0.662 * height)))

    # albatross' wings & body
    alba_surf.blit(wings_surf2, (-20, -45))
    alba_surf.blit(wings_surf, (30, 0))
    draw.ellipse(alba_surf, white, (x_0 + 130, y_0 + 50, 160, 80))

    # albatross' legs
    alba_surf.blit(leg_surf, (0.436 * length, 0.662 * height))
    alba_surf.blit(leg0_surf, (0.472 * length, 0.506 * height))
    alba_surf.blit(leg2_surf, (0.418 * length, 0.4285 * height))
    alba_surf.blit(leg2_surf, (0.364 * length, 0.435 * height))

    # rest albatross' parts
    draw.polygon(alba_surf, black,
                 [(0.79 * length, 0.6 * height), (0.872 * length, 0.59 * height), (0.893 * length, 0.609 * height),
                  (0.872 * length, 0.631 * height), (0.79 * length, 0.621 * height)])
    draw.polygon(alba_surf, (255, 221, 85),
                 [(0.79 * length, 0.6 * height), (0.872 * length, 0.59 * height), (0.89 * length, 0.61 * height),
                  (0.872 * length, 0.63 * height), (0.79 * length, 0.62 * height)])
    draw.ellipse(alba_surf, white, (0.23 * length, 0.63 * height, 0.109 * length, 0.039 * height))
    draw.polygon(alba_surf, black,
                 [(0.79 * length, 0.61 * height), (0.818 * length, 0.611 * height), (0.89 * length, 0.6 * height)])
    draw.ellipse(alba_surf, white, (x_0 + 0.49 * length, y_0 + 0.065 * height, 0.145 * length, 0.052 * height))
    draw.ellipse(alba_surf, white, (x_0 + 0.6 * length, y_0 + 0.065 * height, 0.109 * length, 0.052 * height))
    draw.circle(alba_surf, black, (x_0 + 0.682 * length, y_0 + 0.09 * height), 5)
    screen.blit(alba_surf, (0, 0))
    alba_screen2 = pygame.transform.scale(alba_surf, (150, 150))
    screen.blit(alba_screen2, (250, 270))
    alba_screen3 = pygame.transform.flip(alba_screen2, True, False)
    screen.blit(alba_screen3, (400, 300))


def draw_fish(weight_fish, length_fish):
    """
    Функция рисует тело рыбки
    :param weight_fish: ширина рыбки
    :param length_fish: длина рыбки
    :return: функция ничегоо не возвращает
    """
    r = (weight_fish ** 2 + length_fish ** 2) / (2 * weight_fish)
    z = 2 * r - 2 * weight_fish

    # body
    draw.circle(surf3, black, (250, 200), int(r) + 1)
    draw.circle(surf4, black, (250, 200 + int(z)), int(r) + 1)
    draw.circle(surf1, fishy, (250, 200), int(r))
    draw.circle(surf2, fishy, (250, 200 + int(z)), int(r))


def print_fishes():
    """
    Функция вызывает функцию, рисующую рыбку, и рисует для нее плавники на доп поверхностях. затем эти поверхности
    отображаются на главном экране в разных местах.
    :return: функция ничего не возвращает
    """
    draw_fish(weight_fish, length_fish)

    surf3.blit(surf4, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(surf3, (89, 382))
    surf1.blit(surf2, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    draw.circle(surf1, (7, 60, 184), (280, 270), 6)
    draw.circle(surf1, black, (280, 270), 3)
    draw.circle(surf1, black, (x_second_fish + 7, y_second_fish + 13), 8)
    draw.circle(surf1, fins, (x_second_fish + 7, y_second_fish + 13), 7)
    draw.polygon(surf1, black,
                 [(x_second_fish - 1, y_second_fish), (x_second_fish + 11, y_second_fish),
                  (x_second_fish + 26, y_second_fish + 11), (x_second_fish + 11, y_second_fish + 15),
                  (x_second_fish, y_second_fish + 12)])
    draw.polygon(surf1, fins,
                 [(x_second_fish, y_second_fish), (x_second_fish + 10, y_second_fish),
                  (x_second_fish + 24, y_second_fish + 10), (x_second_fish + 11, y_second_fish + 15),
                  (x_second_fish, y_second_fish + 12)])
    draw.polygon(surf1, black,
                 [(x_tail + 42, y_tail + 14), (x_tail + 42, y_tail + 12), (x_tail, y_tail), (x_tail + 7, y_tail + 29)])
    draw.polygon(surf1, fishy, [(x_tail + 41, y_tail + 13), (x_tail + 1, y_tail + 1), (x_tail + 8, y_tail + 28)])
    draw.circle(surf1, black, (x_big_fin + 49, y_big_fin + 13), 6)
    draw.polygon(surf1, black,
                 [(x_big_fin - 2, y_big_fin - 1), (x_big_fin + 46, y_big_fin + 6), (x_big_fin + 47, y_big_fin + 19),
                  (x_big_fin + 24, y_big_fin + 17)])
    draw.polygon(surf1, fins,
                 [(x_big_fin, y_big_fin), (x_big_fin + 45, y_big_fin + 7), (x_big_fin + 47, y_big_fin + 19),
                  (x_big_fin + 25, y_big_fin + 17)])
    draw.circle(surf1, fins, (x_big_fin + 48, y_big_fin + 13), 6)
    draw.circle(surf1, fins, (20 + x_fish, 12 + y_fish), 3)
    draw.polygon(surf1, black,
                 [(12 + x_fish, y_fish), (x_fish + 23, y_fish), (x_fish + 23, y_fish + 11), (18 + x_fish, y_fish + 15),
                  (x_fish - 2, 15 + y_fish)])
    draw.polygon(surf1, fins,
                 [(13 + x_fish, y_fish), (x_fish + 22, y_fish), (x_fish + 22, y_fish + 11), (18 + x_fish, y_fish + 14),
                  (x_fish, 14 + y_fish)])
    screen.blit(surf1, (89, 382))
    flipeweight_fish = pygame.transform.flip(surf3, True, False)
    screen.blit(flipeweight_fish, (-150, 370))
    flipeweight_fish = pygame.transform.flip(surf1, True, False)
    screen.blit(flipeweight_fish, (-150, 370))
    screen.blit(surf3, (220, 300))
    screen.blit(surf1, (220, 300))


def cloud(x0, y0, surface):
    """
    Функция описывает отрисовку облака на экране
    :param x0: координата x левого верхнего угла облака
    :param y0: координата y левого верхнего угла облака
    :param surface: поверхность для облака
    :return: функция ничего не возвращает
    """
    cloudcolor = 'white'
    pygame.draw.circle(surface, cloudcolor, (x0 + 20, y0 + 30), 20)
    pygame.draw.circle(surface, cloudcolor, (x0 + 55, y0 + 35), 35)
    pygame.draw.circle(surface, cloudcolor, (x0 + 75, y0 + 45), 25)
    pygame.draw.circle(surface, cloudcolor, (x0 + 80, y0 + 20), 20)
    pygame.draw.circle(surface, cloudcolor, (x0 + 25, y0 + 50), 15)


def move_cloud(counter_, speed):
    """
    Функция перемещает облако
    :param counter_: счетчик часов
    :param speed: скорость  облака
    :return: функция ничего не возвращает
    """
    cloud_ = pygame.Surface((100, 80))
    cloud_.set_colorkey('black')
    cloud(0, 0, cloud_)
    screen.blit(cloud_, (counter_ * speed, 50 - 20 * sin(counter_ / 20)))


pygame.init()

FPS = 30
screen = pygame.display.set_mode((550, 770))
alba_surf = pygame.Surface((550, 707), pygame.SRCALPHA, 32)
surface = pygame.Surface((320, 240), pygame.SRCALPHA, 32)
surface.convert_alpha()
surf1 = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
surf2 = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
surf3 = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
surf4 = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
wings_surf = pygame.Surface((550, 707), pygame.SRCALPHA, 32)
leg_surf = pygame.Surface((550, 707), pygame.SRCALPHA, 32)
leg1_surf = pygame.Surface((550, 707), pygame.SRCALPHA, 32)

# COLORS
black = (0, 0, 0)
white = (255, 255, 255)
fishy = (71, 136, 147)
red = (180, 50, 50)

weight_fish = 15
length_fish = 48
r = (weight_fish ** 2 + length_fish ** 2) / (2 * weight_fish)
z = 2 * r - 2 * weight_fish
fins = (102, 99, 112)
size = (0, 0, 300, 200)
x_big_fin = 215
y_big_fin = 235
x_fish = 210
y_fish = 280
x_tail = 160
y_tail = 255
x_second_fish = 255
y_second_fish = 283

pygame.display.update()
clock = pygame.time.Clock()
done = False
counter = 0

while not done:
    clock.tick(FPS)
    counter += 1

    draw_background(screen, 550, 770)

    print_seabirds(550, 770)

    print_albatross(50, 400, 550, 770)

    print_fishes()

    move_cloud(counter, 4)

    move_cloud(counter, 8)

    move_cloud(counter, 16)

    move_cloud(counter, 25)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

pygame.quit()
