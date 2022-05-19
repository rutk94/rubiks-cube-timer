from tkinter import *
import statistics

# ROOTS
root = Tk()
root.title('Rubik\'s cube timer')

optionsFrame = LabelFrame(root, text='Options')
optionsFrame.grid(row=0, rowspan=10, column=1, sticky=N+S)

scoresFrame = Canvas(optionsFrame, bg='white', bd=5, height=100, scrollregion=(0,0,0,120))
scoresFrame.grid(row=4, columnspan=3, sticky=W+E)

# VARIABLES
font_timer = ('Helvetica', 32)
font_button = ('Helvetica', 20)
font_texts = ('Cambria', 12)
font_scores = ('Cambria', 10)

times = []
scores = []
deleteButtons = []

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
    label_score['text'] = timesFormatChanger((min, sec, msec))

    if not stopButton['state'] == DISABLED:
    # timer will go until we click STOP
        if msec < 999:
            root.after(1, timer, min, sec, msec+1)
        elif msec == 999:
            if sec < 59:
                root.after(1, timer, min, sec+1)
            elif sec == 59:
                root.after(1, timer, min+1)
    else:
        startButton.config(state=NORMAL)
        times.append((min, sec, msec))
        # after clicking STOP, time will be saved on list and showed on canvas
        saveScore(timesFormatChanger((min, sec, msec)))
        showScore()

def timesFormatChanger(timeTuple):
    # changes format of score text to '{min}:{sec}.{msec}'
    min = timeTuple[0]
    sec = timeTuple[1]
    msec = timeTuple[2]
    if min in range (0,10):
        min_score = '0%d' % min
    else:
        min_score = '%d' % min

    if sec in range(0,10):
        sec_score = ':0%d' % sec
    else:
        sec_score = ':%d' % sec

    if msec in range(0,10):
        msec_score = '.00%d' % msec
    elif msec in range(10,100):
        msec_score = '.0%d' % msec
    elif msec in range(100,1000):
        msec_score = '.%d' % msec

    return min_score + sec_score + msec_score

def saveScore(score):
    # creating a score text and saving on list
    scores.append(score)

def showScore():
    # showing score on canvas

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
    
    n = 1 # number of line / score
    for score in scores:
        rowNumber = (len(scores)-scores.index(score))*20
        numberLabel = Label(scoresFrame, text='{}.'.format(n), font=font_scores, bg='white')
        scoreLabel = Label(scoresFrame, text=score, font=font_scores, bg='white')
        buttonLabel = deleteButtonCreator(n)
        scoresFrame.create_window(50, rowNumber, window=numberLabel)
        scoresFrame.create_window(150, rowNumber, window=scoreLabel)
        scoresFrame.create_window(250, rowNumber, window=buttonLabel)
        print(n)
        n += 1

    # showing a scrollbar on canvas
    if len(scores) == 5:
        v = Scrollbar(optionsFrame, orient=VERTICAL, command=scoresFrame.yview)
        v.grid(row=4, column=2, sticky=E+N+S)
        scoresFrame['yscrollcommand'] = v.set
    # increasing scrollregion on canvas after every new label
    scoresFrame['scrollregion'] = (0,0,0,20*len(scores))
    # mouse wheel scrolling on canvas
    scoresFrame.bind('<MouseWheel>', on_mouse_wheel)
    # actualize best score
    bestScoresActualize()

def deleteButtonCreator(scoreIndex):
    # creating delete button for each line
    source = '''
button{0}Label = Button(scoresFrame, text='x', bg='white', fg='red', bd=0, command=lambda: deleteScore({0}-1))
deleteButtons.append(button{0}Label)
'''.format(scoreIndex)
    exec(source)
    return deleteButtons[-1]

def deleteScore(scoreIndex):
    # deleting score from canvas
    times.remove(times[scoreIndex])
    scores.remove(scores[scoreIndex])
    scoresFrame.delete('all')
    # showing scores again without deleted score
    showScore()
    # actualize best scores
    bestScoresActualize()

