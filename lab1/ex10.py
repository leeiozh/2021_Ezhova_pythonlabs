import turtle

n = int(input("Enter numbers of circles >> "))
x = 1
def flower(x):
    while x <= n:
        turtle.circle(50)
        turtle.left(360 / n)
        x += 1

flower(x)
input()