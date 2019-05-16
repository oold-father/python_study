
#%%
from tkinter import *
import tkinter.messagebox
import random   
class snake(Frame):   
        def __init__(self, master=None):   
                Frame.__init__(self, master)   
                self.body = [(0,0)]   
                self.bodyid = []   
                self.food = [ -1, -1 ]   
                self.foodid = -1   
                self.gridcount = 10    
                self.size = 500   
                self.di = 3   
                self.speed = 400  
   
                self.top = self.winfo_toplevel()   
                self.top.resizable(False, False)   
                self.grid()   
                self.canvas = Canvas(self)   
                self.canvas.grid()   
                self.canvas.config(width=self.size, height=self.size,relief=RIDGE)   
   
                self.drawgrid()   
                s = self.size/self.gridcount   
                id = self.canvas.create_rectangle(self.body[0][0]*s,self.body[0][1]*s,    
                        (self.body[0][0]+1)*s, (self.body[0][1]+1)*s, fill="yellow")   
                self.bodyid.insert(0, id)
                #self.bind_all("<KeyRelease>", self.keyrelease)   
                self.drawfood()
                
                self.after(self.speed, self.drawsnake)   
        def drawgrid(self):   
                s = self.size/self.gridcount   
                for i in range(0, self.gridcount+1):   
                        self.canvas.create_line(i*s, 0, i*s, self.size)   
                        self.canvas.create_line(0, i*s, self.size, i*s)   
        def drawsnake(self):   
                s = self.size/self.gridcount   
                head = self.body[0]   
                new = [head[0], head[1]]
                l_new={}
                if self.di == 1:
                        new = [head[0], (head[1]-1)]
                        l_new['1']=new
                        new = [(head[0]+1), head[1]]
                        l_new['2']=new
                        new = [(head[0]-1), head[1]]
                        l_new['4']=new
                elif self.di == 2:   
                        new = [(head[0]+1), head[1]]
                        l_new['2']=new
                        new = [head[0], (head[1]-1)]
                        l_new['1']=new
                        new = [head[0], (head[1]+1)]
                        l_new['3']=new
                elif self.di == 3:   
                        new = [head[0], (head[1]+1)]
                        l_new['3']=new
                        new = [(head[0]+1), head[1]]
                        l_new['2']=new
                        new = [(head[0]-1), head[1]]
                        l_new['4']=new
                else:   
                        new = [(head[0]-1), head[1]]
                        l_new['4']=new
                        new = [head[0], (head[1]-1)]
                        l_new['1']=new
                        new = [head[0], (head[1]+1)]
                        l_new['3']=new
                #if new[0] < 0 or new[0] >= self.gridcount or new[1] < 0 or new[1] >= self.gridcount:
                        #tkinter.messagebox.showinfo("end","游戏结束");
                        #exit()

                l_new={v:k for k,v in l_new.items()}
                dic=[]
                for i in l_new:
                    if i[0] < 0 or i[0] >= self.gridcount or i[1] < 0 or i[1] >= self.gridcount:
                        continue
                    elif (i[0],i[1]) in self.body:
                        continue
                    else:
                        distnce=abs(self.food[0]+self.food[1]-i[0]-i[1])
                        dic.append([int(l_new[i]),i,distance])
                print(dic)
                if next == (self.food[0], self.food[1]):   
                        self.body.insert(0, next)   
                        self.bodyid.insert(0, self.foodid)   
                        self.drawfood()   
                else:   
                        tail = self.body.pop()   
                        id = self.bodyid.pop()   
                        self.canvas.move(id, (next[0]-tail[0])*s, (next[1]-tail[1])*s)   
                        self.body.insert(0, next)   
                        self.bodyid.insert(0, id)   
   
                self.after(self.speed, self.drawsnake)
        def drawfood(self):   
                s = self.size/self.gridcount   
                x = random.randrange(0, self.gridcount)   
                y = random.randrange(0, self.gridcount)   
                while (x, y) in self.body:   
                        x = random.randrange(0, self.gridcount)   
                        y = random.randrange(0, self.gridcount)   
                id = self.canvas.create_rectangle(x*s,y*s, (x+1)*s, (y+1)*s, fill="red")   
                self.food[0] = x   
                self.food[1] = y   
                self.foodid = id
                
        def keyrelease(self, event):   
                if event.keysym == "Up" and self.di != 3:   
                        self.di = 1   
                elif event.keysym == "Right" and self.di !=4:   
                        self.di = 2   
                elif event.keysym == "Down" and self.di != 1:   
                        self.di = 3   
                elif event.keysym == "Left" and self.di != 2:   
                        self.di = 4   
   
app = snake()   
app.master.title("Greedy Snake")   
app.mainloop()


#%%



