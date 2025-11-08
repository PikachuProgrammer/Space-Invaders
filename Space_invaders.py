import turtle
import os
import time
import random

# things needed to do:
# Make seperate laser class for enemy and player

#Set up the window
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.tracer(0)                    # disable automatic screen updates

#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerSpeed = 7

Round = 1 #The round the player is on

GameStatus = "booting up"

#Create the enemy

enemyspeed = 2


Enemies = []

class Enemy:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = 2

        self.turtle = turtle.Turtle()
        self.turtle.color("red")
        self.turtle.shape("circle")
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setposition(self.x, self.y)
    def move(self):
        # Move the enemy back and down
        x = self.turtle.setx(self.turtle.xcor() + self.speed)
        if self.turtle.xcor() > 280:
            y = self.turtle.ycor()
            y -= 40
            self.turtle.sety(y)
            self.speed *= -1
        if self.turtle.xcor() < -280:
            y = self.turtle.ycor()
            y -= 40
            self.turtle.sety(y)
            self.speed *= -1

    def shoot(self):
        i = random.randint(1,100)
        if i == 1:
            laser = EnemyLaser(self.turtle.xcor(), self.turtle.ycor() - 20)
            laser.turtle.showturtle()
            EnemyLasers.append(laser)
    

# Laser class
Lasers = []
EnemyLasers = []
class Laser:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = "ready"
        self.speed = 20

        self.turtle = turtle.Turtle()
        self.turtle.color("yellow")
        self.turtle.shape("triangle")
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setheading(90)
        self.turtle.shapesize(0.5, 0.5)
        self.turtle.hideturtle()
        self.turtle.setposition(x, y)
    def move(self):
        y = self.turtle.ycor()
        y += self.speed
        self.turtle.sety(y)
        if self.turtle.ycor() > 275:
            self.turtle.hideturtle()
            self.state = "ready"

class EnemyLaser:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = "ready"
        self.speed = 20

        self.turtle = turtle.Turtle()
        self.turtle.color("yellow")
        self.turtle.shape("triangle")
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.setheading(90)
        self.turtle.shapesize(0.5, 0.5)
        self.turtle.hideturtle()
        self.turtle.setposition(x, y)
    def move(self):
        y = self.turtle.ycor()
        y -= self.speed
        self.turtle.sety(y)
        if self.turtle.ycor() < -275:
            self.turtle.hideturtle()
            self.state = "ready"


#player movement
def move_left():
    x = player.xcor()
    x -= playerSpeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerSpeed
    if x > 280:
        x = 280
    player.setx(x)



# collision detection
def isCollision(t1, t2, threshold=20):
    return t1.distance(t2) < threshold

LastShotTime = 0

def create_laser():
    global LastShotTime
    current_time = time.time()
    if current_time - LastShotTime > 1:  # 1 second cooldown
        LastShotTime = current_time
        laser = Laser(player.xcor(), player.ycor() + 10)
        laser.turtle.showturtle()
        Lasers.append(laser)

    else:
        return
    
# Create controls
wn.listen()                      # listens for keyboard inputs
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(create_laser, "space")

def round1():
    x = -200

    while len(Enemies) < 5:
        enemy = Enemy(x,250)
        Enemies.append(enemy)
        x += 25
        print(x)
        time.sleep(0.1)
    return


#Main game loop
while True:
    if Round == 1 and GameStatus == "booting up":
        round1()
        GameStatus = "playing"
    if len(Enemies) == 0 and GameStatus == "playing":
        Text = turtle.Turtle()
        Text.color("white")
        Text.hideturtle()
        Text.write("You won!", align="center", font=("Arial", 24, "normal"))
        GameStatus = "game over"

    for enemy_laser in EnemyLasers:# controls every Enemy laser in the list:
        enemy_laser.move()
        if isCollision(enemy_laser.turtle, player,15):
            player.hideturtle()
            print("Game Over")
            GameStatus = "game over"
            Text = turtle.Turtle()
            Text.hideturtle()
            Text.color("white")
            Text.penup()
            Text.write("Game Over", align="center", font=("Arial", 24, "normal"))


        if enemy_laser.turtle.ycor() < -275:
            EnemyLasers.remove(enemy_laser)



    for laser in Lasers:# controls every Player laser in the list
        laser.move()

        if laser.turtle.ycor() > 275:
            Lasers.remove(laser)
            laser.turtle.hideturtle()

    for enemy in Enemies:# controls every enemy in the list
        enemy.move()
        enemy.shoot()
        
        for laser in Lasers:
           if isCollision(laser.turtle, enemy.turtle,15):
               laser.turtle.hideturtle()
               enemy.turtle.hideturtle()
               Lasers.remove(laser)
               Enemies.remove(enemy)
    wn.update()                   # update the screen once per frame
    time.sleep(1/60)              # cap to ~60 FPS





