from tkinter import Tk,Frame, Button
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

        


    def matplotCanvas(self):
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(self.x,self.y)

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side = "bottom", fill = "both", expand = True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        canvas._tkcanvas.pack(side = "top", fill = "both", expand = True)








if __name__ == '__main__':
    root = MyGUI()
    MyGUI.matplotCanvas(root)
    root.mainloop()
 


'''

class User_Interface:
    
    
    
    
    
    def __init__(self,  master):
        self.frame = Frame(master)
        self.frame.pack()
        self.start_button = Button(master,text="Comenzar la ejecucion", command=self.mainFunction)
        self.start_button.pack(side="left")
        #self.sv_button = Button(master,text="Iniciar servidor de prueba", command=DummySV.main())
        #self.sv_button.pack(side="left")
    
    
    
    
    
    
    

    def plotGraph (self,x,y):
        
        fig = Figure(figsize=(6,6))
        a = fig.add_subplot(111)
        a.plot(x,y)
        
        a.set_title ("Lectura del laser", fontsize=16)
        a.set_ylabel("Y", fontsize=14)
        a.set_xlabel("X", fontsize=14)

        canvas = FigureCanvasTkAgg(fig, self)
        
        canvas.get_tk_widget().pack(side = "bottom", fill = "both", expand = True)
        canvas.draw()
        
        
    

    
    

    """Aqui se crea la ventana principal de la interfaz grafica y se instancia el objeto
    con los metodos para conectar y tratar los datos"""
    root = Tk()
    myclass = User_Interface(root)
    
    root.mainloop()
    
    
    
    
'''