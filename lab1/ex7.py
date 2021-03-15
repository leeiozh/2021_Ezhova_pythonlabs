import turtle

turtle.shape('turtle')

for i in range(360*10):

    turtle.forward(1 + i / 1000)
    turtle.left(1)

input()