import tkinter as tk
import sys
sys.path.insert(0, "D:/2M/Vision/Computer_Vision_Project")
from Part_2.game import Game

class GameLauncher(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Game Launcher")
        self.geometry("300x200")
        
        self.create_widgets()

    def create_widgets(self):
        label_width = tk.Label(self, text="Camera Width:")
        label_width.pack(pady=5)
        self.entry_width = tk.Entry(self)
        self.entry_width.pack(pady=5)

        label_height = tk.Label(self, text="Camera Height:")
        label_height.pack(pady=5)
        self.entry_height = tk.Entry(self)
        self.entry_height.pack(pady=5)

        label_game_width = tk.Label(self, text="Game Frame Width:")
        label_game_width.pack(pady=5)
        self.entry_game_width = tk.Entry(self)
        self.entry_game_width.pack(pady=5)

        label_game_height = tk.Label(self, text="Game Frame Height:")
        label_game_height.pack(pady=5)
        self.entry_game_height = tk.Entry(self)
        self.entry_game_height.pack(pady=5)

        launch_button = tk.Button(self, text="Launch Game", command=self.launch_game)
        launch_button.pack(pady=10)

    def launch_game(self):
        try:
            cap_width = int(self.entry_width.get())
            cap_height = int(self.entry_height.get())
            game_frame_width = int(self.entry_game_width.get())
            game_frame_height = int(self.entry_game_height.get())

            # Create and run the game
            game = Game(cap_width, cap_height, game_frame_width, game_frame_height)
            game.run()

        except ValueError:
            print("Please enter valid numeric values for dimensions.")

if __name__ == "__main__":
    app = GameLauncher()
    app.mainloop()
