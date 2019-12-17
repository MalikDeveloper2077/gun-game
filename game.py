from random import randint, choice
import math
import tkinter as tk

WIDTH = 1200
HEIGHT = 800
MAX_TARGETS = 15
TARGET_COLORS = ['green', 'red', 'black', 'blue', 'pink', 'yellow', 'magenta']
GUN_X = 40
GUN_Y = HEIGHT // 3


class Gun:
    def __init__(self):
        self.x = GUN_X
        self.y = GUN_Y
        self.power = 10
        self.angle = 1
        self.speed = randint(3, 5)
        self.fire_on = False
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

        if self.fire_on:
            canvas.itemconfig(self.gun_id, fill="red")

        canvas.coords(self.gun_id, self.x, self.y,
                      self.x + max(self.power, self.x) * math.cos(self.angle),
                      self.y + max(self.power, self.x) * math.sin(self.angle)
                      )


class Target:
    def __init__(self):
        self.radius = randint(15, 35)
        self.x = randint(WIDTH // 1.3, WIDTH - self.radius)
        self.y = randint(self.radius, HEIGHT - self.radius)
        self.speed_x = randint(7, 15)
        self.speed_y = randint(7, 15)
        self.color = choice(TARGET_COLORS)
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

        if self.y + self.radius >= HEIGHT or self.y - self.radius <= 0:
            self.speed_y = -self.speed_y

    def show(self):
        """ Shows target move """
        canvas.move(self.target_id, self.speed_x, self.speed_y)


def tick():
    """ Method updates the canvas every 50 ms """
    gun.move()
    gun.show()

    for target in targets:
        target.move()
        target.show()

    root.after(50, tick)


def main():
    """ App interface and settings
    Define elements on canvas + binds
    """
    global root, canvas, gun, targets

    root = tk.Tk()
    root.title("Gun Game")
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    # All elements on canvas
    gun = Gun()
    targets = [Target() for target in range(randint(5, MAX_TARGETS))]

    # Binds
    canvas.bind('<Motion>', gun.aiming)

    tick()
    root.mainloop()


main()
