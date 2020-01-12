from random import randint, choice
import math
import time
import tkinter as tk
import winsound

WIDTH = 1200
HEIGHT = 800
MIN_TARGETS = 7
MAX_TARGETS = 15
TARGET_AND_BULLET_COLORS = ['green', 'red', 'black', 'blue', 'pink', 'yellow', 'magenta', 'cyan']
GUN_X = 25
GUN_Y = randint(50, HEIGHT - 50)
BULLET_RADIUS = 8


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
        """To move the gun along y.
        Y of the gun increases on self.speed
        """
        self.y += self.speed

        if self.y >= HEIGHT - 50 or self.y <= 50:
            self.speed = -self.speed

    def show(self):
        """Show gun move"""
        canvas.move(self.gun_id, 0, self.speed)

    def aiming(self, event=0):
        """To aim at a target.
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
        """Shoot bullets when the <Button-1> is pressed.
        Speed of bullet depends on power
        """
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
        """All binds for gun"""
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
        """To move the gun's bullet.
        
        The method increases the x and y on speed
        and remove part of speed in one drawing frame
        
        """
        self.x += self.speed_x
        self.y += self.speed_y

        if self.speed_x > 0:
            self.speed_x -= 0.25
        else:
            self.speed_x += 0.25

        if self.speed_y > 0:
            self.speed_y -= 0.25
        else:
            self.speed_y += 0.25

        if self.x + self.radius >= WIDTH or self.x - self.radius <= 20:
            self.speed_x = -self.speed_x

        if self.y + self.radius >= HEIGHT - 20 or self.y - self.radius <= 20:
            self.speed_y = -self.speed_y

    def show(self):
        """Show bullet move on the canvas"""
        canvas.move(self.bullet_id, self.speed_x, self.speed_y)

    def hit(self):
        """Remove the target at bullet hit.
        Call the target.remove() and increase the score
        """
        global score

        for target in targets:
            if self.y <= target.y:
                if self.x + self.radius >= target.x - target.radius \
                        and (target.y - target.radius) - (self.y + self.radius) <= 0:
                    target.remove()
                    score += 1

    def remove(self):
        """Check and Delete the bullet if -3 < speed < 3"""
        if -3 <= self.speed_x <= 3 and -3 <= self.speed_y <= 3:
            bullets.remove(self)
            canvas.delete(self.bullet_id)


class Target:
    
    def __init__(self):
        self.radius = randint(13, 35)
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
        """To move the target every time which specified in tick().
        
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
        """Show target move on the canvas"""
        canvas.move(self.target_id, self.speed_x, self.speed_y)

    def remove(self):
        """Remove the target when bullet hit the target"""
        targets.remove(self)
        canvas.delete(self.target_id)


def tick():
    """The method updates the canvas every 50 ms.
    Labels and call the canvas elements functions
    """
    # Labels
    score_label = tk.Label(text=f"{score}", font=("Helvetica", 16))
    score_label.place(x=20, y=20)

    # Gun functions
    gun.move()
    gun.binds()
    gun.show()

    # Target functions
    if targets:
        for target in targets:
            target.move()
            target.show()
    else:
        for bullet in bullets:
            canvas.delete(bullet.bullet_id)
        canvas.delete(gun.gun_id)
        bullets.clear()
        new_game_elements()
        time.sleep(0.5)

    # Bullet functions
    if bullets:
        for bullet in bullets:
            bullet.move()
            bullet.show()
            bullet.hit()
            bullet.remove()

    root.after(50, tick)


def new_game_elements():
    """All elements on the canvas"""
    global gun, targets, bullets
    gun = Gun()
    targets = [Target() for target in range(randint(MIN_TARGETS, MAX_TARGETS))]
    bullets = []


def music():
    """Background music"""
    tracks = ['music/giorno.wav', 'music/giorno_christmas.wav', 'music/josuke.wav']
    winsound.PlaySound(choice(tracks), winsound.SND_ALIAS | winsound.SND_ASYNC)


def main():
    """App interface and settings"""
    global root, canvas, score
    
    # Settings
    root = tk.Tk()
    root.title("Gun Game")
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    root.iconbitmap('icon.ico')
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    # Main score
    score = 0

    # Call main methods
    new_game_elements()
    music()
    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
