"""
GUI Classes for Job Shop Scheduler

This script defines two classes, GUI and GUI_Update, which provide graphical 
user interfaces for visualizing the job shop scheduling results using Gantt charts.

Classes:
    GUI: A class to display a single Gantt chart.
    GUI_Update: A class to display an updating sequence of Gantt charts.

Functions:
    __init__(self, image_bytes): Initializes the GUI with a single Gantt chart.
    __init__(self, machine_log, config): Initializes the GUI_Update with multiple Gantt charts.
    update(self): Updates the displayed Gantt chart in the GUI_Update class.
"""

from visualization.Gantt import Gantt
import io
from tkinter import *
from PIL import Image, ImageTk

simmode = ''

class GUI:
    """
    A class to display a single Gantt chart.
    
    Attributes:
        tk (Tk): The main tkinter window.
        image_bytes (bytes): The bytes of the Gantt chart image.
        image (Image): The PIL image object.
        tk_images (PhotoImage): The tkinter-compatible image object.
        frame1 (LabelFrame): The frame containing the Gantt chart.
        gantt (Label): The label displaying the Gantt chart.
    """
    
    def __init__(self, image_bytes):
        """
        Initializes the GUI with a single Gantt chart.
        
        Parameters:
            image_bytes (bytes): The bytes of the Gantt chart image.
        """
        self.tk = Tk()
        self.tk.title("Job Shop Scheduler - Hyunjin Oh")
        self.tk.geometry("1280x720")
        self.tk.resizable(False, False)
        self.image_bytes = image_bytes
        self.image = Image.open(io.BytesIO(self.image_bytes)) # 0으로 초기화하긴 했지만 byte가 들어올거라 괜찮음
        self.tk_images = ImageTk.PhotoImage(self.image)

        self.frame1 = LabelFrame(self.tk, text=simmode)
        self.frame1.grid(column=0, row=0)
        self.gantt = Label(self.frame1, text=simmode)
        self.gantt.grid(column=0, row=0, sticky=N + E + W + S)
        self.gantt.config(image=self.tk_images)
        self.tk.mainloop()


class GUI_Update:
    """
    A class to display an updating sequence of Gantt charts.
    
    Attributes:
        config: Configuration object with simulation settings.
        RANDOM_SEED (int): The random seed for reproducibility.
        tk (Tk): The main tkinter window.
        image_bytes (list): List of bytes for each Gantt chart image.
        image (list): List of PIL image objects.
        tk_images (list): List of tkinter-compatible image objects.
        current_image (int): Index of the current image being displayed.
        frame1 (LabelFrame): The frame containing the Gantt chart.
        gantt (Label): The label displaying the Gantt chart.
    """
    
    def __init__(self, machine_log, config):
        """
        Initializes the GUI_Update with multiple Gantt charts.
        
        Parameters:
            machine_log (DataFrame): The machine log DataFrame.
            config: Configuration object with simulation settings.
        """
        self.config = config
        self.RANDOM_SEED = 42
        self.tk = Tk()
        self.tk.title("Job Shop Scheduler - Hyunjin Oh")
        self.tk.geometry("1680x720+400+200")
        self.tk.resizable(False, False)
        self.image_bytes = [1 for i in range(self.config.n_show)]
        self.image = [1 for i in range(self.config.n_show)]
        self.tk_images = [1 for i in range(self.config.n_show)]
        self.current_image = 1

        for i in range(1, self.config.n_show):
            self.image_bytes[i] = Gantt(machine_log, i)
            self.image[i] = Image.open(io.BytesIO(self.image_bytes[i])) # 0으로 초기화하긴 했지만 byte가 들어올거라 괜찮음
            self.tk_images[i] = ImageTk.PhotoImage(self.image[i])

        self.frame1 = LabelFrame(self.tk, text=simmode)
        self.frame1.grid(column=0, row=0)
        self.gantt = Label(self.frame1, text=simmode)
        self.gantt.grid(column=0, row=0, sticky=N + E + W + S)

        self.update()
        self.tk.mainloop()

    def update(self):
        """
        Updates the displayed Gantt chart in the GUI_Update class.
        """
        total_images = self.config.n_op # slide show처럼 돌릴 이미지 개수

        self.gantt.config(image=self.tk_images[self.current_image])

        if self.current_image < self.config.n_op:
            self.current_image += 1

        if self.current_image == 1:
            self.tk.after(self.config.show_interval_time, self.update)  # Pause for show_interval_time milliseconds
        else:
            self.tk.after(self.config.finished_pause_time, self.update)  # Pause for finished_pause_time milliseconds
