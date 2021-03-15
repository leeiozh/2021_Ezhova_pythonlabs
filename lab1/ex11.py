import turtle

def butterfly(n):

    turtle.circle(n)
    turtle.circle(-n)

turtle.left(90)
n = 10

x = 1

while x <= 20:
    butterfly(n)
    n += 5
    x += 1

input()