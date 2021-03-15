from random import randint
import turtle


number_of_turtles = 10
steps_of_time_number = 1000

speedX = [randint(-5, 5) for i in range(number_of_turtles)]
speedY = [randint(-5, 5) for i in range(number_of_turtles)]
x = [randint(-200, 200) for i in range(number_of_turtles)]
y = [randint(-200, 200) for i in range(number_of_turtles)]

pool = [turtle.Turtle(shape='turtle') for i in range(number_of_turtles)]

for i in range(number_of_turtles):
    pool[i].penup()
    pool[i].speed(10)
    pool[i].goto(x[i], y[i])

for t in range(steps_of_time_number):
    for i in range(number_of_turtles):
        x[i] += speedX[i]
        y[i] += speedY[i]
        if x[i] > 200 or x[i] < -200:
            speedX[i] *= -1
        if y[i] > 200 or y[i] < -200:
            speedY[i] *= -1
        pool[i].goto(x[i], y[i])
        for c in range(number_of_turtles):
            if abs(x[c] - x[i]) <= 10 and abs(y[c] - y[i]) <= 10:
                speedX[c] *= -1
                speedX[i] *= -1
                speedY[c] *= -1
                speedY[i] *= -1