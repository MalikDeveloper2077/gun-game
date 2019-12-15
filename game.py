from random import randint, choice
import tkinter as tk

WIDTH = 800
HEIGHT = 600
TARGET_COLORS = ['green', 'red', 'black', 'blue', 'pink', 'yellow']


class Target:
    def __init__(self):
        self.radius = randint(15, 35)
        self.x = randint(500, WIDTH - self.radius)
        self.y = randint(self.radius, HEIGHT - self.radius)
        self.speed_x = randint(7, 15)
        self.speed_y = randint(7, 15)
        self.color = choice(TARGET_COLORS)
        self.target_id = canvas.create_oval(
            self.x - self.radius, self.y - self.radius, self.x + self.radius,
            self.y + self.radius, fill=self.color
        )

    def move(self):
        """ Перемещение мяча за единицу времени
        Метод увеличивает x и y снаряда, тем самым двигает его
        на speed_x и speed_y за один кадр прорисовки
        """
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x + self.radius >= WIDTH or self.x - self.radius <= 500:
            self.speed_x = -self.speed_x

        if self.y + self.radius >= HEIGHT or self.y - self.radius <= 0:
            self.speed_y = -self.speed_y

    def show(self):
        """ Показ движения цели на холсте """
        canvas.move(self.target_id, self.speed_x, self.speed_y)


def tick():
    """ Метод прорисовывает (обновляет) холст
    За единицу времени - 50 милисекунд
    """
    for target in targets:
        target.move()
        target.show()

    root.after(50, tick)


def main():
    global root, canvas, targets

    root = tk.Tk()
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    targets = [Target() for target in range(randint(2, 7))]

    tick()
    root.mainloop()


main()
