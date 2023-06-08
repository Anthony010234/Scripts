import tkinter as tk
import csv, os, sys, datetime, keyboard
import matplotlib.pyplot as plt
import time as time1
import datetime as date1
from datetime import *
from tkinter import *
from tkinter import messagebox
from pandastable import Table

#Set working directory to be script location
os.chdir(os.path.dirname(sys.argv[0]))

global filepath
global KeepAwakeSeconds
global RefreshKA
global ResetCount
global Count

KeepAwakeSeconds = 0
RefreshKA = 0
Count = 0

counter = 66600
running = False
tt2=datetime.fromtimestamp(counter)

filepath = "recordedtime.txt"

HEIGHT = 300
WIDTH = 500

def counter_label(label): 
    def count(): 
        if running: 
            global counter
            global KeepAwakeSeconds
            global RefreshKA
            global ResetCount
            global Count

            ResetCount = (KeepAwakeSeconds * 10) - 1
    
            # To manage the initial delay. 
            if counter==66600:             
                display="00:00:00"
            else:
                tt = datetime.fromtimestamp(counter) - tt2
                string = tt
                display=string
                #print(Count)
                Count += 1
                #time1.sleep(1)
                print(Count)
                print(KeepAwakeSeconds)
                #$print(ResetCount)
                if Count > 0 and KeepAwakeSeconds > 0:
                    a =  Count % KeepAwakeSeconds
                    
                    if a==0:
                        print('0000000000')
                        keyboard.press_and_release('caps lock')
                        time1.sleep(.01)
                        keyboard.press_and_release('caps lock')

                if Count == ResetCount:
                    Count=0
                
            label['text']=display   # Or label.config(text=display) 
    
            # label.after(arg1, arg2) delays by  
            # first argument given in milliseconds 
            # and then calls the function given as second argument. 
            # Generally like here we need to call the  
            # function in which it is present repeatedly. 
            # Delays by 1000ms=1 seconds and call count again. 
            label.after(1000, count)  
            counter += 1
    
    # Triggering the start of the counter. 
    count()      
    
# start function of the stopwatch 
def Start(label): 
    global running 
    global RefreshKA
    global ResetCount
    global KeepAwakeSeconds

    running=True
    counter_label(label) 
    start['state']='disabled'
    stop['state']='normal'
    reset['state']='disabled'
    Record['state']='disabled'
    label.config(bg='Green')


    if RefreshKA == 0:
        KeepAwake_time = open("Settings.config", "r")
        for x in KeepAwake_time:
            if 'KeepAwake' in x:
                DefaultKeepAwake2 = x.replace('\n','').replace('KeepAwake=','')
                DefaultKeepAwake2 = int(DefaultKeepAwake2)
                if DefaultKeepAwake2>0:
                    KeepAwakeSeconds = DefaultKeepAwake2
                    RefreshKA = 1
                    ResetCount = (KeepAwakeSeconds * 10) - 1
                    

    
# Stop function of the stopwatch 
def Stop(): 
    global running 
    running = False
    label.config(bg='RED')
    time1.sleep(1)
    start['state']='normal'
    stop['state']='disabled'
    reset['state']='normal'
    Record['state']='normal'

def Record():

    response=messagebox.askyesno('Reset?','Confirm: Record & Reset Time?')
    if response:
    
        DateTimeValue = date1.datetime.now()
        DateToday = DateTimeValue.strftime("%d_%m_%Y")

        try:
            file = open("recordedtime.txt", 'r')
            file.close()
        except IOError:
            with open("recordedtime.txt", 'a') as file_object:
                file_object.write("Date (dd_mm_yy),TotalTime(hr:min)"+'\n')
                file_object.close()

        with open("recordedtime.txt", 'a') as file_object:
            file_object.write(DateToday+","+label.cget("text")+'\n')
            file_object.close()

        if running==False:       
            reset['state']='disabled'
            Record['state']='disabled'
            label['text']='00:00:00'
            label.config(bg='white')

        global counter 
        counter=66600

# Reset function of the stopwatch 
def Reset(label):
    
    response=messagebox.askyesno('Reset?','Confirm: Reset Timer?')
    if response:
        global counter 
        counter=66600
        
        # If reset is pressed after pressing stop. 
        if running==False:       
            reset['state']='disabled'
            Record['state']='disabled'
            label['text']='00:00:00'
            label.config(bg='white')
        
        # If reset is pressed while the stopwatch is running. 
        else:                
            label['text']='00:00:00'
            label.config(bg='Green')


