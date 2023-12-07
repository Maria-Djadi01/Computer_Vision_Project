import tkinter as tk
import random
import sys

# sys.path.append("../../Computer_Vision_Project")
# sys.path.insert(1, "../Part_1")
# import object_detection


class BrickRacingGame:
    def __init__(self, master):
        self.master = master
        self.car_width = 30
        self.car_height = 30
        self.car_color = "green"
        self.car_pos = [320, 400]

        self.obstacle_width, self.obstacle_height = 50, 30
        self.obstacle_color = "red"
        self.obstacle_speed = 3
        self.obstacle_id = None
        self.new_obstacle_created = False

        self.score = 0

        self.game_started = False
        self.game_ended = False

        self.start_button = tk.Button(
            self.master, text="Start", command=self.start_game
        )
        self.start_button.place(relx=0.9, rely=0.1, anchor="center")

        self.end_button = tk.Button(self.master, text="End", command=self.end_game)
        self.end_button.place(relx=0.9, rely=0.2, anchor="center")

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}")
        self.score_label.place(relx=0.9, rely=0.3, anchor="center")

        self.canvas = tk.Canvas(self.master, width=399, height=570, bg="black")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.car = self.canvas.create_rectangle(
            self.car_pos[0],
            self.car_pos[1],
            self.car_pos[0] + self.car_width,
            self.car_pos[1] + self.car_height,
            fill=self.car_color,
        )

        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

    def move_left(self, event):
        self.car_pos[0] -= 133
        if self.car_pos[0] >= 0:
            self.draw_car()
        else:
            self.car_pos[0] = 54

    def move_right(self, event):
        self.car_pos[0] += 133
        if self.car_pos[0] + self.car_width < self.canvas.winfo_width():
            self.draw_car()
        else:
            self.car_pos[0] = 320

    def start_game(self):
        if not self.game_started:
            self.game_ended = False
            self.game_started = True
            self.score = 0
            self.score_label.config(text=f"Score: {self.score}")
            self.countdown()
            self.car_pos = [320, 400]
            self.canvas.delete(self.car)
            self.car = self.canvas.create_rectangle(
                self.car_pos[0],
                self.car_pos[1],
                self.car_pos[0] + self.car_width,
                self.car_pos[1] + self.car_height,
                fill=self.car_color,
            )

            self.game_loop()

    def end_game(self):
        if not self.game_ended:
            self.game_ended = True
            self.game_started = False
            self.canvas.delete("all")
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Game Over",
                font=("Helvetica", 30),
                fill="red",
            )

    def countdown(self):
        countdown_text = ["3", "2", "1", "GO!"]

        for i, text in enumerate(countdown_text, start=1):
            self.canvas.delete("countdown_text")  # Delete only the text item
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text=text,
                font=("Helvetica", 30),
                fill="red",
                tags="countdown_text",  # Add a tag to the text item
            )
            self.master.update()
            self.master.after(500)
            self.canvas.delete("countdown_text")  # Delete only the text item
            self.draw_car()
            self.master.update()
            self.master.after(500)

    def draw_car(self):
        self.canvas.coords(
            self.car,
            self.car_pos[0],
            self.car_pos[1],
            self.car_pos[0] + self.car_width,
            self.car_pos[1] + self.car_height,
        )

    def generate_obstacle(self):
        x = random.choice([320, 187, 54])
        self.obstacle_id = self.canvas.create_rectangle(
            x,
            0,
            x + self.obstacle_width,
            self.obstacle_height,
            fill=self.obstacle_color,
        )

    def move_obstacle(self, obstacle_id):
        if obstacle_id:
            self.canvas.move(obstacle_id, 0, self.obstacle_speed)
            obstacle_coords = self.canvas.coords(obstacle_id)
            if obstacle_coords[1] + self.obstacle_height > self.canvas.winfo_height():
                self.score += 1
                print("Score: ", self.score)
                self.canvas.delete(obstacle_id)
                self.obstacle_id = None

    def game_over(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            text=f"Game Over\nYour score is: {self.score}",
            font=("Helvetica", 30),
            fill="red",
        )

    def game_loop(self):
        # if not self.game_ended:
        #     self.game_ended = False
        self.score_label.config(text=f"Score: {self.score}")
        self.draw_car()
        if not self.obstacle_id or not self.new_obstacle_created:
            self.generate_obstacle()
            self.new_obstacle_created = True

        for obstacle_id in self.canvas.find_all():
            if obstacle_id == self.car:
                continue
            self.move_obstacle(obstacle_id)

        # Check if the current obstacle has passed a certain position
        if self.obstacle_id:
            obstacle_coords = self.canvas.coords(self.obstacle_id)
            if obstacle_coords[1] > 350:
                self.new_obstacle_created = False

        # Check for collisions
        for obstacle_id in self.canvas.find_all():
            if obstacle_id == self.car:
                continue
            obstacle_coords = self.canvas.coords(obstacle_id)
            if (
                obstacle_coords[1] + self.obstacle_height >= self.car_pos[1]
                and obstacle_coords[1] <= self.car_pos[1] + self.car_height
                and obstacle_coords[0] + self.obstacle_width >= self.car_pos[0]
                and obstacle_coords[0] <= self.car_pos[0] + self.car_width
            ):
                self.canvas.delete(self.car)
                self.canvas.delete(self.obstacle_id)
                self.obstacle_id = None
                self.game_over()
                self.game_started = False
                return

        self.master.after(10, self.game_loop)


root = tk.Tk()
root.title("Vision Project")
window_width = 700
window_height = 600

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

centerX = int(screen_width / 2 - window_width / 2)
centerY = int(screen_height / 2 - window_height / 2)

root.geometry(f"{window_width}x{window_height}+{centerX}+{centerY}")

game = BrickRacingGame(root)

root.mainloop()
