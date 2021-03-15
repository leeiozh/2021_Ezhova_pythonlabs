import turtle

turtle.shape('turtle')
for i in range(1, 11):

    turtle.forward(10 * i)
    turtle.left(90)
    turtle.forward(10 * i)
    turtle.left(90)
    turtle.forward(10 * i)
    turtle.left(90)
    turtle.forward(10 * i)
    turtle.right(45)
    turtle.penup()
    turtle.forward(7)
    turtle.left(135)
    turtle.pendown()


input()