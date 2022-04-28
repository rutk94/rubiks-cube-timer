from ast import Num
import secrets
from tkinter import *
import time

# ROOTS
root = Tk()
root.title('Rubik\'s cube timer')

timerFrame = LabelFrame(root, bd=0)
timerFrame.grid(row=3, column=0)

optionsFrame = LabelFrame(root, text='options')
optionsFrame.grid(rowspan=9, column=1)

global font_timer
font_timer = ('Helvetica', 32)
global font_button
font_button = ('Helvetiva', 20)

times = []

# FUNCTIONS
def countdown(cdVar=3):
    label_countdown['text'] = '{}'.format(cdVar)

    if cdVar <=5 and cdVar > 0:
        root.after(1000, countdown, cdVar-1)
    else:
        label_countdown['text'] = ''
        stopButton.config(state=NORMAL)
        timer()

def timer(min=0, sec=0, msec=0):
    startButton.config(state=DISABLED)

    if min in range(0,10):
        label_min['text'] = '0{}'.format(min)
    else:
        label_min['text'] = '{}'.format(min)

    if sec in range(0,10):
        label_sec['text'] = ':0{}'.format(sec)
    else:
        label_sec['text'] = ':{}'.format(sec)

    if msec in range(0,10):
        label_msec['text'] = ':00{}'.format(msec)
    elif msec in range(10,100):
        label_msec['text'] = ':0{}'.format(msec)
    elif msec in range(100,1000):
        label_msec['text'] = ':{}'.format(msec)

    if not stopButton['state'] == DISABLED:
        if msec >= 0 and msec < 1000:
            root.after(1, timer, min, sec, msec+1)
            if msec == 999:
                if sec < 59:
                    root.after(10, timer, min, sec+1, 0)
                elif sec == 59:
                    root.after(1, timer, min+1, 0, 0)
    else:
        startButton.config(state=NORMAL)
        times.append((min, sec, msec))

def start_on_event(e):
    root.unbind('<space>')
    root.bind('<space>', stop_on_event)
    start()

def start():
    root.unbind('<space>')
    root.bind('<space>', stop_on_event)
    
    restartButton.config(state=DISABLED)
    if label_msec['text'] == ':000':
        countdown()
    else:
        stopButton.config(state=NORMAL)
        timer(times[-1][0], times[-1][1], times[-1][2])

def stop_on_event(e):
    root.unbind('<space>')
    root.bind('<space>', start_on_event)
    stop()

def stop():
    root.unbind('<space>')
    root.bind('<space>', start_on_event)
    startButton.config(state=NORMAL)
    stopButton.config(state=DISABLED)
    restartButton.config(state=NORMAL)

def restart():
    label_min['text'] = '00'
    label_sec['text'] = ':00'
    label_msec['text'] = ':000'
    restartButton.config(state=DISABLED)


def on_enter(e):
    e.widget['foreground'] = 'orange'

def on_leave(e):
    e.widget['foreground'] = 'black'

# IMAGES
rubiksCubeImg = PhotoImage(file=r'D:\Dokumenty\KURSY\PYTHON\projekty\rubiks-cube-timer\img\rubiks_cube.png')
rubiksCubeImg = rubiksCubeImg.subsample(2,2)
rubiksCubeImgLabel = Label(root,
                            image=rubiksCubeImg)
rubiksCubeImgLabel.grid(row=0, column=0)

# LABELS
# label = Label(root, width=10)
# label.pack()

label_min = Label(timerFrame, 
                    text='00',
                    font=font_timer)
label_min.grid(row=0, column=0)

label_sec = Label(timerFrame,
                    text=':00',
                    font=font_timer)
label_sec.grid(row=0, column=1)

label_msec = Label(timerFrame,
                    text=':000',
                    font=font_timer)
label_msec.grid(row=0, column=2)

label_countdown = Label(root,
                        text='',
                        font=font_button)
label_countdown.grid(row=4, column=0)

label_text = Label(root,
                    text='Press START to activate the TIMER')
label_text.grid(row=5, column=0, sticky=W+E)

# BUTTONS
startButton = Button(root, 
                    text='START',
                    font=font_button,
                    command=start,
                    bd=0,
                    activeforeground='orange')
startButton.grid(row=6, column=0, sticky=W+E)
startButton.bind('<Enter>', on_enter)
startButton.bind('<Leave>', on_leave)

stopButton = Button(root, 
                    text='STOP',
                    font=font_button,
                    command=stop,
                    bd=0,
                    activeforeground='orange',
                    state=DISABLED)
stopButton.grid(row=7, column=0)
stopButton.bind('<Enter>', on_enter)
stopButton.bind('<Leave>', on_leave)

restartButton = Button(root,
                        text='RESTART',
                        font=font_button,
                        command=restart,
                        bd=0,
                        activeforeground='orange',
                        state=DISABLED)
restartButton.grid(row=8, column=0)
restartButton.bind('<Enter>', on_enter)
restartButton.bind('<Leave>', on_leave)

exitButton = Button(root,
                    text='EXIT',
                    font=font_button,
                    command=exit,
                    bd=0,
                    activeforeground='orange')
exitButton.grid(row=9, column=0)
exitButton.bind('<Enter>', on_enter)
exitButton.bind('<Leave>', on_leave)


root.bind('<space>', start_on_event)

root.mainloop()