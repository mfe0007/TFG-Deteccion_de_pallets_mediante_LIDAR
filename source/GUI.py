from tkinter import Tk,Frame, Button, Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
    




class MyGUI(Tk):
    def __init__(self,x,y):
        super(MyGUI, self).__init__()
        self.title("Tkinter Matplotlib Embeding")
        self.x = x
        self.y = y
        self.minsize(640, 400)
        #self.wm_iconbitmap('icon.ico')
        #self.configure(background = '#4D4D4D')

        


    def matplotCanvas(self,fps):
        f = Figure(figsize=(5,5), dpi=100)
        
        a = f.add_subplot(111)
        a.plot(self.x,self.y)
        
        canvas = FigureCanvasTkAgg(f, self)
        close_button = Button(canvas._tkcanvas,text="Siguiente",command=canvas.delete("all"))
        close_button.pack()
        canvas.draw()
        canvas.get_tk_widget().pack(side = "bottom", fill = "both", expand = True)
        frames = Label(canvas._tkcanvas,text="FPS: "+str(round(fps,2)))
        

        toolbar = NavigationToolbar2Tk(canvas, self)
        canvas._tkcanvas.pack(side = "top", fill = "both", expand = True)
        frames.pack()
