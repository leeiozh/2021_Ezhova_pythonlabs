import turtle
from numpy import cos
from numpy import pi

step = 25

turtle.shape('turtle')
turtle.penup()
turtle.forward(step)
turtle.pendown()

for j in range(1, 11):
    turtle.pendown()
    turtle.left(90 + 180 / (j + 2))
    for i in range(j + 2):
        turtle.forward(step * j * (2 - 2 * cos(pi * 2 / (j + 2))) ** 0.5)
        turtle.left(360 / (j + 2))
    turtle.right(90 + 180 / (j + 2))
    turtle.penup()
    turtle.forward(step)
    turtle.pendown()

input()