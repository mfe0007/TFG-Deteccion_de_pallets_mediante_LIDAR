from matplotlib import style
import matplotlib.pyplot as plt

    




class MyGUI():
    
    
    style.use('fivethirtyeight')

    counter = 0
    path = "Matplotlib_logs/trama"
    

        
    def printPoints(self,z,points,text):
        self.counter += 1
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)   
        xs = []
        ys = []
        for p in points:
            
            x = p[0]
            y = p[1]
            xs.append(x)
            ys.append(y)
        ax1.clear()
        ax1.plot(xs,ys,linestyle=':')
        path = self.path + str(self.counter)
        plt.figtext(0,0,text)
        plt.savefig(path)

        plt.show()
        
        
    
        
    
    
    def __init__(self,points):
        self.puntos = points
        
        


    
