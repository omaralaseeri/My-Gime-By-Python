
from tkinter import *
import math
import random

class GameObject:
    def __init__(self,canvas,id):
        self.canvas=canvas
        self.id=id
    def get_position(self):
        return self.canvas.coords(self.id)
    def move(self,x,y):
        self.canvas.move(self.id,x,y)
    def delete(self):
        self.canvas.delete(self.id)

class Ball(GameObject):
    def __init__(self,canvas,x,y):
        self.radius=10
        self.speed=10
        self.direction=[]
        x1,y1=x-self.radius,y-self.radius
        x2, y2 = x + self.radius, y + self.radius
        id=canvas.create_oval(x1,y1,x2,y2,fill="black")
        super(Ball,self).__init__(canvas,id)
    def init_direction(self,angle):
        self.direction=[math.cos(angle),math.sin(angle)]
    def change_position(self):
        x=self.direction[0]*self.speed
        y = self.direction[1] * self.speed
        self.move(x,y)

class Arrow(GameObject)\
        :
    def __init__(self,canvas,x,y):
        self.angle=-3.14/2
        x1,y1=x,y
        x2,y2=x1+100*math.cos(self.angle),y1+100*math.sin(self.angle)
        id=canvas.create_line(x1,y1,x2,y2,arrow=LAST)
        super(Arrow,self).__init__(canvas,id)
    def right(self,event):
        self.angle+=0.2
        if self.angle>=-0.1:
            self.angle=-0.1
        self.update()
    def left(self,event):
        self.angle-=0.2
        if self.angle<=-3.1:
            self.angle=-3.1
        self.update()
    def update(self):
        coords=self.get_position()
        x1,y1=coords[0],coords[1]
        x2, y2 = x1 + 100 * math.cos(self.angle), y1 + 100 * math.sin(self.angle)
        self.canvas.coords(self.id,x1,y1,x2,y2)
class Brick(GameObject):
    colors={1:"Magenta",2:'Yellow',3:'Cyan',4:'Green',5:'Blue'}
    width=30
    height=30
    def __init__(self,canvas,x,y,hits):
        self.hits=hits
        self.color=Brick.colors[hits]
        x1,y1=x-Brick.width/2,y-Brick.height/2
        x2,y2=x+Brick.width/2,y+Brick.height/2
        id=canvas.create_rectangle(x1,y1,x2,y2,fill=self.color,tags='brick')
        super(Brick,self).__init__(canvas,id)
        self.text=self.canvas.create_text(x1+10,y1+10,text=str(self.hits))

    def hit(self):
        self.hits-=1
        if self.hits==0:
            self.canvas.delete(self.id)
            self.canvas.delete(self.text)
        else:
            self.canvas.itemconfig(self.text,text=str(self.hits))
            self.canvas.itemconfig(self.id,fill=Brick.colors[self.hits])
class Game:
    def __init__(self):
        self.w=800
        self.h=500
        self.ball=None
        self.arrow=None
        self.bricks={}
        self.text_start=None
        self.bottom_line=self.h-100
        self.top_line=50
        self.window=Tk()
        self.window.geometry("{}x{}+{}+{}".format(self.w,self.h,100,100))
        self.window.title("My Game")
        self.canvas=Canvas(self.window,width=self.w,height=self.h)
        self.canvas.pack()
        self.canvas.focus_set()
        self.add_ball()
        self.add_arrow()
        self.add_bricks(4)
        self.add_text_start()
        self.window.mainloop()
    def add_ball(self):
        self.ball=Ball(self.canvas,self.w/2,self.bottom_line)
    def add_arrow(self):
        coords=self.ball.get_position()
        x,y=(coords[0]+coords[2])/2 , (coords[1]+coords[3])/2
        self.arrow=Arrow(self.canvas,x,y)
        self.canvas.bind("<Left>",self.arrow.left)
        self.canvas.bind("<Right>", self.arrow.right)
    def add_bricks(self,nb_lines):
        for x in range(Brick.width,self.w-Brick.width,Brick.width):
            for y in range(nb_lines):
                x_brick=x+Brick.width/2
                y_brick=self.top_line+y*Brick.height
                if random.choice([True,False]):
                    obj=Brick(self.canvas,x_brick,y_brick,random.randrange(1,6))
                    self.bricks[obj.id]=obj
    def add_text_start(self):
        self.text_start=self.draw_text("Press Space to start",400,200)
        self.canvas.bind("<space>", self.start_game)
    def draw_text(self,text,x,y,size='30'):
        font =('Times',size)
        return self.canvas.create_text(x,y,text=text,font=font)
    def start_game(self,event):
        self.canvas.unbind("<space>")
        self.canvas.unbind("<Left>")
        self.canvas.unbind("<Right>")
        self.delete_start_text()
        self.ball.init_direction(self.arrow.angle)
        self.delete_arrow()
        self.game_loop()
    def game_loop(self):
        coords=self.ball.get_position()
        if coords[1]>=self.bottom_line:
            self.ball.move(0,-20)
            self.init_game()
        else:
            self.check_collision()
            if len(self.canvas.find_withtag("brick"))==0:
                self.draw_text("you win",400,250)
            else:
                self.ball.change_position()
                self.canvas.after(10,self.game_loop)
    def check_collision(self):
        coords=self.ball.get_position()
        if coords[0]<=0 or coords[2]>=self.w:
            self.ball.direction[0]*=-1
        elif coords[1]<=0:
            self.ball.direction[1] *= -1
        else:
            list_id=list(self.canvas.find_overlapping(*coords))
            list_id.remove(self.ball.id)
            obj_list=[self.bricks[x] for x in list_id if x in self.bricks]
            if len(obj_list)>1:
                self.ball.direction[1]*=-1
            elif len(obj_list)==1:
                coords_obj=obj_list[0].get_position()
                x_b=(coords[0]+coords[2]) /2
                x_obj=(coords_obj[0]+coords_obj[2])/2
                if x_b>x_obj:
                    self.ball.direction[0]=1
                elif x_b<x_obj:
                    self.ball.direction[0] = -1
                else:
                    self.ball.direction[1] *= -1
            for obj in obj_list:
                obj.hit()
    def init_game(self):
        self.add_arrow()
        self.add_text_start()
        self.canvas.bind("<space>", self.start_game)

    def delete_start_text(self):
        self.canvas.delete(self.text_start)
    def delete_arrow(self):
        self.arrow.delete()

Game()