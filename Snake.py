import random as r
import tkinter as tk


class Snake:
    def __init__(self, canvas):
        self.body_size = 2
        self.space_size = 20
        self.body_color = "#3ede3e"
        self.coordinates = []
        self.squares = []
        self.canvas = canvas

        for _ in range(self.body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(x, y, x + self.space_size, y + self.space_size,
                                                  fill=self.body_color, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, canvas, width, height):
        self.space_size = 20
        self.food_color = "#db1309"
        self.canvas = canvas
        self.width = width
        self.height = height

        # Modify the following lines
        x = r.randint(0, (self.width // self.space_size) - 1) * self.space_size
        y = r.randint(0, (self.height // self.space_size) - 1) * self.space_size
        self.coordinates = [x, y]
        self.canvas.create_oval(x, y, x + self.space_size, y + self.space_size, fill=self.food_color, tag="eat")

class Game:
    def __init__(self):
        self.height = 400
        self.width = 400
        self.speed = 300
        self.background_color = "#000000"
        self.direction = "right"
        self.score = 0

        self.win = tk.Tk()
        self.win.title("Snake Game")

        self.label = tk.Label(self.win, text="points: {}".format(self.score), font=('consolas', 15))
        self.label.pack()

        self.canvas = tk.Canvas(self.win, bg=self.background_color, height=self.height, width=self.width)
        self.canvas.pack()

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.width, self.height)

        self.win.update()
        win_width = self.win.winfo_width()
        win_height = self.win.winfo_height()
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = int((screen_width / 2) - (win_height / 2))
        y = int((screen_height / 2) - (win_height / 2))
        self.win.geometry(f"{win_width}x{win_height}+{x}+{y}")

        self.win.bind('<Left>', lambda event: self.change_direction('left'))
        self.win.bind('<Right>', lambda event: self.change_direction('right'))
        self.win.bind('<Up>', lambda event: self.change_direction('up'))
        self.win.bind('<Down>', lambda event: self.change_direction('down'))

        self.next_turn()

        self.win.mainloop()

    def next_turn(self):
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= self.snake.space_size
        elif self.direction == "down":
            y += self.snake.space_size
        elif self.direction == "left":
            x -= self.snake.space_size
        elif self.direction == "right":
            x += self.snake.space_size

        self.snake.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + self.snake.space_size, y + self.snake.space_size,
                                              fill=self.snake.body_color)
        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text="points: {}".format(self.score))
            self.canvas.delete("eat")
            self.food = Food(self.canvas, self.width, self.height)
        else:
            self.snake.coordinates.pop()
            self.canvas.delete(self.snake.squares[-1])
            self.snake.squares.pop()

        if self.check_collision():
            self.game_over()
        else:
            self.win.after(self.speed, self.next_turn)

    def check_collision(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= self.width:
            return True
        if y < 0 or y >= self.height:
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def change_direction(self, new_direction):
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, text="GAME OVER",font=('Helvetica','30','bold'),
                                fill="Red", tags="gameover")


game = Game()
