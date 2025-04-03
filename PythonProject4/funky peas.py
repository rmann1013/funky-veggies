import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class TransparentGifPlayer:
    def __init__(self, gif_path, speed_factor=1.0):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window borders
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.wm_attributes('-transparentcolor', 'black')  # Make black transparent

        self.gif_path = gif_path
        self.speed_factor = speed_factor
        self.frames = []
        self.delays = []  # Store frame delays
        self.load_gif()

        self.label = tk.Label(self.root, bg='black')
        self.label.pack()

        self.position_window()  # Move to bottom-right

        self.update_frame(0)

        self.root.bind("<space>", self.restart_gif)  # Restart on spacebar
        self.root.bind("<q>", self.quit_app)  # Quit on 'q'

        self.root.mainloop()

    def load_gif(self):
        gif = Image.open(self.gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")  # Preserve transparency
            self.frames.append(ImageTk.PhotoImage(frame))
            self.delays.append(frame.info.get("duration", 100))  # Default to 100ms if missing

    def position_window(self):
        """Automatically positions the GIF at the bottom-right of the screen."""
        self.root.update_idletasks()  # Ensure window dimensions are calculated

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Get GIF dimensions (first frame)
        gif = Image.open(self.gif_path)
        gif_width, gif_height = gif.size

        # Calculate bottom-right position
        x_position = screen_width - gif_width + 90  # 20px padding from right
        y_position = screen_height - gif_height - 20 # 60px padding from bottom

        self.root.geometry(f"{gif_width}x{gif_height}+{x_position}+{y_position}")

    def update_frame(self, index):
        """Updates the GIF frame and loops it."""
        frame_delay = int(self.delays[index] / self.speed_factor)  # Adjust speed
        self.label.configure(image=self.frames[index])
        index = (index + 1) % len(self.frames)  # Loop GIF
        self.root.after(frame_delay, self.update_frame, index)

    def restart_gif(self, event=None):
        """Restarts the GIF from the beginning."""
        self.update_frame(0)

    def quit_app(self, event=None):
        """Closes the application."""
        self.root.destroy()

# Path to GIF file
gif_path = "C:/Users/16142/Documents/GitHub/funky-veggies/PythonProject4/peas no background.gif"

# Play GIF with transparency at bottom-right
TransparentGifPlayer(gif_path, speed_factor=0.8)
