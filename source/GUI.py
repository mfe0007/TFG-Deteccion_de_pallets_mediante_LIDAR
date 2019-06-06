from matplotlib import style
import matplotlib.animation as animation
import matplotlib.pyplot as plt


    




class MyGUI():

    style.use('fivethirtyeight')
    
    def __init_(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        
        
    
    def animate(self,i,points):
        
           
        #lines = [line.rstrip('\n') for line in points]
        #print(lines)

        xs = []
        ys = []
        for line in points:
            if len(line)>1:
                x = line[0]
                y = line[1]
                xs.append(x)
                ys.append(y)
        self.ax1.clear()
        # print(len(xs))
        self.ax1.plot(xs,ys,linestyle='-')

        print("Plotting new data")
        

#pasar datos  funcion animate sin fichero
    def start(self,function,points):
        fig = plt.figure()
        self.ax1 = fig.add_subplot(1,1,1)
        a = animation.FuncAnimation(fig, self.animate, fargs=[points], interval = 0.1)
        plt.show(block=False)
        plt.show()
        

    
   