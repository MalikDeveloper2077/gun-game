from random import randint, choice
import math
import tkinter as tk

WIDTH = 1200
HEIGHT = 800
MAX_TARGETS = 15
TARGET_AND_BULLET_COLORS = ['green', 'red', 'black', 'blue', 'pink', 'yellow', 'magenta']
GUN_X = 25
GUN_Y = randint(20, HEIGHT - 20)
BULLET_RADIUS = 7


class Gun:
    def __init__(self):
        self.x = GUN_X
        self.y = GUN_Y
        self.power = 10
        self.angle = 1
        self.speed = randint(3, 5)
        self.gun_id = canvas.create_line(
            self.x, self.y, 25, self.y, width=8
        )

    def move(self):
        """ Moving the gun along y
        Y of the gun increases on self.speed
        """
        self.y += self.speed

        if self.y >= HEIGHT - 30 or self.y <= 30:
            self.speed = -self.speed

    def show(self):
        """ Show gun move """
        canvas.move(self.gun_id, 0, self.speed)

    def aiming(self, event=0):
        """ To aim at a target
        Depends on mouse position
        """
        if event:
            try:
                self.angle = math.atan((event.y - self.y) / (event.x - self.x))
            except ZeroDivisionError:
                self.angle = math.atan((event.y - self.y) / 1)

        canvas.coords(self.gun_id, self.x, self.y,
                      self.x + self.x * math.cos(self.angle),
                      self.y + self.x * math.sin(self.angle)
                      )

    def shoot(self, event):
        """ To shoot bullets when button of mouse have clicked
        Speed of bullet depends on power"""
        if self.angle >= 0.7:
            self.power = 80
        elif 0.5 <= self.angle <= 0.7:
            self.power = 50
        else:
            self.power = 40

        speed_x = self.power * math.cos(self.angle)
        speed_y = self.power * math.sin(self.angle)
        bullet = Bullet(
            speed_x,
            speed_y,
            self.x + self.x * math.cos(self.angle),
            self.y + self.x * math.sin(self.angle)
        )
        bullets.append(bullet)

    def binds(self):
        """ All binds for gun """
        canvas.bind('<Motion>', self.aiming)
        canvas.bind('<Button-1>', self.shoot)


class Bullet:
    def __init__(self, speed_x, speed_y, x, y):
        self.radius = BULLET_RADIUS
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = choice(TARGET_AND_BULLET_COLORS)
        self.bullet_id = canvas.create_oval(
            x - self.radius, y - self.radius, x + self.radius,
            y + self.radius, fill=self.color
        )

    def move(self):
        """ Moving the gun's bullet
        The method increases the x and y on speed
        in one drawing frame
        """
        self.x += self.speed_x
        self.y += self.speed_y

        if self.speed_x > 0:
            self.speed_x -= 0.1
        else:
            self.speed_x += 0.1

        if self.speed_y > 0:
            self.speed_y -= 0.1
        else:
            self.speed_y += 0.1

        if self.x + self.radius >= WIDTH or self.x - self.radius <= 20:
            self.speed_x = -self.speed_x

        if self.y + self.radius >= HEIGHT - 20 or self.y - self.radius <= 20:
            self.speed_y = -self.speed_y

    def show(self):
        """ Shows bullet move on the canvas """
        canvas.move(self.bullet_id, self.speed_x, self.speed_y)

    def remove(self):
        """ Check and Deletes the bullet after 7 seconds
        if bullet speed equals 0
        """
        if -3 <= self.speed_x <= 3 or -3 <= self.speed_y <= 3:
            bullets.remove(self)
            canvas.delete(self.bullet_id)


class Target:
    def __init__(self):
        self.radius = randint(10, 35)
        self.x = randint(WIDTH // 1.3, WIDTH - self.radius)
        self.y = randint(self.radius, HEIGHT - self.radius)
        self.speed_x = randint(7, 15)
        self.speed_y = randint(7, 15)
        self.color = choice(TARGET_AND_BULLET_COLORS)
        self.target_id = canvas.create_oval(
            self.x - self.radius, self.y - self.radius, self.x + self.radius,
            self.y + self.radius, fill=self.color
        )

    def move(self):
        """ Moving the target every time which specified in tick()
        The method increases the x and y on speed_x and
        speed_y in one drawing frame
        """
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x + self.radius >= WIDTH or self.x - self.radius <= WIDTH // 1.5:
            self.speed_x = -self.speed_x

        if self.y + self.radius >= HEIGHT - 20 or self.y - self.radius <= 20:
            self.speed_y = -self.speed_y

    def show(self):
        """ Shows target move on the canvas """
        canvas.move(self.target_id, self.speed_x, self.speed_y)


def tick():
    """ Method updates the canvas every 50 ms """
    gun.move()
    gun.binds()
    gun.show()

    for target in targets:
        target.move()
        target.show()

    if bullets:
        for bullet in bullets:
            bullet.move()
            bullet.show()
            bullet.remove()

    root.after(50, tick)


def main():
    """ App interface and settings
    Define elements on canvas
    """
    global root, canvas, gun, targets, bullets

    root = tk.Tk()
    root.title("Gun Game")
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    # All elements on canvas
    gun = Gun()
    targets = [Target() for target in range(randint(5, MAX_TARGETS))]
    bullets = []

    tick()
    root.mainloop()


main()