def TableView():
    Window = tk.Toplevel()
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)

    class TestApp(tk.Frame):
        def __init__(self, parent, filepath):
            super().__init__(parent)
            self.table = Table(self, showtoolbar=False, showstatusbar=False)
            self.table.importCSV(filepath)
            self.table.show()


    app = TestApp(canvas, filepath)
    app.pack(fill=tk.BOTH)

    chartbutton = tk.Button(canvas, text="Chart View", bg='White', fg='Black',command=lambda: ChartView())
    chartbutton.pack()

    
    def on_close():
        MainForm.deiconify()
        Window.destroy()

    MainForm.withdraw()
    Window.protocol("WM_DELETE_WINDOW", on_close)
    canvas.pack()

def ChartView():

    xaxis = []
    yaxis = []


    with open(filepath,'r') as inf:
        content = csv.reader(inf, delimiter=",")
        next(content)
        for row in content:
            Date = row[0]
            TotalTime = row[1]

            #if TotalTime == "0:0":
                #continue


            xaxis.append(Date)
            yaxis.append(TotalTime)

            print(Date+"----"+TotalTime)
    

    plt.subplots(num="Recorded Times Graph")
    plt.title("Recorded Times")
    plt.barh(xaxis, yaxis)
    plt.xlabel("Time (Hours:Minutes)")
    plt.ylabel("Date")
    plt.tight_layout(pad=4)
    plt.xticks(rotation=45)
    plt.show()


def Settings():

    Window = tk.Toplevel()
    Window.geometry('500x300')
    #canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)

    global RefreshKA

    Default_time = open("Settings.config", "r")
    for x in Default_time:
        if 'Hours' in x:
            DefaultHours = x.replace('\n','').replace('Hours=','')
        if 'KeepAwake' in x:
            DefaultKeepAwake = x.replace('\n','').replace('KeepAwake=','')


    Label(Window, text='Work Hours. example: 7h 30m is 7.5 \nCurrently: '+DefaultHours+' Hours').grid(row=0)
    e1 = Entry(Window,width=7)
    e1.grid(row=0, column=1,sticky=W)
    

    Label(Window, text='KeepAwake? (in Seconds) 0=disabled \nCurrently: '+DefaultKeepAwake+' Seconds').grid(row=1)
    e2 = Entry(Window,width=7)
    e2.grid(row=1, column=1,sticky=W)

    

    def On_Save():
        #Updating HOURS
        Hours = e1.get()
        KeepAwakeValue = e2.get()
        print(Hours)
        print(KeepAwakeValue)

        if Hours != "" : 
            NewHours = 'Hours='+Hours
            print("NewHours "+Hours)
        else:
            NewHours = 'Hours='+DefaultHours
            print("old hours "+Hours)

        if KeepAwakeValue != "":
            NewKeepAwake = 'KeepAwake='+KeepAwakeValue
            print("newKeepAwake "+NewKeepAwake)
        else:
            NewKeepAwake = 'KeepAwake='+DefaultKeepAwake
            print("KeeoldpAwake "+NewKeepAwake)

        with open('Settings.config', 'w') as file_object:
            file_object.write(NewHours+'\n'+NewKeepAwake)
            file_object.close()
        RefreshKA = 0
        on_close()
        


    Save_button = Button(Window, text='Save', width=10,command=On_Save)
    Save_button.place(x=10, y=250)
    
    def on_close():
        MainForm.deiconify()
        Window.destroy()

    MainForm.withdraw()

    Window.protocol("WM_DELETE_WINDOW", on_close)
    canvas.pack()







############### MAIN FORM FOR TIME TRACKER ###############

MainForm = tk.Tk()
MainForm.title("Python Guides")





############### MAIN FORM CANVAS!! ###############

canvas = tk.Canvas(MainForm, height=170, width=300)

label = Label(canvas, text="00:00:00", fg="black", font="Verdana 30 bold", relief='sunken', bg='white', width= 8)
label.place(relx=0.12, rely=0.05)

start = Button(canvas, text='Start', width=8, command=lambda: Start(label))
stop = Button(canvas, text='Pause',width=8,state='disabled', command=lambda: Stop()) 
reset = Button(canvas, text='Reset',width=8, state='disabled', command=lambda: Reset(label))
Record = Button(canvas, text="Record &\nReset",width=8, state='disabled', command=lambda: Record())

start.place(x='40',y='70')
reset.place(x='168',y='70')
stop.place(x='40',y='100')
Record.place(x='168',y='110')



canvas.pack()



#Menubar Configuration
menubar = Menu(MainForm)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Settings", command=lambda: Settings())
filemenu.add_command(label="Exit", command=canvas.quit)
menubar.add_cascade(label="File", menu=filemenu)

viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_command(label="Recorded History", command=lambda: TableView())
menubar.add_cascade(label="View", menu=viewmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command='')
menubar.add_cascade(label="Help", menu=helpmenu)

MainForm.config(menu=menubar)

def on_close():
    response=messagebox.askyesno('Exit','Exit?\n\n(Un-Recorded times will be lost!!)')
    if response:
        MainForm.destroy()

MainForm.protocol('WM_DELETE_WINDOW',on_close)
MainForm.mainloop()