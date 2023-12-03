    self.move_obstacle(self.obstacle_id)

        # Change the range to allow for obstacles more frequently
        new_obstacle_frequency = random.randint(1, 5)

        if new_obstacle_frequency == 1 and not self.obstacle_id:
            self.generate_obstacle()
        elif self.obstacle_id:
            obstacle_coords = self.canvas.coords(self.obstacle_id)

            # Check if the obstacle and the car overlap
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