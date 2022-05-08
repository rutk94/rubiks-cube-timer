from ast import Num
import secrets
from tkinter import *
import time

# ROOTS
root = Tk()
root.title('Rubik\'s cube timer')

timerFrame = LabelFrame(root, bd=0)
timerFrame.grid(row=3, column=0)

optionsFrame = LabelFrame(root, text='Options')
optionsFrame.grid(row=0, rowspan=10, column=1, sticky=N+S)

scoresFrame = LabelFrame(optionsFrame, bg='white')
scoresFrame.grid(row=4, columnspan=5, sticky=W+E)

global font_timer
font_timer = ('Helvetica', 32)
global font_button
font_button = ('Helvetiva', 20)

times = []
scoreNumberLabels = []
scoreLabels = []
scoreDeleteButtons = []

restartVar = IntVar()
restartVar.set(1)

countdownVar = IntVar()

# FUNCTIONS
def countdown(cdVar):
    label_countdown['text'] = '{}'.format(cdVar)

    if cdVar <= countdownVar.get() and cdVar > 0:
        root.after(1000, countdown, cdVar-1) # uruchomienie odliczania
    else:
        label_countdown['text'] = ''
        stopButton.config(state=NORMAL)
        timer()                              # uruchomienie stopera

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

    if not stopButton['state'] == DISABLED:     # dopóki nie aktywujemy przycisku STOP, stoper będzie działał
        if msec >= 0 and msec < 1000:
            root.after(1, timer, min, sec, msec+1)
            if msec == 999:
                if sec < 59:
                    root.after(10, timer, min, sec+1, 0)
                elif sec == 59:
                    root.after(1, timer, min+1, 0, 0)
    else:
        startButton.config(state=NORMAL)
        times.append((min, sec, msec))          # po wciśnięciu STOP, czas zostanie zapisany na liście 'times'
        showScore()

def showScore():
    min = times[-1][0]
    if min < 10:
        min = '0%d' % min

    sec = times[-1][1]
    if sec < 10:
        sec = '0%d' % sec

    msec = times[-1][2]
    if msec in range(0,10):
        msec = '00%d' % msec
    elif msec in range(10,100):
        msec = '0%d' % msec

    scoreLabel = Label(scoresFrame, text='{}.\t{}:{}:{}'.format(len(scoreLabels)+1, min, sec, msec), bg='white')
    scoreLabels.append(scoreLabel)
    if len(scoreLabels) <= 10:
        for scoreLabel in scoreLabels:
            rowNumber = len(scoreLabels) - scoreLabels.index(scoreLabel)
            scoreLabel.grid(row=rowNumber, column=1)
    else:
        pass

def start_on_event(e):
    root.unbind('<space>')
    root.bind('<space>', stop_on_event)
    start()

def start():
    root.unbind('<space>')
    root.bind('<space>', stop_on_event)
    restartButton.config(state=DISABLED)

    if restartVar.get() == 1:
        restart()
        stopButton.config(state=NORMAL)
        cdVar = countdownVar.get()
        if cdVar > 0:
            countdown(cdVar)
        else:
            timer()
    elif restartVar.get() == 0:
        stopButton.config(state=NORMAL)
        if len(times) == 0:
            timer()
        else:
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


# LABELS
rubiksCubeImgLabel = Label(root, image=rubiksCubeImg, bd=2)
rubiksCubeImgLabel.grid(row=0, column=0)

# titleLabel = Label(root, text='Title')
# titleLabel.grid(row=1, column=0)

# scrambleLabel = Label(root, text='scramble')
# scrambleLabel.grid(row=2, column=0)

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

## Options LABELS
restartOptionLabel = Label(optionsFrame, text='Restart timer every time after START?')
restartOptionLabel.grid(row=0, column=0, sticky=W)

restartOptionButtonYes = Radiobutton(optionsFrame, text='Yes', value=1, variable=restartVar)
restartOptionButtonYes.grid(row=0, column=1)

restartOptionButtonNo = Radiobutton(optionsFrame, text='No', value=0, variable=restartVar)
restartOptionButtonNo.grid(row=0, column=2)

countdownOptionLabel = Label(optionsFrame, text='Duration of countdown after START:')
countdownOptionLabel.grid(row=1, column=0, sticky=W)

countdownOptionMenu = OptionMenu(optionsFrame, countdownVar, 0, 3, 5, 10, 15, 30)
countdownOptionMenu.grid(row=1, column=1, sticky=W+E)


### Score LABELS
# for n in range(1,6):
#     # scoreNumberLabel = Label(scoresFrame, bg='white')
#     # scoreNumberLabel.grid(row=n-1, column=0, sticky=W)
#     # scoreNumberLabels.append(scoreNumberLabel)

#     scoreLabel = Label(scoresFrame, bg='white')
#     scoreLabel.grid(row=n-1, column=1)
#     scoreLabels.append(scoreLabel)



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

## Options BUTTONS
# for n in range(1,6):
#     scoreDeleteButton = Button(scoresFrame, fg='red', bd=0, bg='white')
#     scoreDeleteButton.grid(row=n-1, column=2, sticky=E)
#     scoreDeleteButtons.append(scoreDeleteButton)


root.bind('<space>', start_on_event)

root.mainloop()