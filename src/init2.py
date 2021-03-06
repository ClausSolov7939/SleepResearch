import os
from shutil import move
from tkinter import *
from tkinter import filedialog
# get settings from configuration file
configstd={
            "screen": "Оконный", 
            "program": "Задачки",
            "control": "Обычное",
            "file": "None",
            "tone_play": 1,

           # "inverse": 0, 
            
            "width": 1024, 
            "height": 768, 
            "round": 20, 
            
            "tone_rate": 440,
            "tone_volume": 4096,
            "tone_delay": 1.5,

            "radius_multiplier": 1.5,
            "possible": 200, 
            "freq": 0.25, 
            
            "sensivity": 20, 
            "dot_time":0.5,
            "time":5, 

            }

config={}
if not(os.path.exists("config.txt")):
    config=configstd
#-----------------------------------
    f=open("config.txt", "w")
    for i in config:
        f.write(str(i)+" "+str(config[i])+"\n")
    f.close()
#-----------------------------------
else:
    f=open("config.txt", "r")
    for i in f:
        try:
            if '\n' in i:
                config.update({i.split(" ")[0]:i.split(" ")[1][:-1]}) 
            else:
                config.update({i.split(" ")[0]:i.split(" ")[1]}) 
        except Exception as e:
            pass
    
    for i in configstd.keys():
        if not(i in config.keys()):
            config.update({i:configstd.get(i)}) 
        
#====================================================#
print(config)
start_prog=False
root = Tk()
root.resizable(False, False)
root.title('Окно конфигураций')

lbl=[[],(13,18,17,20),("Главные настройки", "Тон пробуждения", "Мыши","Задачки"),
    ("Режим окна:","Ширина (пикс.): ","Высота (пикс.): ","Управление: ","Программа: ","Кол-во опытов: "),
    ("Включение тона", "Частота тона (Гц)", "Громкость тона %","Длительность тона (с.)"),
    ("Множ. сумм радиусов (пикс.)","Зона ожидания (пикс.)", "Частота записи (с.)"),
    ("Чувствительность мыши (пикс.)","Время ожидания (c.)","Время ответа (c.)")]

