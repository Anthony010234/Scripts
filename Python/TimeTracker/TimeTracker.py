#Import required modules
import tkinter,os,sys,datetime,keyboard
import time as time1
from time import *
from datetime import *
from os import system
from tkinter import messagebox
from tkinter import *
from tkinter.font import BOLD

#Set working directory to be script location
os.chdir(os.path.dirname(sys.argv[0]))

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
    reset['state']='normal'
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

# Reset function of the stopwatch 
def Reset(label):
    
    response=messagebox.askyesno('Reset?','Are you sure you want to Reset?')
    if response:
        global counter 
        counter=66600
        
        # If rest is pressed after pressing stop. 
        if running==False:       
            reset['state']='disabled'
            label['text']='00:00:00'
            label.config(bg='white')
        
        # If reset is pressed while the stopwatch is running. 
        else:                
            label['text']='00:00:00'
            label.config(bg='Green')

#Settings Screen
def Settings():

    global RefreshKA

    Settings_timetracker = tkinter.Tk()
    Settings_timetracker.title('Settings')
    Settings_timetracker.resizable(0,0)
    Settings_timetracker.geometry('375x300')
    #Settings_timetracker.iconbitmap('stopwatch_icon-icons.com_64805.ico')
    Settings_timetracker.lift()
    Settings_timetracker.attributes("-topmost", True)

    Main_timetracker.attributes('-type', 1)
    
    Default_time = open("Settings.config", "r")
    for x in Default_time:
        if 'Hours' in x:
            DefaultHours = x.replace('\n','').replace('Hours=','')
        if 'KeepAwake' in x:
            DefaultKeepAwake = x.replace('\n','').replace('KeepAwake=','')


    Label(Settings_timetracker, text='Work Hours. example: 7h 30m is 7.5 \nCurrently: '+DefaultHours+' Hours').grid(row=0)
    e1 = Entry(Settings_timetracker,width=7)
    e1.grid(row=0, column=1,sticky=W)
    

    Label(Settings_timetracker, text='KeepAwake? (in Seconds) 0=disabled \nCurrently: '+DefaultKeepAwake+' Seconds').grid(row=1)
    e2 = Entry(Settings_timetracker,width=7)
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

            #newfile = open("Settings.config", "w")
        with open('Settings.config', 'w') as file_object:
            file_object.write(NewHours+'\n'+NewKeepAwake)
            file_object.close()
        RefreshKA = 0
        on_closing()
        
        
    
    def on_closing():
        Main_timetracker.lift()
        Main_timetracker.attributes('-topmost', 0)
        Settings_timetracker.destroy()

    
    Save_button = Button(Settings_timetracker, text='Save', width=10,command=On_Save)
    Save_button.place(x=10, y=250)

    
    Settings_timetracker.protocol("WM_DELETE_WINDOW", on_closing)
    Settings_timetracker.mainloop()


#About Screen
def About():
    #Splash screen Configuration
    Splash_timetracker = tkinter.Tk()
    Splash_timetracker.title('About')
    Splash_timetracker.resizable(0,0)
    #Splash_timetracker.iconbitmap('stopwatch_icon-icons.com_64805.ico')
    Splash_timetracker.lift()
    Splash_timetracker.attributes("-topmost", True)
    
    About_Label = Message(Splash_timetracker, text="Work Time Tracker", width=400,font=('Arial', 24, BOLD))
    About_Label3 = Message(Splash_timetracker, text="This app was designed to help with time management while working from home.\n", width=300,font=('Arial', 10))
    About_Label2 = Message(Splash_timetracker, text="App Created By: Anthony\nIcon made by EpicCoders from https://icon-icons.com/\n\nCode References:\nhttps://www.geeksforgeeks.org/create-stopwatch-using-python/", width=400,font=('Arial', 10))
    
    About_Label.pack()
    About_Label3.pack()
    About_Label2.pack()

    def on_closing():
        Main_timetracker.lift()
        Main_timetracker.attributes('-type', 0)
        Splash_timetracker.destroy()
        
    Main_timetracker.attributes('-type', 1)
    Splash_timetracker.protocol("WM_DELETE_WINDOW", on_closing)
    Splash_timetracker.mainloop()


    

#Main Window Configuration
Main_timetracker = tkinter.Tk()
Main_timetracker.title('Work Time Tracker')
Main_timetracker.resizable(0,0)
Main_timetracker.geometry("300x170")
#Main_timetracker.iconbitmap('stopwatch_icon-icons.com_64805.ico')
Main_timetracker.lift()

def on_close():
    response=messagebox.askyesno('Exit','Are you sure you want to exit?')
    if response:
        Main_timetracker.destroy()

#Menubar Configuration
menubar = Menu(Main_timetracker)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Settings", command=Settings)
filemenu.add_command(label="Exit", command=Main_timetracker.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=About)
menubar.add_cascade(label="Help", menu=helpmenu)

Main_timetracker.config(menu=menubar)

try:
  open('Settings.config')
except FileNotFoundError:
  #open('Settings.config',"a")
  with open('Settings.config', 'w') as file_object:
                file_object.write('Hours=7.6'+'\n'+'KeepAwake=0')
                file_object.close()

label = Label(Main_timetracker, text="00:00:00", fg="black", font="Verdana 30 bold", relief='sunken', bg='white', width= 8)
label.place(relx=0.12, rely=0.05)

start = Button(Main_timetracker, text='Start', width=8, command=lambda:Start(label))
stop = Button(Main_timetracker, text='Pause',width=8,state='disabled', command=Stop) 
reset = Button(Main_timetracker, text='Reset',width=8, state='disabled', command=lambda:Reset(label))

start.place(x='40',y='70')
reset.place(x='168',y='70')
stop.place(x='40',y='100')


#Luanch Main Window
Main_timetracker.protocol('WM_DELETE_WINDOW',on_close)
Main_timetracker.mainloop()
