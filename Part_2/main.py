import tkinter as tk
import sys

sys.path.insert(0, r"C:\Users\HI\My-Github\Computer_Vision_Project")
from Part_2.game import Game
from Part_1.green_screen import GreenScreen
from Part_1.object_detection import ObjectDetector
import cv2


class GameLauncher(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Game Launcher")
        self.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        label_game_width = tk.Label(self, text="Game Frame Width:")
        label_game_width.pack(pady=5)
        self.entry_game_width = tk.Entry(self)
        self.entry_game_width.pack(pady=5)

        label_game_height = tk.Label(self, text="Game Frame Height:")
        label_game_height.pack(pady=5)
        self.entry_game_height = tk.Entry(self)
        self.entry_game_height.pack(pady=5)

        launch_game_button = tk.Button(self, text="Launch Game", command=self.launch_game)
        launch_game_button.pack(pady=10)
        
        launch_green_screen = tk.Button(self, text="Launch Green Screen", command=self.launch_green_screen)
        launch_green_screen.pack(pady=10)
        
        launch_object_detector = tk.Button(self, text="Launch Object Detector", command=self.launch_object_detector)
        launch_object_detector.pack(pady=10)

    def launch_game(self):
        try:
            cap_width = int(self.entry_width.get())
            cap_height = int(self.entry_height.get())
            game_frame_width = int(self.entry_game_width.get())
            game_frame_height = int(self.entry_game_height.get())

            # Create and run the game
            game = Game(game_frame_width, game_frame_height)
            game.run()

        except ValueError:
            print("Please enter valid numeric values for dimensions.")
    
    def launch_green_screen(self):
        try:
            green_screen = GreenScreen("D:/2M/Vision/Computer_Vision_Project/back.jpg")

            green_screen.run()

        except ValueError:
            print("Please enter valid numeric values for dimensions.")

    def launch_object_detector(self):
        try:
            # Run the object detector
            object_detector = ObjectDetector()
            object_detector.run()
        except ValueError:
            print("Please enter valid numeric values for dimensions.")


# if __name__ == "__main__":
#     app = GameLauncher()
#     app.mainloop()
