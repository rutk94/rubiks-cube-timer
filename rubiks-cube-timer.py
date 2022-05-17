from tkinter import *

# ROOTS
root = Tk()
root.title('Rubik\'s cube timer')

timerFrame = LabelFrame(root, bd=0)
timerFrame.grid(row=3, column=0)

optionsFrame = LabelFrame(root, text='Options')
optionsFrame.grid(row=0, rowspan=10, column=1, sticky=N+S)

scoresFrame = Canvas(optionsFrame, bg='white', bd=5, height=100, scrollregion=(0,0,0,120))
scoresFrame.grid(row=4, columnspan=3, sticky=W+E)

global font_timer
font_timer = ('Helvetica', 32)
global font_button
font_button = ('Helvetica', 20)
global font_texts
font_texts = ('Cambria', 12)
global font_scores
font_scores = ('Cambria', 10)

times = []
scores = []
scoreLabelNumbers = []
scoreLabels = []
scoreDeleteButtons = []
scoreLines = [] # (scoreLabelNumber, scoreLabel, scoreDeleteButton)

restartVar = IntVar()
restartVar.set(1)

countdownVar = IntVar()

# FUNCTIONS
def countdown(cdVar):
    label_countdown['text'] = '{}'.format(cdVar)

    if cdVar <= countdownVar.get() and cdVar > 0:
        # starting a countdown
        root.after(1000, countdown, cdVar-1) 
    else:
        label_countdown['text'] = ''
        stopButton.config(state=NORMAL)
        # starting a timer
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
    # timer will go until we click STOP
        if msec >= 0 and msec < 1000:
            root.after(1, timer, min, sec, msec+1)
            if msec == 999:
                if sec < 59:
                    root.after(10, timer, min, sec+1, 0)
                elif sec == 59:
                    root.after(1, timer, min+1, 0, 0)
    else:
        startButton.config(state=NORMAL)
        # after clicking STOP, time will be saved on list and showed on canvas
        saveScore(min, sec, msec)

def timesFormatChange(index):
    min = times[index][0]
    if min < 10:
        min = '0%d' % min

    sec = times[index][1]
    if sec < 10:
        sec = '0%d' % sec

    msec = times[index][2]
    if msec in range(0,10):
        msec = '00%d' % msec
    elif msec in range(10,100):
        msec = '0%d' % msec

    return (min, sec, msec)

def saveScore(min, sec, msec):
    times.append((min, sec, msec))
    min_score = timesFormatChange(-1)[0]
    sec_score = timesFormatChange(-1)[1]
    msec_score = timesFormatChange(-1)[2]

    # creating a score text and saving on list
    score = '\t{}:{}:{}'.format(min_score, sec_score, msec_score)
    scores.append(score)

    # creating a score label number
    scoreLabelNumber = Label(scoresFrame, text=scores.index(score), font=font_scores)
    scoreLabelNumbers.append(scoreLabelNumber)

    # creating a score Label and saving on list
    scoreLabel = Label(scoresFrame, text=score, bg='white', font=font_scores)
    scoreLabels.append(scoreLabel)

    # creating a delete button and saving on list
    scoreDeleteButton = Button(scoresFrame, text='x', fg='red', bd=0, bg='white', 
                                command=lambda: deleteScore(scoreLabels.index(scoreLabel)))
    scoreDeleteButtons.append(scoreDeleteButton)

    # scoreLines.append((scoreLabelNumber, scoreLabel, scoreDeleteButton))

    showScore()

def showScore():
    def on_mouse_wheel(event=None):
    # mouse wheel scrolling on canvas
        def _scroll(e=None):
            nonlocal shift_scroll, scroll, scrolled
            if scrolled == 105:
                return
            if shift_scroll:
                scoresFrame.xview_scroll(scroll, 'units')
            else:
                scoresFrame.yview_scroll(scroll, 'units')
            scrolled += 1
        scrolled = 0
        shift_scroll = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        _scroll()

    # showing score labels and delete button on canvas
    for scoreLabel in scoreLabels:
        rowNumber = (len(scoreLabels)-scoreLabels.index(scoreLabel))*20
        # scoreLabelNumber = Label(scoresFrame, text='{}.'.format(scoreLabels.index(scoreLabel)+1), font=font_scores, bg='white')
        # number = scoresFrame.create_window(50, rowNumber, window=scoreLabelNumber)
        time = scoresFrame.create_window(100, rowNumber, window=scoreLabel)
        button = scoresFrame.create_window(250, rowNumber, window=scoreDeleteButtons[scoreLabels.index(scoreLabel)])
    scoreLines.append((time, button))
    print(scoreLines)
        # print(scoreLines)
    
    # for scoreLine in scoreLines:
    #     rowNumber = (len(scoreLines)-scoreLines.index(scoreLine))*20
        
    #     number = scoresFrame.create_window(50, rowNumber, window=scoreLine[0])
    #     score = scoresFrame.create_window(100, rowNumber, window=scoreLine[1])
    #     button = scoresFrame.create_window(250, rowNumber, window=scoreLine[2])

    #     scoreLinesShowed.append((number, score, button))

    # showing a scrollbar on canvas
    if len(scores) == 5:
        v = Scrollbar(optionsFrame, orient=VERTICAL, command=scoresFrame.yview)
        v.grid(row=4, column=2, sticky=E+N+S)
        scoresFrame['yscrollcommand'] = v.set

    # increasing scrollregion on canvas after every new label
    scoresFrame['scrollregion'] = (0,0,0,20*len(scores))

    # mouse wheel scrolling on canvas
    scoresFrame.bind('<MouseWheel>', on_mouse_wheel)

    bestScore()

