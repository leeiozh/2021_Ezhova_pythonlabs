import turtle
from numpy import cos
from numpy import pi

def DrawStar(peaks):

    if peaks == 1:
        print('ERROR')

    if peaks % 2 == 1:
        for i in range(peaks):
            turtle.forward(300)
            if i != peaks - 1:
                turtle.left(180 - 180 / peaks)

    else:
        DrawStar(peaks // 2)
        turtle.left(180 - 180 / peaks)
        turtle.penup()
        turtle.forward(300 / cos(pi / peaks))
        turtle.pendown()
        turtle.left(180 - 180 / peaks)
        DrawStar(peaks // 2)



DrawStar(int(input('Enter number of peaks >> ')))

input()