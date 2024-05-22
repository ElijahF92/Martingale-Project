import tkinter as tk
from math import*
from pynput.mouse import Listener, Button, Controller
import time
import pyautogui
import pytesseract
import cv2

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

def fillProg():
    progEntryLabel.config(text=1)

def calc():
    print("working?")
    myVal = progLabel.cget("text")
    print(myVal)
    progEntry.insert(0,string=myVal)

chipPosX = 0
chipPosY = 0
betPosX = 0
betPosY = 0
winPosX = 0
winPosY = 0
Win = tk.Tk()

Win.title("Betting Automator")
Win.geometry('245x845')

automatorFrame = tk.Frame(Win)
#automatorFrame.configure(bg="white")
automatorFrame.pack(padx=20, pady=20)
calcFrame = tk.Frame(Win)
calcFrame.configure()
calcFrame.pack(padx=20)

options = [
    "Maximize Gains",
    "Equalize Losses",
    "Minimize losses"
]
calcHeader = tk.Label(calcFrame, text= "Calculate Odds", pady=10)
calcHeader.grid(column=0, row=0, columnspan=2, sticky="W")
clicked = tk.StringVar() 
clicked.set( "Maximize Gains" ) 
dropDown = tk.OptionMenu( calcFrame , clicked , *options ) 
dropDown.grid(column =0, row =3, columnspan=2, sticky="W")
#dropDown.pack() 

bankrollLabel = tk.Label(calcFrame, text = "Bankroll:", anchor="e", width=12)
bankrollLabel.grid(column =0, row =1, sticky="W")

bankrollEntry = tk.Entry(calcFrame, width=8)
bankrollEntry.grid(column =1, row =1)

betAmountLabel = tk.Label(calcFrame, text = "Bet Amount:", anchor="e", width=12)
betAmountLabel.grid(column =0, row =2, sticky="W")

betAmountEntry = tk.Entry(calcFrame, width=8)
betAmountEntry.grid(column =1, row =2)

lossesLabel = tk.Label(calcFrame, text = "Consecutive Losses to Lose:")
lossesLabel.grid(column =0, row =5, columnspan=2, sticky="W")
oddsLabel = tk.Label(calcFrame, text = "Odds: Na%")
oddsLabel.grid(column =0, row =6)
progLabel = tk.Label(calcFrame, text = "")
progLabel.grid(column=0, row=7, columnspan=2, sticky="W")

calcButton =tk.Button(calcFrame, text = "Calculate" ,
            fg = "red", command=calculateOdds)
calcButton.grid(column=0, row=4, columnspan=2, sticky="W")
header = tk.Label(automatorFrame, text= "Set Positions", pady=10)
header.grid(column=0, row=0, sticky="W")
ChipPosLabel = tk.Label(automatorFrame, text= "Chip Position:",  width=12, padx=10, anchor= "e")
ChipPosLabel.grid(column=0, row=1, sticky="W")
setButtonChip = tk.Button(automatorFrame, text= "set", fg= "red", command=lambda: mouseEvent(btn="chip"))
setButtonChip.grid(column=1, row=1, sticky="W")
BetPosLabel = tk.Label(automatorFrame, text= "Betting Position:", width=12, padx=10, anchor= "e")
BetPosLabel.grid(column=0, row=2, sticky="W")
setButtonBet = tk.Button(automatorFrame, text= "set", fg= "red", command=lambda: mouseEvent(btn="bet"))
setButtonBet.grid(column=1, row=2, sticky="W")
winPosLabel = tk.Label(automatorFrame, text= "Winning Position:",  width=12, padx=10, anchor= "e")
winPosLabel.grid(column=0, row=3, sticky="W")
setButtonWin = tk.Button(automatorFrame, text= "set", fg= "red", command=lambda: mouseEvent(btn="win"))
setButtonWin.grid(column=1, row=3, sticky="W")
progEntryLabel = tk.Label(automatorFrame, text= "Betting Progression", anchor= "w", pady=10)
progEntryLabel.grid(column=0, row=4, sticky="W")
takeFromCalc = tk.Button(automatorFrame, text= "from calc", fg= "black", font=("Arial", 10), width=5, command=calc)
takeFromCalc.grid(column=1, row=4, columnspan= 2)
progEntry = tk.Entry(automatorFrame, width=20)
progEntry.grid(column=0, row=5, columnspan=2, sticky="W")
startButton = tk.Button(automatorFrame, text= "Start", fg= "green", command= start)
startButton.grid(column=0, row=6, columnspan= 2)
Win.mainloop()






