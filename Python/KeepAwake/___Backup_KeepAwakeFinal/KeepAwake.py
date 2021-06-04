import keyboard,time,datetime,os,sys
from datetime import datetime

#+++++++++++++++++++++++++++++++++++++++++++++++++++
#VARIABLES BELOW
#+++++++++++++++++++++++++++++++++++++++++++++++++++
CreatedDate = "06/05/2021"
INTRO = '\x1b[6;30;42m' + f'KeepAwake - Helping you keep track of working time\nCreated by: Anthony Hanna\nCreated on: {CreatedDate}\n' + '\x1b[0m'
#+++++++++++++++++++++++++++++++++++++++++++++++++++


def clear(): #Function to clear screen
    os.system( 'cls' )

def KeepAwake(value = 0): #MAIN FUNCTION
    count = 0

    if value > 0:
        print(f'You entered {value} Seconds')
        time.sleep(5)
    else:
        value = inputNumber("Please enter how many seconds between keypress:\n")
        print(f'You entered {value} Seconds')
        time.sleep(3)

    startTime = datetime.now()
    while (True):
        
        keyboard.press_and_release('caps lock')
        time.sleep(.01)
        keyboard.press_and_release('caps lock')
        
        count = count + 1

        timeElapsed=datetime.now()-startTime

        clear()
        print(INTRO)
        print ('Refreshing every:',value, 'Seconds')
        print('Time elpased (hh:mm:ss.ms) {}'.format(timeElapsed))
        time.sleep(value)

def inputNumber(message): #Function to ensure integer is selected
  while True:
    try:
        userInput = int(input(message))       
    except ValueError:
        clear()
        print("Not Valid! Try again.")
        continue
    else:
        return userInput 
        break

####################
#SCRIPT STARTS HERE
####################

clear()
print(INTRO)

try:
    arg1 = sys.argv[1]
    KeepAwake(int(arg1))

except KeyboardInterrupt:
    print('Bye!')

except:
    try:
        KeepAwake()
    except KeyboardInterrupt:
        print('Bye!')


