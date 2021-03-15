import turtle

x = -300
y = 0
Vx = 20
Vy = 40
g = 10
dt = 0.1

while x < 300:
    if y < 0:
        Vy *= - 0.8
        y *= - 1
    Vy -= g * dt
    y += Vy * dt
    x += Vx * dt
    turtle.goto(x, y)

input()