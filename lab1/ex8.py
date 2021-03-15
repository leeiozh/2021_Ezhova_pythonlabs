import turtle

turtle.shape('turtle')

for i in range(1, 21):

    turtle.forward(10 * i)
    turtle.left(90)
    turtle.forward(10 * i)
    turtle.left(90)


input()