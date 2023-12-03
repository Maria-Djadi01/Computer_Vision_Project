import tkinter as tk
import random


class BrickRacingGame:
    def __init__(self, master):
        self.master = master
        self.car_width = 30
        self.car_height = 30
        self.car_color = "green"
        # pos if the right upper corner of the rectangle
        self.car_pos = [320, 400]

        # Obstacles
        self.obstacle_width, self.obstacle_height = 50, 30
        self.obstacle_color = "red"
        self.obstacle_speed = 3
        self.obstacle_frequency = 1
        self.obstacle_id = None
        self.new_obstacle_created = False

        self.score = 0

        self.canvas = tk.Canvas(self.master, width=399, height=570, bg="black")
        self.canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Draw the car
        self.car = self.canvas.create_rectangle(
            self.car_pos[0],
            self.car_pos[1],
            self.car_pos[0] + self.car_width,
            self.car_pos[1] + self.car_height,
            fill=self.car_color,
        )

        # Move the car using Arrows
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)

        # self.generate_obstacle()
        self.game_loop()

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
                self.canvas.delete(obstacle_id)
                self.obstacle_id = None

    def game_loop(self):
        # Move the existing obstacle
        self.move_obstacle(self.obstacle_id)

        # Check if the obstacle has reached a specific position
        if self.obstacle_id:
            obstacle_coords = self.canvas.coords(self.obstacle_id)
            if (
                obstacle_coords[1] + self.obstacle_height >= 300
                and not self.new_obstacle_created
            ):
                self.new_obstacle_created = True
                # Generate multiple obstacles in one iteration
                num_new_obstacles = (
                    3  # Set the number of obstacles you want to generate
                )
                for _ in range(num_new_obstacles):
                    self.generate_obstacle()

        # Check if the obstacle has passed the specified y-coordinate, reset the flag
        if self.obstacle_id and obstacle_coords[1] + self.obstacle_height >= 400:
            self.new_obstacle_created = False

        # Rest of the code remains unchanged
        new_obstacle_frequency = random.randint(1, 5)
        if (
            new_obstacle_frequency == 1
            and not self.obstacle_id
            and not self.new_obstacle_created
        ):
            # Generate one obstacle in each iteration
            self.generate_obstacle()

        elif self.obstacle_id:
            obstacle_coords = self.canvas.coords(self.obstacle_id)
            if (
                obstacle_coords[1] + self.obstacle_height > self.car_pos[1]
                and obstacle_coords[0] < self.car_pos[0] + self.car_width
                and obstacle_coords[0] + self.obstacle_width > self.car_pos[0]
            ):
                self.canvas.delete(self.obstacle_id)
                self.obstacle_id = None
                self.score += 1
                print("Score:", self.score)

        self.master.after(10, self.game_loop)


# Create the main Tkinter window
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

# Run the Tkinter event loop
root.mainloop()
