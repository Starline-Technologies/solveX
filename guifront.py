from tkinter import *

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Draw Character")
        
        self.coords = []

        # Create canvas and bind mouse events
        self.canvas = Canvas(self.master, width=300, height=300, bg="white")
        self.canvas.grid(row=0, column=0, pady=2, sticky=W)

        self.canvas.bind("<ButtonPress-1>", self.start_pos)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

        # Create label to display status messages
        self.status_label = Label(self.master, text="")
        self.status_label.grid(row=1, column=0, pady=2, sticky=W)

        # Create button to submit drawing
        self.button_submit = Button(self.master, text="Submit", command=self.submit_drawing)
        self.button_submit.grid(row=2, column=0, pady=2)

        # Create button to clear canvas
        self.button_clear = Button(self.master, text="Clear", command=self.clear_all)
        self.button_clear.grid(row=3, column=0, pady=2)

    def start_pos(self, event):
        # Capture starting position of mouse click
        self.coords.append((event.x, event.y))

    def draw_lines(self, event):
        # Draw line on canvas and capture coordinates
        x1, y1 = self.coords[-1]
        x2, y2 = event.x, event.y
        self.canvas.create_line(x1, y1, x2, y2, width=8)
        self.coords.append((x2, y2))

    def clear_all(self):
        # Clear canvas and reset status label and coordinates list
        self.canvas.delete("all")
        self.status_label.configure(text="")
        self.coords = []

    def submit_drawing(self):
        if len(self.coords) == 0:
            self.status_label.configure(text="Error: nothing to submit")
        else:
            # Display coordinates in status label
            self.status_label.configure(text=f"Submitted {len(self.coords)} coordinates: {self.coords}")

root = Tk()
app = App(root)
root.mainloop()