def deleteScore(scoreNumber):
    
    time = scoreLines[scoreNumber][0]
    button = scoreLines[scoreNumber][1]
    
    scoresFrame.delete(time)
    scoresFrame.delete(button)

    # scoreLabels[scoreNumber]['fg'] = 'gray'
    # scoreDeleteButtons[scoreNumber].configure(fg='#D3D3D3', state=DISABLED)

    times.remove(times[scoreNumber])
    scores.remove(scores[scoreNumber])
    scoreLabels.remove(scoreLabels[scoreNumber])
    scoreDeleteButtons.remove(scoreDeleteButtons[scoreNumber])
    scoreLines.remove(scoreLines[scoreNumber])
    print(scoreLines)

    showScore()
    bestScore()

def bestScore():
    if len(times) > 0:
        bestScore = min(times)
        bestScoreIndex = times.index(bestScore)
        min_best = timesFormatChange(bestScoreIndex)[0]
        sec_best = timesFormatChange(bestScoreIndex)[1]
        msec_best = timesFormatChange(bestScoreIndex)[2]
        bestScoreLabel.config(text='{}:{}:{}'.format(min_best, sec_best, msec_best))
    else:
        bestScoreLabel.config(text='00:00:000')

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

label_min = Label(timerFrame, text='00', font=font_timer)
label_min.grid(row=0, column=0)

label_sec = Label(timerFrame, text=':00', font=font_timer)
label_sec.grid(row=0, column=1)

label_msec = Label(timerFrame, text=':000', font=font_timer)
label_msec.grid(row=0, column=2)

label_countdown = Label(root, text='', font=font_button)
label_countdown.grid(row=4, column=0)

label_text = Label(root, text='Press START to activate the TIMER')
label_text.grid(row=5, column=0, sticky=W+E)

## Options LABELS
restartOptionLabel = Label(optionsFrame, text='Restart timer every time after START?', font=font_texts)
restartOptionLabel.grid(row=0, column=0, sticky=W)

restartOptionButtonYes = Radiobutton(optionsFrame, text='Yes', value=1, variable=restartVar, font=font_texts)
restartOptionButtonYes.grid(row=0, column=1)

restartOptionButtonNo = Radiobutton(optionsFrame, text='No', value=0, variable=restartVar, font=font_texts)
restartOptionButtonNo.grid(row=0, column=2)

countdownOptionLabel = Label(optionsFrame, text='Duration of countdown after START:', font=font_texts)
countdownOptionLabel.grid(row=1, column=0, sticky=W)

countdownOptionMenu = OptionMenu(optionsFrame, countdownVar, 0, 3, 5, 10, 15, 30)
countdownOptionMenu.grid(row=1, column=1, sticky=W+E)

bestScoreLabelText = Label(optionsFrame, text='Best score:', font=font_texts)
bestScoreLabelText.grid(row=5, column=0)

bestScoreLabel = Label(optionsFrame, font=font_texts)
bestScoreLabel.grid(row=5, column=1, columnspan=2)


### Score LABELS
# scoreLabel = Label(scoresFrame, bg='white')


# BUTTONS
startButton = Button(root, text='START', font=font_button, command=start, bd=0, activeforeground='orange')
startButton.grid(row=6, column=0, sticky=W+E)
startButton.bind('<Enter>', on_enter)
startButton.bind('<Leave>', on_leave)

stopButton = Button(root, text='STOP', font=font_button, command=stop, bd=0, activeforeground='orange', state=DISABLED)
stopButton.grid(row=7, column=0)
stopButton.bind('<Enter>', on_enter)
stopButton.bind('<Leave>', on_leave)

restartButton = Button(root, text='RESTART', font=font_button, command=restart, bd=0, activeforeground='orange', state=DISABLED)
restartButton.grid(row=8, column=0)
restartButton.bind('<Enter>', on_enter)
restartButton.bind('<Leave>', on_leave)

exitButton = Button(root, text='EXIT', font=font_button, command=exit, bd=0, activeforeground='orange')
exitButton.grid(row=9, column=0)
exitButton.bind('<Enter>', on_enter)
exitButton.bind('<Leave>', on_leave)

## Options BUTTONS
# scoreDeleteButton = Button(scoresFrame, text='x', fg='red', bd=0, bg='white')


root.bind('<space>', start_on_event)

root.mainloop()