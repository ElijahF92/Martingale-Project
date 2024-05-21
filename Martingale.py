import tkinter as tk
from math import*
from pynput.mouse import Listener, Button, Controller
import time

mouse = Controller()
def start():
    
    def bet(amount):
        # Select chip
        mouse.position = (chipPosX, chipPosY)
        for i in range(1, amount):
            mouse.click(Button.left)
        time.sleep(0.1)
        # bet
        mouse.position = (betPosX, betPosY)
        mouse.click(Button.left)
    
    bet(1)
    time.sleep(0.1)
    mouse.position = (winPosX, winPosY)
    if winCondition:
        bet(1)
    else:
        bet()


def mouseEvent(btn):
    global betPosX, betPosY, chipPosX, chipPosY, winPosX, winPosY
    xPos = 0
    yPos = 0

    def on_click(x, y, button, pressed):
        nonlocal xPos, yPos
        xPos = x
        yPos = y
        if not pressed:
            print(f"Click location: ({x}, {y})")
            return False  # Stop listener

    with Listener(on_click=on_click) as listener:
        listener.join()
    
    if btn == "bet":
        
        setButtonBet.config(fg="green")
        betPosX = xPos
        betPosY = yPos
    elif btn == "chip":
        setButtonChip.config(fg="green")
        chipPosX = xPos
        chipPosY = yPos
    else:
        setButtonWin.config(fg="green")
        winPosX = xPos
        winPosY = yPos
        #SELECTION WINDOW HERE

def calculateOdds():
    offset = options.index(clicked.get())
    bankroll = float(bankrollEntry.get()) - offset if bankrollEntry.get() else 1
    betAmount = float(betAmountEntry.get()) if betAmountEntry.get() else 1
    myVal = floor(log2(bankroll/betAmount + 1)) + offset
    print(floor(log2(bankroll/betAmount + 1)))
    myString = "Consecutive Losses to Lose: " + str(myVal)
    percent = round((100*pow(19/37, myVal)), 3)
    myString2 = "Odds: " + str(percent) + "%, " + "1/" + str(round(100/percent))
    lossesLabel.config(text=myString)
    oddsLabel.config(text=myString2)
    progString = ("-" + str(int(betAmount))) * (offset+1)
    progString = progString[1:]
    for i in range(1, myVal-offset):
        progString = progString + "-" + str(int(betAmount * pow(2, i)))
    progLabel.config(text= progString)

preferencesWin = tk.Tk()
preferencesWin.title("Preferences")
preferencesWin.geometry('450x200')

options = [
    "Maximize Gains",
    "Equalize Losses",
    "Minimize losses"
]
clicked = tk.StringVar() 
clicked.set( "Maximize Gains" ) 
dropDown = tk.OptionMenu( preferencesWin , clicked , *options ) 
dropDown.grid(column =0, row =3)
#dropDown.pack() 

bankrollLabel = tk.Label(preferencesWin, text = "Bankroll")
bankrollLabel.grid(column =0, row =0)

bankrollEntry = tk.Entry(preferencesWin, width=10)
bankrollEntry.grid(column =0, row =1)

betAmountLabel = tk.Label(preferencesWin, text = "Bet Amount")
betAmountLabel.grid(column =1, row =0)

betAmountEntry = tk.Entry(preferencesWin, width=10)
betAmountEntry.grid(column =1, row =1)

lossesLabel = tk.Label(preferencesWin, text = "Consecutive Losses to Lose:")
lossesLabel.grid(column =2, row =0)
oddsLabel = tk.Label(preferencesWin, text = "Odds: Na%")
oddsLabel.grid(column =2, row =1)
progLabel = tk.Label(preferencesWin, text = "")
progLabel.grid(column=2, row=2)

calcButton =tk.Button(preferencesWin, text = "Calculate" ,
             fg = "red", command=calculateOdds)
calcButton.grid(column=0, row=2)

automationWin = tk.Toplevel(preferencesWin)
automationWin.transient( preferencesWin )
automationWin.title( "Child" )

chipPosX = 0
chipPosY = 0
betPosX = 0
betPosY = 0
winPosX = 0
winPosY = 0

ChipPosLabel = tk.Label(automationWin, text= "Set Chip Position")
ChipPosLabel.grid(column=0, row=0)
setButtonChip = tk.Button(automationWin, text= "set", fg= "red", command=lambda: mouseEvent(btn="chip"))
setButtonChip.grid(column=0, row=1)
BetPosLabel = tk.Label(automationWin, text= "Set Betting Position")
BetPosLabel.grid(column=1, row=0)
setButtonBet = tk.Button(automationWin, text= "set", fg= "red", command=lambda: mouseEvent(btn="bet"))
setButtonBet.grid(column=1, row=1)
winPosLabel = tk.Label(automationWin, text= "Set Winning Position")
winPosLabel.grid(column=2, row=0)
setButtonWin = tk.Button(automationWin, text= "set", fg= "red", command=lambda: mouseEvent(btn="win"))
setButtonWin.grid(column=2, row=1)
startButton = tk.Button(automationWin, text= "Start", fg= "green", command= start)
startButton.grid(column=1, row=2)

preferencesWin.mainloop()