for i in range(len(lbl[2])):
  lbl[0].append(LabelFrame(root, text=lbl[2][i]))
  lbl[0][i].grid(column=i%2, row=i//2, sticky="NEWS", padx=5, pady=5)

for i in range(len(lbl[0])):
  for j in range(len(lbl[3+i])):
    Label(lbl[0][i],text=lbl[3+i][j]).grid(column=0, row=j, sticky="NEWS")
#------------------------------------------------------------------------------------------------

def select_file():
    global file
    filetypes = (('.txt файлы', '*.txt'), ('Все файлы', '*.*'))
    file = filedialog.askopenfilename(title='Выберите файл', initialdir='/', filetypes=filetypes)
    show_file["text"]=file

def ableTone():
  global enable, wids
  for i in wids[1][1:]:
    if enable.get()==0:
      i["state"]="disable"
    else:
      i["state"]="normal"

file="None"

mode = StringVar()
ctrl = StringVar()
prog = StringVar()
enable = IntVar()

lst = [["Оконный", "Экранный"], ["Задачки", "Мыши"], ["Обычное", "Инверсия"]]

wids=[[OptionMenu(lbl[0][0], mode, *lst[0]),
       Spinbox(lbl[0][0], from_= 0, to = 2560),
       Spinbox(lbl[0][0], from_= 0, to = 1440),
       OptionMenu(lbl[0][0], ctrl, *lst[2]),
       OptionMenu(lbl[0][0], prog, *lst[1]),
       Spinbox(lbl[0][0], from_= 0, to = 1440)],

      [Checkbutton(lbl[0][1],variable = enable, onvalue = 1, offvalue = 0, command=ableTone),
       Spinbox(lbl[0][1], from_= 0, to = 20000),
       Spinbox(lbl[0][1], from_= 0, to = 50000),
       Spinbox(lbl[0][1], from_= 0, to = 1000)],
      [Spinbox(lbl[0][2], from_= 0, to = 2560),
       Spinbox(lbl[0][2], from_= 0, to = 5000),
       Spinbox(lbl[0][2], from_= 0, to = 5000)],
      [Spinbox(lbl[0][3], from_= 0, to = 2560),
       Spinbox(lbl[0][3], from_= 0, to = 1440),
       Spinbox(lbl[0][3], from_= 0, to = 2560),
       Button(lbl[0][3], text="Выбор файла",relief="raised", command=select_file)]]

s=list(config.keys())
n=5
for i in wids:
    for j in i:
        if type(j) is Spinbox:
          j.delete(0,"end")
          j.insert(1,config[s[n]])
#          print(s[n])
          n+=1

mode.set(config["screen"])
ctrl.set(config["control"])
prog.set(config["program"])
enable.set(config["tone_play"])

ableTone()

for i in wids:
  for j in range(len(i)):
    if type(i[j]) is Button:
      i[j].grid(column=0, columnspan=2,row=j, sticky="NEWS")
    else:
      i[j].grid(column=1,row=j, sticky="news")

    i[j].config(width=10, relief="groove")
show_file=Label(lbl[0][3], wraplength=340, text=config["file"])
show_file.grid(column=0,columnspan=2,rowspan=2,row=4, sticky="NEWS")
#---------------------------------------------------------------------------------------
def start():
  global start_prog
  s=list(config.keys())
  n=5
  print("-----------------")
  for i in wids:
    for j in range(len(i)):
      if type(i[j]) is Spinbox:
        config[s[n]]=i[j].get()

        n+=1
  config["control"]=ctrl.get()
  config["screen"]=mode.get()
  config["program"]=prog.get()
  config["tone_play"]=enable.get()
  config["file"]=file    
#-----------------------------------
  f=open("config.txt", "w")
  for i in config:
      f.write(str(i)+" "+str(config[i])+"\n")
  f.close()
#-----------------------------------
  start_prog=True
  root.destroy()

done=Button(root, text="Начать Эксперимент", relief="groove", command=start)
done.grid(column=0, row=2, columnspan=2, sticky="NEWS")
root.mainloop()
#==============================================================================================
print(config)
import pygame as pg
import numpy
import serial
import serial.tools.list_ports
import time
from random import uniform

pg.mixer.init(44100,-16,2,512)
pg.init()

if not(os.path.exists("res")):
  os.mkdir("res")

# initialize window
width,height=int(config["width"]), int(config["height"])
if int(config["screen"]=="Экранный"): root=pg.display.set_mode((width,height), pg.FULLSCREEN)
elif int(config["screen"]=="Оконный"): root=pg.display.set_mode((width,height))
clock=pg.time.Clock()

#initialize COM-Port 
port_work=True
portname=""
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
    if "USB-SERIAL CH340" in desc:
        portname=port
if portname=="":  port_work=False

try:
    time_code=serial.Serial(port=portname, baudrate=9600, timeout=.1)
    time.sleep(2)
except Exception as e:
    port_work=False
#    print(e)

# create the siren's sample
arr = numpy.array([int(config["tone_volume"]) * numpy.sin(2.0 * numpy.pi * int(config["tone_rate"]) * x /44100) for x in range(0, 44100)]).astype(numpy.int16)
arr2 = numpy.c_[arr,arr]
sound = pg.sndarray.make_sound(arr2)

#play tone
if int(config["tone_play"])==1 and start_prog==True:# and port_work==True:
    print("play")
    if port_work: time_code.write(bytearray([1]))      
    sound.play(-1)
    pg.time.wait(int(float(config["tone_delay"])*1000))
    sound.stop()

# set to start program
main=True
#-----------------------------------------------------------------
#-----------------------------------------------------------------
if start_prog==True:
  if config["program"]=="Задачки":
    file_name="Tasks "+time.strftime("%d.%m.%y %H.%M.%S")
    from textGen import Gen
    roundi=0

    pg.font.init()
    myfont = pg.font.SysFont('Comic Sans MS', 150)

    r=w=TT=FF=TF=FT=missed=0
    sqr=200
    red=0
    green=0

    log=[]
    answer=True

    fill=0
    fillstep=1
    new=True
    file_not=False
    dot_flag=True

    class sqr():
        intances=[]
        def __init__(self, x, y, size, color, fill=0):
            self.x=x
            self.y=y
            self.size=size
            self.color=color
            self.fill=fill
            sqr.intances.append(self)
        def draw(self, root):
            pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.size), width=2)
            if self.fill<0:
            #    print(self.x, self.size-self.fill, self.size, self.fill)
                pg.draw.rect(root, self.color, (self.x, self.y+self.size+self.fill, self.size, abs(self.fill)))
            elif self.fill>0:
                pg.draw.rect(root, self.color, (self.x, self.y, self.size, self.fill))

    if config["file"]!="None":
        try:
            fin=open(config["file"], "r")
            #print(fin)
        except Exception as e:
            print(e)
            file_not=True




    size=100
    good=sqr((width-size)/2, height/4-size/2, size, (0,255,0))
    bad=sqr((width-size)/2, height*(3/4)-size/2, size, (255,0,0))
    
    while main:

        if new==True:
            root.fill((128,128,128))
            pg.draw.circle(root, (255,255,255), (width//2, height//2), (10))
            pg.display.update()
            pg.time.wait(int(float(config["dot_time"])*1000))
            roundi+=1
            if roundi>int(config["round"]): break
            rtime=0
            new=False
            pg.event.clear()
            if port_work: time_code.write(bytearray([3]))            
            if (config["file"]!="None" or config["file"]!="None") and file_not==False:
                d=fin.readline()
                #print(d)
                if d=="": break
                d=d.split()
                text = d[0] 
                res = bool(int(d[1]))
            else:
                #print("Gen")
                d=Gen()
                text = d[2] 
                res = bool(int(d[1]))
            if res==True: r+=1
            else: w+=1
            a=time.time()

        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE): 
                #if port: time_code.write(bytearray([0]))
                main=False

            if event.type==pg.MOUSEWHEEL:
              if rtime==0: 
                  rtime=time.time()-a; 
                  print(rtime)
                  if port_work: time_code.write(bytearray([4]))
              if int(config["control"]=="Обычное"):
                if event.y>0:
                    good.fill-=event.y*int(config["sensivity"])
                    bad.fill=0
                else:
                    bad.fill-=event.y*int(config["sensivity"])
                    good.fill=0
              elif int(config["control"]=="Инверсия"):
                if event.y<0:
                    good.fill-=event.y*int(config["sensivity"])
                    bad.fill=0
                else:
                    bad.fill-=event.y*int(config["sensivity"])
                    good.fill=0



        if abs(good.fill)>size or abs(bad.fill)>size:
            if abs(good.fill)>size:
                log.append([str(roundi),text,str(res),"True", str(res==True),str(round(rtime,4))])
                answer=True
            if abs(bad.fill)>size:
                log.append([str(roundi),text,str(res),"False", str(res==False),str(round(rtime,4))])
                answer=False


            if res == True and answer == True:
                TT+=1
            if res == False and answer == False:
                FF+=1
            if res == True and answer == False:
                TF+=1
            if res == False and answer == True:
                FT+=1
            
            good.fill=0
            bad.fill=0
            new=True


        if time.time()-a>float(config["time"]):
    #        time_code.write(bytearray([3,0]))
            rtime=time.time()-a
            log.append([str(roundi),text,str(res),"Missed","Missed", str(round(rtime,4))])
            bad.fill=good.fill=0
            missed+=1
            new=True

    #-----------------------------v
        textSur = myfont.render(text, True, (255, 255, 255))
        root.fill((128,128,128))
        root.blit(textSur,((width-textSur.get_width())/2,(height-textSur.get_height())/2))
        good.draw(root)
        bad.draw(root)
        pg.display.update()
        clock.tick(60)
    #    ---------------------------
    #    pg.image.save(root, "vid/"+str(vid)+".png")
    #    images.append(imageio.imread("vid/"+str(vid)+".png"))
    #    vid+=1
    #    ----------------------
    #-----------------------------^
    #imageio.mimsave('vid/movie.gif', images)
    fout=open("res/"+file_name+".txt", "w")
    fout.write("Раунд\tПример\tОценка_примера\tОтветил\tВывод\tВремя реакции\n")
    for i in log:
        fout.write(i[0]+"\t"+i[1]+"\t"+i[2]+"\t\t"+i[3]+"\t"+i[4]+"\t"+i[5]+"\n")
    fout.write("Задачи\t\t\tОтветил\nTrue\tFalse\t\tT->T\tF->F\tT->F\tF->T\tMissed\n")
    fout.write(str(r)+"\t"+str(w)+"\t\t"+str(TT)+"\t"+str(FF)+"\t"+str(TF)+"\t"+str(FT)+"\t"+str(missed)+"\n")
    fout.close()
  elif config["program"]=="Мыши":
    #-----------------------------------------------
    from random import randint, choice
    
    dir_name="Mouse "+time.strftime("%d.%m.%y %H.%M.%S")
    posible=int(config["possible"])
    coef=float(config["radius_multiplier"])

    photo=pg.Surface((width, height))
    if not(os.path.exists("res")):
        os.mkdir("res")
    if not(os.path.exists("res/"+dir_name)):
        os.mkdir("res/"+dir_name)
    if not(os.path.exists("res/"+dir_name+"/log_img")):
        os.mkdir("res/"+dir_name+"/log_img")
    if not(os.path.exists("res/"+dir_name+"/log_txt")):
        os.mkdir("res/"+dir_name+"/log_txt")

    class ball():
        x=0
        r=40
        y=height-r*2

    class hole():
        r=40
        x=width-r
        y=r

    class path():
        x=0
        y=0

    new=True
    a=[]
    g=0
    not_g=0
    a_g=0
    s=0
    s2=0
    ri=0
    tim=0
    
    #---------------------------------------------

    while main:
        if new==True:
            ri+=1
            if ri>int(config["round"]): break
            f=open("res/"+dir_name+"/log_txt/"+str(ri)+".txt", "w")
            f.write("Траектории | Разрешение: "+str(width)+"x"+str(height)+" | Частота в секундах: "+str(config["freq"])+"\n")
            f.write("Зеленая\t\tСиняя\n")
            f.write("x\ty\tx\ty\n")
            rtime=0
            new=False
            movement=False
            if port_work: time_code.write(bytearray([2])) 
            photo.fill((128,128,128))
            pg.draw.circle(photo, (0,0,0), (hole.x, hole.y), hole.r)
            pg.draw.rect(photo, (255,0,0), (0,height-posible,posible, posible), width=2)
            s=0
            s2=0
            
    #-norm------------------------------------------------v
            ball.x, ball.y=ball.r, height-ball.r
            path.x, path.y=ball.x+ball.r/2, ball.y-ball.r/2
    #-------------------------------------------------^

            m=randint(1,4)
            x1,y1 = width-(2*hole.r+ball.r), ball.r
            x2,y2 = width-ball.r, ball.r+2*hole.r
#-----------------------------------------------
            if m==1:
                c=(y1-ball.y)/((x1-ball.x)**2)
                c=uniform(c,c+c/2)
                delta_y=lambda: 2*c*(ball.x-ball.r)
            if m==2:
                c=(y2-ball.y)/((x2-ball.x)**2)
                c=uniform(c,c-c/2)
                delta_y=lambda: 2*c*(ball.x-ball.r)
            if m==3:
                c=(ball.y-y1)/((x1-ball.x)**2)
                c=uniform(c,c+c/2)
                delta_y=lambda: 2*c*(ball.x-x1)
            if m==4:
                c=(ball.y-y2)/((x2-ball.x)**2)
                c=uniform(c-c/2,c)
                delta_y=lambda: 2*c*(ball.x-x2)
            atime=tim=time.time()
    #-----------------------------------------------------v
        det_x, det_y= ball.x+ball.r/2, ball.y-ball.r/2
        det2_x, det2_y = path.x, path.y
    #-----------------------------------------------------^

        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE): 
    #            if port_work: time_code.write(bytearray([0])) 
                main=False
            if event.type==pg.MOUSEWHEEL and (ball.x>posible or ball.y<height-posible):
                if rtime==0: 
                  rtime=time.time()-atime; 
                  print(rtime)
                  if port_work: time_code.write(bytearray([4]))
                movement=True
                if int(config["control"]=="Обычное"): ball.y-=event.y*20
                elif int(config["control"]=="Инверсия"): ball.y+=event.y*20
    #-----------------------------------------------------------------------------------------------------------------v
    #    print((time()-tim))
        
        if (time.time()-tim)>float(config["freq"]):
            tim=time.time()
    #        print("check")
            f.write(str(int(ball.x+ball.r/2))+"\t"+str(int(ball.y-ball.r/2))+"\t"+str(int(path.x))+"\t"+str(int(path.y))+"\n")

        ball.y+=delta_y()*5
        ball.x+=5
        path.y+=delta_y()*5
        path.x+=5
        

        root.fill((128,128,128))
        pg.draw.circle(root, (0,0,0), (hole.x, hole.y), hole.r)
        pg.draw.circle(root, (128,0,0), (ball.x, ball.y), ball.r)
    #------------------------------------------------------------------------------------------------------------------v
        pg.draw.line(photo, (0,255,0), (det_x, det_y), (ball.x+ball.r/2, ball.y-ball.r/2), 2)
        pg.draw.rect(photo, (0,0,255), (path.x, path.y, 3,3))
    #-------------------------------------------------------------------------------------------------------------------^

        pg.display.update()
    #    ---------------------------
    #    pg.image.save(root, "vid/"+str(vid)+".png")
    #    images.append(imageio.imread("vid/"+str(vid)+".png"))
    #    vid+=1
    #    ----------------------
        clock.tick(60)


        s+=(((ball.x+ball.r/2)-det_x)**2 + ((ball.y-ball.r/2)-det_y)**2)**(1/2)
        s2+=((path.x-det2_x)**2 + (path.y-det2_y)**2)**(1/2)


        l=((ball.x-hole.x)**2+(ball.y-hole.y)**2)**(1/2)
        flag=(l<=coef*ball.r)
        if (ball.x+ball.r>width or ball.y+ball.r>height or ball.y-ball.r<0) or flag : 
            if movement==False: rtime=time.time()-atime
            #pg.draw.circle(photo, (255,0,0), (ball.x, ball.y), ball.r)
            f.write(str(int(ball.x))+"\t"+str(int(ball.y))+"\t"+str(int(path.x))+"\t"+str(int(path.y))+"\n")
            f.close()
            pg.image.save(photo, "res/"+dir_name+"/log_img/"+str(ri)+".png")
            if movement==False: a_g+=1; flag="Missed"
            else:
               if flag: g+=1
               else: not_g+=1

            a.append([flag, round(s), round(s2), int(ball.x), int(ball.y), round(rtime,4)])
            new=True

    #imageio.mimsave('vid/movie.gif', images)
    f=open("res/"+dir_name+"/main_log.txt", "w")
    f.write("Мыши:\tДобравшиеся\tПропавшие\tДобравшиеся сами\tРазрешение окна: "+str(width)+"x"+str(height)+"\n")
    f.write("\t"+str(g)+"\t\t"+str(not_g)+"\t\t"+str(a_g)+"\n")
    f.write("\t\tДлины:\t\t\t\t\tФин. координаты:\n")
    f.write("Раунд\tПопал\tСиний\tЗеленый\tРазница\tВремя реакции\tx\ty\n")
    #print(a)
    for i in range(len(a)):
        f.write(str(i+1)+"\t"+str(a[i][0])+"\t"+str(a[i][1])+"\t"+str(a[i][2])+"\t"+str(a[i][1]-a[i][2])+"\t"+str(a[i][5])+"\t\t"+str(a[i][3])+"\t"+str(a[i][4])+"\n")
    f.close()

if port_work: time_code.write(bytearray([5])) 
pg.quit()
