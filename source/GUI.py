from matplotlib import style
import matplotlib.animation as animation
import matplotlib.pyplot as plt


    




class MyGUI():

    style.use('fivethirtyeight')
    
    def __init_(self):
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        
        
    
    def animate(self,i):
        try:
            data = open('plotdata.txt','r')
            #data.read()
            lines = [line.rstrip('\n') for line in data]
            #print(lines)

            xs = []
            ys = []
            for line in lines:
                if len(line)>1:
                    x,y = line.split(',')
                    xs.append(x)
                    ys.append(y)
            self.ax1.clear()
            self.ax1.plot(xs,ys,linestyle='-')

            print("Plotting new data")
        finally:
            data.close()

    def start(self,function):
        fig = plt.figure()
        self.ax1 = fig.add_subplot(1,1,1)

        a = animation.FuncAnimation(fig, function, interval = 1)
        plt.ioff()
        print("Before plt.show")
        plt.show(block=False)
        print("After plt show")
        plt.show()
        

    
   