def scoreChangeToMsec(score):
    # changes score into amount of miliseconds - e.g. 00:01.000 = 1000 msec
    result = score[0]*60000+score[1]*1000+score[2]
    return result

def scoreChangeToNormal(scoreInMsec):
    scoreInMsec = int(round(scoreInMsec, 0))
    if scoreInMsec >= 60000:
        min = scoreInMsec // 60000
        sec = (scoreInMsec - 60000) // 1000
        msec = int(str(scoreInMsec)[-3:])
    else:
        min = 0
        sec = scoreInMsec // 1000
        msec = int(str(scoreInMsec)[-3:])
    return (min, sec, msec)

def bestScoresActualize():
    # actualizing best score and average scores
    scoresInMsec = []

    if len(times) > 0:
        # best score
        bestScore = min(times) # = (min, sec, msec)
        bestScoreText = timesFormatChanger(bestScore)
        bestScoreLabel.config(text=bestScoreText)
        # average score
        for score in times:
            scoreInMsec=scoreChangeToMsec(score) # change score to amount of miliseconds
            scoresInMsec.append(scoreInMsec)
        avgScoreInMsec = statistics.mean(scoresInMsec)
        avgScoreTuple = scoreChangeToNormal(avgScoreInMsec) # change score to format (min, sec, msec)
        avgScore = timesFormatChanger(avgScoreTuple) # change score to format '{min}:{sec}.{msec}'
        averageScoreLabel.config(text=avgScore)
    else:
        bestScoreLabel.config(text='--:--.---')
        averageScoreLabel.config(text='--:--.---')

    if len(times) >= 5:
        avg5ScoreInMsec = statistics.mean(scoresInMsec[-5:])
        avg5ScoreTuple = scoreChangeToNormal(avg5ScoreInMsec)
        avg5Score = timesFormatChanger(avg5ScoreTuple)
        average5ScoreLabel.config(text=avg5Score)
    else:
        average5ScoreLabel.config(text='--:--.---')

    if len(times) >= 10:
        avg10ScoreInMsec = statistics.mean(scoresInMsec[-10:])
        avg10ScoreTuple = scoreChangeToNormal(avg10ScoreInMsec)
        avg10Score = timesFormatChanger(avg10ScoreTuple)
        average10ScoreLabel.config(text=avg10Score)
    else:
        average10ScoreLabel.config(text='--:--.---')

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
    label_score['text'] = '00:00.000'
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

label_score = Label(root, text='00:00.000', font=font_timer)
label_score.grid(row=3)

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
bestScoreLabelText.grid(row=5, column=0, sticky=E)
bestScoreLabel = Label(optionsFrame, font=font_texts)
bestScoreLabel.grid(row=5, column=1, columnspan=2)

averageScoreLabelText = Label(optionsFrame, text='Average score:', font=font_texts)
averageScoreLabelText.grid(row=6, column=0, sticky=E)
averageScoreLabel = Label(optionsFrame, font=font_texts)
averageScoreLabel.grid(row=6, column=1, columnspan=2)

average5ScoreLabelText = Label(optionsFrame, text='Average score (last 5):', font=font_texts)
average5ScoreLabelText.grid(row=7, column=0, sticky=E)
average5ScoreLabel = Label(optionsFrame, font=font_texts)
average5ScoreLabel.grid(row=7, column=1, columnspan=2)

average10ScoreLabelText = Label(optionsFrame, text='Average score (last 10):', font=font_texts)
average10ScoreLabelText.grid(row=8, column=0, sticky=E)
average10ScoreLabel = Label(optionsFrame, font=font_texts)
average10ScoreLabel.grid(row=8, column=1, columnspan=2)

### Score LABELS - created in showScore func

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

## Options BUTTONS - created in deleteButtonCreator func

root.bind('<space>', start_on_event)

root.mainloop()